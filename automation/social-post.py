"""
Auto-post new ClearCents blog posts to Pinterest and Reddit.
Triggered by GitHub Actions when new files are added to _posts/.
"""

import os
import sys
import json
import time
import requests
import frontmatter
from pathlib import Path

SITE_URL = os.environ.get('SITE_URL', 'https://clearcentslife.com')

# Category slug → subreddits (ordered by relevance; posts to the first one only)
SUBREDDIT_MAP = {
    'budgeting':     ['ynab', 'personalfinance', 'Frugal'],
    'save-money':    ['Frugal', 'povertyfinance', 'personalfinance'],
    'side-hustles':  ['beermoney', 'SideHustle', 'WorkOnline'],
    'debt-free':     ['debtfree', 'povertyfinance', 'personalfinance'],
    'investing':     ['Bogleheads', 'personalfinance', 'investing'],
}

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def build_post_url(meta, file_path):
    """Reconstruct the Jekyll permalink /:category/:slug/ from front matter + filename."""
    cats = meta.get('categories', [])
    category_slug = cats[0].lower().replace(' ', '-') if cats else 'blog'
    stem = Path(file_path).stem                     # 2026-07-25-my-post-title
    parts = stem.split('-')
    if len(parts) > 3:
        slug = '-'.join(parts[3:])                  # strip YYYY-MM-DD- prefix
    else:
        slug = stem
    return f"{SITE_URL}/{category_slug}/{slug}/"


def category_slug(meta):
    cats = meta.get('categories', [])
    return cats[0].lower().replace(' ', '-') if cats else ''


# ─────────────────────────────────────────────────────────────
# Pinterest  (API v5)
# ─────────────────────────────────────────────────────────────

def refresh_pinterest_token():
    """Exchange refresh token for a new access token and print it for Secret rotation."""
    refresh_token = os.environ.get('PINTEREST_REFRESH_TOKEN')
    client_id     = os.environ.get('PINTEREST_CLIENT_ID')
    client_secret = os.environ.get('PINTEREST_CLIENT_SECRET')
    if not all([refresh_token, client_id, client_secret]):
        return None
    resp = requests.post(
        'https://api.pinterest.com/v5/oauth/token',
        data={
            'grant_type':    'refresh_token',
            'refresh_token': refresh_token,
        },
        auth=(client_id, client_secret),
    )
    if resp.ok:
        data = resp.json()
        print(f"[Pinterest] New access token obtained (expires in {data.get('expires_in', '?')}s)")
        return data['access_token']
    print(f"[Pinterest] Token refresh failed: {resp.status_code} {resp.text}")
    return None


def post_to_pinterest(meta, post_url, _token=None):
    token = _token or os.environ.get('PINTEREST_ACCESS_TOKEN')
    if not token:
        print("[Pinterest] No access token — skipping")
        return

    # Board IDs stored as JSON: {"budgeting":"123","save-money":"456",...}
    raw_boards = os.environ.get('PINTEREST_BOARD_IDS', '{}')
    try:
        board_ids = json.loads(raw_boards)
    except json.JSONDecodeError:
        print("[Pinterest] PINTEREST_BOARD_IDS is not valid JSON — skipping")
        return

    cat = category_slug(meta)
    board_id = board_ids.get(cat) or board_ids.get('default')
    if not board_id:
        print(f"[Pinterest] No board ID for category '{cat}' — skipping")
        return

    image_url = meta.get('image', '')
    if not image_url:
        image_url = f"{SITE_URL}/assets/images/defaults/{cat}.jpg"

    pin = {
        'link':        post_url,
        'title':       meta.get('title', '')[:100],
        'description': meta.get('description', '')[:500],
        'board_id':    board_id,
        'media_source': {
            'source_type': 'image_url',
            'url':         image_url,
        },
    }

    resp = requests.post(
        'https://api.pinterest.com/v5/pins',
        json=pin,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type':  'application/json',
        },
    )

    if resp.status_code in (200, 201):
        pin_id = resp.json().get('id', '?')
        print(f"[Pinterest] ✅ Pin created: {pin_id}")
    elif resp.status_code == 401 and _token is None:
        print("[Pinterest] Token expired — attempting refresh...")
        new_token = refresh_pinterest_token()
        if new_token:
            post_to_pinterest(meta, post_url, _token=new_token)
    else:
        print(f"[Pinterest] ❌ {resp.status_code}: {resp.text}")


# ─────────────────────────────────────────────────────────────
# Reddit  (via REST API — no extra library needed)
# ─────────────────────────────────────────────────────────────

def get_reddit_token():
    client_id     = os.environ.get('REDDIT_CLIENT_ID')
    client_secret = os.environ.get('REDDIT_CLIENT_SECRET')
    username      = os.environ.get('REDDIT_USERNAME')
    password      = os.environ.get('REDDIT_PASSWORD')
    if not all([client_id, client_secret, username, password]):
        return None, None
    resp = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth=(client_id, client_secret),
        data={'grant_type': 'password', 'username': username, 'password': password},
        headers={'User-Agent': f'ClearCents/1.0 by {username}'},
    )
    if resp.ok:
        return resp.json().get('access_token'), username
    print(f"[Reddit] Auth failed: {resp.status_code} {resp.text}")
    return None, None


def post_to_reddit(meta, post_url):
    token, username = get_reddit_token()
    if not token:
        print("[Reddit] No credentials — skipping")
        return

    cat = category_slug(meta)
    subreddits = SUBREDDIT_MAP.get(cat, ['personalfinance'])
    title = meta.get('title', '')

    headers = {
        'Authorization': f'bearer {token}',
        'User-Agent':    f'ClearCents/1.0 by {username}',
        'Content-Type':  'application/x-www-form-urlencoded',
    }

    posted = False
    for sub in subreddits:
        data = {
            'kind':    'link',
            'sr':      sub,
            'title':   title,
            'url':     post_url,
            'resubmit': False,
            'nsfw':    False,
        }
        resp = requests.post(
            'https://oauth.reddit.com/api/submit',
            headers=headers,
            data=data,
        )
        body = resp.json()
        # Reddit wraps responses in jquery array
        errors = body.get('json', {}).get('errors', [])
        if resp.ok and not errors:
            permalink = body.get('json', {}).get('data', {}).get('url', '')
            print(f"[Reddit] ✅ Posted to r/{sub}: {permalink}")
            posted = True
            break
        else:
            reason = errors[0] if errors else resp.text[:200]
            print(f"[Reddit] ⚠️  r/{sub} rejected: {reason} — trying next subreddit")
            time.sleep(2)

    if not posted:
        print(f"[Reddit] ❌ Could not post to any subreddit for category '{cat}'")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────

def main():
    raw = os.environ.get('NEW_POST_FILES', '').strip()
    if not raw:
        print("No new post files detected.")
        sys.exit(0)

    files = [f for f in raw.split('\n') if f.startswith('_posts/') and f.endswith('.md')]
    if not files:
        print("No new .md files in _posts/ — nothing to post.")
        sys.exit(0)

    batch_all = os.environ.get('BATCH_POST_ALL', '').lower() == 'true'
    targets = sorted(files) if batch_all else [sorted(files)[-1]]

    for i, target in enumerate(targets):
        print(f"\n📢 Posting ({i+1}/{len(targets)}): {target}")
        try:
            post = frontmatter.load(target)
            meta = post.metadata
            url  = build_post_url(meta, target)
            print(f"   Title : {meta.get('title')}")
            print(f"   URL   : {url}")
            print(f"   Cat   : {category_slug(meta)}")
        except Exception as e:
            print(f"Failed to parse {target}: {e}")
            continue

        post_to_pinterest(meta, url)
        time.sleep(3)
        post_to_reddit(meta, url)
        if i < len(targets) - 1:
            time.sleep(5)


if __name__ == '__main__':
    main()

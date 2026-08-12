#!/usr/bin/env python3
"""
Auto-post new ClearCents blog posts to Pinterest.
Runs via GitHub Actions on every new _posts/*.md push.
"""

import os
import sys
import time
import requests
import frontmatter

SITE_URL        = os.environ.get('SITE_URL', 'https://clearcentslife.com').rstrip('/')
NEW_POST_FILES  = os.environ.get('NEW_POST_FILES', '').strip()
BATCH_POST_ALL  = os.environ.get('BATCH_POST_ALL', 'false').lower() == 'true'

PINTEREST_ACCESS_TOKEN  = os.environ.get('PINTEREST_ACCESS_TOKEN', '')
PINTEREST_REFRESH_TOKEN = os.environ.get('PINTEREST_REFRESH_TOKEN', '')
PINTEREST_CLIENT_ID     = os.environ.get('PINTEREST_CLIENT_ID', '')
PINTEREST_CLIENT_SECRET = os.environ.get('PINTEREST_CLIENT_SECRET', '')
PINTEREST_BOARD_IDS     = os.environ.get('PINTEREST_BOARD_IDS', '')

CATEGORY_HASHTAGS = {
    'budgeting':    '#budgeting #budgettips #moneytips #personalfinance #savemoney',
    'save-money':   '#savemoney #frugalliving #moneysavingtips #personalfinance #budgeting',
    'side-hustles': '#sidehustle #makemoney #extraincome #sideincome #personalfinance',
    'debt-free':    '#debtfree #debtpayoff #financialfreedom #getoutofdebt #personalfinance',
    'investing':    '#investing #stockmarket #wealthbuilding #financialfreedom #personalfinance',
}


def refresh_token():
    if not (PINTEREST_REFRESH_TOKEN and PINTEREST_CLIENT_ID and PINTEREST_CLIENT_SECRET):
        return PINTEREST_ACCESS_TOKEN
    resp = requests.post(
        'https://api.pinterest.com/v5/oauth/token',
        data={'grant_type': 'refresh_token', 'refresh_token': PINTEREST_REFRESH_TOKEN},
        auth=(PINTEREST_CLIENT_ID, PINTEREST_CLIENT_SECRET),
        timeout=15,
    )
    if resp.ok:
        new_token = resp.json().get('access_token', '')
        if new_token:
            print("Pinterest token refreshed.")
            return new_token
    print(f"Token refresh failed ({resp.status_code}), using existing token.")
    return PINTEREST_ACCESS_TOKEN


def build_description(meta):
    categories = meta.get('categories', [])
    cat = categories[0] if categories else ''
    tags = meta.get('tags', [])
    base_desc = meta.get('description', meta.get('title', ''))
    tag_hashtags = ' '.join('#' + t.replace(' ', '').replace('-', '') for t in tags[:5])
    cat_hashtags = CATEGORY_HASHTAGS.get(cat, '#personalfinance #moneytips')
    return f"{base_desc}\n\n{cat_hashtags} {tag_hashtags}".strip()[:500]


def get_post_url(meta, filepath):
    permalink = meta.get('permalink', '')
    if permalink:
        return SITE_URL + '/' + permalink.strip('/') + '/'
    categories = meta.get('categories', [])
    cat = categories[0] if categories else 'blog'
    slug = os.path.basename(filepath).replace('.md', '')
    slug = '-'.join(slug.split('-')[3:])
    return f"{SITE_URL}/{cat}/{slug}/"


def pin_to_pinterest(meta, post_url, token, board_ids):
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    title = meta.get('title', '')[:100]
    description = build_description(meta)
    image_url = meta.get('image', '')
    if not image_url:
        print("No image in post — skipping pin.")
        return
    for board_id in board_ids:
        payload = {
            'board_id': board_id,
            'title': title,
            'description': description,
            'link': post_url,
            'media_source': {'source_type': 'image_url', 'url': image_url},
        }
        resp = requests.post('https://api.pinterest.com/v5/pins', headers=headers, json=payload, timeout=20)
        if resp.ok:
            print(f"Pin created (id={resp.json().get('id')}) on board {board_id}")
        else:
            print(f"Pinterest error (board={board_id}): {resp.status_code} {resp.text[:200]}")
        time.sleep(2)


def main():
    if not NEW_POST_FILES:
        print("No new post files. Nothing to post.")
        return
    post_files = [f.strip() for f in NEW_POST_FILES.splitlines() if f.strip()]
    if not BATCH_POST_ALL:
        post_files = post_files[-1:]
    print(f"Posts to process: {post_files}")
    token = refresh_token()
    board_ids = [b.strip() for b in PINTEREST_BOARD_IDS.split(',') if b.strip()]
    if not token:
        print("No Pinterest access token. Set PINTEREST_ACCESS_TOKEN secret.")
        sys.exit(1)
    if not board_ids:
        print("No board IDs. Set PINTEREST_BOARD_IDS secret.")
        sys.exit(1)
    for filepath in post_files:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath} — skipping.")
            continue
        with open(filepath, 'r', encoding='utf-8') as fh:
            post = frontmatter.load(fh)
        meta = post.metadata
        post_url = get_post_url(meta, filepath)
        print(f"\nTitle : {meta.get('title', '')}")
        print(f"URL   : {post_url}")
        pin_to_pinterest(meta, post_url, token, board_ids)
        time.sleep(3)
    print("\nDone.")


if __name__ == '__main__':
    main()

"""
One-time OAuth helper — run this locally to get a Pinterest access token
with boards:write and pins:write scopes.

Usage:
    python automation/get-pinterest-token.py

Then visit the URL it prints, approve the app, and it will print your
access_token and refresh_token to paste into GitHub Secrets.
"""

import http.server
import threading
import webbrowser
import urllib.parse
import requests
import sys
import os

CLIENT_ID     = "1594243"
CLIENT_SECRET = os.environ.get("PINTEREST_CLIENT_SECRET") or input("Paste your App Secret Key: ").strip()
REDIRECT_URI  = "http://localhost:8080/callback"
SCOPES        = "boards:read,boards:write,pins:read,pins:write,user_accounts:read"
STATE         = "clearcents_oauth"

auth_code = None

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Authorized! You can close this tab.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>No code received.</h2>")

    def log_message(self, *args):
        pass  # suppress server logs

auth_url = (
    f"https://www.pinterest.com/oauth/"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI)}"
    f"&response_type=code"
    f"&scope={SCOPES}"
    f"&state={STATE}"
)

print("\n=== Pinterest OAuth Token Generator ===")
print(f"\nOpening browser to authorize your app...")
print(f"If it doesn't open automatically, visit:\n  {auth_url}\n")

server = http.server.HTTPServer(("localhost", 8080), Handler)
thread = threading.Thread(target=server.handle_request)
thread.start()
webbrowser.open(auth_url)
thread.join(timeout=120)

if not auth_code:
    print("Timed out waiting for authorization. Try again.")
    sys.exit(1)

print("Authorization code received. Exchanging for tokens...")

resp = requests.post(
    "https://api.pinterest.com/v5/oauth/token",
    data={
        "grant_type":   "authorization_code",
        "code":         auth_code,
        "redirect_uri": REDIRECT_URI,
    },
    auth=(CLIENT_ID, CLIENT_SECRET),
)

if not resp.ok:
    print(f"Token exchange failed: {resp.status_code} {resp.text}")
    sys.exit(1)

data = resp.json()

print("\n✅ Success! Update your GitHub Secrets with these values:\n")
print(f"PINTEREST_ACCESS_TOKEN  = {data.get('access_token')}")
print(f"PINTEREST_REFRESH_TOKEN = {data.get('refresh_token', 'N/A')}")
print(f"\nScopes granted: {data.get('scope', 'unknown')}")
print(f"Token expires in: {data.get('expires_in', '?')} seconds")

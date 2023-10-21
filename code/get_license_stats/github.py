# NOTE: Did not end up using this.

import requests

GITHUB_TOKEN = 'TOKEN_HERE'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Fetch top repositories based on stars
response = requests.get(
    'https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc',
    headers=HEADERS
)
top_repos = response.json().get('items', [])

license_count = {}

for repo in top_repos:
    repo_name = repo['full_name']
    license_endpoint = f"https://api.github.com/repos/{repo_name}/license"
    license_resp = requests.get(license_endpoint, headers=HEADERS)
    license_data = license_resp.json()

    license_key = license_data.get('license', {}).get('key', 'unknown')
    license_count[license_key] = license_count.get(license_key, 0) + 1

print(license_count)

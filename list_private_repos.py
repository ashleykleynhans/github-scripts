#!/usr/bin/env python3
import os
import sys
import requests


def list_private_repos():
    """Retrieve and display private GitHub repositories for authenticated user."""
    token = os.getenv('GITHUB_TOKEN')

    if not token:
        print('GITHUB_TOKEN environment variable not set')
        sys.exit(1)

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    url = 'https://api.github.com/user/repos'
    params = {'visibility': 'private', 'per_page': 100}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        repos = response.json()
        private_repos = [
            {
                'name': repo['name'],
                'url': repo['html_url'],
                'description': repo['description']
            }
            for repo in repos if repo['private'] and repo['owner']['type'] == 'User'
        ]

        return private_repos

    except requests.exceptions.RequestException as e:
        print(f'Error accessing GitHub API: {e}')
        return None


if __name__ == '__main__':
    repos = list_private_repos()

    if repos:
        for repo in repos:
            print(f'\nName: {repo["name"]}')
            print(f'URL: {repo["url"]}')
            print(f'Description: {repo["description"]}')

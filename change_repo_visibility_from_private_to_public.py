#!/usr/bin/env python3
import os
import sys
import requests


def modify_repo_visibility(token, repo_name):
    """Change repository visibility from private to public."""
    url = f'https://api.github.com/repos/{repo_name}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {'private': False}

    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f'Error modifying repository {repo_name}: {e}')
        return False


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
                'description': repo['description'],
                'full_name': repo['full_name']
            }
            for repo in repos if repo['private'] and repo['owner']['type'] == 'User'
        ]

        return private_repos, token

    except requests.exceptions.RequestException as e:
        print(f'Error accessing GitHub API: {e}')
        return None, None


if __name__ == '__main__':
    repos, token = list_private_repos()

    if repos:
        for repo in repos:
            print(f'\nName: {repo["name"]}')
            print(f'URL: {repo["url"]}')
            print(f'Description: {repo["description"]}')
            
            response = input(f'\nMake {repo["name"]} public? (y/N): ').lower()
            if response == 'y':
                if modify_repo_visibility(token, repo['full_name']):
                    print(f'Successfully made {repo["name"]} public')
                else:
                    print(f'Failed to make {repo["name"]} public')

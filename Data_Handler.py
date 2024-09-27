import requests

def fetch_github_user_info(username):
    """Holt die Benutzerinformationen von GitHub."""
    try:
        r = requests.get(f'https://api.github.com/users/{username}')

        if r.status_code == 200:
            user_data = r.json()
            return [user_data.get('login'), user_data.get('public_repos'), user_data.get('avatar_url')]

        print(f"Fehler: {r.status_code}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Anfrage: {e}")
        return None
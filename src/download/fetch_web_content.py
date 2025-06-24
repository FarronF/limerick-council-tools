import requests

def fetch_web_content(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
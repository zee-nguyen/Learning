import requests


def fetch_data(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.excetions.RequestError as e:
        print("error")
        return None


data = fetch_data("https://jsonplaceholder.typicode.com/posts")
print(data)

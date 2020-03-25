import requests
import requests.auth
from django.conf import settings


from django.shortcuts import render


def index(request):
    client_auth = requests.auth.HTTPBasicAuth(settings.REDDIT_KEY, settings.REDDIT_SECRET)
    post_data = {
        "grant_type": "password",
        "username": settings.REDDIT_USERNAME,
        "password":  settings.REDDIT_PASSWORD,
    }
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    headers = {"Authorization": f"bearer {response.json()['access_token']}",
               "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/best", headers=headers)

    # response = requests.get("https://www.reddit.com/r/redditdev/hot.json")

    children = response.json()['data']['children']
    children = children[:5]
    for child in children:
        response = requests.get(
            "https://oauth.reddit.com/" + child['data']['permalink'], headers=headers)
        if response.status_code != 200:
            child['status'] = "failure"
        else:
            child["comments"] = response.json()[1]['data']['children'][:5]

    ctx = {
        'reddit_items': children,
    }

    return render(request, "index.html", context=ctx)

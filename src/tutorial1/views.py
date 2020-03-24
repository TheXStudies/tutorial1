import requests
import requests.auth
from django.conf import settings


from django.shortcuts import render


def index(request):
    client_auth = requests.auth.HTTPBasicAuth(settings['REDDIT_KEY'], settings['REDDIT_SECRET'])
    post_data = {
        "grant_type": "password",
        "username": settings["REDDIT_USERNAME"],
        "password":  settings["REDDIT_USERNAME"],
    }
    headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                             headers=headers)
    headers = {"Authorization": f"bearer {response.json()['access_token']}",
               "User-Agent": "ChangeMeClient/0.1 by YourUsername"}
    response = requests.get("https://oauth.reddit.com/best", headers=headers)

    # response = requests.get("https://www.reddit.com/r/redditdev/hot.json")

    ctx = {
        'reddit_items': response.json()['data']['children'],
    }

    return render(request, "index.html", context=ctx)

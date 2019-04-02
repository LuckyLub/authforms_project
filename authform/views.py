from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

@login_required(login_url='/users/login/')
def frontpage(request):
    context = {}
    user = request.user
    api_key = user.profile.api_key
    topic = user.profile.topic.lower()

    url= f"https://api.nytimes.com/svc/topstories/v2/{topic}.json?api-key={api_key}"
    res = requests.get(url).json()
    if "fault" not in res.keys():
        context["results"] = res["results"]

    return render(request, "frontpage.html", context)


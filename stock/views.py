import json
import requests

from rest_framework.generics import ListAPIView
from .models import Company
from .serializers import CompanySerializer

def create_token(verifier):
    """
    [KIS API] Create the token to call the api
    """

    API = "/oauth2/tokenP"
    URL = f"{verifier.config['URL_BASE']}{API}"
    headers = {"content-type":"application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": verifier.config["APP_KEY"],
        "appsecret": verifier.config["APP_SECRET"],
    }
    res = requests.post(URL, headers=headers, data=json.dumps(body))

    if res.status_code == 200:
        access_token = {"authorization": res.json()["access_token"]}
        with open(verifier.config['TOKEN'], 'w') as f:
            json.dump(access_token, f)
        print("[create_token] Success - " + str(res.status_code))
    else:
        print("[create_token] Fail - " + str(res.status_code))


class CompanyListView(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

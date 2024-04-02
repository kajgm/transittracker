import requests
import os
import json
from format import *

API_ENDPOINT = "http://api.translink.ca/RTTIAPI/V1/stops/"
TOP_PATH = os.path.realpath("..")
CRED_PATH = TOP_PATH + "/credentials.json"


def get_api_key():
    translink_api_key = ""
    transit_app_api_key = ""
    try:
        with open(CRED_PATH, "r") as json_file:
            api_json = json.load(json_file)
        translink_api_key = api_json["translink_api_key"]
        transit_app_api_key = api_json["transit_app_api_key"]
    except:
        print("credentials.json not found, please enter credentials")
        translink_api_key = input("translink_api_key: ")
        transit_app_api_key = input("transit_app_api_key: ")

    return [translink_api_key, transit_app_api_key]


class transitApi:
    api_key = None
    auth = None
    headers = None
    stop = None

    def __init__(self, stp):
        self.auth = ""
        self.headers = {"Accept": "application/json"}
        self.api_key = get_api_key()[0]
        self.stop = stp

    def get_stop_info(self):
        res = None
        try:
            res = requests.get(
                API_ENDPOINT + str(self.stop) + "/estimates",
                headers=self.headers,
                params={"apiKey": self.api_key},
            )
        except:
            print(
                f"{tformatting.FAIL}Error: Failed to perform get request{tformatting.ENDC}"
            )

        return res

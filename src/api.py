import requests
import os
import json
from format import *

TL_API_ENDPOINT = "http://api.translink.ca/RTTIAPI/V1/stops/"
TA_API_ENDPOINT = "https://external.transitapp.com/v3/public/"
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
    TL_headers = None
    TA_auth = None
    TL_stop = None
    TA_stop = None

    def __init__(self, TL_stp, TA_stp):
        api_keys = get_api_key()
        self.TL_api_key = api_keys[0]
        self.TA_api_key = api_keys[1]
        self.TL_stop = TL_stp
        self.TA_stop = TA_stp

    def get_TL_stop_info(self):
        res = None
        try:
            res = requests.get(
                TL_API_ENDPOINT + str(self.TL_stop) + "/estimates",
                headers={"Accept": "application/json"},
                params={"apiKey": self.TL_api_key},
            )
        except:
            print(
                f"{tformatting.FAIL}Error: Failed to perform get request{tformatting.ENDC}"
            )

        return res

    def get_TA_stop_info(self):
        res = None
        try:
            res = requests.get(
                TA_API_ENDPOINT + "route_details",
                headers={"apiKey": self.TA_api_key},
                params={
                    "global_route_id": self.TA_stop,
                    "include_next_departure": True,
                },
                timeout=20,
            )
        except:
            print(
                f"{tformatting.FAIL}Error: Failed to perform get request{tformatting.ENDC}"
            )

        return res

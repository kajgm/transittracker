import requests
import os
import json
import datetime
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
    TA_route = None
    TA_name = None
    TA_headsign = None

    def __init__(self, TL_stp, TA_stp, TA_rt, TA_nm, TA_hsgn):
        api_keys = get_api_key()
        self.TL_api_key = api_keys[0]
        self.TA_api_key = api_keys[1]
        self.TL_stop = TL_stp
        self.TA_stop = TA_stp
        self.TA_route = TA_rt
        self.TA_name = TA_nm
        self.TA_headsign = TA_hsgn

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

    def get_TA_itinerary_info(self):
        res = None
        try:
            res = requests.get(
                TA_API_ENDPOINT + "route_details",
                headers={"apiKey": self.TA_api_key},
                params={
                    "global_route_id": self.TA_route,
                    "include_next_departure": True,
                },
                timeout=20,
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
                TA_API_ENDPOINT + "stop_departures",
                headers={"apiKey": self.TA_api_key},
                params={
                    "global_stop_id": self.TA_stop,
                },
                timeout=20,
            )
        except:
            print(
                f"{tformatting.FAIL}Error: Failed to perform get request{tformatting.ENDC}"
            )

        return res

    # returns a list of scheduled departures for a route
    def get_TA_route_time(self):
        res = self.get_TA_itinerary_info()
        itineraries = list(
            filter(
                lambda itnry: itnry["direction_headsign"]
                == "Coquitlam Central Station",
                res.json()["itineraries"],
            )
        )

        stops = []

        for itinerary in itineraries:
            for stop in itinerary["stops"]:
                if stop["stop_name"] == "Pitt River Rd / Mary Hill Rd Westbound":
                    stops.append(stop)

        departures = []

        nowTime = datetime.datetime.now()

        for stop in stops:
            epochTime = stop["next_departure"]["departure_time"]
            depTime = datetime.datetime.fromtimestamp(epochTime)
            timeDiff = depTime - nowTime
            timeLeft = divmod(timeDiff.total_seconds(), 60)[0]

            # only get departures within a 2-hour timeframe
            if timeLeft < 120:
                departures.append(int(timeLeft))

        return departures

    # returns realtime departures for a stop
    def get_TA_stop_time(self):

        res = self.get_TA_stop_info()

        nowTime = datetime.datetime.now()

        # since this stop has only 1 route, we don't need to do any filtering and can index 0
        # we should add the ability to filter routes later
        schedItem = res.json()["route_departures"][0]["itineraries"][0][
            "schedule_items"
        ][0]

        epochTime = schedItem["departure_time"]
        isRealTime = schedItem["is_real_time"]

        depTime = datetime.datetime.fromtimestamp(epochTime)
        depString = depTime.strftime("%I:%M %p")
        timeDiff = depTime - nowTime
        timeLeft = divmod(timeDiff.total_seconds(), 60)[0]

        return [int(timeLeft), isRealTime, depString]

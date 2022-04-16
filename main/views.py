from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import pickle
import flexpolyline as fp
import pandas as pd


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class V1View(APIView):
    def post(self, request):

        src_addr = request.data["src"]
        dst_addr = request.data["dst"]
        src = getCoordinates(src_addr)
        dst = getCoordinates(dst_addr)

        HERE_API_KEY = "**********************************"

        route_url = "https://router.hereapi.com/v8/routes"

        params = {
            "origin": src,
            "destination": dst,
            "routingMode": "short",
            "apiKey": HERE_API_KEY,
            "alternatives": 6,
            "transportMode": "car",
            "return": "actions,polyline,summary",
        }

        response = requests.get(route_url, params=params).json()

        n_routes = len(response["routes"])
        waypoints = [
            [[[] for _ in range(n_routes)] for _ in range(n_routes)]
            for _ in range(n_routes)
        ]

        route_scores = []
        print(n_routes)
        for i in range(n_routes):
            route_obj = response["routes"][i]
            for j in range(len(route_obj["sections"])):
                section_obj = route_obj["sections"][j]
                positions = fp.decode(section_obj["polyline"])
                route_waypoints = [list(ele) for ele in positions]

            waypoints[i] = route_waypoints
            route_scores.append((getScore(waypoints[i]), i))

        route_scores.sort()
        print(route_scores)

        all_routes = []
        for i in range(n_routes):
            j = route_scores[i][1]
            distance = response["routes"][j]["sections"][0]["summary"]["length"] / 1000
            duration = response["routes"][j]["sections"][0]["summary"]["baseDuration"]
            json_body = {
                "waypoints": waypoints[j],
                "distance": distance,
                "duration": duration,
                "score": route_scores[i][0],
            }
            all_routes.append(json_body)
        return Response(all_routes, status=status.HTTP_200_OK)


class clusterView(APIView):
    def get(self, request):
        df = pd.read_csv(os.getcwd() + "/model/final.csv")
        payload = df.values.tolist()
        return Response({"clusters": payload}, status=status.HTTP_200_OK)


def getScore(waypoints):
    filename = os.getcwd() + "/model/finalized_kNN_model.sav"
    model = pickle.load(open(filename, "rb"))
    y_pred = model.predict(waypoints)
    return sum(y_pred)


def getCoordinates(addr):
    addr_url = "http://dev.virtualearth.net/REST/v1/Locations"
    BING_API_KEY = "**********************************"
    params = {"query": addr, "maxResults": 1, "key": BING_API_KEY}
    response = requests.get(addr_url, params=params).json()
    addr = response["resourceSets"][0]["resources"][0]["point"]["coordinates"]

    return str(addr[0]) + "," + str(addr[1])

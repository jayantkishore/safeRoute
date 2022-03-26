from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
import pickle
import pandas as pd
class HomePageView(TemplateView):
    template_name = 'home.html'
class AboutPageView(TemplateView):
    template_name = 'about.html'
class V1View(APIView):
    def post(self, request):
        
        src = request.data['src']
        dst = request.data['dst']
        API_KEY="ApeJ9VF0hG73kt0lv0qLdSMAOUUNI3vn-SEMmrc7s6ywCKLjWEgeSA6EJW5ODb3k"
        
        route_url="http://dev.virtualearth.net/REST/V1/Routes/Driving"
       
        params = {
            'wp.0': src,
            'wp.1': dst,
            'routeAttributes': 'routePath',
            'key':API_KEY,
            'maxSolutions':3,
            'routePathOutput':'Points'

        }
        json_body = {
            'message' : "hi"
        }
        #url = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=23.81172, 86.442141&wp.1=23.813814, 86.441608&routeAttributes=routePath&key=ApeJ9VF0hG73kt0lv0qLdSMAOUUNI3vn-SEMmrc7s6ywCKLjWEgeSA6EJW5ODb3k&maxSolutions=5&routePathOutput=Points"
        response = requests.get(route_url,params=params).json()

        ##print(type(response))
        ##print(response)
        n_routes=response['resourceSets'][0]['estimatedTotal']
        waypoints = [[[ [] for _ in range(n_routes)] for _ in range(n_routes)] for _ in range(n_routes)]
       # route_scores=[[None]*2]*n_routes
        route_scores = []
        print(n_routes)
        for i in range(n_routes):
            waypoints[i]=response["resourceSets"][0]["resources"][i]["routePath"]["line"]["coordinates"]
            route_scores.append((getScore(waypoints[i]),i))
            #route_scores[i][0]=i
            #route_scores[i][1]=getScore(waypoints[i])
        print(route_scores)
        route_scores.sort()
        #route_scores = Sort(route_scores)
        # optimal_route_idx = route_scores[0][1]
        # optimal_route = response["resourceSets"][0]["resources"][optimal_route_idx]["routePath"]["line"]["coordinates"]

        # return Response(optimal_route,status = status.HTTP_200_OK)
        all_routes=[]
        for i in range(n_routes):
            j = route_scores[i][1]
            waypoints = response["resourceSets"][0]["resources"][j]["routePath"]["line"]["coordinates"]
            distance = response["resourceSets"][0]["resources"][j]['travelDistance']
            duration = response["resourceSets"][0]["resources"][j]['travelDuration']
            json_body={'waypoints':waypoints,'distance':distance,'duration':duration,'score':route_scores[i][0]}
            all_routes.append(json_body)
        return Response(all_routes,status = status.HTTP_200_OK)


class clusterView(APIView):
    def get(self,request):
        df = pd.read_csv(os.getcwd()+'/model/crime.csv')
        payload = df.values.tolist()
        return Response({'clusters':payload},status = status.HTTP_200_OK)
#def Sort(sub_li):

#    return(sorted(sub_li, key = lambda x: x[1],reverse=True))
def getScore(waypoints):
    filename = os.getcwd()+'/model/finalized_kNN_model.sav'
    model = pickle.load(open(filename, 'rb'))
    y_pred = model.predict(waypoints)
    return sum(y_pred)
        
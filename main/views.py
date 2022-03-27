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
    template_name = 'home.html'
class AboutPageView(TemplateView):
    template_name = 'about.html'
class V1View(APIView):
    def post(self, request):
        
        src_addr = request.data['src']
        dst_addr = request.data['dst']
        src = getCoordinates(src_addr)
        dst = getCoordinates(dst_addr)

        HERE_API_KEY="GjDOz0a4Xv04xFVpe8ywIaw1DNQvIX3SJHCgSD3WMs0"
        
        route_url="https://router.hereapi.com/v8/routes"
       
        params = {
            'origin': src,
            'destination': dst,
            'routingMode': 'short',
            'apiKey':HERE_API_KEY,
            'alternatives':6,
            'transportMode':'car',
            'return':'actions,polyline,summary'
        }
        #json_body = {
        #    'message' : "hi"
        #}
        #url = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=23.81172, 86.442141&wp.1=23.813814, 86.441608&routeAttributes=routePath&key=ApeJ9VF0hG73kt0lv0qLdSMAOUUNI3vn-SEMmrc7s6ywCKLjWEgeSA6EJW5ODb3k&maxSolutions=5&routePathOutput=Points"
        response = requests.get(route_url,params=params).json()

        ##print(type(response))
        ##print(response)
        n_routes=len(response['routes'])
        waypoints = [[[ [] for _ in range(n_routes)] for _ in range(n_routes)] for _ in range(n_routes)]
       # route_scores=[[None]*2]*n_routes
        route_scores = []
        print(n_routes)
        for i in range(n_routes):
            route_obj = response['routes'][i]
            for j in range(len(route_obj['sections'])):
                section_obj = route_obj['sections'][j]
                positions = fp.decode(section_obj['polyline'])
                route_waypoints = [list(ele) for ele in positions]
                
                          
                # for k in range(len(section_obj['actions'])):
                #     point=[]
                #     point.append(positions[section_obj['actions'][k]['offset']][0])
                #     point.append(positions[section_obj['actions'][k]['offset']][1])
                #     route_waypoints.append(point)

            waypoints[i]=route_waypoints
            route_scores.append((getScore(waypoints[i]),i))
            #route_scores[i][0]=i
            #route_scores[i][1]=getScore(waypoints[i])
        
        route_scores.sort()
        print(route_scores)
        #route_scores = Sort(route_scores)
        #optimal_route_idx = route_scores[0][1]
        #optimal_route = waypoints[optimal_route_idx]
        #return Response(optimal_route,status = status.HTTP_200_OK)
        all_routes=[]
        for i in range(n_routes):
            j = route_scores[i][1]
            distance = response['routes'][j]['sections'][0]['summary']['length']/1000
            duration = response['routes'][j]['sections'][0]['summary']['baseDuration']
            json_body={'waypoints':waypoints[j],'distance':distance,'duration':duration,'score':route_scores[i][0]}
            all_routes.append(json_body)
        return Response(all_routes,status = status.HTTP_200_OK)

class clusterView(APIView):
    def get(self,request):
        df = pd.read_csv(os.getcwd()+'/model/final.csv')
        payload = df.values.tolist()
        return Response({'clusters':payload},status = status.HTTP_200_OK)
#def Sort(sub_li):

#    return(sorted(sub_li, key = lambda x: x[1],reverse=True))
def getScore(waypoints):
    filename = os.getcwd()+'/model/finalized_kNN_model.sav'
    model = pickle.load(open(filename, 'rb'))
    y_pred = model.predict(waypoints)
    return sum(y_pred)
def getCoordinates(addr):
    addr_url = 'http://dev.virtualearth.net/REST/v1/Locations'
    BING_API_KEY = 'ApeJ9VF0hG73kt0lv0qLdSMAOUUNI3vn-SEMmrc7s6ywCKLjWEgeSA6EJW5ODb3k'
    params = {
        'query': addr,
        'maxResults': 1,
        'key':BING_API_KEY
    }
    response = requests.get(addr_url,params=params).json()
    addr = response['resourceSets'][0]['resources'][0]['point']['coordinates']

    return str(addr[0])+','+str(addr[1])

   

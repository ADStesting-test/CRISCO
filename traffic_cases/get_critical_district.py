import json
import os
import random

# get road districts and accident-prone districts
# root_path = os.path.abspath(os.path.dirname(__file__)).split('RACER')[0]
# path = os.path.join(root_path, "RACER/traffic_cases/RoadDistrict")


path = "RoadDistrict"
f = open(path, encoding='utf-8')
road_set = json.load(f)
f.close()

def get_roads(id):
    return road_set[id]["roads"]

def get_ego_district(road_type):
    return road_set[road_type]["ego_lane"]

def get_hazard_section(road_type, hazard_section):
    return road_set[road_type][hazard_section]

def get_ego_next_lane(road_type):
    return road_set[road_type]["ego_next_lane"]

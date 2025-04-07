import json
import os
import random

from generate_scenario.environment_generation.environment_sampling import importance_sampling
import lgsvl
import math

def define_environment(sim, weather):
    rain, fog, wetness, cloudiness, damage = 0, 0, 0, 0, 0
    for item in weather:
        if item == "sunny":
            time = math.ceil(importance_sampling(0.8, 1)[0]*15)
            sim.set_time_of_day(time, fixed=True)
        if item == "rainy":
            rain = importance_sampling(0.7, 1)[0]
            rain = round(rain, 2)
        if item == "foggy":
            fog = importance_sampling(0.6, 1)[0]
            fog = round(fog, 2)
        if item == "snowy":
            snow = 0.05
            damage = round(snow, 2)
        if item == "windy":
            fog = max(round(importance_sampling(0.5, 1)[0], 2), fog)
            damage = 0.05
        if item == "cloudy":
            cloudiness = importance_sampling(0.7, 1)[0]
            cloudiness = round(cloudiness, 2)
        if item == "dusk":
            time = round(importance_sampling(0.9, 1)[0]*11, 2)
            sim.set_time_of_day(time, fixed=True)
        if item == "night":
            time = random.choice([round(importance_sampling(0.9, 1)[0]*12, 2), round(importance_sampling(0.1, 0.9)[0]*4, 2)])
            sim.set_time_of_day(time, fixed=True)
    sim.weather = lgsvl.WeatherState(rain=rain, fog=fog, wetness=wetness, cloudiness=cloudiness, damage=damage)

# current_script_path = os.path.abspath(sys.argv[0])
# root_path = get_project_root(current_script_path)
path = os.chdir("..")
path = os.chdir("..")
root_path = os.getcwd()
path = os.path.join(root_path, "traffic_cases/RoadDistrict")
f = open(path, encoding='utf-8')
traffic_signal_json = json.load(f)
f.close()

def get_traffic_signal(road_type):
    traffic_signal_array = traffic_signal_json[road_type]["signal_position"]

    return traffic_signal_array

def define_road_traffic_signal_svl(sim, road_type):
    signal_position = get_traffic_signal(road_type)
    if road_type == 'crossing' or road_type == 'T-junction':
        for signal_light in signal_position:
            signal = sim.get_controllable(lgsvl.Vector(signal_light), "signal")
            control_policy = "trigger=60;green=30;yellow=3;red=20;loop"
            signal.control(control_policy)
    elif road_type == 'straight road':
        for signal_light in signal_position:
            signal = sim.get_controllable(lgsvl.Vector(signal_light), "signal")
            control_policy = "trigger=80;green=100;yellow=0;red=0;loop"
            signal.control(control_policy)

# def define_weather_svl(parameter_list, parameters):
#     # weather_parameter in svl
#     rain, fog, wetness, cloudiness = 0, 0, 0, 0
#     for i in range(len(parameter_list)):
#         if parameter_list[i] in environment_svl_json['view_factors']:
#             visibility = importance_sampling(0.4, 1)
#             visibility = round(visibility[0], 2)
#             cloudiness = 1 - visibility
#         if parameter_list[i] in environment_svl_json['ground_factors']:
#             wetness = importance_sampling(0.6, 1)
#             wetness = round(wetness[0], 2)
#         if parameter_list[i] == 'heavy rain':
#             rain = importance_sampling(0.7, 1)
#             rain = round(rain[0], 2)
#         if parameter_list[i] == 'fog':
#             fog = importance_sampling(0.5, 1)
#             fog = round(fog[0], 2)
#     return lgsvl.WeatherState(rain=rain, fog=fog, wetness=wetness, cloudiness=cloudiness)

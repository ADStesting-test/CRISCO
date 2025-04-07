import re
import sys

from generate_scenario.checker import get_project_root

sys.path.append("..")
from generate_scenario.connect_simulator import *
from generate_scenario.environment_generation.define_environment_svl  import *
from generate_scenario.generate_behavior_trajectory import *

import json


def reproduce_scenarios(file, way):
    # connect to simulator
    sim = connect_svl()

    # Loads the named map in the connected simulator, and define traffic signal state on selected road
    # if sim.current_scene == lgsvl.wise.DefaultAssets.map_sanfrancisco:
    #     sim.reset()
    # else:
    #     sim.load(lgsvl.wise.DefaultAssets.map_sanfrancisco)
    if sim.current_scene == "SanFrancisco_correct":
           sim.reset()
    else:
        sim.load("SanFrancisco_correct")

    scenario_json = file
    # define_road_traffic_signal_svl(sim, scenario_json["road type"])

    # current_script_path = os.path.abspath(sys.argv[0])
    # root_path = get_project_root(current_script_path)
    root_path = os.chdir("..")
    root_path = os.getcwd()
    path = os.path.join(root_path, "configuration/requirement_items")
    f = open(path, encoding='utf-8')
    requirement_set = json.load(f)
    f.close()
    behaviors_set = requirement_set["behaviors"]

    # define environment parameter
    # weather = scenario_json["weather"]
    # sim.weather = lgsvl.WeatherState(rain=round(weather[0]["rain"], 2), fog=round(weather[1]["fog"] , 2), wetness=round(weather[2]["wetness"], 2), cloudiness=round(weather[3]["cloudiness"], 2), damage=round(weather[4]["damage"], 2))
    # sim.set_time_of_day(weather[5]["time_of_day"], fixed=True)

    # define participants and their trajectories
    ego_spawn = None
    for key, value in scenario_json.items():
        if any(char.isdigit() for char in key):
            tmp = re.sub(r'\d+', '', key)
            if 'Pedestrian' in key:
                generate_pedestrian_participants(sim, value)
            else:
                generate_vehicle_participants(sim, value, tmp)
        elif key in behaviors_set:
            if 'Pedestrian' in key:
                generate_pedestrian_participants(sim, value)
            else:
                generate_vehicle_participants(sim, value, key)
        elif key == "ego":
            ego_spawn = lgsvl.Vector(value[0][0], 0, value[0][1])
            if way == "replay":
                generate_vehicle_participants(sim, value, key, True)
            elif way == "retest":
                ego_init = value[0]
                ego_destination = value[-1]
                ego_speed = value[0][2]
                # spawn ego
                ego_state, _ = spawn(sim, ego_init[0], ego_init[1], ego_speed)
                # bridge ego into Apollo
                ego = sim.add_agent('2e966a70-4a19-44b5-a5e7-64e00a7bc5de', lgsvl.AgentType.EGO, ego_state)
                # ego_destination = get_position(sim, ego_destination[0], ego_destination[1])
                bridgeApollo(sim, ego, ego_destination)

    print("start reproducing scenario")

    # execute the scenario
    tr = lgsvl.Transform(lgsvl.Vector(0, 50, 0) + ego_spawn, lgsvl.Vector(90, 0, 0))
    sim.set_sim_camera(tr)
    for i in range(500):
        sim.run(0.1)

    print("finish reproducing scenario")

# if __name__ == '__main__':
#     key = "cut in11"
#     tmp = re.sub(r'\d+', '', key)
#     tmp = tmp + "9"
#     print(tmp)




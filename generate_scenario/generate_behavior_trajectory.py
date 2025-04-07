import random
import sys

# from func_timeout import func_set_timeout


from generate_scenario.behavior_trajectory_solver.cut_in import cut_in
from generate_scenario.behavior_trajectory_solver.cut_out import cut_out
from generate_scenario.behavior_trajectory_solver.follow_lane import follow_lane
from generate_scenario.behavior_trajectory_solver.follow_vehicle import follow_vehicle
from generate_scenario.behavior_trajectory_solver.park import park
from generate_scenario.behavior_trajectory_solver.pedestrian_cross import pedestrian_cross
from generate_scenario.behavior_trajectory_solver.pedestrian_walk import pedestrian_walk
from generate_scenario.behavior_trajectory_solver.retrograde import retrograde
from generate_scenario.behavior_trajectory_solver.turn_around import turn_around
from generate_scenario.behavior_trajectory_solver.vehicle_cross import vehicle_cross
from generate_scenario.checker import get_project_root
from generate_scenario.get_waypoints import *


# @func_set_timeout(10)
def generate_trajectory(network, road_type, behavior, ego_init, ego_dest, ego_speed, num, hazard_section):
    if behavior == 'follow vehicle':
        return follow_vehicle(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'follow lane':
        return follow_lane(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'cut in':
        return cut_in(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'cut out':
        return cut_out(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == "change lane":
        behavior = random.choice(["cut in", "cut out"])
        return generate_trajectory(network, road_type, behavior, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == "brake":
        return generate_trajectory(network, road_type, "follow lane", ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'retrograde':
        return retrograde(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'park':
        return park(network, road_type, ego_init, ego_dest, num, hazard_section)
    elif behavior == 'walk cross road':
        return pedestrian_cross(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'walk along road':
        return pedestrian_walk(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'vehicle cross':
        return vehicle_cross(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)
    elif behavior == 'turn around':
        return turn_around(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section)


def generate_behavior_trajectory(network, road_type, behavior, ego_init, ego_dest, ego_speed, num):
    # try:
    #     trajectory = generate_trajectory(network, road_type, behavior, ego_init, ego_dest, ego_speed, num)
    # except:
    #     trajectory = generate_trajectory(network, road_type, behavior, ego_init, ego_dest, ego_speed, num)
    # current_script_path = os.path.abspath(sys.argv[0])
    # root_path = get_project_root(current_script_path)
    root_path = os.chdir("..")
    root_path = os.getcwd()
    path = os.path.join(root_path, "configuration/requirement_items")
    f = open(path, encoding='utf-8')
    requirement_set = json.load(f)
    f.close()
    hazard_section_set = requirement_set["hazard section"]
    hazard_section_straight = requirement_set["hazard section straight"]
    print("start generating trajectory")
    if road_type == "straight road":
        hazard_section = random.choice(hazard_section_straight)
    else:
        hazard_section = random.choice(hazard_section_set)
    trajectory = generate_trajectory(network, road_type, behavior, ego_init, ego_dest, ego_speed, num, hazard_section)
    print("finish generating trajectory")
    return trajectory


def generate_vehicle_participants(sim, trajectories, behavior, ego=False):
    if behavior == 'Park':
        vehicle, rotation = spawn(sim, trajectories[0], trajectories[1], 0, reverse=True)
        vehicle_type = random.choice(["Sedan", "BoxTruck"])
        agent = sim.add_agent(vehicle_type, lgsvl.AgentType.NPC, vehicle)
    else:
        if ego:
            vehicle_type = "SUV"
            vehicle, rotation = spawn(sim, trajectories[0][0], trajectories[0][1], 0)
            waypoints = get_vehicle_waypoints_time(sim, trajectories)
        else:
            vehicle_type = random.choice(["Sedan", "BoxTruck"])
            vehicle, rotation = spawn(sim, trajectories[0][0][0], trajectories[0][0][1], 0)
            waypoints = get_vehicle_waypoints_time(sim, trajectories[0], trajectories[1])

        agent = sim.add_agent(vehicle_type, lgsvl.AgentType.NPC, vehicle)
        agent.follow(waypoints)


def generate_pedestrian_participants(sim, trajectories):
    walker, _ = spawn(sim, trajectories[0][0][0], trajectories[0][0][1], 0)
    agent = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, walker)
    waypoints = get_walk_waypoints_time(sim, trajectories[0], trajectories[1])
    agent.follow(waypoints)
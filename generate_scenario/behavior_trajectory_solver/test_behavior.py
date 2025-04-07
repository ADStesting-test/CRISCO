import sys

from scenic.core.vectors import Vector

sys.path.append("../..")
from generate_scenario.generate_behavior_trajectory import generate_behavior_trajectory
from generate_scenario.get_map import get_network

sys.path.append("../..")
import random

import lgsvl

from generate_scenario.connect_simulator import connect_svl, bridgeApollo
from generate_scenario.get_waypoints import spawn, get_vehicle_waypoints_time

network = get_network()

sim = connect_svl()
if sim.current_scene == lgsvl.wise.DefaultAssets.map_sanfrancisco_correct:
    sim.reset()
else:
    sim.load(lgsvl.wise.DefaultAssets.map_sanfrancisco_correct)
sim.set_time_of_day(24)

ego_spawn = [-63.8, -120.5]
ego_destination = [33.3, -40]
# ego_spawn = [33.3, -40]
# ego_destination = [79, -84]
ego_speed = random.randint(8, 12)
print("npc starting and destination lanes:")
npc_starting_lane = network.laneAt(Vector(-2, -7.2))
npc_dest_lane = network.laneAt(Vector(33.3, -40))
npc_connecting_lane = network.laneAt(Vector(16.1, -25))
print(npc_starting_lane.id)
print(npc_dest_lane.id)
print(npc_connecting_lane.id)

behavior = "vehicle cross"
road_type = "crossing"
hazard_section = "turning"
trajectories = generate_behavior_trajectory(network, road_type, behavior, ego_spawn, ego_destination, ego_speed, 1, hazard_section)
trajectory = trajectories[0]
# waypoints = get_vehicle_waypoints_time(sim, trajectory[0], trajectory[1])

# print("trajectory")
# print(trajectory)
# print("waypoints:")
# print(waypoints)

# vehicle_type = "Sedan"
# vehicle, rotation = spawn(sim, trajectory[0][0][0], trajectory[0][0][1], 0)
# agent = sim.add_agent(vehicle_type, lgsvl.AgentType.NPC, vehicle)
# agent.follow(waypoints)
#
# for i in range(500):
#     sim.run(0.1)

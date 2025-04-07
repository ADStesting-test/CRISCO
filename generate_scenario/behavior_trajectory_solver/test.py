import random

import lgsvl
from z3 import *

from generate_scenario.behavior_trajectory_solver.connect_lanes import combine_center_line
from generate_scenario.behavior_trajectory_solver.cut_in import cut_in
from generate_scenario.behavior_trajectory_solver.cut_out import cut_out
from generate_scenario.behavior_trajectory_solver.follow_lane import follow_lane
from generate_scenario.behavior_trajectory_solver.follow_vehicle import follow_vehicle
from generate_scenario.behavior_trajectory_solver.park import park
from generate_scenario.behavior_trajectory_solver.pedestrian_cross import pedestrian_cross
from generate_scenario.behavior_trajectory_solver.pedestrian_walk import pedestrian_walk
from generate_scenario.behavior_trajectory_solver.point_in_road import *
from generate_scenario.behavior_trajectory_solver.retrograde import retrograde
from generate_scenario.behavior_trajectory_solver.vehicle_cross import vehicle_cross
from generate_scenario.connect_simulator import connect_svl
from generate_scenario.generate_behavior_trajectory import generate_vehicle_participants
from traffic_cases.get_critical_district import get_hazard_section


# def cut_in(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section):
#     print("cut in")
#
#     accident_prone = get_hazard_section(road_type, hazard_section)
#     # get lanes of initial position and destination of ego
#     ego_point = Vector(ego_init[0], ego_init[1])
#     ego_init_lane = network.laneAt(ego_point)
#     # ego_road = network.findPointIn(ego_point, network.roads, False)
#     ego_dest_lane = network.laneAt(Vector(ego_dest[0], ego_dest[1]))
#     line_string = combine_center_line(network, ego_init_lane, ego_dest_lane, road_type)
#     ego_init_project_length = line_string.project(Point(ego_init[0], ego_init[1]))
#     ego_dest_project_length = line_string.project(Point(ego_dest[0], ego_dest[1]))
#
#     rejection = True
#     waypoint_sequence = []
#
#     while rejection:
#         # select destination of npc in accident-prone area
#         npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
#                     random.uniform(accident_prone[1][0], accident_prone[1][1])]
#         npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
#         while npc_dest_lane != ego_dest_lane:
#             npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
#                         random.uniform(accident_prone[1][0], accident_prone[1][1])]
#             npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
#         # select initial position of npc outside accident-prone area
#
#         npc_init_project_length, npc_init_lane, center_line, npc_dest_project_length = cut_in_init_position(network, ego_init, ego_init_project_length, npc_dest, npc_dest_lane, road_type)
#
#         # z3 solver
#         T = Real("T")
#         C = Real("C")
#
#         ego_initial_position = Real("ego_initial_position")
#         ego_target_position = Real("ego_target_position")
#         # solve constraints of waypoints
#         npc_initial_speed = Real("npc_initial_speed")
#         npc_target_speed = Real("npc_target_speed")
#         npc_initial_position = Real("npc_initial_position")
#         npc_target_position = Real("npc_target_position")
#         npc_accelerate = Real("npc_accelerate")
#         npc_average_speed = Real("npc_average_speed")
#
#         time_c = []
#         position_c = []
#         speed_c = []
#         time = random.randint(0, 2)
#         # driving time and trigger time
#         time_c += [T * ego_speed == ego_target_position - ego_initial_position] + \
#                   [T - C >= time] + \
#                   [And(T >= 1, C >= 1)]
#         # speeds
#         speed_c += [And(0 <= npc_initial_speed, npc_initial_speed <= 25)] + \
#                    [And(0 <= npc_target_speed, npc_target_speed <= 25)] + \
#                    [npc_average_speed == (npc_target_speed + npc_initial_speed) / 2.0] + \
#                    [npc_accelerate == (npc_target_speed - npc_initial_speed) / C] + \
#                    [And(-10 <= npc_accelerate, npc_accelerate <= 5.5)]
#         # positions
#         position_c += [ego_initial_position == ego_init_project_length] + \
#                       [ego_target_position == ego_dest_project_length] + \
#                       [npc_target_position == npc_dest_project_length] + \
#                       [npc_initial_position == npc_init_project_length] + \
#                       [C * npc_average_speed == npc_target_position - npc_initial_position]
#
#         s = Solver()
#         s.add(speed_c + position_c + time_c)
#
#         set_option(rational_to_decimal=True)
#         set_option(precision=1)
#
#         set_option(rational_to_decimal=True)
#         set_option(precision=1)
#
#         res = []
#         cnt = 0
#         m = None
#         while cnt < 100:
#             cnt += 1
#             if s.check() == sat:
#                 m = s.model()
#                 res.append([toNum(m.evaluate(npc_initial_speed)), toNum(m.evaluate(npc_target_speed)),
#                             toNum(m.evaluate(npc_initial_position))])
#                 fml = And(npc_initial_speed == res[-1][0], npc_target_speed == res[-1][1],
#                           npc_initial_position == res[-1][2])
#                 s.add(Not(fml))
#
#         if len(res) < num:
#             continue
#         rejection = False
#         ans_list = random.sample(res, num)
#         for ans in ans_list:
#             # center_line = combine_center_line(npc_init_lane, npc_dest_lane)
#             waypoints = []
#             t = toNum(m.evaluate(T))
#             c = toNum(m.evaluate(C))
#             acc = (ans[1] - ans[0]) / c
#             ra = random.randint(0, int(c) - 1)
#             for i in range(int(c * 10)):
#                 speed = ans[0] + acc * (i + 1) * 0.1
#                 pos = ans[2] + (ans[0] + speed) / 2.0 * (i + 1) * 0.1
#                 if road_type == "straight road":
#                     if i < ra * 10:
#                         p = npc_init_lane.centerline.lineString.interpolate(pos)
#                         waypoints.append([p.x, p.y, speed])
#                     else:
#                         p = npc_dest_lane.centerline.lineString.interpolate(pos)
#                         waypoints.append([p.x, p.y, speed])
#                 elif road_type == "urban":
#                     p = center_line.interpolate(pos)
#                     waypoints.append([p.x, p.y, speed])
#             waypoint_sequence.append([waypoints, t - c])
#
#     return waypoint_sequence
#
#
# def cut_in_init_position(network, position, ego_init_project_length, npc_dest, npc_dest_lane, road_type):
#     # relative = random.choice(['front', 'behind'])
#     # relative = 'behind'
#     npc_init = get_npc_init_point(network, position, road_type)
#     npc_point = Vector(npc_init[0], npc_init[1])
#     npc_init_lane = network.laneAt(npc_point)
#     center_line = combine_center_line(network, npc_init_lane, npc_dest_lane, road_type)
#     npc_dest_project_length = center_line.project(Point(npc_dest[0], npc_dest[1]))
#     npc_init_project_length = center_line.project(Point(npc_init[0], npc_init[1]))
#     while npc_init_lane == npc_dest_lane or abs(ego_init_project_length - npc_init_project_length) < 5 or (npc_dest_project_length - npc_init_project_length) < random.randint(5, 20):
#         npc_init = get_npc_init_point(network, position, road_type)
#         npc_point = Vector(npc_init[0], npc_init[1])
#         npc_init_lane = network.laneAt(npc_point)
#         center_line = combine_center_line(network, npc_init_lane, npc_dest_lane, road_type)
#         npc_init_project_length = center_line.project(Point(npc_init[0], npc_init[1]))
#         npc_dest_project_length = center_line.project(Point(npc_dest[0], npc_dest[1]))
#     return npc_init_project_length, npc_init_lane, center_line, npc_dest_project_length

if __name__ == '__main__':
    network = get_network()
    sim = connect_svl()
    if sim.current_scene == lgsvl.wise.DefaultAssets.map_sanfrancisco_correct:
        sim.reset()
    else:
        sim.load(lgsvl.wise.DefaultAssets.map_sanfrancisco_correct)
    # trajectory = cut_in(network, "crossing", [-63, -120.5], [135.6, 90], 5, 1, "end")
    # trajectory = cut_in(network, "crossing", [-63, -120.5], [-38.3, -96.2], 5, 1, "turning")
    sim.set_time_of_day(24)
    sim.set_time_of_day(6, fixed=True)
    # trajectory = cut_in(network, "crossing", [-63, -120.5], [1, -51.1], 10, 1, "junction")
    trajectory = follow_lane(network, "crossing", [-63, -120.5], [135.6, 90], 10, 1, "end")
    generate_vehicle_participants(sim, trajectory[0], "cut in")
    tr = lgsvl.Transform(lgsvl.Vector(0, 50, 0) + lgsvl.Vector(trajectory[0][0][0][0], 10, trajectory[0][0][0][1]), lgsvl.Vector(90, 0, 0))
    sim.set_sim_camera(tr)
    for i in range(500):
        sim.run(0.1)
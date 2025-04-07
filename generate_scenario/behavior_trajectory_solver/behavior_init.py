import random

from scenic.core.vectors import Vector
from shapely.geometry import Point

from generate_scenario.behavior_trajectory_solver.connect_lanes import combine_center_line
from generate_scenario.behavior_trajectory_solver.point_in_road import straight_road_init_point


def cut_in_init_position(network, position, ego_init_project_length, npc_dest, npc_dest_lane, road_type):
    relative = random.choice(['front', 'behind'])
    # relative = 'behind'
    # , same_lane = False, relative = relative
    npc_init = straight_road_init_point(network, position, road_type, relative=relative)
    npc_point = Vector(npc_init[0], npc_init[1])
    npc_init_lane = network.laneAt(npc_point)
    center_line = combine_center_line(network, npc_init_lane, npc_dest_lane, road_type)
    npc_dest_project_length = center_line.project(Point(npc_dest[0], npc_dest[1]))
    npc_init_project_length = center_line.project(Point(npc_init[0], npc_init[1]))
    while npc_init_lane == npc_dest_lane or abs(ego_init_project_length - npc_init_project_length) < 5 or (npc_dest_project_length - npc_init_project_length) < random.randint(5, 20):
        npc_init = straight_road_init_point(network, position, road_type, relative=relative)
        npc_point = Vector(npc_init[0], npc_init[1])
        npc_init_lane = network.laneAt(npc_point)
        center_line = combine_center_line(network, npc_init_lane, npc_dest_lane, road_type)
        npc_init_project_length = center_line.project(Point(npc_init[0], npc_init[1]))
        npc_dest_project_length = center_line.project(Point(npc_dest[0], npc_dest[1]))
    return npc_init_project_length, npc_init_lane, center_line, npc_dest_project_length

def cut_out_init_position(network, position, npc_dest, npc_dest_lane, ego_init_project_length, road_type):
    # npc_init = sample_road_points(position)
    # relative = random.choice(['front', 'behind'])
    relative = 'front'
    npc_init = straight_road_init_point(network, position, road_type, relative=relative)
    npc_point = Vector(npc_init[0], npc_init[1])
    npc_init_lane = network.laneAt(npc_point)
    center_line = combine_center_line(network, npc_init_lane, npc_dest_lane, road_type)
    npc_dest_project_length = center_line.project(Point(npc_dest[0], npc_dest[1]))
    npc_init_project_length = center_line.project(Point(npc_init[0], npc_init[1]))
    while npc_init_lane == npc_dest_lane or abs(npc_init_project_length-ego_init_project_length) < 5 or abs(npc_init_project_length-ego_init_project_length) > 30 or (npc_dest_project_length - npc_init_project_length) < random.randint(5, 50):
        npc_init = straight_road_init_point(network, position, road_type, relative=relative)
        npc_point = Vector(npc_init[0], npc_init[1])
        npc_init_lane = network.laneAt(npc_point)
        center_line = combine_center_line(network, npc_init_lane, npc_dest_lane, road_type)
        npc_init_project_length = center_line.project(Point(npc_init[0], npc_init[1]))
        npc_dest_project_length = center_line.project(Point(npc_dest[0], npc_dest[1]))
    return npc_init_project_length, npc_init_lane, center_line, npc_dest_project_length

def follow_lane_init_position(network, road_type, position, npc_dest_lane, npc_dest_project_length, ego_line_string, ego_init_length):
    npc_init = straight_road_init_point(network, position, road_type, same_lane=True, relative='behind', reverse=None)
    npc_point = Vector(npc_init[0], npc_init[1])
    npc_init_lane = network.laneAt(npc_point)
    npc_init_project_length = npc_dest_lane.centerline.lineString.project(Point(npc_init[0], npc_init[1]))
    npc_init_length = ego_line_string.project(Point(npc_init[0], npc_init[1]))
    while (npc_init_length - ego_init_length) < 5 or (npc_dest_project_length - npc_init_project_length) < random.randint(5, 20):
        npc_init = straight_road_init_point(network, position, road_type, same_lane=True, relative='behind', reverse=None)
        npc_point = Vector(npc_init[0], npc_init[1])
        npc_init_lane = network.laneAt(npc_point)
        npc_init_project_length = npc_dest_lane.centerline.lineString.project(Point(npc_init[0], npc_init[1]))
        npc_init_length = ego_line_string.project(Point(npc_init[0], npc_init[1]))


    return npc_init_project_length, npc_init_lane

def follow_vehicle_init_position(network, position, npc_dest_project_length, line_string, road_type):
    npc_init = straight_road_init_point(network, position, road_type, same_lane=True, relative='behind')
    npc_point = Vector(npc_init[0], npc_init[1])
    npc_init_lane = network.laneAt(npc_point)
    ego_init_project_length = line_string.project(Point(position[0], position[1]))
    npc_init_project_length = line_string.project(Point(npc_init[0], npc_init[1]))
    while (npc_dest_project_length - npc_init_project_length) < random.randint(20, 50) or (ego_init_project_length - npc_init_project_length) < 10:
        npc_init = straight_road_init_point(network, position, road_type, same_lane=True, relative='behind')
        npc_point = Vector(npc_init[0], npc_init[1])
        npc_init_lane = network.laneAt(npc_point)
        npc_init_project_length = line_string.project(Point(npc_init[0], npc_init[1]))
    return npc_init_project_length, npc_init_lane
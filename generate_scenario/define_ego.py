import json
import os
import random

from scenic.core.vectors import Vector
from shapely.geometry import Point

from traffic_cases.get_critical_district import get_hazard_section, get_ego_next_lane, get_ego_district
from generate_scenario.behavior_trajectory_solver.connect_lanes import combine_center_line
from generate_scenario.behavior_trajectory_solver.point_in_road import get_point_in_segment


def define_ego_state(network, road_type):
    rejection = True
    while rejection:
        # define destination in accident-prone area
        if road_type == "straight road":
            hazard_section = "end"
        else:
            hazard_section = random.choice(["turning", "junction", "end"])
        dest_disrtict = get_hazard_section(road_type, hazard_section)
        ego_destination_x = random.uniform(dest_disrtict[0][0], dest_disrtict[0][1])
        ego_destination_y = random.uniform(dest_disrtict[1][0], dest_disrtict[1][1])
        ego_destination = [ego_destination_x, ego_destination_y]
        dest_lane = network.laneAt(Vector(ego_destination_x, ego_destination_y))
        # define intial position and speed randomly
        intial_range = get_ego_district(road_type)
        ego_spawn = get_ego_init_point(network, intial_range[0], road_type)
        init_lane = network.laneAt(Vector(ego_spawn[0], ego_spawn[1]))
        lane_string = combine_center_line(network, init_lane, dest_lane, road_type)
        dest_project_length = lane_string.project(Point(ego_destination_x, ego_destination_y))
        init_project_length = lane_string.project(Point(ego_spawn[0], ego_spawn[1]))
        
        if dest_lane.road != init_lane.road or (dest_lane == init_lane and (dest_project_length - init_project_length) >= random.randint(50, 70)):
            rejection = False

    ego_speed = random.randint(6, 12)

    return ego_destination, ego_spawn, ego_speed


def get_ego_init_point(network, position, road_type):
    road = network.findPointIn(Vector(position[0], position[1]), network.roads, False)
    lanes = road.lanes
    search_lanes = []
    next_lane = get_ego_next_lane(road_type)
    next_lane_intersection = network.intersectionAt(Vector(next_lane[0], next_lane[1]))
    incoming_lanes = next_lane_intersection.incomingLanes
    for lane in lanes:
        if lane in incoming_lanes:
            search_lanes.append(lane)

    lane_index = random.randint(0, len(search_lanes)-1)
    lane = search_lanes[lane_index]
    segments = lane.centerline.segments
    entrance_point = segments[1]
    entrance_length = lane.centerline.lineString.project(Point(entrance_point[0], entrance_point[1]))
    segment_index = random.randint(1, len(lane.centerline.segments)-1)
    segment = segments[segment_index]
    point = get_point_in_segment(segment)
    point_length = lane.centerline.lineString.project(Point(point[0], point[1]))
    while (point_length-entrance_length) < 10:
        segment_index = random.randint(1, len(lane.centerline.segments) - 1)
        segment = segments[segment_index]
        point = get_point_in_segment(segment)
        point_length = lane.centerline.lineString.project(Point(point[0], point[1]))

    return point
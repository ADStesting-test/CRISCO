import random

from scenic.core.vectors import Vector
from shapely.geometry import Point

from generate_scenario.behavior_trajectory_solver.behavior_init import cut_in_init_position, follow_lane_init_position, \
    follow_vehicle_init_position
from generate_scenario.behavior_trajectory_solver.connect_lanes import combine_center_line
from generate_scenario.behavior_trajectory_solver.point_in_road import get_point_in_segment
from generate_scenario.define_ego import define_ego_state
from traffic_cases.get_critical_district import get_hazard_section


def straight_behavior2intersection(network, road_type, hazard_section, behavior, ego_init, ego_dest, npc_dest):

    accident_prone = get_hazard_section(road_type, hazard_section)

    ego_point = Vector(ego_init[0], ego_init[1])
    ego_init_lane = network.laneAt(ego_point)
    # ego_road = network.findPointIn(ego_point, network.roads, False)
    ego_dest_lane = network.laneAt(Vector(ego_dest[0], ego_dest[1]))
    line_string = combine_center_line(network, ego_init_lane, ego_dest_lane, road_type)
    ego_init_project_length = line_string.project(Point(ego_init[0], ego_init[1]))
    ego_dest_project_length = line_string.project(Point(ego_dest[0], ego_dest[1]))

    npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
    if behavior == "cut in":
        if hazard_section == "middle" or "junction":
            npc_init_project_length, npc_init_lane, center_line, npc_dest_project_length = cut_in_init_position(network,
                                                                                                                ego_init,
                                                                                                                ego_init_project_length,
                                                                                                                npc_dest,
                                                                                                                npc_dest_lane,
                                                                                                                road_type)
        else:
            # while npc_dest_lane != ego_dest_lane:
            #     npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
            #                 random.uniform(accident_prone[1][0], accident_prone[1][1])]
            #     npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
            road = network.findPointIn(Vector(npc_dest[0], npc_dest[1]), network.roads, False)
            lanes = road.lanes
            lane = random.choice(lanes)
            while lane == npc_dest_lane:
                lane = random.choice(lanes)
            segments = lane.centerline.segments
            entrance_point = segments[1]
            entrance_length = lane.centerline.lineString.project(Point(entrance_point[0], entrance_point[1]))
            segment_index = random.randint(1, int(len(lane.centerline.segments) / 3))
            segment = segments[segment_index]
            point = get_point_in_segment(segment)
            point_length = lane.centerline.lineString.project(Point(point[0], point[1]))
            npc_init_lane = lane
            npc_init_project_length = entrance_length
            npc_dest_project_length = point_length
        return npc_init_project_length, npc_init_lane, npc_dest_project_length
    if behavior == "cut out":
        if hazard_section == "middle" or "junction":
            npc_init_project_length, npc_init_lane, center_line, npc_dest_project_length = cut_out_init_position(
                network, ego_init, npc_dest, npc_dest_lane, ego_init_project_length, road_type)
        else:
            # while npc_dest_lane == ego_dest_lane:
            #     npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
            #                 random.uniform(accident_prone[1][0], accident_prone[1][1])]
            #     npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
            road = network.findPointIn(Vector(npc_dest[0], npc_dest[1]), network.roads, False)
            lanes = road.lanes
            lane = random.choice(lanes)
            while lane == npc_dest_lane:
                lane = random.choice(lanes)
            segments = lane.centerline.segments
            entrance_point = segments[1]
            entrance_length = lane.centerline.lineString.project(Point(entrance_point[0], entrance_point[1]))
            segment_index = random.randint(1, int(len(lane.centerline.segments) / 3))
            segment = segments[segment_index]
            point = get_point_in_segment(segment)
            point_length = lane.centerline.lineString.project(Point(point[0], point[1]))
            npc_init_lane = lane
            npc_init_project_length = entrance_length
            npc_dest_project_length = point_length
        return npc_init_project_length, npc_init_lane, npc_dest_project_length
    if behavior == "follow lane":
        if hazard_section == "middle" or "junction":
            npc_dest_project_length = npc_dest_lane.centerline.lineString.project(Point(npc_dest[0], npc_dest[1]))
            npc_init_project_length, npc_init_lane = follow_lane_init_position(network, road_type, npc_dest,
                                                                               npc_dest_lane, npc_dest_project_length,
                                                                               line_string, ego_init_project_length)
        else:
            # while npc_dest_lane == ego_dest_lane:
            #     npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
            #                 random.uniform(accident_prone[1][0], accident_prone[1][1])]
            #     npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
            road = network.findPointIn(Vector(npc_dest[0], npc_dest[1]), network.roads, False)
            lanes = road.lanes
            lane = random.choice(lanes)
            while lane == npc_dest_lane:
                lane = random.choice(lanes)
            segments = lane.centerline.segments
            entrance_point = segments[1]
            entrance_length = lane.centerline.lineString.project(Point(entrance_point[0], entrance_point[1]))
            segment_index = random.randint(1, int(len(lane.centerline.segments) / 3))
            segment = segments[segment_index]
            point = get_point_in_segment(segment)
            point_length = lane.centerline.lineString.project(Point(point[0], point[1]))
            npc_init_lane = lane
            npc_init_project_length = entrance_length
            npc_dest_project_length = point_length
        return npc_init_project_length, npc_init_lane
    if behavior == "follow vehicle":
        if hazard_section == "middle" or "junction":
            npc_dest_project_length = npc_dest_lane.centerline.lineString.project(Point(npc_dest[0], npc_dest[1]))
            npc_init_project_length, npc_init_lane = follow_vehicle_init_position(network, ego_init, npc_dest_project_length, line_string, road_type)
        else:
            # while npc_dest_lane == ego_dest_lane:
            #     npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
            #                 random.uniform(accident_prone[1][0], accident_prone[1][1])]
            #     npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
            road = network.findPointIn(Vector(npc_dest[0], npc_dest[1]), network.roads, False)
            lanes = road.lanes
            lane = random.choice(lanes)
            while lane == npc_dest_lane:
                lane = random.choice(lanes)
            segments = lane.centerline.segments
            entrance_point = segments[1]
            entrance_length = lane.centerline.lineString.project(Point(entrance_point[0], entrance_point[1]))
            segment_index = random.randint(1, int(len(lane.centerline.segments) / 3))
            segment = segments[segment_index]
            point = get_point_in_segment(segment)
            point_length = lane.centerline.lineString.project(Point(point[0], point[1]))
            npc_init_lane = lane
            npc_init_project_length = entrance_length
            npc_dest_project_length = point_length
        return npc_init_project_length, npc_init_lane

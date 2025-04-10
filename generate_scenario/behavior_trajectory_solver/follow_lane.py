from z3 import *

from generate_scenario.behavior_trajectory_solver.behavior_init import follow_lane_init_position
from generate_scenario.behavior_trajectory_solver.connect_lanes import combine_center_line
from generate_scenario.behavior_trajectory_solver.point_in_road import *
from generate_scenario.behavior_trajectory_solver.straight_behavior_intersection import straight_behavior2intersection
from traffic_cases.get_critical_district import get_hazard_section


def follow_lane(network, road_type, ego_init, ego_dest, ego_speed, num, hazard_section):
    print("follow lane")

    if hazard_section != "turning" and hazard_section != "junction":
        accident_prone = get_hazard_section(road_type, hazard_section)
    else:
        accident_prone = get_hazard_section(road_type, "middle")
    # get lanes of initial position and destination of ego
    ego_point = Vector(ego_init[0], ego_init[1])
    ego_init_lane = network.laneAt(ego_point)
    ego_dest_lane = network.laneAt(Vector(ego_dest[0], ego_dest[1]))
    ego_line_string = combine_center_line(network, ego_init_lane, ego_dest_lane, road_type)
    ego_init_project_length = ego_line_string.project(Point(ego_init[0], ego_init[1]))
    ego_dest_project_length = ego_line_string.project(Point(ego_dest[0], ego_dest[1]))

    rejection = True
    waypoint_sequence = []
    while rejection:
        # select destination of npc in accident-prone area
        npc_dest = [random.uniform(accident_prone[0][0], accident_prone[0][1]),
                    random.uniform(accident_prone[1][0], accident_prone[1][1])]
        npc_dest_lane = network.laneAt(Vector(npc_dest[0], npc_dest[1]))
        npc_dest_project_length = npc_dest_lane.centerline.lineString.project(Point(npc_dest[0], npc_dest[1]))
        if road_type != "straight road":
            npc_init_project_length, npc_init_lane = straight_behavior2intersection(network, road_type, hazard_section, "follow lane", ego_init, ego_dest, npc_dest)
        else:
        # select initial position of npc outside accident-prone area
            npc_init_project_length, npc_init_lane = follow_lane_init_position(network, road_type, npc_dest, npc_dest_lane, npc_dest_project_length, ego_line_string, ego_init_project_length)

        # z3 solver
        T = Real("T")
        C = Real("C")

        ego_initial_position = Real("ego_initial_position")
        ego_target_position = Real("ego_target_position")
        # solve constraints of waypoints
        npc_initial_speed = Real("npc_initial_speed")
        npc_target_speed = Real("npc_target_speed")
        npc_initial_position = Real("npc_initial_position")
        npc_target_position = Real("npc_target_position")
        npc_accelerate = Real("npc_accelerate")
        npc_average_speed = Real("npc_average_speed")

        time_c = []
        position_c = []
        speed_c = []
        time = random.randint(0, 2)
        # driving time and trigger time
        time_c += [T * ego_speed == ego_target_position - ego_initial_position]+ \
                [T - C >= time] + \
                [And(T >= 1, C >= 1)]
        # speeds
        speed_c += [And(0 <= npc_initial_speed, npc_initial_speed <= 25)] + \
                [And(0 <= npc_target_speed, npc_target_speed <= 25)] + \
                [npc_target_speed == npc_initial_speed] + \
                [npc_average_speed == (npc_target_speed + npc_initial_speed) / 2.0] + \
                [npc_accelerate == (npc_target_speed - npc_initial_speed) / C] + \
                [And(-10 <= npc_accelerate, npc_accelerate <= 5.5)]
        # positions
        position_c += [ego_initial_position == ego_init_project_length] + \
                    [ego_target_position == ego_dest_project_length] + \
                    [npc_target_position == npc_dest_project_length] + \
                    [npc_initial_position == npc_init_project_length]+ \
                    [C * npc_average_speed == npc_target_position - npc_initial_position]

        s = Solver()
        s.add(speed_c + position_c + time_c)
        set_option(rational_to_decimal=True)
        set_option(precision=1)

        res = []
        cnt = 0
        m= None
        while cnt < 100:
            cnt += 1
            if s.check() == sat:
                m = s.model()
                res.append([toNum(m.evaluate(npc_initial_speed)), toNum(m.evaluate(npc_target_speed)),
                            toNum(m.evaluate(npc_initial_position))])
                fml = And(npc_initial_speed == res[-1][0], npc_target_speed == res[-1][1], npc_initial_position == res[-1][2])
                s.add(Not(fml))

        if len(res) < num:
            continue
        rejection = False

        ans_list = random.sample(res, num)
        for ans in ans_list:
            # center_line = combine_center_line(npc_init_lane, npc_dest_lane)
            waypoints = []
            t = toNum(m.evaluate(T))
            c = toNum(m.evaluate(C))
            acc = (ans[1] - ans[0]) / c
            for i in range(int(c * 10)):
                speed = ans[0] + acc * (i + 1) * 0.1
                pos = ans[2] + (ans[0] + speed) / 2.0 * (i + 1) * 0.1
                p = npc_dest_lane.centerline.lineString.interpolate(pos)
                waypoints.append([p.x, p.y, speed])
            waypoint_sequence.append([waypoints, t-c])

    return waypoint_sequence



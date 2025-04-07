import os
import sys

sys.path.append("..")
from generate_scenario.define_ego import define_ego_state
from generate_scenario.get_map import get_network
from generate_scenario.connect_simulator import *
from generate_scenario.environment_generation.define_environment_svl import *
from generate_scenario.generate_behavior_trajectory import *
from generate_scenario.determine_participants import *
import copy

network = get_network()
participants, participant_trajectories = [], []
ego_trajectory = []
ettc_threshold = 2.0
root_path = os.chdir("..")
root_path = os.getcwd()
path = os.path.join(root_path, "configuration/requirement_items")
f = open(path, encoding='utf-8')
requirement_set = json.load(f)
patterns = requirement_set["patterns"]
patterns_straight = requirement_set["patterns_straight"]
f.close()


def generate_test_cases(road_type, specified_behaviors, num, input_behaviors):
    global participants
    global participant_trajectories
    global road
    global isCollision
    global ego_trajectory
    isCollision = False
    road = road_type

    sim = connect_svl()
    # define ego and compute running time
    ego_destination, ego_spawn, ego_speed = define_ego_state(network, road_type)

    # generate scenarios
    ettc = 500
    scenarios = []
    trajectories = []
    actual_speed = round(ego_speed/2, 2)
    # generate initial abstract scenarios
    for behavior in specified_behaviors:
        # generate trajectories of selected behaviors
        trajectory = generate_behavior_trajectory(network, road_type, behavior, ego_spawn, ego_destination,
                                                  actual_speed, num)
        trajectories.append(trajectory)

    # if len(behaviors) == 1:
    #     behaviors.append(behaviors[0])
    #     trajectory = generate_behavior_trajectory(network, road_type, behaviors[0], ego_spawn, ego_destination,
    #                                               actual_speed, num, hazard_section)
    #     trajectories.append(trajectory)

    # generate concrete scenarios
    for i in range(num):
        scenario = []
        for j in range(len(trajectories)):
            scenario.append((specified_behaviors[j], trajectories[j][i]))
        scenarios.append(scenario)

    # evaluate and alter scenarios
    new_scenarios = []
    for scenario in scenarios:
        scenario_ettc = True
        for behavior, traj in scenario:
            if len(traj) == 1:
                traj = traj[0]
            ettc = min(ettc, cal_TTC(network, ego_spawn, ego_destination, actual_speed, traj, behavior, road_type))
            if ettc > ettc_threshold:
                scenario_ettc = False
                new_scenario = expand_scenario(scenario, behavior, ego_spawn, ego_destination, actual_speed, road_type, input_behaviors)
                new_scenarios.append(new_scenario)
        if scenario_ettc:
            new_scenarios.append(scenario)

    # execute scenario
    for scenario in new_scenarios:
        # print(scenario)
        print("Current Scene = {}".format(sim.current_scene))

        # Loads the named map in the connected simulator, and define traffic signal state on selected road
        # if sim.current_scene == "SanFrancisco_correct":
        #    sim.reset()
        # else:
        #    sim.load("SanFrancisco_correct")
        if sim.current_scene == lgsvl.wise.DefaultAssets.map_sanfrancisco_correct:
            sim.reset()
        else:
            sim.load(lgsvl.wise.DefaultAssets.map_sanfrancisco_correct)
        sim.set_time_of_day(0)

        # define the static environment
        # define_environment(sim, weather)
        print("environment has been constructed")
        define_road_traffic_signal_svl(sim, road_type)

        # spawn ego
        ego_state, _ = spawn(sim, ego_spawn[0], ego_spawn[1], actual_speed)
        # bridge ego into Apollo
        ego = sim.add_agent('2e966a70-4a19-44b5-a5e7-64e00a7bc5de', lgsvl.AgentType.EGO, ego_state)
        # ego_destination = get_position(sim, ego_destination[0], ego_destination[1])
        bridgeApollo(sim, ego, ego_destination)
        print("ego vehicle has been spawn")

        # monitor safety violation of ego vehicle
        ego.on_collision(on_collision)

        for behavior, trajectory in scenario:
            if 'Pedestrian' in behavior:
                generate_pedestrian_participants(sim, trajectory)
            else:
                generate_vehicle_participants(sim, trajectory, behavior)
            participants.append(behavior)
            participant_trajectories.append(trajectory)

        isCollision = False
        ego_trajectory = []
        for i in range(500):
            # signal = sim.get_controllable(lgsvl.Vector([100.7, 15, -86.4]), "signal")
            # print(signal.control_policy)
            tr = ego.state.transform
            ego_trajectory.append([tr.position.x, tr.position.z, ego.state.speed])
            sim.run(0.1)

            if isCollision:
               break

        # scenario_folder = os.path.join(root_path, "safety_violation_scenarios")
        # scenario_list = os.listdir(scenario_folder)
        if isCollision:
            record_scenario(sim, road_type)


def expand_scenario(scenario, behavior, ego_spawn, ego_destination, ego_speed, road_type, input_behaviors):
    ettc = 500
    if road_type == "straight road":
        behavior_patterns = patterns_straight
    else:
        behavior_patterns = patterns
    behavior_set = [behavior]
    for each in behavior_patterns:
        if behavior in each:
            for i in each:
                if i != behavior:
                    behavior_set.append(i)
    behavior = random.choice(input_behaviors)
    trajectory = generate_behavior_trajectory(network, road_type, behavior, ego_spawn, ego_destination, ego_speed, 1)
    if len(trajectory) == 1:
        trajectory = trajectory[0]
    ettc = min(ettc, cal_TTC(network, ego_spawn, ego_destination, ego_speed, trajectory, behavior, road_type))
    scenario.append((behavior, trajectory))
    if ettc > ettc_threshold:
        behavior = random.choice(input_behaviors)
        trajectory = generate_behavior_trajectory(network, road_type, behavior, ego_spawn, ego_destination, ego_speed, 1)
        if len(trajectory) == 1:
            trajectory = trajectory[0]
    scenario.append((behavior, trajectory))
    return scenario


def on_collision(agent1, agent2, contact):
    global isCollision
    isCollision = True


def record_scenario(sim, road_type):
    global ego_trajectory
    # current_script_path = os.path.abspath(sys.argv[0])
    # root_path = get_project_root(current_script_path)
    scenario_example = os.path.join(root_path, "reproduce_safety_violation_scenarios/scenario_example")
    f = open(scenario_example, encoding='utf-8')
    scenario_json = json.load(f)
    f.close()
    test_description_folder = os.path.join(root_path, "scenario_description_folder/" + road_type)
    file_nums = visitDir(test_description_folder)

    scenario_folder = os.path.join(root_path, "safety_violation_scenarios/" + road_type + "/" + str(file_nums))
    folder = os.path.exists(scenario_folder)
    if not folder:
        os.makedirs(scenario_folder)
    file_nums = visitDir(scenario_folder)
    scenario_record = os.path.join(scenario_folder, "safety_violation_" + str(file_nums))
    # scenario_record = os.path.join(root_path,
    #                                "safety_violation_scenarios/" + road_type + "/safety_violation_" + str(file_nums))

    scenario_json["road type"] = road_type
    # scenario_json["weather"] = [{"rain": sim.weather.rain}, {"fog": sim.weather.fog}, {"wetness": sim.weather.wetness}, {"cloudiness": sim.weather.cloudiness}, {"damage": sim.weather.damage}, {"time_of_day": sim.time_of_day}]
    scenario_json["ego"] = ego_trajectory

    for i in range(len(participants)):
        if participants[i] in scenario_json:
            this_key = participants[i] + str(i)
            scenario_json[this_key] = participant_trajectories[i]
        elif participants[i] not in scenario_json:
            scenario_json[participants[i]] = participant_trajectories[i]
    del scenario_json["agent"]
    file = open(scenario_record, 'w')
    json.dump(scenario_json, file, ensure_ascii=False)
    file.close()



# if __name__ == '__main__':
#     sim = connect_svl()
#     if sim.current_scene == lgsvl.wise.DefaultAssets.map_sanfrancisco_correct:
#         sim.reset()
#     else:
#         sim.load(lgsvl.wise.DefaultAssets.map_sanfrancisco_correct)
#     controllables = sim.get_controllables()
#     signal = controllables[0]
#     print(signal.transform.position)
    # ego_spawn = [135.5, 88.5]
    # ego_speed = 8
    # # ego_destination = [40.9, -37.3]
    # ego_state, _ = spawn(sim, ego_spawn[0], ego_spawn[1], ego_speed)
    # # bridge ego into Apollo
    # ego = sim.add_agent('2e966a70-4a19-44b5-a5e7-64e00a7bc5de', lgsvl.AgentType.EGO, ego_state)
    # # ego_destination = get_position(sim, ego_destination[0], ego_destination[1])
    # # bridgeApollo(sim, ego, ego_destination)
    #
    # for i in range(500):
    #     sim.run(0.1)

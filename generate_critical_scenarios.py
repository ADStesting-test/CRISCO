import json
import os
import argparse
import random
import sys
import time

from generate_scenario.checker import get_project_root, array2str, get_all_subsets, is_subset
from generate_scenario.generate_test_scenarios import generate_test_cases
import warnings

from generate_scenario.get_waypoints import visitDir

warnings.filterwarnings("ignore")


# initialize arg constructor
parser = argparse.ArgumentParser()
# add the arg in the constructor
parser.add_argument('--r', type=str, default='no-input')
# get args from command line
args = parser.parse_args()
# retrieve test requirement file
road_type = str(args.r)

current_script_path = os.path.abspath(sys.argv[0])
root_path = get_project_root(current_script_path)
path = os.path.join(root_path, "configuration/requirement_items")
f = open(path, encoding='utf-8')
requirement_set = json.load(f)
f.close()

road_set = requirement_set["road"]
behaviors_set = requirement_set["behaviors"]
behavior_straight = requirement_set["behaviors_straight"]
# hazard_section_set = requirement_set["hazard section"]
# hazard_section_straight = requirement_set["hazard section straight"]
patterns = requirement_set["patterns"]
patterns_straight = requirement_set["patterns_straight"]

if road_type == 'no-input':
    user_input = input("Please input the road type that you want to test the ADS on. The road can be one of the three types: "+ array2str(road_set) + "\n")
    while user_input not in road_set:
        user_input = input("Please select a road type from the three ones: "+array2str(road_set) + "\n")
    road_type = user_input

if road_type == "straight road":
    behaviors_input = input("Please select one or more participant behaviors (separated by commas), or input 'R' to use a recommended behavior pattern to test the ADS: " + array2str(behavior_straight) + "\n")
    if behaviors_input == 'R':
        selected_behaviors = random.choice(patterns_straight)
        behaviors = behavior_straight
    else:
        input_again = True
        while input_again:
            behaviors_input = behaviors_input.split(",")
            for i in range(len(behaviors_input)):
                behaviors_input[i] = behaviors_input[i].strip()
                if behaviors_input[i] not in behavior_straight:
                    behaviors_input = input("Please select participant behaviors from the following ones: " + array2str(behavior_straight) + "\n")
                    break
                if i == len(behaviors_input) - 1:
                    input_again = False
                    behaviors = behaviors_input
                    result = get_all_subsets(behaviors_input)
                    selected_behaviors = []
                    for each in result:
                        if is_subset(each, patterns_straight):
                            selected_behaviors.append(each)
                    if len(selected_behaviors) == 0:
                        selected_behaviors = behaviors_input
            break

else:
    behaviors_input = input(
        "Please select one or more participant behaviors (separated by commas), or input 'R' to use to randomly select behaviors to test the ADS: " + array2str(behaviors_set) + "\n")
    if behaviors_input == 'R':
        selected_behaviors = random.choice(patterns)
        behaviors = behaviors_set
    else:
        input_again = True
        while input_again:
            behaviors_input = behaviors_input.split(",")
            for i in range(len(behaviors_input)):
                behaviors_input[i] = behaviors_input[i].strip()
                if behaviors_input[i] not in behaviors_set:
                    behaviors_input = input("Please select participant behaviors from the following ones: " + array2str(behaviors_set) + "\n")
                    break
                if i == len(behaviors_input) - 1:
                    input_again = False
                    behaviors = behaviors_input
                    result = get_all_subsets(behaviors_input)
                    selected_behaviors = []
                    for each in result:
                        if is_subset(each, patterns_straight):
                            selected_behaviors.append(each)
                    if len(selected_behaviors) == 0:
                        selected_behaviors = behaviors_input
            break

number_input = input("Please input the number of test scenarios that you want to generate: " + "\n")
number = int(number_input)

max_participant_input = input("Please input the maximal number of participants in the test scenario: " + "\n")
max_participant_num = int(max_participant_input)

scenario_example = os.path.join(root_path, "reproduce_safety_violation_scenarios/scenario_example")
f = open(scenario_example, encoding='utf-8')
scenario_json = json.load(f)
f.close()

scenario_json["road type"] = road_type
scenario_json["behaviors"] = selected_behaviors
scenario_json["number of participants"] = max_participant_num
scenario_json["number of scenarios"] = number
del scenario_json["agent"]

test_description_folder = os.path.join(root_path, "scenario_description_folder/"+road_type)
exist = os.path.exists(test_description_folder)
if not exist:
    os.makedirs(test_description_folder)
file_nums = visitDir(test_description_folder)
test_description_path = os.path.join(test_description_folder, str(file_nums+1))

file = open(test_description_path, 'w')
json.dump(scenario_json, file, ensure_ascii=False)
file.close()

test_scenario_description = ""
generate_test_cases(road_type, selected_behaviors, number, behaviors)
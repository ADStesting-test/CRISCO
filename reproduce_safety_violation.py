import argparse
import json
import os
import time
import sys

from generate_scenario.checker import get_project_root
from reproduce_safety_violation_scenarios.reproduce_scenario import reproduce_scenarios


# initialize arg constructor
parser = argparse.ArgumentParser()
# add the arg in the constructor
parser.add_argument('--r', type=str)
parser.add_argument('--s', type=str, default='1/safety_violation_0')
parser.add_argument('--w', type=str, default='replay')
# get args from command line
args = parser.parse_args()
road = str(args.r)
scenario = str(args.s)
way = str(args.w)
current_script_path = os.path.abspath(sys.argv[0])
root_path = get_project_root(current_script_path)
path = os.path.join(root_path, "safety_violation_scenarios/" + road + "/" + scenario)
f = open(path, encoding='utf-8')
file = json.load(f)
f.close()

reproduce_scenarios(file, way)
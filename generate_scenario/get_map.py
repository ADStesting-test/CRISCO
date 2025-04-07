import json
import sys
from scenic.core.vectors import Vector
from scenic.domains.driving.roads import Network
import os

from generate_scenario.checker import get_project_root

# get map file
# root_path = os.path.abspath(os.path.dirname(__file__)).split('racer')[0]
# selected_map = os.path.join(root_path, "racer/configuration/map")
# current_script_path = os.path.abspath(sys.argv[0])
# root_path = get_project_root(current_script_path)
root_path = os.chdir("..")
root_path = os.getcwd()
path = os.path.join(root_path, "configuration/map")
f = open(path, encoding='utf-8')
map_json = json.load(f)
f.close()
map_name = map_json["map"]

def get_network():
    try:
        path = os.path.join(root_path, "configuration/"+map_name)
        network = Network.fromFile(path)
        return network
    except FileNotFoundError:
        print("The selected map was not in map folder of lgsvl dictionary")
        sys.exit(1)

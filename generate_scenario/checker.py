import json
import os
import sys
from collections import OrderedDict


def get_project_root(path):
    # 获取当前脚本所在的目录
    script_directory = os.path.dirname(path)

    # 逐级向上查找，直到找到包含主脚本的目录（即项目根目录）
    while "racer" not in script_directory.split("/")[-1]:
        script_directory = os.path.dirname(script_directory)

    return script_directory

# root_path = os.path.abspath(os.path.dirname(__file__)).split('racer')[0]
# path = os.path.join(root_path, "racer/configuration/requirement_items")


def requirement_checker(road_type, behaviors, hazard_section):
    current_script_path = os.path.abspath(sys.argv[0])
    root_path = get_project_root(current_script_path)
    path = os.path.join(root_path, "configuration/requirement_items")
    f = open(path, encoding='utf-8')
    requirement_set = json.load(f)
    f.close()
    road_set = requirement_set["road"]
    # weather_set = requirement_set["weather"]
    behaviors_set = requirement_set["behaviors"]
    hazard_section_set = requirement_set["hazard section"]
    for behavior in behaviors:
        if behavior not in behaviors_set:
            print(behavior + " is not a valid participant behavior")
            sys.exit()

    if hazard_section not in hazard_section_set:
        print(hazard_section + " is not a valid hazard section")
        sys.exit()

    if road_type == "straight road":
        for behavior in behaviors:
            if behavior == "vehicle cross" or behavior == "turn around":
                print(behavior + " is infeasible on " + road_type)
                sys.exit()
            if hazard_section == "turning" or hazard_section == "junction":
                print(hazard_section + " is not valid on" + road_type)

    # for item in weather:
    #     if item not in weather_set:
    #         print(item + " is not a valid weather")
    #         sys.exit()
    #     if item == "sunlight":
    #         for each in weather:
    #             if each == "night" or each == "foggy" or each == "cloudy":
    #                 print(item + " and " + each + " is conflicting")
    #                 sys.exit()

    # print("The test requirements are valid.")
    print("RACER will generate critical scenarios and execute in the simulator to test the AUT")


def is_combination_present(array1, array2):
    # 将数组转换为集合
    set1 = set(array1)
    set2 = set(array2)
    # set2 = set(tuple(row) for row in array2)
    # set2 = list(ordered_set_of_tuples.keys())

    # 判断array1的元素组合是否是array2的子集
    if set1.issubset(set2):
        # print("数组1中的元素组合在数组2中存在")
        return True
    else:
        # print("数组1中的元素组合在数组2中不存在")
        return False


def is_subset(array1, array2):
    set1 = set(array1)
    label = False
    for each in array2:
        set2 = set(each)
        if set1 == set2:
            label = True
            return True
    return label

def get_all_subsets(arr):
    all_subsets = [[]]

    for element in arr:
        current_subsets = [subset + [element] for subset in all_subsets]
        all_subsets.extend(current_subsets)

    return all_subsets


def array2str(array):
    result_str = ", ".join(array)

    return result_str


if __name__ == '__main__':
    test = ["vehicle cross", "turn around", "cut in"]
    patterns = [["cut in", "cut out"], ["turn around", "vehicle cross"], ["turn around", "cut in"]]
    # input_array = [1, 2, 3]
    result = get_all_subsets(test)
    behaviors = []
    for each in result:
        if is_subset(each, patterns):
            behaviors.append(each)
    print(behaviors)
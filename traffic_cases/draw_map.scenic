# # param map = localPath("D:\\Workspace\\RoadRunner\\Scenes\\Beijing_Road_v4\\Beijing_Road_v4.xodr")

# param map = localPath('../../../tests/formats/opendrive/maps/CARLA/Town04.xodr')
# param carla_map = 'Town04'
# param render = 0
# param record = 'C:/Users/dell/Desktop/Scenario Logs'
# model scenic.simulators.carla.model

# param map = localPath('D:/Workspace/Scenic/examples/lgsvl/maps/Straight2LaneSame.xodr')
param map = localPath('/home/thx/Documents/Workspace/RACER/configuration/SanFrancisco.xodr')
param lgsvl_map = 'SanFrancisco'
model scenic.simulators.lgsvl.model

param time_step = 1.0/10

ego = Car at -323.5 @ -105.6,
        with blueprint "vehicle.lincoln.mkz2017"
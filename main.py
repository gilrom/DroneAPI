from DroneClient import DroneClient
import time
import airsim.utils
from Controller import DroneController

if __name__ == "__main__":
    client = DroneClient()
    client.connect()

    print(client.isConnected())

    time.sleep(4)
    #set starting position
    client.setAtPosition(-300, -200, -100)

    controller = DroneController(client)


    time.sleep(3)
    target_pos = (-500, -900, -100)
    controller.navigateTangentBug(target_pos)

    # client.flyToPosition(-346, -420, -100, 10)

    # while True:
    #     print(type(client.getLidarData().points))
    #     print(list(client.getLidarData().points))
    #     # print(client.getPose())
    #     time.sleep(1)

from DroneClient import DroneClient
from DroneTypes import Pose
import numpy as np
from scipy.spatial.transform import Rotation as R
import time


def transform(point, pose:Pose):
    r = R.from_euler('zyx', [-pose.orientation.z_rad, -pose.orientation.y_rad, -pose.orientation.x_rad])
    r_mat = r.as_matrix()
    p = np.array([[pose.pos.x_m],[pose.pos.y_m],[pose.pos.z_m]])
    T=np.append(r_mat,p,axis=1)
    T = np.append(T,np.array([[0,0,0,1]]),axis=0)
    print(T)
    return (T @ np.array(point+[1]).T).T

class DroneController:
    def __init__(self, client:DroneClient) -> None:
        self.client = client
        self.lidar_rad = 35
        self.speed = 6.0
        self.threshold = 1
        # self.target_position = None
        # self.path_distance = None
        # self.path_complete = False
        # self.obstacle_detected = False
        # self.obstacle_start = None
        # self.obstacle_end = None
        # self.obstacle_distance = None

    def navigateTangentBug(self, target_pos):
        path_complete = False
        self.client.flyToPosition(*target_pos, self.speed)
        # We ignore z coordinate
        d2_target_pos = target_pos[:2]
        while not path_complete:
            curr_pos = self.client.getPose()
            curr_pos_coord = [curr_pos.pos.x_m, curr_pos.pos.y_m, curr_pos.pos.z_m]
            print(curr_pos_coord)
            d2_curr_pos = curr_pos_coord[:2]
            d_follow = np.linalg.norm(np.array(d2_target_pos) - np.array(d2_curr_pos)) - self.lidar_rad
            lidar_data = self.client.getLidarData()
            # print(lidar_data)
            if lidar_data.points != [0.0]:
                print("Obs Detected")
                trans_lidar = transform(lidar_data.points, curr_pos)
                print(f"trans:{trans_lidar}")
                d2_lidar_data = trans_lidar[:2]
                d_reach = np.linalg.norm(np.array(d2_lidar_data) - np.array(d2_target_pos))
                if d_reach >= d_follow:
                    print("follow obs")
                    #follow obstacle
                    self.client.flyToPosition(trans_lidar[0], trans_lidar[1], target_pos[2], 3.0)
                else:
                    print("flying to tar")
                    self.client.flyToPosition(*target_pos, self.speed)
            else:
                print("flying to tar")
                self.client.flyToPosition(*target_pos, self.speed)
            path_complete = np.linalg.norm(np.array(d2_target_pos) - np.array(d2_curr_pos)) <= self.threshold
            time.sleep(1)


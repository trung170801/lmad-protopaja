import cv2
import math
import numpy as np
from path_state import PathState
from distance import Heuristic
from astar import astar
import time
from skimage import draw

def process_image(image,cond):
    reclassifying_val = 90, 0
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray[cond(gray)] = reclassifying_val[0]
    gray[~cond(gray)] = reclassifying_val[1]     # Boolean Indexing
    return gray

# Private function which return a boolean-indexed version of the image.
# It selects only the pixel contains the value that fits the given brightness
# of the road.
def cond(image):
    return ((image > road_val_range[0]) &  # road_val_range[1] and road_val_range[2] is the range of 
            (image < road_val_range[1]))   # brightness of road surface (the part of the picture we need).
    # Return False if its not the road

def find_road_top_bot(image):
    height, width = int(image.shape[0]), int(image.shape[1])
    # try:
    # Remove the bottom part of the image from the search by slicing until (height-height/10)
    all_road = np.where(image[0:int(height-height/10),:] == reclassifying_val[0])
    top = all_road[0][0], all_road[1][0]
    
    bot_row = all_road[0][::-1][0] # A list
    list_bot_col = np.where(image[bot_row] == reclassifying_val[0])[0]
    mid_bot_col = list_bot_col[len(list_bot_col)//2]
    bot = bot_row,mid_bot_col
    return top,bot
    # except:
        # return None


def find_bot(image):
    height,width = int(image.shape[0]), int(image.shape[1])
    all_available = np.where(image[0:int(height-height/10),:] == reclassifying_val[0])
    da_x = all_available[0][::-1]
    list_y = np.where(image[da_x] == reclassifying_val[0])[1]
    da_y = list_y[len(list_y)//2]


img = cv2.imread(
    'Test Data\\00e9be89-00001005_train_color.png', 1)

road_val_range = (89,92)
height, width = int(img.shape[0]), int(img.shape[1]-1)


# This is the substitute for the road_val_range.
# When the pixels where the roads appear is determined,
# they are assigned to the first value of the tuple.
# Every other pixels are assigned to the latter value.
reclassifying_val = 90, 0





processed_img = process_image(img,cond)
current_pos = height-1,int(width/2)
goal,start = find_road_top_bot(processed_img)

# def reduce_size(current_pos, goal):
#     x = (current_pos[0] - goal[0])%4
#     y = (current_pos[1] - goal[0])%4
#     return goal[0]-x,goal[1]-y

# goal = reduce_size(current_pos,goal)
# print(goal)


if __name__ == "__main__":
    # A few basic examples/tests.
    # Use test_astar.py for more proper testing.
    # ------------------------------------------------
    # Example 1

    grid_S = PathState(start,processed_img)
    grid_G = PathState(goal, processed_img)
    heuristic = Heuristic(grid_G)
    print(grid_G)
    print(goal)
    print(current_pos)

    stime = time.process_time()
    nice = astar(grid_S,
                      lambda state: heuristic(state) < 60,
                      heuristic)
    etime = time.process_time()
    # plan = list((nice.source, nice.target))
    
    # print(f"Plan:")
    # s = grid_S
    # # print(s)
    # for i, p in enumerate(plan):
    #     s = s.apply(p)
    #     print(f"step: {i}, cost: {p.cost}")
    #     print(str(s))
    for x, y in nice:
        rr, cc = draw.line(
            int(x[0]), int(x[1]), int(y[0]), int(y[1]))
        img[rr, cc] = 255


    print(f"Time: {etime - stime}")
    cv2.imshow('ngon', img)
    cv2.waitKey(0)
    # print(f"Calculated cost: {sum(p.cost for p in plan)}")
    















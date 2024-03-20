import cv2
import numpy as np
import pathlib

from misc import *
from mapp import *
from graph import *
from lidar import *
from plotters import *


def bresenham_line(x0, y0, x1, y1,map_):
    points = []
    line = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy
    
    while True:
        points.append((x0, y0))
        if map_[x0, y0] == 0:
            map_[x0, y0] = 100
            line.append((x0,y0))
  
        if x0 == x1 and y0 == y1:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    
    return points,line


def rotate_left():   
    return left, forw, right, back

def rotate_right():   
    return  right, back, left, forw

def rotate_back():   
    return  back, left, forw, right


def obstacle_avoid_left(start_obs,end_obs):
    global forw, right, back, left
    forw = -1,0
    right = 0,1
    back = 1,0
    left = 0,-1

    ok = True

    forw_right = -1,1
    forw_left = -1,-1
    back_left = 1,-1
    back_right = 1,1

    x,y = start_obs
    x_end, y_end = end_obs 

    path = []

    if map_[x+right[0],y+right[1]] == 255:
        ok = True
    elif map_[x+forw[0],y+forw[1]] == 255:
        forw, right,back, left = rotate_left()
    elif map_[x+left[0],y+left[1]] == 255:
        forw, right,back, left = rotate_back()
    elif map_[x+back[0],y+back[1]] == 255:
        forw, right,back, left = rotate_right()

    elif map_[x+forw_right[0],y+forw_right[1]] == 255:
        x,y = x+forw[0],y+forw[1] #движение вперед
    elif map_[x+forw_left[0],y+forw_left[1]] == 255:
        forw, right,back, left = rotate_left()
        x,y = x+forw[0],y+forw[1] #движение вперед
    elif map_[x+back_left[0],y+back_left[1]] == 255:
        forw, right,back, left = rotate_back()
        x,y = x+forw[0],y+forw[1] #движение вперед
    elif map_[x+back_right[0],y+back_right[1]] == 255:
        forw, right,back, left = rotate_right()
        x,y = x+forw[0],y+forw[1] #движение вперед

    while (x != x_end or y != y_end):
        path.append((x,y))
        #print(x,y)
        if map_[x+right[0],y+right[1]] != 255: #если справа нет препятствия
            forw, right,back, left = rotate_right()
            x,y = x+forw[0],y+forw[1] #движение вперед
        elif map_[x+forw[0],y+forw[1]] != 255: #если впереди нет препятствия
            x,y = x+forw[0],y+forw[1] #движение вперед
        elif map_[x+left[0],y+left[1]] != 255: #если слева нет препятствия
            forw, right,back, left = rotate_left()
            x,y = x+forw[0],y+forw[1] #движение вперед
        else: #если сзади нет препятствия
            forw, right,back, left = rotate_back()
            x,y = x+forw[0],y+forw[1] #движение вперед

        if map_[x,y] == 100:
            if x-4 <= x_end <= x+4 and y-4 <= y_end <= y+4: 
                return path
            elif len(path)<6:
                continue
            else:
                return None
            
    return path
            

def obstacle_avoid_right(start_obs,end_obs):
    global forw, right, back, left
    forw = -1,0
    right = 0,1
    back = 1,0
    left = 0,-1

    forw_right = -1,1
    forw_left = -1,-1
    back_left = 1,-1
    back_right = 1,1

    x,y = start_obs
    x_end, y_end = end_obs 

    path = []

    if map_[x+left[0],y+left[1]] == 255:
        ok = True
    elif map_[x+forw[0],y+forw[1]] == 255:
        forw, right,back, left = rotate_right()
    elif  map_[x+right[0],y+right[1]]== 255:
        forw, right,back, left = rotate_back()
    elif map_[x+back[0],y+back[1]] == 255:
        forw, right,back, left = rotate_left()

    elif map_[x+forw_right[0],y+forw_right[1]] == 255:
        forw, right,back, left = rotate_right()
        x,y = x+forw[0],y+forw[1] #движение вперед
    elif map_[x+forw_left[0],y+forw_left[1]] == 255:
        x,y = x+forw[0],y+forw[1] #движение вперед
    elif map_[x+back_left[0],y+back_left[1]] == 255:
        forw, right,back, left = rotate_left()
        x,y = x+forw[0],y+forw[1] #движение вперед
    elif map_[x+back_right[0],y+back_right[1]] == 255:
        forw, right,back, left = rotate_back()
        x,y = x+forw[0],y+forw[1] #движение вперед

    if map_[x+right[0],y+right[1]] == 255:
        forw, right,back, left = rotate_back()
    elif map_[x+forw[0],y+forw[1]] == 255:
        forw, right,back, left = rotate_back()

    while (x != x_end or y != y_end):
        path.append((x,y))
        #print(x,y)
        if map_[x+left[0],y+left[1]] != 255: #если слева нет препятствия
            forw, right,back, left = rotate_left()
            x,y = x+forw[0],y+forw[1] #движение вперед
        elif map_[x+forw[0],y+forw[1]] != 255: #если впереди нет препятствия
            x,y = x+forw[0],y+forw[1] #движение вперед
        elif map_[x+right[0],y+right[1]] != 255: #если слева нет препятствия
            forw, right,back, left = rotate_right()
            x,y = x+forw[0],y+forw[1] #движение вперед
        else: #если сзади нет препятствия
            forw, right,back, left = rotate_back()
            x,y = x+forw[0],y+forw[1] #движение вперед


        if map_[x,y] == 100:
            if x-4 <= x_end <= x+4 and y-4 <= y_end <= y+4: 
                return path
            elif len(path)<6:
                continue
            else:
                return None
            
    return path

def plot(points, map_image):
    binary_map_rgb = cv2.cvtColor(map_image.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    
    for point in points:
        cv2.circle(binary_map_rgb,(point[1],point[0]),3,(0,255,0),-1)

    cv2.imshow('Visibility Graph', binary_map_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    # Считываем данные и строим карту
    data_path = pathlib.Path('..','..','data', 'examp2.txt')
    odom, lidar = read_txt(str(data_path))
    pts = stupid_slam(odom, lidar)
    map_ = render_ptc(pts, 100, ksize=9, msize=9)



    #start_point = (200, 200)
    #start_point = (240, 300)
    #start_point = (450, 500)
    #start_point = (650, 650)
    start_point= (500, 1100)
    end_point = (240, 300)
    #end_point = (450, 1240)
    #end_point = (500, 1240)


    points_on_line,line_draw = bresenham_line(*start_point, *end_point,map_)
    count = 0
    for i in range(len(points_on_line) - 1):
        start_point = points_on_line[i]
        end_point = points_on_line[i + 1]
        x,y = start_point
        x1,y1 = end_point

        if map_[x1,y1] == 255 and map_[x,y] == 100:
            start_obs = x,y
        
        if map_[x1,y1] == 100 and map_[x,y] == 255:
            end_obs = x,y
            count +=1
            path = obstacle_avoid_left(start_obs,end_obs)
            
            if path:
                line_draw.extend(path)
            else:
                path = obstacle_avoid_right(start_obs,end_obs)
                if path:
                    line_draw.extend(path)
        


    cv2.imshow("Path", map_)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    plot(line_draw,map_)
    print(count)

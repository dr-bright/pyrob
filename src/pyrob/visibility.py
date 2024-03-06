from .misc import *
from .mapp import *
from .graph import *
from .lidar import *
from .plotters import *

import pathlib
import cv2
import numpy as np

import matplotlib.pyplot as plt

# Функция для проверки пересечения отрезков
def line_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    d = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

    if d == 0:
        return True  # Отрезки параллельны или совпадают

    ua = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3)) / d
    ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / d

    if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
        if (x1 == x3 and y1 == y3) or (x1 == x4 and y1 == y4) or (x2 == x3 and y2 == y3) or (x2 == x4 and y2 == y4):
            return True  # Отрезки пересекаются в концах
        else:
            return False  # Отрезки пересекаются
    else:
        return True  # Отрезки не пересекаются

# Функция для построения графа видимости
def visibility_graph(obstacle, start):
    obstacles = []
    obstacles.append(start)
    for i in range(len(obstacle)):
        obstacles.append(obstacle[i])
    # Проверяем видимость между всеми парами вершин
    edges_vids = []
    visible = False
    for i in range(len(obstacles)):
        for j in range(len(obstacles[i])):
            for l in range(len(obstacles)):
                if i != l or i == l == 0:
                    for s in range(len(obstacles[l])):
                        if i != l or j != s:          
                            for k in range(len(edges)):
                                line = obstacles[i][j],obstacles[l][s]
                                if line_intersection(line, edges[k]):
                                    visible = True
                                    #print("True")
                                    #print(line, edges[k])
                                else:
                                    #print("False")
                                    #print(line, edges[k])
                                    visible = False
                                    break
                            if visible == True:
                                #print('a')
                                edges_vids.append((obstacles[i][j],obstacles[l][s]))

    return edges_vids

edges = [] 

def graph_visib(map_, show=False):
    obstacles_vertices = []  # Список для хранения вершин каждого контура

    if show:
        _, show = plt.subplots()

    _, threshold = cv2.threshold(map_, 110, 255, cv2.THRESH_BINARY) 

    # Detecting contours in image. 
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    # Going through every contours found in the image. 
    for cnt in contours: 
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

        if len(approx) > 5:
        # Добавляем координаты вершин текущего контура в список
            vertices = [tuple(vertex[0]) for vertex in approx]
            obstacles_vertices.append(vertices)

            # Рисуем точки для каждой вершины
            for vertex in vertices:
                cv2.circle(map_, vertex, 5, (0, 0, 255), -1)
                
            for i in range(len(vertices) - 1):
                edge = (vertices[i], vertices[i+1])
                edges.append(edge)
            # Добавляем ребро между последней и первой вершинами
            edge = (vertices[-1], vertices[0])
            edges.append(edge)


    # Отображаем изображение, если необходимо
    if show:
        cv2.imshow('image2', map_)  
        if cv2.waitKey(0) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()

    return obstacles_vertices

def visualize(obstacles, visib, map_, start):
    # Создаем копию карты для визуализации
    map_vis = map_.copy()

    # Рисуем препятствия
    #for obstacle in obstacles:
     #   cv2.polylines(map_vis, [np.array(obstacle)], True, (0, 0, 255), 2)

    # Рисуем стартовую точку
    cv2.circle(map_vis, start[0], 10, (0, 255, 0), -1)

    # Рисуем ребра видимости
    for edge in visib:
        cv2.line(map_vis, edge[0], edge[1], (255, 0, 0), 2)

    # Отображаем изображение
    cv2.imshow('Visibility Graph', map_vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

path = pathlib.Path('..','..','data', 'examp2.txt')

start = [(470,450), (730,600)]
odom, lidar = read_txt(str(path))
pts = stupid_slam(odom, lidar)
map_ = render_ptc(pts, 100, ksize= 9, msize = 9)
obstacless = graph_visib(map_, show=True)
visib = visibility_graph(obstacless,start)

visualize(obstacless, visib, map_, start)
print(obstacless)  # Печать списка с координатами вершин каждого контура
print(edges)
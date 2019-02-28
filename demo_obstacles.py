import turtle
import reeds_shepp as rs
import utils
import draw
import math
import random as rd


"""
draw start vector by choosing two points (base and direction)
draw end vector by choosing two points (base and direction)
draw obstacles by choosing two points (top-left corner and bottom-right corner)
press "run"

it is still a bit buggy on the obstacles because there's a security margin 
so the paths do not collide with the obstacles, but the algo isn't optimal
"""

INF = 1e9
EPS = 1e-9

SAFETY = 2*draw.SCALE

speedy = turtle.Turtle()

START = None
END = None

BOUNDARIES = draw.scale([-9,7,9,-7])
RUN_BOUNDARIES = draw.scale([-2.1,7.7,.6,7.3])

# obstacle = 4 values: top-left coords and bottom-right coords
OBSTACLES = [] #[draw.scale([-7,8,7,7]),draw.scale([7,7,8,-7]),draw.scale([-7,-7,7,-8]),draw.scale([-8,7,-7,-7])]

STEP = 1

def collision(pt, obstacle, safety):
    if pt[0] >= obstacle[0] - safety and pt[0] <= obstacle[2] + safety \
    and pt[1] <= obstacle[1] + safety and pt[1] >= obstacle[3] - safety:
        return True
    else:
        return False

def read_click(x, y):
    global STEP
    global START
    global END
    global OBSTACLES

    if not collision([x,y], BOUNDARIES, 0):
        if STEP == 3 and collision([x,y], RUN_BOUNDARIES, 10):
            STEP = 4
            run()
        else:
            return

    if STEP == 1:
        if START:
            theta = utils.rad2deg(math.atan2(y - START[1], x - START[0]))
            START[2] = theta
            draw.goto(speedy, START, scale_pos=False)
            speedy.pencolor("#00FF00")
            draw.vec(speedy)
            speedy.pencolor("#000000")
            STEP = 2
        else:
            if not point_obstacles_collision([x,y], OBSTACLES, SAFETY):
                START = [x, y, None]

    elif STEP == 2:
        if END:
            theta = utils.rad2deg(math.atan2(y - END[1], x - END[0]))
            END[2] = theta
            draw.goto(speedy, END, scale_pos=False)
            speedy.pencolor("#0000FF")
            draw.vec(speedy)
            speedy.pencolor("#000000")
            STEP = 3
        else:
            if not point_obstacles_collision([x,y], OBSTACLES, SAFETY):
                END = [x, y, None]

    elif STEP == 3:
        if not OBSTACLES or len(OBSTACLES[-1]) == 4: # new obstacles
            OBSTACLES.append([x,y])
        else: # finish current obstacle
            if x > OBSTACLES[-1][0] and y < OBSTACLES[-1][1]: # check it has correct form
                OBSTACLES[-1] += [x,y]
                if collision(START[:2], OBSTACLES[-1], SAFETY) \
                or collision(END[:2], OBSTACLES[-1], SAFETY):
                    OBSTACLES.pop(-1)
                else:
                    draw.goto(speedy, OBSTACLES[-1][:2] + [0], scale_pos=False)
                    speedy.begin_fill()
                    for i in range(2):
                        speedy.left(90)
                        speedy.forward(OBSTACLES[-1][3] - OBSTACLES[-1][1])
                        speedy.left(90)
                        speedy.forward(OBSTACLES[-1][0] - OBSTACLES[-1][2])
                    speedy.end_fill()
            else:
                OBSTACLES.pop(-1)

def line_line_collision(pt1, pt2, pt3, pt4):
    try:
        uA = ((pt4[0]-pt3[0])*(pt1[1]-pt3[1]) - (pt4[1]-pt3[1])*(pt1[0]-pt3[0])) / ((pt4[1]-pt3[1])*(pt2[0]-pt1[0]) - (pt4[0]-pt3[0])*(pt2[1]-pt1[1]));
        uB = ((pt2[0]-pt1[0])*(pt1[1]-pt3[1]) - (pt2[1]-pt1[1])*(pt1[0]-pt3[0])) / ((pt4[1]-pt3[1])*(pt2[0]-pt1[0]) - (pt4[0]-pt3[0])*(pt2[1]-pt1[1]));
    except ZeroDivisionError:
        return True
    return (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1)

def line_rect_collision(pt1, pt2, rect, safety):
  left = line_line_collision(pt1, pt2, [rect[0]-safety, rect[1]+safety], [rect[0]-safety,rect[3]-safety])
  right = line_line_collision(pt1, pt2, [rect[2]+safety,rect[1]+safety], [rect[2]+safety, rect[3]-safety])
  top = line_line_collision(pt1, pt2, [rect[0]-safety, rect[1]+safety], [rect[2]+safety,rect[1]+safety])
  bottom = line_line_collision(pt1, pt2, [rect[0]-safety,rect[3]-safety], [rect[2]+safety, rect[3]-safety])

  return (left or right or top or bottom)

def point_obstacles_collision(pt, obstacles, safety):
    for obstacle in obstacles:
        if collision(pt, obstacle, safety):
            return True
    return False

def line_obstacles_collision(pt1, pt2, obstacles, safety):
    for obstacle in obstacles:
        if line_rect_collision(pt1, pt2, obstacle, safety):
            return True
    return False


def run():
    # 1 - find points such that there exist a path

    pts_from_start = [START[:2]]
    pts_from_end = [END[:2]]

    start_from = { 0: 0 }
    end_from = { 0: 0 }

    connection = False
    while not connection:
        x = rd.uniform(BOUNDARIES[0], BOUNDARIES[2])
        y = rd.uniform(BOUNDARIES[3], BOUNDARIES[1])
        pt1 = [x,y]

        if point_obstacles_collision(pt1, OBSTACLES, SAFETY):
            draw.goto(speedy, pt1 + [0], scale_pos=False)
            speedy.dot(5, "#FF0000")
        else:
            connected_start = False
            for i2, pt2 in enumerate(pts_from_start):
                if not line_obstacles_collision(pt1, pt2, OBSTACLES, SAFETY):
                    draw.goto(speedy, pt1 + [0], scale_pos=False)
                    speedy.dot(5, "#00FF00")
                    start_from[len(pts_from_start)] = i2
                    pts_from_start.append(pt1)
                    connected_start = True
                    break
            for i2, pt2 in enumerate(pts_from_end):
                if not line_obstacles_collision(pt1, pt2, OBSTACLES, SAFETY):
                    draw.goto(speedy, pt1 + [0], scale_pos=False)
                    speedy.dot(5, "#0000FF")
                    end_from[len(pts_from_end)] = i2
                    pts_from_end.append(pt1)
                    if connected_start:
                        connection = True
                    break


    path = [pts_from_start[-1]]
    idx = len(pts_from_start)-1
    while idx != 0:
        idx = start_from[idx]
        path.insert(0, pts_from_start[idx])
    idx = len(pts_from_end)-1
    while idx != 0:
        idx = end_from[idx]
        path.append(pts_from_end[idx])

    speedy.pencolor("#FF00FF")
    draw.goto(speedy, path[0] + [0], scale_pos=False)
    for i in range(len(path)-1):
        speedy.goto(path[i+1])


    draw.SCALE = 40

    augmented_path = [(draw.unscale(START[0]), draw.unscale(START[1]), START[2])]
    for i in range(1, len(path)-1):
        dx = path[i+1][0] - path[i][0]
        dy = path[i+1][1] - path[i][1]
        theta = math.atan2(dy, dx)
        augmented_path.append((draw.unscale(path[i][0]), draw.unscale(path[i][1]), utils.rad2deg(theta)))
    augmented_path.append((draw.unscale(END[0]), draw.unscale(END[1]), END[2]))

    speedy.pencolor("#00AAAA")
    for i in range(len(augmented_path) - 1):
        paths = rs.get_all_paths(augmented_path[i], augmented_path[i+1])
        for path in paths:
            draw.goto(speedy, augmented_path[i])
            draw.draw_path(speedy, path)

    speedy.pencolor("#FF0000")
    speedy.pensize(3)
    draw.goto(speedy, augmented_path[0])
    speedy.speed(8)
    for i in range(len(augmented_path) - 1):
        path_opt = rs.get_optimal_path(augmented_path[i], augmented_path[i+1])
        draw.draw_path(speedy, path_opt)





def main():

    # init
    speedy.speed(0)
    speedy.ht()

    turtle.onscreenclick(read_click)

    # draw boundaries
    # draw.goto(speedy, BOUNDARIES[:2] + [0], scale_pos=False)
    # for i in range(2):
    #     speedy.left(90)
    #     speedy.forward(BOUNDARIES[3] - BOUNDARIES[1])
    #     speedy.left(90)
    #     speedy.forward(BOUNDARIES[0] - BOUNDARIES[2])

    # write instructions
    draw.goto(speedy, (-7, 7.8, 0))
    speedy.write("1. Choose start vector", font=("Arial", 12, "italic"))
    draw.goto(speedy, (-6, 7.3, 0))
    speedy.write("2. Choose end vector", font=("Arial", 12, "italic"))
    draw.goto(speedy, (-3, 7.8, 0))
    speedy.write("3. Place obstacles", font=("Arial", 12, "italic"))
    draw.goto(speedy, (-2, 7.3, 0))
    speedy.write("4. Click here to run", font=("Arial", 12, "bold italic"))

    turtle.done()


if __name__ == '__main__':
    main()

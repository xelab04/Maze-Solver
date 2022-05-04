import pygame, sys, os, subprocess, random, time, math
from pygame.locals import *
import savestates

save_1 = savestates.save_1
save_2 = savestates.save_2
save_3 = savestates.save_3
black = (0,0,0)

window_width = 960
window_height = 720
size = 40

fps = 30
fpsCLOCK = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Artificial Intelligence')
font_obj = pygame.font.Font('freesansbold.ttf',20)

colour_dict = {
    "black" : (0,0,0),
    "white" : (255,255,255),
    "yellow" : (255,255,0),
    "blue" : (0,255,255)
    }

colour_txt = ["black","white","yellow","blue"]
colour_num = [(0,0,0),(255,255,255),(255,255,0),(0,255,255)]

def mod(num):
    if num < 0:
        return num * -1
    else:
        return num

class NODE():

    def __init__(self, point, goal, start):
        self.coords = point

        y,x = point
        i,j = goal
        p,q = start
        self.path_cost = mod(y-i) + mod(x-j)
        self.distance = mod(y-p) + mod(x-q)

class STACK():
    def __init__(self, starting_node):
        self.array = [starting_node]

    def retrieve(self):
        return self.array[-1]

    def delete(self):
        #is this -1 or -2?
        self.array = self.array[0:-1:]

    def add(self,node):
        self.array.append(node)

    def output(self):
        print(self.array)

class QUEUE(STACK):
    def retrieve(self):
        return self.array[0]

    def delete(self):
        self.array = self.array[1::]

class DFS():
    def __init__(self,start,end):
        self.starting_point = start
        self.goal = end

        self.frontier = STACK(NODE(self.starting_point, self.goal, self.starting_point))
        self.explored = [self.starting_point]


    def pos_actions(self,coords, matrix):
        y,x = coords
        temp_actions = []
        possible_action = [(0,-1),(-1,0),(0,1),(1,0)]

        for action in possible_action:

            if (y+action[0] < 0 or y+action[0] > 17 or x+action[1] < 0 or x+action[1] > 23):
                continue

            elif matrix[y+action[0]][x+action[1]] in ["black","blue"] and (y+action[0],x+action[1]) not in self.explored:
                #for node in self.explored:
                #    if node.coords != (y+action[0], x+action[1]):
                #        temp_actions.append(action)
                temp_actions.append(action)

        return temp_actions

    def solve(self,matrix):
        while self.frontier.array != []:

            node = self.frontier.retrieve()

            draw_rect(node.coords,(255,255,0))
            pygame.display.update()
            pygame.time.wait(100)

            self.frontier.delete()
            self.explored.append(node.coords)

            if node.coords == self.goal:
                print("Route Found")
                return True

            actions = self.pos_actions(node.coords,matrix)

            y,x = node.coords
            for action in actions:
                self.frontier.add(NODE((y+action[0],(x+action[1])),self.goal, self.starting_point))


        print("No Solutions")
        return False

class BFS(DFS):
    def __init__(self,start,end):
        self.starting_point = start
        self.goal = end

        self.frontier = QUEUE(NODE(self.starting_point, self.goal, self.starting_point))
        self.explored = [self.starting_point]

class GBFS():
    def __init__(self,start,end):
        self.starting_point = start
        self.goal = end

        self.frontier = [NODE(self.starting_point,self.goal, self.starting_point)]
        self.explored = [self.starting_point]


    def pos_actions(self,coords, matrix):
        y,x = coords
        temp_actions = []
        possible_action = [(0,-1),(-1,0),(0,1),(1,0)]

        for action in possible_action:

            if (y+action[0] < 0 or y+action[0] > 17 or x+action[1] < 0 or x+action[1] > 23):
                continue

            elif matrix[y+action[0]][x+action[1]] in ["black","blue"] and (y+action[0],x+action[1]) not in self.explored:
                temp_actions.append(action)

        return temp_actions

    def min_frontier(self,frontier):
        minimal = float("inf")
        for node in frontier:
            if node.path_cost < minimal:
                minimal = node.path_cost
                min_node = node
        index = frontier.index(min_node)
        return min_node, index

    def solve(self,matrix):
        while self.frontier != []:

            node, index = self.min_frontier(self.frontier)

            draw_rect(node.coords,(255,255,0))
            pygame.display.update()
            pygame.time.wait(100)

            self.frontier.pop(index)
            self.explored.append(node.coords)

            if node.coords == self.goal:
                print("Route Found")
                return True

            actions = self.pos_actions(node.coords,matrix)

            y,x = node.coords
            for action in actions:
                self.frontier.append(NODE((y+action[0],(x+action[1])),self.goal, self.starting_point))


        print("No Solutions")
        return False

class ASTAR():
    def __init__(self,start,end):
        self.starting_point = start
        self.goal = end

        self.frontier = [NODE(self.starting_point,self.goal, self.starting_point)]
        self.explored = [self.starting_point]


    def pos_actions(self,coords, matrix):
        y,x = coords
        temp_actions = []
        possible_action = [(0,-1),(-1,0),(0,1),(1,0)]

        for action in possible_action:

            if (y+action[0] < 0 or y+action[0] > 17 or x+action[1] < 0 or x+action[1] > 23):
                continue

            elif matrix[y+action[0]][x+action[1]] in ["black","blue"] and (y+action[0],x+action[1]) not in self.explored:
                temp_actions.append(action)

        return temp_actions

    def min_frontier(self,frontier):
        minimal = float("inf")
        for node in frontier:
            if node.path_cost + node.distance < minimal:
                minimal = node.path_cost + node.distance
                min_node = node
        index = frontier.index(min_node)
        return min_node, index

    def solve(self,matrix):
        while self.frontier != []:

            node, index = self.min_frontier(self.frontier)

            draw_rect(node.coords,(255,255,0))
            pygame.display.update()
            pygame.time.wait(100)

            self.frontier.pop(index)
            self.explored.append(node.coords)

            if node.coords == self.goal:
                print("Route Found")
                return True

            actions = self.pos_actions(node.coords,matrix)

            y,x = node.coords
            for action in actions:
                self.frontier.append(NODE((y+action[0],(x+action[1])),self.goal, self.starting_point))


        print("No Solutions")
        return False


def draw_rect(corner,colour):
    y,x = corner
    rect = pygame.Rect(x*size,y*size,size,size)
    pygame.draw.rect(window,colour,rect,0)

def next_colour(colour):
    colours = [(0,0,0),(255,255,255),(255,255,0),(0,255,255)]
    index = colours.index(colour) + 1
    if index == len(colours):
        index = 0
    return colours[index]

def draw_image(dir):
    img = pygame.image.load(dir)
    img = pygame.transform.scale(img, (960, 720))
    rect = img.get_rect()
    rect.center = (window_width/2 -2,window_height/2 -2)

    window.blit(img, rect)

def convert_grid():

    matrix = [[0 for x in range(24)] for y in range(18)]

    for i in range(24):
        for j in range(18):
            x,y = (int(i*size + size/2),int(j*size + size/2))
            colour = window.get_at((x, y))
            #print(colour)
            colour_text = colour_txt[colour_num.index(colour)]
            #print(j,i)
            matrix[j][i] = colour_text

    return matrix

def reset_grid(matrix):
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            if matrix[i][j] == "yellow":
                matrix[i][j] == "black"

    return matrix

def obtain_point():
    #is this inverted?
    x,y = pygame.mouse.get_pos()
    coords = (math.floor(y/size), math.floor(x/size))
    return coords


clicking = False
count = 0
start, end = None, None
ai_count = 0
save_index = -1
matrix = [[0 for x in range(int(window_width/size))] for y in range(int((window_height/size)))]
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            x,y = pygame.mouse.get_pos()
            colour = window.get_at((x, y))
            corner = math.floor(y/size),math.floor(x/size)

            if event.button == 1:
                clicking = True
                colour = next_colour(colour)
            else:
                colour = black

            draw_rect(corner,colour)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            clicking = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_z:
                #get the matrix of the current board state
                temp_matrix = convert_grid()
                for row in temp_matrix:
                    print(row)

            if event.key == pygame.K_x:

                for i in range(18):
                    for j in range(24):
                        colour = window.get_at((j*size + 20, i*size + 20))
                        if colour == (255,255,0):
                            draw_rect((i,j),black)
                #reset the grid, remove all yellow squares

            if event.key == pygame.K_c:

                x,y = pygame.mouse.get_pos()
                corner = math.floor(y/size),math.floor(x/size)

                draw_rect(corner,(0,255,255))

                if start == None and end == None:
                    start = corner
                elif start != None and end == None:
                    end = corner
                elif start != None and end != None:

                    if ai_count == 0:
                        AI = DFS(start,end)
                    elif ai_count == 1:
                        AI = BFS(start,end)
                    elif ai_count == 2:
                        AI = GBFS(start,end)
                    elif ai_count == 3:
                        AI = ASTAR(start,end)

                    matrix = convert_grid()
                    AI.solve(matrix)

                    start = None
                    end = None

            if event.key == pygame.K_v:
                ai_choice = ["DFS","BFS","GBFS","A*"]
                ai_count += 1
                if ai_count > 3:
                    ai_count = 0

                print(f"{ai_choice[ai_count]} has been selected")



            if event.key == pygame.K_w:
                save_index += 1

                if save_index > 2:
                    save_index = 0
                if save_index == 0:
                    save = save_1
                elif save_index == 1:
                    save = save_2
                elif save_index == 2:
                    save = save_3

                for i in range(len(save)):
                    row = save_1[0]
                    for j in range(len(row)):
                        draw_rect((i,j),colour_num[colour_txt.index(save[i][j])])

            if event.key== pygame.K_e:
                name = "/home/alex/Pictures/Mazes/" + "maze" + str(count)
                pygame.image.save(window,name)
                count += 1

    if clicking:
        x,y = pygame.mouse.get_pos()
        #colour = next_colour(colour)
        corner = math.floor(y/size),math.floor(x/size)
        draw_rect(corner,colour)


    pygame.display.update()
    fpsCLOCK.tick(fps)

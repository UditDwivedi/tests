import pygame,time
from pygame.locals import *
pygame.init()

startstring = '''
This is A* algorithm
This is used to find the shortest travel path between two points around obstacles.

A new window named Path has been created
'''

print(startstring)

instruction = '''
A hollow rectangle follows cursor. This is tool.

Blact = Walls/Obstacles  press 1
Red = Start              press 2
Green = End              press 3

Left Click to place current tile.
Right Click to remove tile below the cursor.
Press z to remove previously placed walls.

Press spacebar to run the simulation.
Press r to reset the grid before and after simulation.
Press d to switch between drawing searched cells during simulation or not.

Press i to show these instructions again.

**************************************************************************'''

print(instruction)

width = 840
height = 840
tilesize = 15
infinite = (height//tilesize)*(width//tilesize)+1
color = ((220,220,220),(30,30,30),(255,0,0),(0,255,0),(255,255,0),(0,255,255),(0,0,255),(255,0,255))
clock = pygame.time.Clock()

win = pygame.display.set_mode((width,height))
pygame.display.set_caption('Path')

FPS = 60
font = pygame.font.SysFont('Calibri',15,0,1)
adjacent = ((0,-1),(1,0),(0,1),(-1,0))

start = False
end = False
laying_tool = 1
to_path = False
walls = []

draw_search = True
a = [False,None]

def out_of_bound(current):
    x,y = current
    if x < 0 or x*tilesize >= width or y < 0 or y*tilesize >= height:
        return True

def H_COST(tile,end):
    return (abs(tile[0]-end[0])+abs(tile[1]-end[1]))
        

class NODE:
    def __init__(self,point,state,gcost,parent,end):
        self.x = point[0]
        self.y = point[1]
        self.state = state
        self.gcost = gcost
        self.hcost = abs(self.x-end[0])+abs(self.y-end[1])
        self.fcost = self.gcost + self.hcost
        self.parent = parent

    def draw(self,win):
        pygame.draw.rect(win, color[self.state], (self.x*tilesize,self.y*tilesize,tilesize,tilesize))

def pathfind(Start,End):
    to_search = {}
    To_search = {}
    searched = []
    Searched = {}
    Walls = []
    Min = False
    found = False
    blocked = False
    Run = True
    start = NODE(Start,3,0,None,End)
    To_search[start.fcost] = [start]
    to_search[Start] = [start.fcost]
    Min = start.fcost
    while not found and Run:
        for event in pygame.event.get():
            if event.type == QUIT:
                Run = False
        
        if to_search == {}:
            break
        else:
            Current = To_search[Min][0]
            current = (Current.x,Current.y)
            for i in adjacent:
                new = (current[0]+i[0],current[1]-i[1])                
                if new not in searched and new not in walls and not out_of_bound(new):
                    if new not in to_search:
                        New = NODE(new,3,Current.gcost+1,current,End)
                        Searched[new] = New.parent
                    else:
                        for i in To_search[to_search[new]]:
                            if (i.x,i.y) == new:
                                New = i
                                break
                    if new == End:
                        found = True
                    if new not in to_search:                           
                        to_search[new] = New.fcost
                        if New.fcost not in To_search:
                            To_search[New.fcost] = []
                            if New.fcost < Min:
                                Min = New.fcost
                        To_search[New.fcost].append(New)
                        if draw_search:
                            pygame.draw.rect(win,color[4],(new[0]*tilesize,new[1]*tilesize,tilesize-1,tilesize-1))
                            pygame.display.update()
                    elif new in to_search:
                        if New.fcost > to_search[new]:
                            for cell in To_search[to_search[new]]:
                                if (cell.x,cell.y) == new:
                                    cell.fcost = New.fcost
                                    cell.parent = New.parent
                    
            searched.append(current)
            if current != Start and draw_search:
                pygame.draw.rect(win,color[5],(current[0]*tilesize,current[1]*tilesize,tilesize-1,tilesize-1))
                pygame.display.update()
            
            del to_search[current]
            To_search[Current.fcost].pop(0)
            if To_search[Current.fcost] == []:
                del To_search[Current.fcost]
                if Current.fcost == Min:
                    Min = float('inf')
                    for i in To_search:
                        if i < Min:
                            Min = i
                            
    if Run:
        if found:
            cur = End
            while True:
                pygame.draw.rect(win,color[6],(cur[0]*tilesize,cur[1]*tilesize,tilesize-1,tilesize-1))
                pygame.display.update()
                n_cur = Searched[cur]
                cur = n_cur
                if cur == Start:
                    break                
            return (True,True)
        
        else:
            print('No possible Path exists')
            return (True,False)
    else:
        return ('Exit')

def redraw():
    win.fill(color[0])    

    for wall in walls:
        pygame.draw.rect(win, color[1], (wall[0]*tilesize,wall[1]*tilesize,tilesize,tilesize))
        
    if start:
        pygame.draw.rect(win, color[2], (start[0]*tilesize,start[1]*tilesize,tilesize,tilesize))
    if end:
        pygame.draw.rect(win, color[3], (end[0]*tilesize,end[1]*tilesize,tilesize,tilesize))

    pygame.draw.rect(win, color[laying_tool], (mpos[0]*tilesize-1,mpos[1]*tilesize-1,tilesize,tilesize),4)

    for i in range(-1,width,tilesize):
        pygame.draw.line(win, color[1], (i,0), (i,height))
    for j in range(-1,height,tilesize):
        pygame.draw.line(win, color[1], (0,j), (width,j))    

    pygame.display.update()
    
run = True
while run:

    mpos_ = pygame.mouse.get_pos()
    mpos = (mpos_[0]//tilesize,mpos_[1]//tilesize)
    mice = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if start and end:
                    to_path = True
                else:
                    print('Make sure Start and End exist')
            if event.key == K_r:
                start = False
                end = False
                laying_tool = 1
                to_path = False
                walls = []
                a = (False,None)
            if event.key == K_d:
                draw_search = not draw_search
            if event.key == K_i:
                print(instruction)
                
            if event.key == K_1:
                laying_tool = 1
            if event.key == K_2: 
                laying_tool = 2
            if event.key == K_3:
                laying_tool = 3

    if to_path and start and end:
        a = pathfind(start,end)
        if a == 'Exit':
            run = False
        to_path = False

    if not to_path:
            
        if mice[0]:
            if mpos not in walls and laying_tool == 1 and mpos != start and mpos != end:
                walls.append(mpos)
            if laying_tool == 2 and mpos != end and mpos not in walls:
                start = mpos
            if laying_tool == 3 and mpos != start and mpos not in walls:
                end = mpos
                
        if mice[2]:
            if mpos in walls:
                walls.remove(mpos)
            if start and mpos == start:
                start = False
            if end and mpos == end:
                end = False

        if keys[K_z]:
            if walls != []:
                del walls[-1]
        
    if not a[0]:
        redraw()

    clock.tick(FPS)

pygame.quit()

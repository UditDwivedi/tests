import pygame,math,random
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((600,600))

font1 = pygame.font.SysFont('comicsans',20,1)

player = pygame.Rect(300,300,20,20)
move = [0,0]
path = [None,None,0]
drawline = False
plymove = False
polygondraw = False

class Line:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2
        self.collision = 0
        self.xdif = (self.p1[0]-self.p2[0])
        self.ydif = (self.p1[1]-self.p2[1])
        self.angle = math.atan2(self.ydif,self.xdif)
        self.lenght = math.sqrt(self.xdif**2 + self.ydif**2)
        self.sep = abs(math.cos((self.angle - math.radians(45))%math.radians(90)))

    def update():
        xdif = (self.p1[0]-self.p2[0])
        ydif = (self.p1[1]-self.p2[1])
        self.angle = math.atan2(xdif,ydif)
        self.lenght = math.sqrt(xdif**2 + ydif**2)

    def draw(self,win):
        pygame.draw.line(win, (0,0,self.collision), self.p1, self.p2)

class Polygon:
    def __init__(self,points):
        self.points = points

def find_intersection( p0, p1, p2, p3 ) :

    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y
    if denom == 0 :
        return None # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive : return None # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive : return None # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


    # collision detected

    t = t_numer / denom

    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]

    return intersection_point

def dotprod(unit,vect):
    dif = unit[1] - vect[1]
    mag = unit[0] * vect[0]*math.cos(dif)
    print(mag)
    x = mag * math.cos(unit[1])
    y = mag * math.sin(unit[1])
    return x,y

def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

def distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return (math.sqrt((x1-x2)**2 + (y1-y2)**2))

def sqdistance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return ((x1-x2)**2 + (y1-y2)**2)


def vector(pin,m=True,d=True):
    mag = math.sqrt(pin[0]**2 + pin[1]**2)
    dirc = math.atan2(pin[1],pin[0])
    if m and d:
        return (mag,dirc)
    elif m:
        return (mag)
    else:
        return(dirc)

def plinesegdis(line,point):
    p1,p2 = line.p1,line.p2
    if p1 == p2:
        return distance(p1,point)
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    up = abs(dy*(point[0] - p1[0]) + dx*(p1[1] - point[1]))
    down = dx**2 + dy**2
    dis = up/math.sqrt(down)
    linesq = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
    p1sq = (p1[0] - point[0])**2 + (p1[1] - point[1])**2
    p2sq = (p2[0] - point[0])**2 + (p2[1] - point[1])**2
    Max = linesq + dis**2
    a = dy
    b = -dx
    c = -dy*p1[0]+dx*p1[1]
    bx = b*point[0]
    ay = a*point[1]
    x = (b*(bx - ay)-a*c)/down
    y = (a*(ay - bx)-b*c)/down
    repoint = (x,y)
    if p1sq > Max or p2sq > Max:
        if p1sq < p2sq:
            return math.sqrt(p1sq),p1
        else:
            return math.sqrt(p2sq),p2
    else:
        return dis,repoint

def linecollision(line,rect,move):
    move =[0,0]
    p1,p2,p3,p4 = (rect.left,rect.top),(rect.right,rect.top),(rect.right,rect.bottom),(rect.left,rect.bottom)
    points = (p1,p2,p3,p4)
    for p in points:
        if find_intersection(line.p1,line.p2,p,rect.center):
            r=plinesegdis(line,p)
            move[0] = r[1][0]-p[0]
            move[1] = r[1][1]-p[1]
            break
    rect.x += move[0]
    rect.y += move[1]

def Move(test,move):
    test.x += move[0]
    test.y += move[1]
    for line in lines:
        move = linecollision(line,test,move)

def isconvex(points):
    xs = []
    ys = []
    for point in points:
        xs.append(point[0])
        ys.append(point[1])
    cx = int(sum(xs)/len(xs))
    cy = int(sum(ys)/len(ys))
    cent = (cx,cy)
    f,l = points[0],points[-1]
    temp = f+poins+l
    sqdis = {}
    for i in range(1,len(temp)-1):
        d1 = sqdistaace(temp[i],cent)
        d2 = sqdistaace(temp[i],temp[i-1])
        d3 = sqdistaace(temp[i],cent[i+1])
        sqdis[d1] = (d2,d3)

    concaves = []
        

def isconvex_(points):
    convex = True
    l,r,u,d = float('inf'),-float('inf'),float('inf'),-float('inf')
    down = None
    for point in points:
        if point[0] < l:
            l = point[0]
        if point[0] > r:
            r = point[0]
        if point[1] < u:
            u = point[1]
        if point[1] > d:
            d = point[1]
            down = point
            cut = points.index(point)

    fulllen = len(points)
    if cut == 0:
        cycle = [points[-1]] + points + [points[0]]
    elif cut == fulllen - 1:
        cycle = points[-2:] + points
    else:
        cycle = points[cut-1:] + points[:cut]

    print(points)
    print(cycle)

    yax = 'dec'
    for r in range(1,fulllen+1):
        if cycle[r][0] < cycle[r+1][0]:
            xax = 'dec'
            if 

lines = []
polygons = []
drawrandom = False

sep = 20
polypoints = []

run = True
while run:

    win.fill((255,255,255))

    mpos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                if polygondraw:
                    polygons.append(polypoints)
                    #isconvex(polypoints)
                    isconvex_(polypoints)
                    polygondraw = False
                    polypoints = []
            if event.button == 1:
                if not polygondraw:
                    polypoints = [mpos]
                    polygondraw = True
                else:
                    if mpos not in polypoints:
                        polypoints.append(mpos)
    move = [0,0]

    if keys[K_LEFT]:
        move[0] = -4
    elif keys[K_RIGHT]:
        move[0] = 4
    if keys[K_UP]:
        move[1] = -4
    elif keys[K_DOWN]:
        move[1] = 4

    Move(player,move)

    if keys[K_SPACE]:
        x=random.randint(0,600)
        y=random.randint(0,600)
        lines.append(Line((x,y),(x,y)))
    

    if drawline:
        pygame.draw.line(win, (0,0,0), start, mpos)

    for line in lines:
        ater = plinesegdis(line,mpos)
        line.draw(win)

    for polygon in polygons:
        pygame.draw.polygon(win,(0,0,0),polygon,1)

    if len(polypoints) > 2:
        pygame.draw.polygon(win,(255,0,0),polypoints)

    pygame.draw.rect(win, (255,0,0), player)

    pygame.display.update()

    clock.tick(30)

pygame.quit()

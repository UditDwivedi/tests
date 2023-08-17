import pygame
from pygame.locals import *

size = (40,35)
tilesize = 20
screen = (size[0]*tilesize,size[1]*tilesize)
win = pygame.display.set_mode(screen)

color = ((0,0,0),(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,255,255))
adj = ((1,0),(0,1),(-1,0),(0,-1))

def drawgrid():
    for i in range(0,screen[0],tilesize):
        pygame.draw.line(win,color[0],(i,0),(i,screen[1]))
    for j in range(0,screen[1],tilesize):
        pygame.draw.line(win,color[0],(0,j),(screen[0],j))

def drawblocks():
    for block in blocks:
        pygame.draw.rect(win,color[3],block,3)

def drawsetblock():
    if allowblock:
        pygame.draw.rect(win,color[2],new,3)
    else:
        pygame.draw.rect(win,color[1],new,3)

def blockcollision(b1,b2):
    if b1[0] < b2[0]+b2[2] and b1[0]+b1[2] > b2[0]:
        if b1[1] < b2[1]+b2[3] and b1[1] + b1[3] > b2[1]:
            return True

def cutblock(block,y):
    b1 = (block[0],block[1],block[2],y-block[1])
    b2 = (block[0],y,block[2],block[3]-b1[3])
    return [b1,b2]
    
def cutblockx(b1,b2):
    x1,y1,w1,h1 = b1
    x2,y2,w2,h2 = b2

    cut1 = [None,None]

    new = []
    
    if y1 < y2:
        n = cutblock(b1,y2)
        new.append(n[0])
        r1 = n[1]
        r2 = b2
    elif y1 > y2:
        n = cutblock(b2,y1)
        new.append(n[0])
        r1 = b1
        r2 = n[1]        
    else:
        r1 = b1
        r2 = b2

    d1,d2 = r1[1]+r1[3],r2[1]+r2[3]

    if d1 < d2:
        new.append(r1)
        new.extend(cutblock(r2,d1))
    elif d1 > d2:
        new.append(r2)
        new.extend(cutblock(r1,d2))
    else:
        new.append(r1)
        new.append(r2)

    return new
        
    
def joinblocky(c):
    join = False

    for b in blocks:
        if b[0] == c[0] and b[2] == c[2]:
            if c[1] == b[1] + b[3] or c[1]+c[3] == b[1]:
                join = True
                break
        
    if join:
        blocks.remove(b)
        update.remove(c)
        update.append((c[0],min(c[1],b[1]),c[2],c[3]+b[3]))
        return True
    return False

def joinblockx(c):
    join = False

    for b in blocks:
        if b[1] == c[1] and b[3] == c[3]:
            if c[0] == b[0] + b[2] or c[0]+c[2] == b[0]:
                join = True
                break
        
    if join:
        blocks.remove(b)
        update.remove(c)
        update.append((min(c[0],b[0]),c[1],c[2]+b[2],c[3]))
        return True
    return False

def blockcheckx(c):
    l = (c[0]-tilesize,c[1],tilesize,c[3])
    r = (c[0]+c[2],c[1],tilesize,c[3])
    for b in blocks:
        if blockcollision(b,l):
            return b
        elif blockcollision(b,r):
            return b
    return False

def processupdate():
    while len(update) > 0:
        print(update)
        c = update[0]
        
        if joinblockx(c):
            continue

        check = blockcheckx(c)
        if check:
            update.extend(cutblockx(c,check))
            update.remove(c)
            blocks.remove(check)
            continue

        if joinblocky(c):
            continue
        
        update.remove(c)
        blocks.append(c)
        
def redraw():
    win.fill(color[7])

    drawgrid()
    drawblocks()
    drawsetblock()

    pygame.display.update()

blocks = []
update = []
blocktype = tilesize*1

run = True
while run:

    mpos = pygame.mouse.get_pos()
    mpos_ = (mpos[0]//tilesize,mpos[1]//tilesize)
    mouse = pygame.mouse.get_pressed()

    new = (mpos_[0]*tilesize,mpos_[1]*tilesize,blocktype,blocktype)
    allowblock = True

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == KEYDOWN:
            if event.key == K_1:
                blocktype = 1*tilesize
            if event.key == K_2:
                blocktype = 2*tilesize
            if event.key == K_3:
                blocktype = 3*tilesize
            if event.key == K_4:
                blocktype = 4*tilesize
            if event.key == K_5:
                blocktype = 5*tilesize

    for block in blocks:
        if blockcollision(block,new):
            allowblock = False
            break

    if allowblock:
        if mouse[0]:
            update.append(new)

    processupdate()                    

    redraw()

pygame.quit()

bug = False

while bug:
    f = input('f ').split(',')
    s = input('s ').split(',')
    F = []
    S = []
    for i in f:
        F.append(int(i))
    for i in s:
        S.append(int(i))
    print(cutblockx(F,S))
            

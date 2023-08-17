import pygame,random
from pygame.locals import *
pygame.init()

WIDTH = 760
HEIGHT = 600
window_size = (760,600)
clock = pygame.time.Clock()

color = ((0,0,0),(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(255,255,255))
world = {}
chuncksize = 200
tilehold = 5
tilesize = chuncksize//tilehold
chunck_dim = (round(WIDTH/chuncksize)+1,round(HEIGHT/chuncksize)+1)
chuncklimit = chunck_dim[0]*chunck_dim[1]

Screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Build')

win = pygame.Surface((WIDTH,HEIGHT))
world = {}

class Player(object):
    def __init__(self,x,y,X,Y):
        self.x = x
        self.y = y
        self.h = 20
        self.w = 20
        self.xvel = 0
        self.yvel = 0
        self.xscroll = 0
        self.yscroll = 0
        self.coords = 1
        
    def draw(self,win):
        pygame.draw.rect(win, color[1], (WIDTH//2 - self.w//2,HEIGHT//2 - self.h//2,self.h,self.w))
        if self.coords == 1:
            win.blit(font.render(str((self.x,self.y)),0,color[0]),(WIDTH//2 - self.w//2,HEIGHT//2 - self.h//2))
            win.blit(font.render(str((round(self.x),round(self.y))),0,color[0]),(WIDTH//2 - self.w//2,HEIGHT//2 - self.h//2+17))
            win.blit(font.render(str((self.xscroll,self.yscroll)),0,color[0]),(0,0))
            win.blit(font.render(str(mpos),0,color[0]),(mousepos[0],mousepos[1]-15))
            win.blit(font.render(str((toptile,topchunck,bottomchunck)),0,color[0]),(0,17))
        
def collision(player,build):
    pass

def generate_chunck(x,y):
    chunck_data = []
    for X in range(chuncksize):
        for Y in range(chuncksize):
            chunck_data.append((x*chuncksize+X,y*chuncksize+Y))
    return chunck_data

def tilelines():
    for i in range(0,WIDTH+1,tilesize):
        pygame.draw.line(win, color[0], (i - player.xscroll%tilesize, 0), (i - player.xscroll%tilesize, HEIGHT))
    for i in range(0,HEIGHT+1,tilesize):
        pygame.draw.line(win, color[0], (0, i - player.yscroll%tilesize), (WIDTH, i - player.yscroll%tilesize))
        
def redraw():
    win.fill(color[7])    
    pygame.draw.rect(win, color[2], (mpos[0]*40-player.xscroll-20+WIDTH//2,mpos[1]*40-player.yscroll-20+HEIGHT//2,tilesize,tilesize))
    for tile in tiles:
        pygame.draw.rect(win, color[5], (tile[0]*40-player.xscroll-20+WIDTH//2,tile[1]*40-player.yscroll-20+HEIGHT//2,tilesize,tilesize))
    for chunck in activechunck:
        for grass in world[chunck]:
            pygame.draw.rect(win, color[3], (grass[0]*40-player.xscroll-20+WIDTH//2,grass[1]*40-player.yscroll-20+HEIGHT//2,tilesize,tilesize))
    player.draw(win)
    tilelines()
    
    Screen.blit(pygame.transform.scale(win,(window_size)),(0,0))
    pygame.display.update()

font = pygame.font.SysFont('Calibri',15,1,0)
player = Player(0,0,0,0)
tiles = []
toptile = (round(player.x-0.5)-WIDTH//2//tilesize,round(player.y-0.5)-HEIGHT//2//tilesize)
topchunck = ((toptile[0])//5,(toptile[1])//5)
world = {}
activechunck = []

gamerun = True
while gamerun:
    
    keys = pygame.key.get_pressed()
    mice = pygame.mouse.get_pressed()
    mousepos = pygame.mouse.get_pos()
    mpos = (round((mousepos[0] + player.xscroll - WIDTH//2)/40), round((mousepos[1] + player.yscroll - HEIGHT//2)/40))
    toptile = (round(player.x-0.5)-WIDTH//2//tilesize,round(player.y-0.5)-HEIGHT//2//tilesize)
    topchunck = ((toptile[0])//5,(toptile[1])//5)
    bottomchunck = (topchunck[0]+5,topchunck[1]+4)
    if topchunck not in activechunck or bottomchunck not in activechunck:
        activechunck = []
        for i in range(topchunck[0],bottomchunck[0]+1):
            for j in range(topchunck[1],bottomchunck[1]+1):
                if ((i,j)) not in world:
                    world[(i,j)] = generate_chunck(i,j)
                activechunck.append((i,j))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamerun = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.coords *= -1
            if event.key == K_LALT:
                print(activechunck)
                print(world)

    player.xvel,player.yvel = 0,0
    
    if keys[pygame.K_LEFT]:
        player.xvel -= 4
    if keys[pygame.K_RIGHT]:
        player.xvel += 4
    if keys[pygame.K_UP]:
        player.yvel -= 4
    if keys[pygame.K_DOWN]:
        player.yvel += 4
        
    player.x = round(player.x+player.xvel/tilesize,1)
    player.xscroll += player.xvel
    player.y = round(player.y+player.yvel/tilesize,1)    
    player.yscroll += player.yvel

    if mice[0]:
        if (round(mpos[0]),round(mpos[1])) not in tiles:
            tiles.append((round(mpos[0]),round(mpos[1])))
    
    redraw()
    
    clock.tick(30)

pygame.quit()

    

import pygame
pygame.init()

win = pygame.display.set_mode((600,600))

world = []
x = 0
y = 0

def redraw():
    win.fill((0,0,0))
    for tile in world:
        if tile[2]==1:
            pygame.draw.rect(win,(0,255,0),(tile[0],tile[1],50,50))
        else:
            pygame.draw.rect(win,(0,0,255),(tile[0],tile[1],50,50))
    pygame.draw.rect(win, (255,0,0),(int(x),int(y),25,25))
    pygame.draw.rect(win, (255,255,255),(0,580,int(fuel/1000),20))
    pygame.display.update()

clock = pygame.time.Clock()

run = True
yvel = 0
fuel = 600000
heat = 25
while run:


    m = pygame.mouse.get_pressed()
    m1 = pygame.mouse.get_pos()
    mpos = (50*(m1[0]//50),50*(m1[1]//50))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if m[0] and mpos not in world:
        world.append([mpos[0],mpos[1],0])

    xvel = 0
    if yvel < 10 and y != 575      :
        yvel += 0.07
        
    if keys[pygame.K_UP] and yvel > -4 and fuel > 0 and y != 0:
        yvel += -0.1
        fuel -= 400
    if keys[pygame.K_SPACE] and fuel > 3000 and yvel > -8 and y != 0 and heat > 0:
        yvel += -0.5
        fuel -= 2500
        heat -= 1
    if not keys[pygame.K_SPACE] and heat < 25:
        heat += 1
    if keys[pygame.K_LEFT]:
        xvel = -4
    if keys[pygame.K_RIGHT]:
        xvel = 4

    for tile in world:
        tile[2]=0
        if (((x+13-tile[0]-25)**2+(y+13-tile[1]-25)**2)**0.5)<56:
            tile[2] = 1
            if y + 25 > tile[1] and y < tile[1] + 50:
                if xvel > 0 and tile[0] - (x+25+xvel) < 0 and x < tile[0] + 50:
                    xvel = tile[0] - (x+25)
                if xvel < 0 and tile[0]+50 - x-xvel > 0 and x + 25 > tile[0]:
                    xvel = tile[0] + 50 - x
            if x + 25 > tile[0] and x < tile[0] + 50:
                if yvel > 0 and tile[1] - (y+25+yvel) < 0 and y < tile[1] + 50:
                    yvel = tile[1] - (y+25)
                if yvel < 0 and tile[1]+50 - y-yvel > 0 and y + 25 > tile[1]:
                    yvel = tile[1] + 50 - y
    if x + xvel < 0:
        x = 0
        xvel = 0
    elif x + xvel > 575:
        x = 575
        xvel = 0
    
    if y + yvel < 0:
        y = 0
        yvel = 0
    elif y + yvel > 575:
        y = 575
        yvel = 0
        
    x += xvel
    y += yvel
    redraw()
    
    clock.tick(60)
    
pygame.quit()

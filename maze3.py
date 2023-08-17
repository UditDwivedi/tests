import pygame
import random
pygame.init()

Width = int(input('Width:'))
Height = int(input('Height:'))
color = ((0,0,255),(255,255,255),(255,0,0),(0,255,0))
ad_cell = ((0,-1),(1,0),(0,1),(-1,0))

cellsize = 8

clock = pygame.time.Clock()

win = pygame.display.set_mode((2*Width*cellsize+cellsize,2*Height*cellsize+cellsize))
pygame.display.set_caption('Maze')
            

def redraw():
    win.fill((0,0,0))
    for cell in cells:
        pygame.draw.rect(win,color[cells[cell][1]],(cell[0]*cellsize*2+cellsize,cell[1]*cellsize*2+cellsize,cellsize,cellsize))
        if cells[cell][3]:
            pygame.draw.rect(win,color[cells[cell][1]],(int(cells[cell][3][0]*cellsize*2+cellsize),int(cells[cell][3][1]*cellsize*2+cellsize),cellsize,cellsize))
    pygame.draw.rect(win,color[2],(create[0]*cellsize*2+cellsize,create[1]*cellsize*2+cellsize,cellsize,cellsize))
    if mazeready:
        pygame.draw.rect(win,color[3],((Width-1)*cellsize*2+cellsize,(Height-1)*cellsize*2+cellsize,cellsize,cellsize))

    pygame.display.update()

cells = {}
create = (0,0)
mazeready = False
maze = False
run = True
close = False
walls = []

while run:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if mazeready:
            if keys[pygame.K_RIGHT] and create[0]<Width-1:
                if(create[0]+0.5,create[1])in(cells[create][3],cells[(create[0]+1,create[1])][3]):
                    create = (create[0]+1,create[1])
            if keys[pygame.K_LEFT] and create[0]>0:
                if (create[0]-0.5,create[1])in(cells[create][3],cells[(create[0]-1,create[1])][3]):
                    create = (create[0]-1,create[1])
            if keys[pygame.K_UP] and create[1]>0:
                if (create[0],create[1]-0.5)in(cells[create][3],cells[(create[0],create[1]-1)][3]):
                    create = (create[0],create[1]-1)
            if keys[pygame.K_DOWN] and create[1]<Height-1:
                if (create[0],create[1]+0.5)in(cells[create][3],cells[(create[0],create[1]+1)][3]):
                    create = (create[0],create[1]+1)
            if create == (Width-1,Height-1) :
                mazeready = False
                close = True
    
    if not close and not mazeready:
        if not maze:
            #Create first cell
            if cells == {}:
                cells[(0,0)] = [[(0,1),(1,0)],1,False,False]
                create = (0,0)
            else:
                for i in ad_cell:
                    if (create[0]+i[0],create[1]+i[1]) in cells and (create[0]+i[0],create[1]+i[1])in cells[create][0]:
                        cells[create][0].remove((create[0]+i[0],create[1]+i[1]))                         
                if cells[tuple(create)][0] != []:
                    new = random.choice(cells[tuple(create)][0])
                    cells[tuple(create)][0].remove(new)
                    cells[new] = [[],0,create]
                    cells[new].append(((new[0]+create[0])/2,(new[1]+create[1])/2))
                    create = new
                    for i in ad_cell:
                        xdif = create[0] + i[0]
                        ydif = create[1] + i[1]
                        if xdif < Width and xdif >= 0 and ydif < Height and ydif >= 0:
                            if (xdif,ydif) not in cells:
                                cells[create][0].append((xdif,ydif))
                else:
                    cells[create][1] = 1
                    create = cells[create][2]
                if create == (0,0):
                    maze = True
        elif maze:
            for cell in cells:
                walls.append(cell)
            mazeready = True

    if close or keys[pygame.K_ESCAPE]:
        run = False

    redraw()
    
    clock.tick(60)
    
pygame.quit()
    

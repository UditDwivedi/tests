import pygame,time,random
from pygame.locals import *
pygame.init()
clock = pygame.time.Clock()

screen = (810,600)
FPS = 30
win = pygame.display.set_mode(screen,0,32)
pygame.display.set_caption('Platformer')

font = pygame.font.SysFont('Calibri',20,1,0)
color = ((0,0,0),(255,0,0),(0,255,0),(255,255,0),(0,255,255),(0,0,255),(255,0,255),(255,255,255))
adjacent = ((0,-1),(1,0),(0,1),(-1,0))

tilesize = 30

class Slope:
    def __init__(self,coord,slope,direction):
        self.coord = coord
        self.slope = slope
        self.direction = direction        
        xcor,ycor = 1,1
        if abs(self.slope) > 1:
            ycor = abs(self.slope)
        else:
            xcor = abs(self.slope)
        if self.slope > 0:
            self.point1 = self.coord
            self.point2 = (self.coord[0]+tilesize/xcor,self.coord[1]+tilesize*ycor)
        else:
            self.point1 = (self.coord[0],self.coord[1]+tilesize*ycor)
            self.point2 = (self.coord[0]+tilesize/xcor,self.coord[1])
            
        if self.direction > 0:
            self.point3 = (self.point1[0],self.point2[1])
        else:
            self.point3 = (self.point2[0],self.point1[1])

        self.points = (self.point1,self.point2,self.point3)
        self.rect = pygame.Rect(self.coord,(tilesize/xcor,tilesize*ycor))

    def draw(self,win):
        pygame.draw.polygon(win, color[5], self.points)

player = pygame.Rect(0,0,20,20)
move = [0,0]
vision_show = False

enemies = []

tiles = {}
slopes = [Slope((90,150),1,1),Slope((90,210),-1,1),Slope((90,270),1,-1),Slope((90,330),-1,-1)]
Slopes = []
available = []
show_path = False
for i in range(0,screen[0],tilesize):
    for j in range(0,screen[1],tilesize):
        tile = (i//tilesize,j//tilesize)
        available.append(tile)
to_avail = available.copy()

def out_of_bound(current):
    x,y = current
    if x < 0 or x*tilesize >= screen[0] or y < 0 or y*tilesize >= screen[1]:
        return True

def pathfind(Start,tiles):
    to_search = {}
    search = []
    path_limit = 16
    searched = {}
    to_search[Start] = [0,None]
    search.append(Start)
    found = False
    new = Start
    while not found:        
        if to_search == {}:
            break
        else:
            current = search[0]
            for ad in adjacent:
                new = (current[0]+ad[0],current[1]+ad[1])
                if not out_of_bound(new) and new not in searched and new not in tiles:
                    gcost = to_search[current][0]+1
                    if gcost < path_limit:
                        if new not in search:
                            search.append(new)
                            to_search[new] = [gcost,current]
                        elif to_search[new][0] > gcost:
                            to_search[new] = [gcost,current]
            searched[current] = to_search[current][1]
            del to_search[current]
            search.remove(current)
    return searched
                        
                            
def move_entity(entity,end):
    x,y = entity.centerx,entity.centery
    endx,endy = end[0]*tilesize + tilesize/2,end[1]*tilesize + tilesize/2
    move = [0,0]
    if (x,y) != (endx,endy):
        if x > endx:
            move[0] -= 1
        elif x < endx:
            move[0] += 1
        if y > endy:
            move[1] -= 1
        elif y < endy:
            move[1] += 1
        a=Move(entity,move,tiles,slopes)
        X,Y = entity.centerx,entity.centery
        if (x,y) == (X,Y):
            return True
    else:
        return True

def spawn_enemy():    
    a = random.choice(available)
    enemies.append([a,pygame.Rect(a[0]*tilesize+5,a[1]*tilesize+5,20,20),random.choice(available),False])

def vision(test,tiles):
    def draw_shade(test,p1,p2,direction):
        pass
    for tile in tiles:
        tile = tiles[tile][0]
        m = slope_calc((test.centerx,test.centery),(tile.centerx,tile.centery))
        if m:
            if test.centerx < tile.left:
                poly = []
                a=[(tile.right,tile.top),(tile.right,tile.bottom)]
                poly = poly+a
                m = slope_calc((test.centerx,test.centery),(tile.right,tile.bottom))
                poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))
                m = slope_calc((test.centerx,test.centery),(tile.right,tile.top))
                poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))                    
                pygame.draw.polygon(win, color[0], poly)
                if test.centery < tile.bottom:
                    poly = []
                    poly.extend([(tile.left,tile.bottom),(tile.right,tile.bottom)])
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.bottom))
                    poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.bottom))
                    poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))                
                    pygame.draw.polygon(win, color[0], poly)
                if test.centery > tile.top:
                    poly = []
                    poly.extend([(tile.left,tile.top),(tile.right,tile.top)])
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.top))
                    poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.top))
                    poly.append((screen[0],(m*screen[0]-(m*test.centerx-test.centery))))                
                    pygame.draw.polygon(win, color[0], poly)

            elif test.centerx > tile.right:
                poly = []
                a=[(tile.left,tile.top),(tile.left,tile.bottom)]
                poly = poly+a
                m = slope_calc((test.centerx,test.centery),(tile.left,tile.bottom))
                poly.append((0,m*0-(m*test.centerx-test.centery)))
                m = slope_calc((test.centerx,test.centery),(tile.left,tile.top))
                poly.append((0,m*0-(m*test.centerx-test.centery)))                    
                pygame.draw.polygon(win, color[0], poly)
                if test.centery < tile.bottom:
                    poly = []
                    poly.extend([(tile.right,tile.bottom),(tile.left,tile.bottom)])
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.bottom))
                    poly.append((0,m*0-(m*test.centerx-test.centery)))
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.bottom))
                    poly.append((0,m*0-(m*test.centerx-test.centery)))                
                    pygame.draw.polygon(win, color[0], poly)
                if test.centery > tile.top:
                    poly = []
                    poly.extend([(tile.right,tile.top),(tile.left,tile.top)])
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.top))
                    poly.append((0,m*0-(m*test.centerx-test.centery)))
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.top))
                    poly.append((0,(m*0-(m*test.centerx-test.centery))))                
                    pygame.draw.polygon(win, color[0], poly)
                    
            else:
                if test.centerx > tile.left:
                    poly = []
                    poly.extend([(tile.left,tile.top),(tile.left,tile.bottom)])                   
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.bottom))
                    poly.append((0,m*0-(m*test.centerx-test.centery)))
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.top))
                    poly.append((0,m*0-(m*test.centerx-test.centery)))                    
                    pygame.draw.polygon(win, color[0], poly)
                if test.centerx < tile.right:
                    poly = []
                    a=[(tile.right,tile.top),(tile.right,tile.bottom)]
                    poly = poly+a
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.bottom))
                    poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.top))
                    poly.append((screen[0],m*screen[0]-(m*test.centerx-test.centery)))                    
                    pygame.draw.polygon(win, color[0], poly)
                
                if test.centery < tile.top:
                    poly = []
                    poly.extend([(tile.left,tile.bottom),(tile.right,tile.bottom)])                   
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.bottom))
                    if m:
                        poly.append((screen[0],screen[0]*m-(m*test.centerx-test.centery)))
                    else:
                        poly.append((test.centerx,screen[1]+screen[0]))
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.bottom))
                    if m:
                        poly.append((0,m*0-(m*test.centerx-test.centery)))
                    else:
                        poly.append((test.centerx,screen[1]+screen[0]))
                    
                    pygame.draw.polygon(win,color[0],poly)
                    
                else:
                    poly = []
                    poly.extend([(tile.left,tile.top),(tile.right,tile.top)])                   
                    m = slope_calc((test.centerx,test.centery),(tile.right,tile.top))
                    if m:
                        poly.append((screen[0],screen[0]*m-(m*test.centerx-test.centery)))
                    else:
                        poly.append((test.centerx,0))
                    m = slope_calc((test.centerx,test.centery),(tile.left,tile.top))
                    if m:
                        poly.append((0,m*0-(m*test.centerx-test.centery)))
                    else:
                        poly.append((test.centerx,0))
                    
                    pygame.draw.polygon(win,color[0],poly)
                    

def slope_calc(p1,p2):
    my = p1[1] - p2[1]
    mx = p1[0] - p2[0]
    if mx == 0:
        return False
    else:
        return (my/mx)

def age_tile(tiles):
    to_del = []
    for t in tiles:
        tiles[t][1] -= 0.1
        if tiles[t][1] <= -0:
            to_del.append(t)
    for i in to_del:
        del tiles[i]
    
def redraw():
    win.fill(color[7])

    if show_path:
        for i in path:
            pygame.draw.rect(win,color[4],(i[0]*tilesize,i[1]*tilesize,tilesize,tilesize))

    for i in range(0,screen[0],tilesize):
        pygame.draw.line(win,color[0],(i,0),(i,screen[1]))
    for j in range(0,screen[1],tilesize):
        pygame.draw.line(win,color[0],(0,j),(screen[0],j))

    for tile in tiles:
        pygame.draw.rect(win,color[5],tiles[tile][0])            
        
    for slope in slopes:
        slope.draw(win)
    
        
    pygame.draw.rect(win,color[1],player)

    for enemy in enemies:
        pygame.draw.rect(win, color[2], enemy[1])

    win.blit(font.render(str(player_tile),1,color[0]),(0,0))

def collision_test(test,tiles,slopes):
    hits = []
    for tile in tiles:
        tile = tiles[tile][0]
        if test.colliderect(tile):
            hits.append(tile)
    for slope in slopes:
        if test.colliderect(slope.rect):
            hits.append(slope)
    return hits

def collision_test_slope(test,slopes):
    hit_slopes = []
    for hit in slopes:
        if test.colliderect(hit.rect):
            hit_slopes.append(hit)
    return hit_slopes

def Move_slope(test,move,slopes):
    hits = collision_test_slope(test,slopes)
    for hit in hits:
        if move[0] > 0:            
            if hit.direction == -1:
                if hit.slope > 0 and test > hit.rect.top:
                    dif = test.top - hit.rect.top
                    if test.right > hit.rect.left + dif:
                        test.y += (test.right-(hit.rect.left + dif))/2
                        test.x -= (test.right-(hit.rect.left + dif))/2
                elif hit.slope < 0 and test.bottom < hit.rect.bottom:
                    dif = hit.rect.bottom - test.bottom
                    if hit.rect.left + dif < test.right:
                        test.y -= (test.right-(hit.rect.left + dif))/2
                        test.x -= (test.right-(hit.rect.left + dif))/2
            else:
                test.right = hit.rect.left   
def Move(test,move,tiles,slopes):    
    test.x += move[0]
    hits = collision_test(test,tiles,slopes)
    for hit in hits:
        if move[0] > 0:
            if type(hit) == Slope:
                if hit.direction == 1 and test.left < hit.rect.left:
                    test.right = hit.rect.left
                elif hit.direction == -1:
                    if hit.slope > 0 and test.top > hit.rect.top:
                        dif = test.top - hit.rect.top
                        if test.right > hit.rect.left + dif:
                            test.y += (test.right-(hit.rect.left + dif))/2
                            test.x -= (test.right-(hit.rect.left + dif))/2
                    elif hit.slope < 0 and test.bottom < hit.rect.bottom:
                        dif = hit.rect.bottom - test.bottom
                        if hit.rect.left + dif < test.right:
                            test.y -= (test.right-(hit.rect.left + dif))/2
                            test.x -= (test.right-(hit.rect.left + dif))/2
                    elif test.left < hit.rect.left:
                        test.right = hit.rect.left
            else:
                test.right = hit.left
        elif move[0] < 0:
            if type(hit) == Slope:
                if hit.direction == -1 and test.right > hit.rect.right:
                    test.right = hit.rect.left
                elif hit.direction == 1:
                    if hit.slope > 0 and test.bottom < hit.rect.bottom:
                        dif = test.bottom - hit.rect.bottom
                        if test.left < hit.rect.right + dif:
                            test.y -= ((hit.rect.right + dif)-test.left)/2
                            test.x += ((hit.rect.right + dif)-test.left)/2
                    elif hit.slope < 0 and test.top > hit.rect.top:
                        dif = hit.rect.top - test.top
                        if hit.rect.right + dif > test.left:
                            test.y += ((hit.rect.right + dif)-test.left)/2
                            test.x += ((hit.rect.right + dif)-test.left)/2
                    elif test.right > hit.rect.right:
                        test.left = hit.rect.right
            else:
                test.left = hit.right
                
    test.y += move[1]
    hits = collision_test(test,tiles,slopes)
    for hit in hits:
        if move[1] > 0:
            if type(hit) == Slope:
                if hit.slope > 0 and test.left > hit.rect.left and hit.direction == 1:
                    dif = test.left - hit.rect.left
                    if test.bottom > hit.rect.top + dif:
                        test.x += (test.bottom-(hit.rect.top + dif))/2
                        test.y -= (test.bottom-(hit.rect.top + dif))/2
                elif hit.slope < 0 and test.right < hit.rect.right and hit.direction == -1:
                    dif = hit.rect.right - test.right
                    if hit.rect.top + dif < test.bottom:
                        test.x -= (test.bottom-(hit.rect.top + dif))/2
                        test.y -= (test.bottom-(hit.rect.top + dif))/2
                elif test.top < hit.rect.top:
                    test.bottom = hit.rect.top
            else:
                test.bottom = hit.top
        elif move[1] < 0:
            if type(hit) == Slope:
                    if hit.slope > 0 and test.right < hit.rect.right and hit.direction == -1:
                        dif = test.right - hit.rect.right
                        if test.top < hit.rect.bottom + dif:
                            test.x -= ((hit.rect.bottom + dif)-test.top)/2
                            test.y += ((hit.rect.bottom + dif)-test.top)/2
                    elif hit.slope < 0 and test.left > hit.rect.left and hit.direction == 1:
                        dif = hit.rect.left - test.left
                        if hit.rect.bottom + dif > test.top:
                            test.x += ((hit.rect.bottom + dif)-test.top)/2
                            test.y += ((hit.rect.bottom + dif)-test.top)/2
                    elif test.bottom > hit.rect.bottom:
                        test.top = hit.rect.bottom
            else:
                test.top = hit.bottom
            
    if test.x < 0:
        test.x = 0
    elif test.right > screen[0]:
        test.right = screen[0]
    if test.y < 0:
        test.y = 0
    elif test.bottom > screen[1]:
        test.bottom = screen[1]

    return test,move

run = True
while run:

    keys = pygame.key.get_pressed()
    mpos = pygame.mouse.get_pos()
    player_tile = (player.centerx//tilesize,player.centery//tilesize)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                vision_show = not vision_show
            if event.key == K_LALT:
                print(enemies)
                print(path)
            if event.key == K_LCTRL:
                show_path = not show_path

        if event.type == MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            mpos_ = (mpos[0]//tilesize,mpos[1]//tilesize)
            tile = pygame.Rect(mpos_[0]*tilesize,mpos_[1]*tilesize,tilesize,tilesize)
            if event.button == 1:                
                if mpos_ not in tiles and mpos_ not in enemies:
                    tiles[mpos_] = [tile,100]
                    available.remove(mpos_)
            if event.button == 3:
                enemies = []
                for i in range(20):
                    spawn_enemy()

    if keys[K_UP]:
        move[1] -= 2
    if keys[K_DOWN]:
        move[1] += 2
    if keys[K_LEFT]:
        move[0] -= 2
    if keys[K_RIGHT]:
        move[0] += 2

    player,move = Move(player, move, tiles, slopes)
    move = [0,0]
    path = pathfind(player_tile,tiles)

    to_remove = []    
    for enemy in enemies:
        if player.colliderect(enemy[1]):
            to_remove.append(enemies.index(enemy))
        enemy[0] = (enemy[1].centerx//tilesize,enemy[1].centery//tilesize)
        if enemy[0] in path and path[enemy[0]]:
            if enemy[2] != path[enemy[0]]:
                enemy[2] = path[enemy[0]]
                enemy[3] = True
        if not enemy[3]:
            enemy[2] = random.choice(available)
            enemy[3] = True
        check = move_entity(enemy[1],enemy[2])
        if check:
            enemy[0] = (enemy[1].centerx//tilesize,enemy[1].centery//tilesize)
            enemy[3] = False

    for to in to_remove:
        enemies.pop(to)

    redraw()   
        
    if vision_show:
        vision(player, tiles)
    pygame.display.update()

    clock.tick(FPS)

pygame.quit()

import pygame, sys
#CLASSES
class Dot():
    pos = ()
    visited = False
    dir_open = []
    def __init__(self, pos_, visited_):
        self.pos = pos_
        self.visited = visited_
        for i in range(8):
            self.dir_open.append(0)

class Edge():
    A = () #point 1
    B = () #point 2
    #X = () #draw point 1
    #Y = () #draw point 2
    state = 1 #0 - None, 1 - empty, 2 - full
    def __init__(self, a, b):
        self.A = a
        self.B = b

#borderPoints = [
#    (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), 
#    (9, 1), (9, 2), (10, 2), (10, 3), (10, 4), (9, 4), (9, 5), 
#    (9, 6), (8, 6), (7, 6), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (1, 6),  
#    (1, 5), (1, 4), (0, 4), (0, 3), (0, 2), (1, 2), (1, 1), (1, 0)
#]
   #HELPER LISTS
borderPoints = [ 
    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), 
    (1, 9), (2, 9), (2, 10), (3, 10), (4, 10), (4, 9), (5, 9), 
    (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), 
    (5, 1), (4, 1), (4, 0), (3, 0), (2, 0), (2, 1), (1, 1), (0, 1)
]
H = [
    (0, 0), (1, 0), (5, 0), (6, 0), 
    (0, 10), (1, 10), (5, 10), (6, 10)
]
H2 = [
    ((2, 0), (1, 1)),
    ((4, 0), (5, 1)),
    ((1, 9), (2, 10)),
    ((5, 9), (4, 10))
]
dirs = [
    (-1, -1),   #0 = NW
    (0, -1),    #1 = N
    (1, -1),    #2 = NE
    (1, 0),     #3 = E
    (1, 1),     #4 = SE
    (0, 1),     #5 = S
    (-1, 1),    #6 = SW
    (-1, 0)     #7 = W
]
   #END HELPER LISTS
   #GENERATING BOARD - DOTS AND EDGES

board = []
edges = []
edgeI = dict()
k = 0
for j in range(11):
    board.append([])
for j in range(11):
    for i in range(7):
        if ((j == 0 or j == 10) and (i == 0 or i == 1 or i == 5 or i ==6)):
            board[j].append(Dot((-2, -2), None))
        else:
            for dd in dirs:
                if (edgeI.get(((i, j), (i+dd[0], j+dd[1]))) is None):
                    if((i+dd[0]>=0 and i+dd[0]<7) and (j+dd[1]>=0 and j+dd[1]<11)) and ((i+dd[0], j+dd[1]) not in H):
                        edges.append(Edge((i, j), (i+dd[0], j+dd[1])))
                        edgeI[((i, j), (i+dd[0], j+dd[1]))] = k
                        edgeI[((i+dd[0], j+dd[1]), (i, j))] = k
                        k+=1

            v = False
            if i ==3 and (j==1 or j==9):
                v = False
            elif i == 0 or i == 6:
                v = True
            elif j == 1 or j == 9 or j == 0 or j == 10:
                v = True
            board[j].append(Dot((i, j), v))
for i in range(len(borderPoints)-1):
    edges[edgeI[(borderPoints[i+1], borderPoints[i])]].state = 2
for e in H2:
    edges[edgeI[e]].state = 0

def distance2(A, B):
    x = A[0] - B[0]
    y = A[1] - B[1]
    return x*x + y*y

def dot_to_pixel(dot, center, cdot, wi):
    xwektor = dot[0] - cdot[0]
    ywektor = dot[1] - cdot[1]
    x = xwektor * wi + center[0]
    y = ywektor * wi + center[1]
    return x, y

def pixel_to_dot(pixel, center, cdot, wi):
    xwektor = (pixel[0]-center[0])//wi
    ywektor = (pixel[1]-center[1])//wi
    x = xwektor + cdot[0]
    y = ywektor + cdot[1]
    return x, y

def normalize(p):
    x, y = p[0], p[1]
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x >= 7:
        x = 6
    if y >= 11:
        y = 10
    return x, y

def goal(point):
    if point[1] == 0:
        return 0
    elif point[1] == 10:
        return 1
    else:
        return None


size = width, height = 600, 600
w = min(width//8, height//12)
CENTER = width//2, height//2
CENTER_DOT = (3, 5)

activeDot = aX, aY = CENTER_DOT
activePoint = aA, aB = CENTER

dots = []
vis = dict()
    

if __name__ == "__main__":
    """    ro = []
    for r in board:
        ro = []
        for d in r:
            if d is not None:                
                ro.append(d.visited)
        print(ro)"""

    pygame.init()
    size = width, height = 600, 600
    w = min(width//8, height//12)
    CENTER = width//2, height//2
    CENTER_DOT = (3, 5)

    activeDot = aX, aY = CENTER_DOT
    activePoint = aA, aB = CENTER
    
    MOUSE_RAD = 20
    mouseDot = mx, my = 0, 0
    
    screen = pygame.display.set_mode(size)

    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 100, 255)
    green = (0, 255, 50)
    red =   (255, 0, 0)
    grey =  (220, 220, 220)
    yellow = (255, 255, 150, 50)
    
    PLAYER = 0
    playerColors = [red, blue]

    SCORE = [0, 0]

    dots = []
    vis = dict()

    for row in board:    
        for dot in row:
            x, y = dot_to_pixel(dot.pos, CENTER, CENTER_DOT, w)
            dots.append((x, y))
            vis[(x, y)] = dot.visited

    while True:
        screen.fill(white)
        Mpos = Mx, My = pygame.mouse.get_pos()
        vis[activePoint] = True
        pygame.draw.rect(screen, playerColors[PLAYER], (0, 0, 80, height))
        pygame.draw.rect(screen, playerColors[PLAYER], (width, 0, -80, height))
        pygame.draw.rect(screen, black, (80, 0, width-160, w*3/4))
        pygame.draw.rect(screen, red, (width//2, 0, -50, w*3/4))
        pygame.draw.rect(screen, blue, (width//2, 0, 50, w*3/4))

        if goal(activeDot) is not None:
            SCORE[goal(activeDot)] += 1
            
            #reset
        font = pygame.font.SysFont("comicsansms", 36)
        txt = str(SCORE[0])+' : '+str(SCORE[1])
        text = font.render(txt, True, white)
        screen.blit(text,(width//2 - text.get_width() // 2, w*3//8 - text.get_height() // 2))
    

        for e in edges:
            if e.state == 1:
                pygame.draw.line(screen, grey, dot_to_pixel(e.A, CENTER, CENTER_DOT, w), dot_to_pixel(e.B, CENTER, CENTER_DOT, w), 1)
            if e.state == 2:
                pygame.draw.line(screen, black, dot_to_pixel(e.A, CENTER, CENTER_DOT, w), dot_to_pixel(e.B, CENTER, CENTER_DOT, w), 2)

        #for d in dots:
            #for i in range(8):
                #pygame.draw.line(screen, grey, d, (d[0]+dirs[i][0]*w, d[1]+dirs[i][1]*w), 1)
        pygame.draw.line(screen, black, activePoint, Mpos, 1)
        pygame.draw.circle(screen, green, activePoint, 4)
        for d in dots:
            if distance2(d, Mpos)<=MOUSE_RAD*MOUSE_RAD:
                pygame.draw.circle(screen, blue, d, 4)
                mouseDot = mx, my = normalize(pixel_to_dot(d, CENTER, CENTER_DOT, w))
            if vis[d]:
                pygame.draw.circle(screen, red, d, 2)
            else:
                pygame.draw.circle(screen, black, d, 2)
        
        pygame.draw.circle(screen, yellow, Mpos, 20, 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if (mouseDot, activeDot) in edgeI:
                    if (edges[edgeI[(mouseDot, activeDot)]].state == 1):
                        #print(mouseDot)
                        if(board[mouseDot[1]][mouseDot[0]].visited==False):
                            PLAYER = not PLAYER
                        edges[edgeI[(mouseDot, activeDot)]].state = 2
                        board[mouseDot[1]][mouseDot[0]].visited = True
                        board[activeDot[1]][activeDot[0]].visited = True

                        activeDot = aX, aY = normalize(mouseDot)
                        activePoint = aA, aB = dot_to_pixel(mouseDot, CENTER, CENTER_DOT, w)



#xwektor = dot.pos[0] - CENTER_DOT[0]
#ywektor = dot.pos[1] - CENTER_DOT[1]
#x = xwektor * w + CENTER[0]
#y = ywektor * w + CENTER[1]
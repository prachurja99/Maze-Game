from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

# # # # # # # # # # # # # # # # # # drawing algorithms # # # # # # # # # # # # # # # # # # #
def draw_pixel(x, y):
    glPointSize(1.3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
    
def MidpointCircle(xc, yc, r):
    d = 1 - r
    x = 0
    y = r
    Symm8way(xc, yc, x, y)
    while x < y:
        if d < 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * (x - y) + 5
            x += 1
            y -= 1
        Symm8way(xc, yc, x, y)

def Symm8way(xc, yc, x, y):
    draw_pixel(xc + x, yc + y)
    draw_pixel(xc - x, yc + y)
    draw_pixel(xc + x, yc - y)
    draw_pixel(xc - x, yc - y)
    draw_pixel(xc + y, yc + x)
    draw_pixel(xc - y, yc + x)
    draw_pixel(xc + y, yc - x)
    draw_pixel(xc - y, yc - x)


def draw_line_0(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    del_E = 2 * dy
    del_NE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    while x < x1:
        draw_org_zone(x, y, zone)
        if d < 0:
            d += del_E
            x += 1
        else:
            d += del_NE
            x += 1
            y += 1


def draw_org_zone(x, y, zone):
    if zone == 0:
        draw_pixel(x, y)
    if zone == 1:
        draw_pixel(y, x)
    if zone == 2:
        draw_pixel(-y, x)
    if zone == 3:
        draw_pixel(-x, y)
    if zone == 4:
        draw_pixel(-x, -y)
    if zone == 5:
        draw_pixel(-y, -x)
    if zone == 6:
        draw_pixel(y, -x)
    if zone == 7:
        draw_pixel(x, -y)


def MidpointLine(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            draw_line_0(x0, y0, x1, y1, 0)

        if dx >= 0 and dy < 0:
            draw_line_0(x0, -y0, x1, -y1, 7)

        if dx < 0 and dy >= 0:
            draw_line_0(-x0, y0, -x1, y1, 3)

        if dx < 0 and dy < 0:
            draw_line_0(-x0, -y0, -x1, -y1, 4)

    else:
        if dx >= 0 and dy >= 0:
            draw_line_0(y0, x0, y1, x1, 1)

        if dx >= 0 and dy < 0:
            draw_line_0(-y0, x0, -y1, x1, 6)

        if dx < 0 and dy >= 0:
            draw_line_0(y0, -x0, y1, -x1, 2)

        if dx < 0 and dy < 0:
            draw_line_0(-y0, -x0, -y1, -x1, 5)


# # # # # # # # # # # # # # # # # # # # END # # # # # # # # # # # # # # # # # # # # #
maze_width = 10 
maze_height = 13  
cell_size = 50 

brick = []
brick_dict = {}

tool_flag = 0  # 0 for drill, 1 for hammer

player_pos = [1, 3]  # in terms of cell coordinates
player_r, enemy_r = 15, 15 #player radius, enemy radius
bullet_r = 5  # bullet radius
bullets = []
total_lives = 3

total_time = 45
remaining_time = total_time
prev_time = time.time()

gold_score=0 #Tracks the total collected gold
score = 0 #ttal player score
game_over = False
pause = False

maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # maze layout
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # divides the screen into grids
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1],  # 0 for empty space, 1 for walls
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
# # # # # # # # # # # # # # # # # #Drawing functions# # # # # # # # # # # # # # # # # # #

def draw_back_arrow():
    glColor3f(0.0, 0.9, 1)
    MidpointLine(10, 40, 50, 40)
    MidpointLine(30, 60, 10, 40)
    MidpointLine(30, 20, 10, 40)

def score_display(sc):
    glPointSize(30)
    glColor3f(1.0, 0.65, 0.0039)
    glBegin(GL_POINTS)
    glVertex2f(80, 45)
    glEnd()
    glPointSize(15)
    glColor3f(0.8, 0.8, 0.8)
    glBegin(GL_POINTS)
    glVertex2f(80, 45)
    glEnd()

    glPointSize(3)
    glColor3f(1.0, 1.0, 1.0)
    MidpointLine(100,45,90,45)
    if len(sc) == 1:
        sc = '0' + sc
    for i in range(len(sc)):
        if i == 0:
            s1, s2, p1, p2, p3 = 130, 110, 60, 30, 45
        else:
            s1, s2, p1, p2, p3 = 160, 140, 60, 30, 45

        if sc[i] == '0':
            MidpointLine(s2, p1, s1, p1)
            MidpointLine(s2, p1, s2, p2)
            MidpointLine(s2, p2, s1, p2)
            MidpointLine(s1, p1, s1, p2)

        elif sc[i] == '1':
            MidpointLine(s1, p1, s1, p2)

        elif sc[i] == '2':
            MidpointLine(s1, p1, s2, p1)
            MidpointLine(s1, p3, s1, p2)
            MidpointLine(s2, p3, s1, p3)
            MidpointLine(s1, p2, s2, p2)
            MidpointLine(s2, p1, s2, p3)

        elif sc[i] == '3':
            MidpointLine(s2, p1, s1, p1)
            MidpointLine(s1, p1, s1, p2)
            MidpointLine(s1, p3, s2, p3)
            MidpointLine(s2, p2, s1, p2)


        elif sc[i] == '4':
            MidpointLine(s1, p2, s1, p1)
            MidpointLine(s2, p3, s2, p2)
            MidpointLine(s2, p3, s1, p3)

        elif sc[i] == '5':

            MidpointLine(s2, p1, s1, p1)
            MidpointLine(s1, p1, s1, p3)
            MidpointLine(s1, p3, s2, p3)
            MidpointLine(s2, p2, s1, p2)
            MidpointLine(s2, p3, s2, p2)

        elif sc[i] == '6':
            MidpointLine(s2, p1, s1, p1)
            MidpointLine(s1, p1, s1, p3)
            MidpointLine(s1, p3, s2, p3)
            MidpointLine(s2, p2, s1, p2)
            MidpointLine(s2, p3, s2, p2)
            MidpointLine(s2, p2, s2, p1)

        elif sc[i] == '7':
            MidpointLine(s2, p2, s1, p2)
            MidpointLine(s1, p2, s2, p1)
        elif sc[i]=='8':
            MidpointLine(s2, p1, s1, p1)
            MidpointLine(s2, p1, s2, p2)
            MidpointLine(s2, p2, s1, p2)
            MidpointLine(s1, p1, s1, p2)
            MidpointLine(s1, p3, s2, p3)
        elif sc[i]=='9':
            MidpointLine(s2, p1, s1, p1)
            MidpointLine(s1, p1, s1, p2)
            MidpointLine(s1, p3, s2, p3)
            MidpointLine(s2, p2, s1, p2)
            MidpointLine(s2, p3, s2, p2)

def draw_pause():
    glColor3f(1, 0.7, 0.9)

    MidpointLine(243, 20, 243, 60)
    MidpointLine(257, 20, 257, 60)


def draw_play():
    glColor3f(1, 0.7, 0.9)
    MidpointLine(235, 20, 235, 60)
    MidpointLine(235, 60, 265, 40)
    MidpointLine(265, 40, 235, 20)
    
def life_display(sc):
    glPointSize(30)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POINTS)
    glVertex2f(325, 45)
    glEnd()

    glPointSize(3)
    glColor3f(1.0, 1.0, 1.0)

    MidpointLine(340,45,350,45)

    s1, s2, p1, p2, p3 = 380, 360, 60, 30, 45

    if sc == '0':
        MidpointLine(s2, p1, s1, p1)
        MidpointLine(s2, p1, s2, p2)
        MidpointLine(s2, p2, s1, p2)
        MidpointLine(s1, p1, s1, p2)

    elif sc == '1':
        MidpointLine(s1, p1, s1, p2)


    elif sc == '2':
        MidpointLine(s1, p1, s2, p1)
        MidpointLine(s1, p3, s1, p2)
        MidpointLine(s2, p3, s1, p3)
        MidpointLine(s1, p2, s2, p2)
        MidpointLine(s2, p1, s2, p3)

    elif sc == '3':
        MidpointLine(s2, p1, s1, p1)
        MidpointLine(s1, p1, s1, p2)
        MidpointLine(s1, p3, s2, p3)
        MidpointLine(s2, p2, s1, p2)

def draw_cross():
    glColor3f(1, 0.0, 0.0)
    MidpointLine(450, 20, 490, 60)
    MidpointLine(450, 60, 490, 20)
    
# # # # # # # # # # # # # # #Character  design# # # # # # # # # # # # # # # # # #
def draw_drill(x, y):
    glColor3f(0.3, 0.9, 0.7)  # Drill color
    MidpointLine(x - 10, y - 5, x + 10, y - 5)
    MidpointLine(x + 10, y - 5, x + 10, y + 5)
    MidpointLine(x + 10, y + 5, x - 10, y + 5)
    MidpointLine(x - 10, y + 5, x - 10, y - 5)
    MidpointLine(x - 5, y + 5, x, y + 15)
    MidpointLine(x, y + 15, x + 5, y + 5)
    MidpointLine(x + 5, y + 5, x - 5, y + 5)

def draw_hammer(x, y):
    glColor3f(0.6, 0.3, 0.1)  # Handle color
    MidpointLine(x - 2, y - 20, x + 2, y - 20)
    MidpointLine(x + 2, y - 20, x + 2, y + 10)
    MidpointLine(x + 2, y + 10, x - 2, y + 10)
    MidpointLine(x - 2, y + 10, x - 2, y - 20)
    glColor3f(0.7, 0.7, 0.7)  # Head color
    MidpointLine(x - 10, y + 10, x + 10, y + 10)
    MidpointLine(x + 10, y + 10, x + 10, y + 15)
    MidpointLine(x + 10, y + 15, x - 10, y + 15)
    MidpointLine(x - 10, y + 15, x - 10, y + 10)
    
def draw_player():
    global player_pos, tool_flag, cell_size
    # Calculating the player's center position
    x = player_pos[0] * cell_size + cell_size // 2
    y = player_pos[1] * cell_size + cell_size // 2

    if tool_flag == 0:  # Drill state
        draw_drill(x, y)
    else:  # Hammer state
        draw_hammer(x, y)

# # # # # # # # # # # # # # #Terrain design# # # # # # # # # # # # # # # # # #
    
def draw_maze():
    for i in range(maze_height):
        for j in range(maze_width):
            if maze[i][j] == 1:
                glColor3f(1, 1, 1)  # white color for walls

                x = j * cell_size  # (x, y) is top left corner pixel for each block
                y = i * cell_size

                MidpointLine(x, y, x + cell_size, y)
                MidpointLine(x + cell_size, y, x + cell_size, y + cell_size)
                MidpointLine(x + cell_size, y + cell_size, x, y + cell_size)
                MidpointLine(x, y + cell_size, x, y)
                


def get_random_e_pos():
    random_pos = []

    while len(random_pos) < 5:  # 5 enemies in each game
        x = random.randint(2, maze_width - 1)
        y = random.randint(3, maze_height - 1)

        if maze[y][x] == 0:  # checking for empty position
            temp_pos = [x, y]
            random_pos.append(temp_pos)

    return random_pos


def get_random_g_pos():
    random_pos2 = []

    while len(random_pos2) < 7:  #7 hidden gold to win the game
        x = random.randint(2, maze_width - 1)
        y = random.randint(3, maze_height - 1)

        if maze[y][x] == 0:  # checking for empty position
            temp_pos = [x, y]
            random_pos2.append(temp_pos)

    return random_pos2

enemy_pos = get_random_e_pos()
gold_pos = get_random_g_pos()

def brick_create():
    global brick, brick_dict
    brick = []
    brick_dict = {}
    r = 0

    def add_brick(x, y):
        if (x,y) not in brick_dict:
            temp = [[x, y], [x, y + 50], [x + 50, y + 50], [x + 50, y]]
            brick_dict[(x,y)] = r
            brick.append(temp)

    for pos in enemy_pos + gold_pos: #creating bricks around enemies and gold
        x, y = pos[0] * cell_size, pos[1] * cell_size
        add_brick(x, y)

brick_create()



def brick_display():
    for brick_pos in brick:
        if brick_pos is not None:
            x, y = brick_pos[0][0], brick_pos[0][1]
            cell_x, cell_y = x // cell_size, y // cell_size

            if [cell_x, cell_y] in gold_pos:
                    glColor3f(0.7, 0.298, 0.0)  # Brick color
                    
                    MidpointLine(brick_pos[0][0], brick_pos[0][1], brick_pos[1][0], brick_pos[1][1])
                    MidpointLine(brick_pos[1][0], brick_pos[1][1], brick_pos[2][0], brick_pos[2][1])
                    MidpointLine(brick_pos[2][0], brick_pos[2][1], brick_pos[3][0], brick_pos[3][1])
                    MidpointLine(brick_pos[3][0], brick_pos[3][1], brick_pos[0][0], brick_pos[0][1])
            else:
                continue   #the brick disappears when the gold is collected


def draw_enemy():
    global enemy_pos, enemy_r, cell_size
    glColor3f(1.0, 0.0, 0.0)  # red color

    adjustment = enemy_r + 10

    for position in enemy_pos:
        x = position[0] * cell_size + adjustment
        y = position[1] * cell_size + adjustment
        MidpointCircle(x, y, enemy_r)


def draw_hidden_gold():
    glColor3f(1.0, 0.84, 0.0)  # Gold color
    adjustment = player_r + 10
    for position in gold_pos:
        x = position[0] * cell_size + adjustment
        y = position[1] * cell_size + adjustment

        # Drawing a simple square for gold
        MidpointLine(x - 5, y - 5, x + 5, y - 5)
        MidpointLine(x + 5, y - 5, x + 5, y + 5)
        MidpointLine(x + 5, y + 5, x - 5, y + 5)
        MidpointLine(x - 5, y + 5, x - 5, y - 5)

############   Timer and Game Over       ####################

def show_timer():
    timer_text = f"Time remaining: {int(remaining_time)} seconds"
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(115, 80)  # setting the text position
    for char in timer_text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

def show_game_over():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(200, 300)  # Center the text on the screen
    game_over_text = "GAME OVER"
    for char in game_over_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    glutSwapBuffers()

def update_timer(val):
    global pause, prev_time, remaining_time, game_over

    current_time = time.time()
    elapsed_time = current_time - prev_time
    prev_time = current_time

    
    if not pause:
        remaining_time -= elapsed_time

        
        if remaining_time <= 0:
            print("Time is up!")
            game_over = True
            pause = True
            print(f"Game Over! Score: {score}")

    glutTimerFunc(1000, update_timer, 0)
    glutPostRedisplay()


# # # # # # # # # # # Controls and Game Logic # # # # # # # # #
def special_key_listener(key, x, y):  # player controls
    global pause

    if pause is False:
        global player_pos

        next_pos = player_pos.copy()
        if key == GLUT_KEY_UP:
            next_pos[1] -= 1
        elif key == GLUT_KEY_DOWN:
            next_pos[1] += 1
        elif key == GLUT_KEY_LEFT:
            next_pos[0] -= 1
        elif key == GLUT_KEY_RIGHT:
            next_pos[0] += 1

        if (0 <= next_pos[0] < maze_width) and (0 <= next_pos[1] < maze_height):  # maze boundary check
            if maze[next_pos[1]][next_pos[0]] == 0:  # wall check
                player_pos = next_pos
                

        glutPostRedisplay()




def mouse_listener(button, state, x, y):
    global pause, game_over, score, player_pos, enemy_pos, bullets,tool_flag,maze,gold_pos, prev_time, remaining_time, total_time, total_lives
    

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:

            # pause icon
            if not game_over:
                if (360 < x < 400) and (0 < y < 60):
                    pause = not pause

            # back icon
            if (0 < x < 60) and (0 < y < 60):
                tool_flag=0
                player_pos = [1, 3]  # in terms of cell coordinates
                bullets = []
                maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # maze layout
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # divides the screen into grids
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1],  # 0 for empty space, 1 for walls
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
                draw_maze()
                total_time = 45
                prev_time = time.time()
                remaining_time = total_time
                total_lives = 3

                enemy_pos = get_random_e_pos()
                gold_pos = get_random_g_pos()

                score = 0
                
            
                
                brick_create()
                brick_display()
                draw_hidden_gold()
                pause = False
                game_over = False
                display()
                print("Starting over!")
                

            # cross icon
            if (740 < x < 800) and (0 < y < 60):
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()


def animate():
    global pause

    if not pause:
        global enemy_pos, bullets, game_over, gold_pos, total_lives

        bullets_to_remove = []

        for bullet in bullets:
            check_pos = bullet.update()
            if check_pos is True:
                bullets_to_remove.append(bullet)

        for bullet in bullets_to_remove:
            bullets.remove(bullet)

        enemy_collision = check_collisions()
        if enemy_collision:
            total_lives -= 1
            print(f"Lost a life! {total_lives} remaining")

            if total_lives <= 0:
                game_over = True
                print(f"Game Over! Score: {score}")
                bullets = []
                enemy_pos = []
                gold_pos = []
                pause = True

        glutPostRedisplay()

    if game_over:
        show_game_over()


# # # # # # # Scoring System # # # # # # # #

def keyboard_listener(key, x, y):  # to create bullet and set shooting direction
    global pause,tool_flag,player_pos, bullet_r, score

    if pause is False:
        if key == b't':  # Press 't' to toggle tools
            tool_flag = 1 - tool_flag
            print("Switched Tool:", "Drill" if tool_flag == 0 else "Hammer")


        pos_adjust = player_r + 10

        x0 = player_pos[0] * cell_size + pos_adjust
        y0 = player_pos[1] * cell_size + pos_adjust

        if tool_flag == 0:
            if key == b'w' or key == b'W':  # up
                new_bullet = Bullet([x0, y0 - 20], [0, -10])
                bullets.append(new_bullet)

            elif key == b's' or key == b'S':  # down
                new_bullet = Bullet([x0, y0 + 20], [0, 10])
                bullets.append(new_bullet)

            elif key == b'a' or key == b'A':  # left
                new_bullet = Bullet([x0 - 20, y0], [-10, 0])
                bullets.append(new_bullet)

            elif key == b'd' or key == b'D':  # right
                new_bullet = Bullet([x0 + 20, y0], [10, 0])
                bullets.append(new_bullet)

        glutPostRedisplay()


class Bullet:
    def __init__(self, pos, velocity, r=bullet_r):
        self.pos = pos
        self.velocity = velocity
        self.r = r

    def update(self):
        self.pos[0] += self.velocity[0]  # updating bullet position
        self.pos[1] += self.velocity[1]

        cell_x = int(self.pos[0] / cell_size)  # find cell coordinates based on bullet pos
        cell_y = int(self.pos[1] / cell_size)

        if (0 <= cell_x < maze_width) and (0 <= cell_y < maze_height):  # boundary check
            if maze[cell_y][cell_x] == 1:  # means bullet-wall collision
                return True  # collision

        return False  # no collision

    def draw(self):
        x = self.pos[0]
        y = self.pos[1]
        r = self.r
        MidpointCircle(x, y, r)


def check_collisions():
    global tool_flag, gold_pos, enemy_pos, score, bullets, enemy_r, player_pos,game_over, pause, total_lives, brick, brick_dict, remaining_time, gold_score


    bullets_to_remove = []
    enemies_to_remove = []
    golds_to_remove = []
    enemy_collision = False

    adjustment = player_r + 10  # Offset to align positions
    player_x = player_pos[0] * cell_size + adjustment
    player_y = player_pos[1] * cell_size + adjustment

    # Check collisions with golds 
    
    
    for gold in gold_pos:
        gold_x = gold[0] * cell_size + adjustment
        gold_y = gold[1] * cell_size + adjustment

        if tool_flag == 1:  # Gold only collected in hammer state
            # Checking if player overlaps with gold
            if abs(player_x - gold_x) <= player_r and abs(player_y - gold_y) <= player_r:
                golds_to_remove.append(gold)
                score += 5 
                gold_score+=5# Award points for collecting gold
                print(f"Gold collected! Score: {score}")

                # Ensuring time bonus can be awarded repeatedly if score thresholds are met
                if score % 30 == 0:
                    remaining_time += 10
                    print(f"Time bonus! 10 seconds added. New time: {remaining_time} seconds")

    for gold in golds_to_remove:
        gold_pos.remove(gold)
        if len(gold_pos) == 0:
            game_over = True
            pause = True
            print(f"No gold left. Game Over! Score: {score}")
            if gold_score==35:
                print("All gold collected! You win!")

    # Checking collisions with enemies
    for enemy in enemy_pos:
        enemy_x = enemy[0] * cell_size + adjustment
        enemy_y = enemy[1] * cell_size + adjustment

        # Distance between player and enemy (for player collision)
        player_dist = ((player_x - enemy_x) ** 2 + (player_y - enemy_y) ** 2) ** 0.5
        if player_dist <= player_r + enemy_r:
            enemies_to_remove.append(enemy)
            if tool_flag == 1:
                enemy_collision = True
            else:
                enemy_collision = False
                
        for bullet in bullets:
            bullet_x, bullet_y = bullet.pos

            if abs(bullet_x - enemy_x) <= enemy_r and abs(bullet_y - enemy_y) <= enemy_r:
                enemies_to_remove.append(enemy)
                bullets_to_remove.append(bullet)
                score += 10  # Award points for defeating an enemy
                print(f"Enemy defeated! Score: {score}")
                if score % 30 == 0:
                    remaining_time += 10
                    print(f"Time bonus! 10 seconds added. New time: {remaining_time} seconds")

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    
    for enemy in enemies_to_remove:
        if tool_flag == 0:
            # Drill logic
            if enemy in enemy_pos:
                enemy_pos.remove(enemy)
                
        if tool_flag == 1:  # Hammer logic (Bomb effect)
            if enemy in enemy_pos:
                enemy_pos.remove(enemy)
                print("Bomb effect triggered!")

                # Bomb effect: Clears nearby bricks and walls
                enemy_cell_x, enemy_cell_y = enemy
                affected_cells = [
                    (enemy_cell_x - 1, enemy_cell_y), (enemy_cell_x + 1, enemy_cell_y),
                    (enemy_cell_x, enemy_cell_y - 1), (enemy_cell_x, enemy_cell_y + 1),
                    (enemy_cell_x - 1, enemy_cell_y - 1), (enemy_cell_x + 1, enemy_cell_y + 1),
                    (enemy_cell_x - 1, enemy_cell_y + 1), (enemy_cell_x + 1, enemy_cell_y - 1)
                ]

                for cell in affected_cells:
                    print(cell)
                    print(gold_pos)
                    for gold in gold_pos:
                        if list(cell) == gold:
                            golds_to_remove.append(gold)
                            gold_pos.remove(gold)
                    if 0 <= cell[0] < maze_width and 0 <= cell[1] < maze_height:
                        if cell[0] != 0 and cell[0] != maze_width - 1 and cell[1] != 0 and cell[1] != maze_height - 1 and cell[1] != 2: #protecting outer walls
                            maze[cell[1]][cell[0]] = 0

    return enemy_collision

    

# # # # # # Function calls and GL setup # # # # # # # 

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_maze()
    show_timer()
    draw_cross()
    draw_back_arrow()
    brick_display()
    draw_hidden_gold()
    life_display(str(total_lives))
    score_display(str(score))

    if pause is True:
        draw_play()
    else:
        draw_pause()


    if game_over is False:
        draw_player()
    for bullet in bullets:
        bullet.draw()
    draw_enemy()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(800, 800)
glutCreateWindow(b"Beat the Maze!")
glClearColor(0, 0, 0, 1)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, maze_width * cell_size, maze_height * cell_size, 0, -1, 1)

glutTimerFunc(1000, update_timer, 0)  # update every second

glutDisplayFunc(display)
glutSpecialFunc(special_key_listener)
glutKeyboardFunc(keyboard_listener)
glutMouseFunc(mouse_listener)
glutIdleFunc(animate)
glutMainLoop()
import pygame
import random
import os

# Initialize Pygame
pygame.init()

##VARIABLES
# Window dimensions
WIDTH = 800
HEIGHT = 400

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# Load images
dino_img = []
dino_img.append(pygame.image.load('assets/dino_stand_94x94.png').convert_alpha())  #0 stand
dino_img.append(pygame.image.load('assets/dino_blink_94x94.png').convert_alpha())  #1 blink
dino_img.append(pygame.image.load('assets/dino_run_left_94x94.png').convert_alpha())  #2 run L
dino_img.append(pygame.image.load('assets/dino_run_right_94x94.png').convert_alpha())  #3 run R
dino_img.append(pygame.image.load('assets/dino_crouch_left_120x99.png').convert_alpha())  #4 crouch run L
dino_img.append(pygame.image.load('assets/dino_crouch_right_120x99.png').convert_alpha())  #5 crouch run R
current_dino_img = dino_img[1]

cloud_img = pygame.image.load('assets/cloud_92x92.png').convert_alpha()
ground_img = pygame.image.load('assets/ground_2437x25.png').convert_alpha()

dinobird_img = []
dinobird_img.append(pygame.image.load('assets/dinobird_fly_down_92x92.png').convert_alpha()) #flydown
dinobird_img.append(pygame.image.load('assets/dinobird_fly_up_92x92.png').convert_alpha()) #flyup

cactus_img = pygame.image.load('assets/cactus_50x100_1.png').convert_alpha()
groundcactus_img = pygame.image.load('assets/cactussmall_34x70_1.png').convert_alpha()
# Dinosaur properties
dino_width = 92
dino_height = 92
dino_x = 50
dino_y = HEIGHT - dino_height - 56
dino_vel_y = 0
dino_hitbox_width = 45
dino_hitbox_height = 40
dino_frame = 0
dino_crouch = 0
dino_crouch_time = 0
gravity = 1

# Dinobird properties
dinobirds = []#contains x, y, vel x, frame
dinobird_width = 92
dinobird_height = 92
dinobird_hitbox_width = 92
dinobird_hitbox_height = 42


### NEED TO MAKE SYSTEM FOR ALL THINGS TO SPAWN RANDOMLY
# Cactus properties
cacti = []#contains x, y, vel x, variant
cactus_width = 32
cactus_height = 50

# Cloud properties
clouds = []#contains x, y, star variant
cloud_width = cloud_img.get_width()
cloud_height = cloud_img.get_height()
cloud_vel_x = -2.5

# GroundCactus properties
groundcacti = []#contains x, y, variant(1-6), speed variant+-1-2
groundcactus_width = 34
groundcactus_height = 70
groundcactus_size = (19,45)

# Ground properties
ground_x = 0
ground_vel_x = -5
ground_y = -50
ground_width = (ground_img.get_width() - 40)

# Game
cactus_spawn_time = 120  # Initial time between cactus spawns
cloud_spawn_time = 100
groundcactus_spawn_time = 80
dinobird_spawn_time = 1200 #400

# Colors
WHITE = (247, 247, 247)
BLACK = (83, 83, 83)
day_color = (247, 247, 247)
night_color = (0, 0, 0)
transition_delay =  1800  # ticks
transition_duration = 180 # ticks 3 seconds
day_duration = 600 # t 10 
day_tracker = 600 # 10
is_day = 1 #day is 1, night is 0

game_time = 0 # ticks
score = 0
font = pygame.font.Font(None, 36)
game_over = False
start_screen = True
difficulty = 0
clock = pygame.time.Clock()
ignore_collision = 0
time = 0

## FUNCTIONS
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def daylight_cycle():
    global WHITE, BLACK
    global day_color, night_color, transition_duration, day_duration, day_tracker, is_day

    if game_time > transition_delay and not game_over:
        #start cycle
        if is_day == 1:
            day_tracker += 1
        if is_day == 0:
            day_tracker -= 1

        if day_tracker > (day_duration + transition_duration):
            is_day = 0
            
            progress = ((day_tracker - day_duration) / transition_duration)

            # Interpolate the RGB values between day_color and night_color
            red = clamp((int((night_color[0] - day_color[0]) * progress + day_color[0])), 0, 255)
            green = clamp((int((night_color[1] - day_color[1]) * progress + day_color[1])), 0, 255)
            blue = clamp((int((night_color[2] - day_color[2]) * progress + day_color[2])), 0, 255)

            WHITE = (red, green, blue)
            BLACK = (255 - red, 255 - green, 255 - blue)
        # else:
        #     WHITE = night_color
        #     BLACK = (255 - night_color[0], 255 - night_color[1], 255 - night_color[2])     
        if day_tracker < 1:
            is_day = 1

            progress = (day_tracker / transition_duration)

            # Interpolate the RGB values between day_color and night_color
            red = clamp((int((day_color[0] - night_color[0]) * progress + night_color[0])), 0, 255)
            green = clamp((int((day_color[1] - night_color[1]) * progress + night_color[1])), 0, 255)
            blue = clamp((int((day_color[2] - night_color[2]) * progress + night_color[2])), 0, 255)

            BLACK = (red, green, blue)
            WHITE = (255 - red, 255 - green, 255 - blue)
        # else:
        #     BLACK = night_color
        #     WHITE = (255 - night_color[0], 255 - night_color[1], 255 - night_color[2])        
    window.fill(WHITE)

def difficultyround():
    # print(str(input)+"  "+str(round((input*((difficulty/100)+1))+input)))
    # return round((input*((difficulty/100)+1))-input)*100
    return (difficulty/100)


def display_score():
    score_text = font.render(("Score: " + str(score)), True, BLACK)
    window.blit(score_text, (10, 10))

    score_text = font.render("Time: " + str(time), True, BLACK)
    window.blit(score_text, (10, 40))


def game_over_screen():
    game_over_text = font.render("Game Over", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(game_over_text, game_over_rect)


def start_game_screen():
    window.fill(BLACK)
    start_text = font.render("Press Space to Start", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(start_text, start_rect)

def spawn_cactus():
    global cacti, cactus_spawn_time, difficulty

    variant = (random.randint(1, 6))

    cactus_x = WIDTH + 20
    cactus_y = HEIGHT - cactus_height - 50
    cactus_vel_x = -5

    cacti.append((cactus_x, cactus_y,cactus_vel_x,variant))

    cactus_spawn_time = int(cactus_spawn_time * 0.95)

def spawn_dinobird():
    global dinobirds, dinobird_spawn_time, difficulty

    dinobird_x = WIDTH + 20
    dinobird_y = HEIGHT - dinobird_height - 50
    dinobird_vel_x = -5
    dinobird_frame = 0
    dinobirds.append((dinobird_x, dinobird_y,dinobird_vel_x,dinobird_frame))

    dinobird_spawn_time = int(dinobird_spawn_time * 0.95)

# Remove the previous definition of spawn_dinobird function
def check_spawn():
    if len(cacti) > 0:
        cactus_x,_,_,_ = cacti[-1]
        if not (cactus_x + (cactus_width/2)) < WIDTH - 30:
            return False

    if len(dinobirds) > 0:
        dinobird_x,_,_,_ = dinobirds[-1]
        if not (dinobird_x + (dinobird_hitbox_width/2)) < WIDTH - 30:
            return False

    return True

def spawn_groundcactus():
    global groundcacti, difficulty

    variant = random.randint(1, 6)
    speedvariant = 1
    groundcactus_x = WIDTH + 20
    groundcactus_y = HEIGHT - groundcactus_height + random.randint(-10,40)
    groundcactus_vel_x = (-5 -(speedvariant/2))

    groundcacti.append((groundcactus_x, groundcactus_y,variant,groundcactus_vel_x))


def spawn_cloud():
    cloud_x = WIDTH
    cloud_y = random.randint(20, 100)
    star_variant = random.randint(1, 9)
    clouds.append((cloud_x, cloud_y, star_variant))


def remove_cactus(index):
    del cacti[index]

def remove_cloud(index):
    del clouds[index]

def remove_groundcactus(index):
    del groundcacti[index]

def remove_dinobird(index):
    del dinobirds[index]

def update_dino_img():
    global dino_frame
    global current_dino_img
    global dino_crouch
    
    if running and is_active and not game_over:
        dino_frame += 1
        if dino_crouch == 1:
            if dino_frame < 5:
                current_dino_img = dino_img[4]  # crouch run left
            elif dino_frame < 10:
                current_dino_img = dino_img[5]  # crouch run right
            else:
                dino_frame = 0  # Reset the frame counter
        else:
            if dino_frame < 5:
                current_dino_img = dino_img[2]  # run left
            elif dino_frame < 10:
                current_dino_img = dino_img[3]  # run right
            elif dino_frame == 10:
                dino_frame = 0  # Reset the frame counter
    else:
        current_dino_img = dino_img[0]  # stand


def update_dinobird_img():
    global dinobirds
    
    for i, dinobird in enumerate(dinobirds):
        dinobird_x,dinobird_y,_,dinobird_frame = dinobird
        if not game_over:
            dinobird_frame += 1

        current_dinobird_img = dinobird_img[0]
        if dinobird_frame < 5:
            current_dinobird_img = dinobird_img[0]  # flydown
        elif dinobird_frame < 25:
            current_dinobird_img = dinobird_img[1]  # flyup
        if dinobird_frame == 25:
            dinobird_frame = 0  # Reset the frame counter
        window.blit(current_dinobird_img, (dinobird_x, dinobird_y))
        dinobirds[i] = (dinobird_x,dinobird_y,_,dinobird_frame)


def check_collision():

    if ignore_collision == 1:
        return False
    dino_hitbox = pygame.Rect(dino_x + (dino_width - dino_hitbox_width) // 2,
                              dino_y + (dino_height - dino_hitbox_height) // 2,
                              dino_hitbox_width,
                              dino_hitbox_height)
    cactusresult = False
    dinobirdresult = False
    for cactus in cacti:
        cactus_x, cactus_y,cactus_vel_x,variant = cactus

        cactus_hitbox = pygame.Rect(cactus_x, cactus_y, cactus_width, cactus_height)
        if dino_hitbox.colliderect(cactus_hitbox) == False:
            cactusresult = False
            # didnt hit cactus
        else:
            cactusresult = True
            break
    for dinobird in dinobirds:
        dinobird_x,dinobird_y,dinobird_vel_x,_ = dinobird

        dinobird_hitbox = pygame.Rect(dinobird_x, dinobird_y, dinobird_hitbox_width, dinobird_hitbox_height)
        if dino_hitbox.colliderect(dinobird_hitbox) == False:
                # didnt hit bird
            dinobirdresult = False
        else:
            dinobirdresult = True
            break
    if cactusresult == False and dinobirdresult == False:
        return False
    else:
        return True

def game_run():
    # Game loop
    global WHITE
    global BLACK
    global transition_delay
    global transition_duration
    global day_duration
    global day_tracker
    global is_day
    global game_time
    global clock
    global running
    global is_active
    global difficulty
    global window
    global start_screen
    global game_over
    global score
    global font
    global game_time
    global ignore_collision

    global dino_x
    global dino_y
    global dino_vel_y
    global dino_crouch
    global time

    global cacti
    global groundcacti
    global dinobirds

    global clouds
    global cloud_width
    global cloud_height
    global cloud_vel_x
    global cloud_spawn_time
    global cactus_spawn_time
    global groundcactus_spawn_time
    global dinobird_spawn_time

    global ground_x
    global ground_vel_x

    #reset global var
    cactus_spawn_time = 120  # Initial time between cactus spawns
    cloud_spawn_time = 100
    groundcactus_spawn_time = 80
    dinobird_spawn_time = 1200 #400

    # Colors
    WHITE = (247, 247, 247)
    BLACK = (83, 83, 83)

    transition_delay =  1800  # ticks
    transition_duration = 180 # ticks 3 seconds
    day_duration = 600 # t 10 
    day_tracker = 600 # 10
    is_day = 1 #day is 1, night is 0

    game_time = 0 # ticks
    score = 0
    game_over = False
    start_screen = True
    difficulty = 0
    clock = pygame.time.Clock()
    ignore_collision = 0

    ## START
    starting = True

    while starting:
        window.blit(dino_img[1], (dino_x, dino_y))
        start_game_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                starting = False
        start_game_screen()


    running = True
    is_active = True
    while running:
        # Handle events
        # dino_crouch = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.ACTIVEEVENT:  # Check if window is active or inactive
                if event.gain == 0:  # Window is inactive
                    is_active = False
                else:  # Window is active
                    is_active = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                ignore_collision = 1
            else: 
                ignore_collision = 0

            if running and is_active and not game_over:
                if (event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP)) or pygame.key.get_pressed()[pygame.K_UP]:
                    if dino_y == HEIGHT - dino_height - 20: 
                        dino_vel_y = -15
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    dino_crouch = 1

                else:
                    dino_crouch = 0

        if is_active and not game_over and running and not starting:
            if (game_time % 60 == 0):
                difficulty = clamp(difficulty + 1, 0, 100)
                time += 1
            dino_y += dino_vel_y
            dino_vel_y += gravity
            


            # Update game objects
            if check_collision() == True:
                game_over = True
                
            if dino_y >= HEIGHT - dino_height - 20:
                dino_y = HEIGHT - dino_height - 20
                dino_vel_y = 0

            cactus_spawn_time -= 1
            if cactus_spawn_time <= 0 and check_spawn() == True:
                spawn_cactus()
                cactus_spawn_time = random.randint(30, clamp(round((1-difficultyround())*100),30,300))
                if dinobird_spawn_time < 100:
                    dinobird_spawn_time = random.randint(30, clamp(round((1-difficultyround())*100),30,300))

            dinobird_spawn_time -= 1
            if dinobird_spawn_time <= 0 and check_spawn() == True:
                spawn_dinobird()
                dinobird_spawn_time = random.randint(30, clamp(round((1-difficultyround())*100),30,300))
                cactus_spawn_time = random.randint(30, clamp(round((1-difficultyround())*100),30,300))

            groundcactus_spawn_time -= 1
            if groundcactus_spawn_time <= 0:
                spawn_groundcactus()                      #      #1-.05  .95 *100  30-95     
                groundcactus_spawn_time = random.randint(30, clamp(round((1-difficultyround())*100),30,300))

            for i, cactus in enumerate(cacti):
                cactus_x, cactus_y, cactus_vel_x,cactus_variant = cactus


                            # -5 (.01*5) 60 2/100
                cactus_x += round(cactus_vel_x-(difficultyround()*5))

                # cactus_x += (cactus_vel_x+(-1*(difficultyround(abs(cactus_vel_x)))))
                cacti[i] = (cactus_x, cactus_y,cactus_vel_x,cactus_variant)
                if cactus_x + cactus_width < 0:
                    remove_cactus(i)
                    if ignore_collision == 0:
                        score += 1
                    break

            for i, dinobird in enumerate(dinobirds):
                dinobird_x, dinobird_y, dinobird_vel_x, dinobird_frame = dinobird

                # dinobird_x += (dinobird_vel_x+(-1*(difficultyround(abs(dinobird_vel_x)))))
                dinobird_x += round(dinobird_vel_x-(difficultyround()*5))

                dinobirds[i] = (dinobird_x,dinobird_y,dinobird_vel_x,dinobird_frame)
                if dinobird_x + dinobird_width < 0:
                    remove_dinobird(i)
                    if ignore_collision == 0:
                        score += 1
                    break

            for i, groundcactus in enumerate(groundcacti):
                groundcactus_x, groundcactus_y,groundcactus_variant,groundcactus_speed_variant = groundcactus

                # groundcactus_x += (groundcactus_speed_variant+(-1*(difficultyround(abs(groundcactus_speed_variant)))))

                groundcactus_x += round(groundcactus_speed_variant-(difficultyround()*5))

                groundcacti[i] = (groundcactus_x, groundcactus_y,groundcactus_variant,groundcactus_speed_variant)

                if groundcactus_x + groundcactus_width < 0:
                    remove_groundcactus(i)
                    break

            # ground_x += (ground_vel_x+(-1*(difficultyround(abs(ground_vel_x)))))
            ground_x += round(ground_vel_x-(difficultyround()*5))
            print(round(ground_vel_x-(difficultyround()*5)))

            if ground_x <= -ground_width:
                ground_x = 0
 
        # Draw the game window (happens even if game paused or over)
        # move clouds
        if not game_over:
            cloud_spawn_time -= 1
            if cloud_spawn_time <= 0:
                spawn_cloud()
                cloud_spawn_time = random.randint(int(cloud_img.get_width() / 4), int(cloud_img.get_width() * 4))

            for i, cloud in enumerate(clouds):
                cloud_x, cloud_y,star_variant = cloud

                cloud_x += cloud_vel_x
                clouds[i] = (cloud_x, cloud_y,star_variant)

                if cloud_x + cloud_width < 0:
                    remove_cloud(i)
        daylight_cycle()

        window.blit(ground_img, (ground_x, HEIGHT - 70))
        window.blit(ground_img, (ground_x + ground_width, HEIGHT - 70))\
        
        for i, groundcactus in enumerate(groundcacti): # groundcactus behind cactus
            groundcactus_x, groundcactus_y,groundcactus_variant,groundcactus_speed_variant = groundcactus
            variant = str(groundcactus_variant)
            if groundcactus_y > HEIGHT - cactus_height - 50:
                window.blit(pygame.transform.scale(pygame.image.load('assets/cactussmall_34x70_' + variant + '.png').convert_alpha(), groundcactus_size), (groundcactus_x, groundcactus_y))

        for i, cactus in enumerate(cacti):
            cactus_x, cactus_y, cactus_vel_x,cactus_variant = cactus

            variant = str(cactus_variant)
            window.blit(pygame.image.load('assets/cactus_50x100_' + variant + '.png').convert_alpha(), (cactus_x, cactus_y - 20))

        for i, groundcactus in enumerate(groundcacti): # groundcactus above cactus
            groundcactus_x, groundcactus_y,groundcactus_variant,groundcactus_speed_variant = groundcactus
            variant = str(groundcactus_variant)
            if groundcactus_y < HEIGHT + cactus_height - 50:
                window.blit(pygame.transform.scale(pygame.image.load('assets/cactussmall_34x70_' + variant + '.png').convert_alpha(), groundcactus_size), (groundcactus_x, groundcactus_y))

        for i, cloud in enumerate(clouds):
            cloud_x, cloud_y,star_variant = cloud
            if is_day == 1:
                window.blit(cloud_img, (cloud_x, cloud_y))
            if is_day == 0: #star_92x92_01.png
                window.blit(pygame.image.load('assets/star_92x92_0' + str(star_variant) + '.png').convert_alpha(), (cloud_x, cloud_y - 20))


        update_dinobird_img()
        update_dino_img()
        window.blit(current_dino_img, (dino_x, dino_y))
        window.blit(ground_img, (ground_x, HEIGHT - 70))
        window.blit(ground_img, (ground_x + ground_width, HEIGHT - 70))
        display_score()

        if game_over:
            game_over_screen()
        pygame.display.update()
        clock.tick(60)  # Elapsed time in seconds
        game_time += 1

game_run()
# Quit the game
pygame.quit()
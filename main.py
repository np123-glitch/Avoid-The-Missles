import pygame
import random
import sys
from pygame.locals import *
import time

pygame.init()


width, height = 640, 480
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Avoid the Missiles!!")


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
fancy_blue = (125, 201, 231)
suble_white = (239, 239, 239)

player_width = 50
player_height = 50
player_x = width // 2 - player_width // 2
player_y = height - player_height - 10
player_speed = 10

obstacle_width = 30
obstacle_height = 30
obstacle_speed = 15

font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()
fps = 60
running = True
game_over = False
obstacles = []
points = 0
targeting = False


def get_score():
    end_time = time.time()
    score = int(end_time - start_time)
    return score

def pause_mode(text, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=((width // 2) - 50, (height // 2) - 50))
    text = pygame.transform.scale(text_surface, (200, 50))
    win.blit(text, text_rect)

def hard_mode():
    global obstacle_speed
    global player_speed
    if targeting == True:
        font.set_italic(True)
        obstacle_speed = 25
        player_speed = 20
        text_surface = font.render("Hard Mode: ON        Press H to toggle", True, (0, 255, 0))
        win.blit(text_surface, (0, 0))
        font.set_italic(False)
    else:
        obstacle_speed = 15
        player_speed = 10
        text_surface = font.render("Hard Mode: OFF        Press H to toggle", True, (255, 0, 0))
        win.blit(text_surface, (0, 0))

def draw_pause_text(text, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, (height // 2) - 200))
    win.blit(text_surface, text_rect)

def draw_text(text, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    win.blit(text_surface, text_rect)

def draw_high_score(color):
    text_surface = font.render('High Score:' + high_score, True, color)
    text_width, text_height = text_surface.get_size()
    top_right_x = win.get_width() - text_width
    top_right_y = 0
    win.blit(text_surface, (top_right_x, top_right_y))

def spawn_obstacle():
    global player_x
    global targeting
    spawn_range = width - obstacle_width
    if targeting:
        new_obstacle = {
            "x": player_x, 
            "y": -obstacle_height, 
        }
    else:
        new_obstacle = {
            "x": random.randint(0, spawn_range), 
            "y": -obstacle_height, 
        }
    obstacles.append(new_obstacle)

def check_hard_mode():
    global obstacle_speed
    if targeting == False:
        obstacle_speed = 15





state = True
start_time = time.time()
with open('score.txt', 'r') as f:
        high_score = f.read()

while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                state = not state
            if event.key == K_h:
                targeting = not targeting

    if state == True:
        
        

        
        win.fill(suble_white)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_x > 15:
            player_x -= player_speed
        if keys[K_RIGHT] and player_x < width - player_width - 15:
            player_x += player_speed

        if targeting:
            if random.randint(1, 10) == 1:
                spawn_obstacle()

        elif random.randint(1,  30) == 1:
            spawn_obstacle()

        for obstacle in obstacles:
            obstacle["y"] += obstacle_speed
            if player_x < obstacle["x"] + obstacle_width and \
                player_x + player_width > obstacle["x"] and \
                player_y < obstacle["y"] + obstacle_height and \
                player_y + player_height > obstacle["y"]:
                game_over = True
                break
        

            if obstacle["y"] > height:
                obstacles.remove(obstacle)
                


        pygame.draw.rect(win, black, (player_x, player_y, player_width, player_height))

        for obstacle in obstacles:
            pygame.draw.rect(win, red, (obstacle["x"], obstacle["y"], obstacle_width, obstacle_height))
        if game_over:
            draw_text("Game Over!", red)
            break
        score = get_score()
        draw_pause_text("Press SPACE to pause", red)
        hard_mode()
        check_hard_mode()
        draw_high_score(fancy_blue)
        draw_text(str(score), red)
    if state == False:
        pause_mode('PAUSED', black)


    pygame.display.update()
    pygame.display.flip()
    
    clock.tick(fps)
end_time = time.time()


if high_score != '':
    if int(high_score) < score:
        with open('score.txt', 'w') as f:
            f.write(str(score))



print(f'Score: {int(end_time - start_time)}')

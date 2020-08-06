import pygame
import random
import math
import sys
import os

current_directory = os.path.dirname(__file__)

pygame.mixer.pre_init(channels=1, buffer=256)
pygame.init()
screen = pygame.display.set_mode((576, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

game_font = pygame.font.Font("04B_19__.ttf", 40)
restart_font = pygame.font.Font("04B_19__.ttf", 50)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = -.999999
high_score = 0
pipe_height = [270, 420, 570]


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            bird_hit.play()
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 640:
        bird_hit.play()
        return False

    return True


def rotate_bird(bird):
    bird_rotated = pygame.transform.rotozoom(bird, -2 * bird_movement, 1)
    return bird_rotated


def draw_floor():
    global floorx
    screen.blit(floor_surface, (floorx, 640))
    screen.blit(floor_surface, (floorx + 576, 640))

    if floorx <= -576:
        floorx = 0


def create_pipe():
    choice = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, choice))
    top_pipe = pipe_surface.get_rect(midtop=(700, choice - 890))

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(f"Score : {math.ceil(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 50))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score : {math.ceil(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"HighScore : {math.ceil(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 600))
        screen.blit(high_score_surface, high_score_rect)

        # continue_surface = restart_font.render("Press Enter Restart", True, (255, 255, 255))
        # continue_rect = continue_surface.get_rect(center=(288, 360))
        # screen.blit(continue_surface, continue_rect)


def update_score(score_, high_score_):
    if score_ >= high_score_:
        high_score_ = score
    return high_score_


bg_url = os.path.join(current_directory, 'sprites', 'background-day.png')

bg_surface = pygame.image.load(bg_url).convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 720))

floor_url = os.path.join(current_directory, 'sprites', 'base.png')

floor_surface = pygame.image.load(floor_url).convert()
floor_surface = pygame.transform.scale(floor_surface, (576, 150))
floorx = 0

upflap_url = os.path.join(current_directory, 'sprites', 'bluebird-upflap.png')
midflap_url = os.path.join(current_directory, 'sprites', 'bluebird-midflap.png')
downflap_url = os.path.join(current_directory, 'sprites', 'bluebird-downflap.png')

bird_upflap = pygame.transform.scale2x(pygame.image.load(upflap_url).convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(midflap_url).convert_alpha())
bird_downflap = pygame.transform.scale2x(pygame.image.load(downflap_url).convert_alpha())

bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0

bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 360))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_url = os.path.join(current_directory, 'sprites', 'pipe-green.png')

pipe_surface = pygame.image.load(pipe_url)
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_over_url = os.path.join(current_directory, 'sprites', 'message.png')

game_over_surface = pygame.transform.scale(pygame.image.load(game_over_url).convert_alpha(), (368, 386))
game_over_rect = game_over_surface.get_rect(center=(288, 320))

flap_url = os.path.join(current_directory, 'audio', 'wing.wav')
hit_url = os.path.join(current_directory, 'audio', 'hit.wav')


flap_sound = pygame.mixer.Sound(flap_url)
bird_hit = pygame.mixer.Sound(hit_url)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_RETURN and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 360)
                bird_movement = 0
                score = -.999999

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            elif bird_index >= 2:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))
    draw_floor()

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

        score += 1 / 200
        score_display("main_game")

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    floorx -= 1

    pygame.display.update()
    clock.tick(120)

import pygame
import sys
from random import choice
from pygame.locals import QUIT
from time import sleep


pygame.init()
# You can set any window size, starting from (200, 200)
win_size = width, height = 1500, 1000
FPS, time = 60, pygame.time.Clock()
window = pygame.display.set_mode(win_size)
pygame.display.set_caption('Pong')
colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
          (0, 255, 237), (254, 0, 255), (255, 120, 0), (214, 0, 255),
          (255, 255, 0), (135, 255, 0)
]
player, player_speed = pygame.Rect(95, height // 2 - 30, 10, 60), 15
sec_player, sec_player_speed = pygame.Rect(width - 105, height // 2 - 30, 10, 60), 15
obj_size, obj_speed = 16, 10
game_obj = pygame.Rect(width // 2 - obj_size, height // 2 - obj_size // 2, obj_size, obj_size)
directions = {
    'top_right': (obj_speed, -obj_speed),
    'top_left': (-obj_speed, -obj_speed),
    'bottom_right': (obj_speed, obj_speed),
    'bottom_left': (-obj_speed, obj_speed),
}
current_direction = choice(list(directions))
player_wins = sec_player_wins = 0
# noinspection PyTypeChecker
font = pygame.font.SysFont(None, 40)
COLOR, BLACK_COLOR = choice(colors), (0, 0, 0)
player_touch, point_sound = pygame.mixer.Sound('touch_player.wav'), pygame.mixer.Sound('point_sound.wav')
border_touch = pygame.mixer.Sound('touch_borders.wav')
possible_y = [height // 2 - obj_size // 2, height // 2 + obj_size,
              height // 2 + obj_size * 4, height // 2 - obj_size * 2,
              height // 2 + obj_size * 5, height // 2 - obj_size * 5,
              110 + obj_size * 2, height - 200 - obj_size * 2
]
used_y = 0


def draw_border(screen):
    # Draws the borders of the playing field
    pygame.draw.rect(screen, COLOR, (50, 100, width - 100, 10))
    pygame.draw.rect(screen, COLOR, (50, 100, 10, height - 200))
    pygame.draw.rect(screen, COLOR, (50, height - 110, width - 100, 10))
    pygame.draw.rect(screen, COLOR, (width - 60, 100, 10, height - 200))
    pygame.draw.line(screen, COLOR, (width // 2 - 1, 100), (width // 2 - 1, height - 110), 10)


def move_player(keys):
    # Movement of the player from the left side
    # Movement keys - W and S
    if keys[pygame.K_w] and player.y > 125:
        player.move_ip(0, -player_speed)
    elif keys[pygame.K_s] and player.y < height - 185:
        player.move_ip(0, player_speed)


def move_sec_player(keys):
    # Movement of the player from the right side
    # Movement keys - top arrow key and bottom arrow key
    if keys[pygame.K_UP] and sec_player.y > 125:
        sec_player.move_ip(0, -sec_player_speed)
    elif keys[pygame.K_DOWN] and sec_player.y < height - 185:
        sec_player.move_ip(0, sec_player_speed)


def move_obj_to_center(obj, possible_directions):
    global current_direction, used_y
    obj.x = width // 2 - obj_size
    obj.y = choice([direction for direction in possible_y if direction != used_y])
    used_y = obj.y
    current_direction = choice(possible_directions)


def move_obj(obj, pl1, pl2):
    # Movement of the game object

    # The ball moves depending on the variable current_direction,
    # which contains the current direction of travel
    global current_direction, player_wins, sec_player_wins
    # Check for collision with players, it true, game object
    # changes the current direction of travel
    if obj.colliderect(pl1):
        player_touch.play()
        if current_direction == 'top_left':
            current_direction = 'top_right'
        else:
            current_direction = 'bottom_right'
    elif obj.colliderect(pl2):
        player_touch.play()
        if current_direction == 'top_right':
            current_direction = 'top_left'
        else:
            current_direction = 'bottom_left'
    # Checking for collisions with the upper and lower borders of the screen
    elif obj.bottom > height - 112:
        border_touch.play()
        if current_direction == 'bottom_left':
            current_direction = 'top_left'
        else:
            current_direction = 'top_right'
    elif obj.top < 111:
        border_touch.play()
        if current_direction == 'top_left':
            current_direction = 'bottom_left'
        else:
            current_direction = 'bottom_right'
    # Checking for collision with the right border of the screen
    # if true, awards one point to the player on the left
    elif obj.right > width - 62:
        if current_direction == 'top_right':
            current_direction = 'top_left'
        else:
            current_direction = 'bottom_left'
        player_wins += 1
        point_sound.play()
        move_obj_to_center(obj, ['top_right', 'bottom_right'])
    # Checking for collision with the left border of the screen
    # if true, awards one point to the player on the right
    elif obj.left < 60:
        if current_direction == 'top_left':
            current_direction = 'top_right'
        else:
            current_direction = 'bottom_right'
        sec_player_wins += 1
        point_sound.play()
        move_obj_to_center(obj, ['top_left', 'bottom_left'])
    obj.move_ip(directions[current_direction])


def main():
    # life_time = int(input('Up to how many wins will the game continue?\n'))
    while True:
        # Frames per second
        time.tick(FPS)
        # Checking out of the game
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        buttons = pygame.key.get_pressed()
        move_player(buttons), move_obj(game_obj, player, sec_player), move_sec_player(buttons)
        window.fill(BLACK_COLOR)
        # Drawing the game
        draw_border(window)
        pygame.draw.rect(window, (255, 255, 255), player)
        pygame.draw.rect(window, (255, 255, 255), sec_player)
        pygame.draw.rect(window, (255, 255, 255), game_obj)
        # Drawing the game score
        text = font.render(f'{player_wins}:{sec_player_wins}', 5, COLOR)
        window.blit(text, (width // 2 - 20, 10))
        pygame.display.update()


main()

import pygame, sys, time, random, numpy as np

# Window size
frame_size_x = 720
frame_size_y = 480

# Difficulty
difficulty = 20

# Initialize pygame
pygame.init()
pygame.display.set_caption('Snake Game - Manual or AI')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
fps_controller = pygame.time.Clock()

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
darkgreen = pygame.Color(6, 40, 0)
blue = pygame.Color(0, 0, 255)

# Functions
def show_score(score):
    score_font = pygame.font.SysFont('consolas', 20)
    score_surface = score_font.render('Score : ' + str(score), True, white)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (frame_size_x/10, 15)
    game_window.blit(score_surface, score_rect)

def message(text, color, y_displace=0):
    font = pygame.font.SysFont('times new roman', 30)
    mesg = font.render(text, True, color)
    mesg_rect = mesg.get_rect(center=(frame_size_x/2, frame_size_y/2 + y_displace))
    game_window.blit(mesg, mesg_rect)

def dist(state, goal):
    return abs(goal[0] - state[0]) + abs(goal[1] - state[1])

def greedy(direction, pos, goal, body):
    directions = ['DOWN', 'UP', 'LEFT', 'RIGHT']
    moves = np.array([[0, 10], [0, -10], [-10, 0], [10, 0]])
    state_dict = {d: pos + m for d, m in zip(directions, moves)}
    distance_dict = {d: dist(pos + m, goal) for d, m in zip(directions, moves)}

    for d in directions.copy():
        if list(state_dict[d]) in body:
            directions.remove(d)

    change = direction
    if len(directions) == 0:
        return change
    if direction not in directions:
        change = directions[0]

    for d in directions:
        if distance_dict[d] < distance_dict[change]:
            change = d

    return change

def snake_game(mode='manual'):
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]

    food_pos = [random.randrange(1, (frame_size_x//10)) * 10,
                random.randrange(1, (frame_size_y//10)) * 10]
    food_spawn = True

    direction = 'RIGHT'
    change_to = direction
    score = 0
    game_over_flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if mode == 'manual':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'

        if mode == 'ai':
            change_to = greedy(direction, np.array(snake_pos), np.array(food_pos), snake_body)

        direction = change_to

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Border conditions
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10 or snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over_flag = True

        # Snake body growing
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10,
                        random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # Background
        game_window.fill(darkgreen)

        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Collision with self
        for block in snake_body[1:]:
            if snake_pos == block:
                game_over_flag = True

        show_score(score)
        pygame.display.update()

        if game_over_flag:
            game_window.fill(black)
            message("YOU LOST!", red, -50)
            message("Press R to Restart or Q to Quit", white, 50)
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_r:
                            snake_game(mode)

        fps_controller.tick(difficulty)

def main_menu():
    while True:
        game_window.fill(black)
        message("Press M for Manual Play", white, -30)
        message("Press A for AI Play", white, 30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    snake_game(mode='manual')
                if event.key == pygame.K_a:
                    snake_game(mode='ai')

if __name__ == "__main__":
    main_menu()

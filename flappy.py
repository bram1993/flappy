import pygame
import random

# Setup
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Game state
gravity = 0.5
bird_movement = 0
game_active = False
game_started = False
score = 0
high_score = 0
speed = 4

# Bird and pipes
bird = pygame.Rect(100, 300, 30, 30)
pipes = []
pipe_gap = 150

def create_pipe():
    height = random.randint(100, 400)
    top = pygame.Rect(400, 0, 50, height)
    bottom = pygame.Rect(400, height + pipe_gap, 50, 600 - height - pipe_gap)
    return top, bottom

def reset_game():
    global bird, bird_movement, pipes, score, game_active, game_started, speed
    bird.y = 300
    bird_movement = 0
    pipes.clear()
    pipes.extend(create_pipe())
    score = 0
    speed = 4
    game_active = True
    game_started = True

pipes.extend(create_pipe())

# Main loop
while True:
    space_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Start or restart game
    if space_pressed:
        if not game_started:
            reset_game()
        elif not game_active:
            if score > high_score:
                high_score = score
            reset_game()

    if game_active:
        if space_pressed:
            bird_movement = -6
        else:
            bird_movement += gravity

        bird.y += bird_movement

        for pipe in pipes:
            pipe.x -= speed

        if pipes[-1].x < 200:
            pipes.extend(create_pipe())

        if pipes[0].x < -50:
            pipes = pipes[2:]
            score += 1
            # Increase speed every few pipes
            if score % 5 == 0:
                speed += 0.5

        for pipe in pipes:
            if bird.colliderect(pipe):
                game_active = False
        if bird.top <= 0 or bird.bottom >= 600:
            game_active = False

    # Drawing
    screen.fill((135, 206, 250))
    pygame.draw.rect(screen, (255, 255, 0), bird)
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), pipe)

    # Scores
    high_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_text, (10, 10))
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (280, 10))

    if not game_started:
        text = font.render("Press SPACE to start", True, (0, 0, 0))
        screen.blit(text, (80, 250))
    elif not game_active:
        text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
        screen.blit(text, (80, 250))
        text2 = font.render("Press SPACE to restart", True, (0, 0, 0))
        screen.blit(text2, (80, 300))

    pygame.display.flip()
    clock.tick(60)
ß

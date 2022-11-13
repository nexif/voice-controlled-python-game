import pygame
import random
import whisper
import sys
from transformers import pipeline
from lib.asr_sr import asr_sr
from lib.asr_whisper import asr_whisper
from lib.asr_facebook import asr_facebook


def your_score(score):
    value = score_font.render("Twój wynik: " + str(score), True, blue)
    dis.blit(value, [0, 0])


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, blue, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def game_loop(asr_type, asr_model=None):
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        if asr_type == 'sr':
            text = asr_sr()
        elif asr_type == 'whisper':
            text = asr_whisper(asr_model)
        elif asr_type == 'facebook':
            text = asr_facebook(asr_model)
        else:
            raise ValueError('Invalid asr_type')

        while game_close:
            dis.fill(black)
            message(
                "Przegrałeś! Naciśnij 'c', aby uruchomić ponownie lub 'q' aby wyjść", red)
            your_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(asr_type)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        if 'lewo' in text:
            x1_change = -snake_block
            y1_change = 0
        elif 'prawo' in text:
            x1_change = snake_block
            y1_change = 0
        elif 'góra' in text:
            y1_change = -snake_block
            x1_change = 0
        elif 'dół' in text:
            y1_change = snake_block
            x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(black)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        your_score(snake_length - 1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(
                0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(
                0, dis_height - snake_block) / 10.0) * 10.0
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


if __name__ == '__main__':
    pygame.init()

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (5, 125, 125)

    dis_width = 300
    dis_height = 200

    dis = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Snake')

    clock = pygame.time.Clock()
    snake_block = 10
    snake_speed = 15

    font_style = pygame.font.SysFont("calibri", 8, bold=pygame.font.Font.bold)
    score_font = pygame.font.SysFont("calibri", 15, bold=pygame.font.Font.bold)

    asr_type = 'sr'  # wartość domyślna
    if len(sys.argv) > 1:
        if sys.argv[1] == 'sr':
            print('Uruchamiam grę z asr_type = sr')
        elif sys.argv[1] == 'whisper':
            print('Uruchamiam grę z asr_type = whisper')
            model = whisper.load_model("base")
            game_loop(sys.argv[1], model)
        elif sys.argv[1] == 'facebook':
            pipe = pipeline(model="facebook/wav2vec2-base-10k-voxpopuli-ft-pl",
                            task='automatic-speech-recognition')
            game_loop(sys.argv[1], pipe)
        else:
            print('Nieprawidłowy argument - uruchamiam grę z asr_type = sr')
            game_loop('sr')

    game_loop(asr_type)

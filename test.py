import pygame
import pygame_menu
from game_lang import GameApp

pygame.init()

WINDOW_SIZE = (800, 600)
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('My Game')


FONT = pygame_menu.font.FONT_8BIT
pygame_menu.BaseImage
img_path = r"C:\Users\diosv\OneDrive\Desktop\background.jpg"

img = pygame_menu.BaseImage(img_path)
mytheme = pygame_menu.Theme(background_color=img)
menu = pygame_menu.Menu('Главное меню', WIDTH, HEIGHT, theme=mytheme)


def start_the_game():
    game = GameApp()
    game.run()

def show_options():
    pass

def resize():
    window_size = screen.get_size()
    new_w, new_h = window_size[0], window_size[1]

    print(menu.get_widgets_column(0))
    
    menu.resize(new_w, new_h)
    menu.enable()


# menu.add.button('Start Game', start_the_game)
menu.add.button('Start game', start_the_game, font_size=30)
menu.add.button('Options', show_options)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.enable()

while True:
    # screen.fill("green")

    menu.draw(screen)

    pygame.display.update()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.VIDEORESIZE:
            # Update the surface
            
            
            # Call the menu event
            resize()
    menu.update(events)
    menu.draw(screen)

    pygame.display.flip()
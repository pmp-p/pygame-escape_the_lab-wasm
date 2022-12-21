import pygame
from pygame import *
from pygame import mixer
import pygame.freetype
import time
import sys
from random import randint
from Programs.Buttons import Button
from Programs.animation import death_animation


class Base:
    pygame.init()
    display = pygame.display
    display.set_caption("ESCAPE THE LAB")


    sprite_images = ["Images/Sprites/SpriteBasic.png",
                     "Images/Sprites/Sprite1.png",
                     "Images/Sprites/Sprite2.png",
                     "Images/Sprites/Sprite2.png",
                     "Images/Sprites/Sprite3.png",
                     "Images/Sprites/Sprite4.png",
                     "Images/Sprites/Sprite5.png",
                     "Images/Sprites/Sprite6.png",
                     "Images/Free_Play_Shop/castle.png"]



SCREEN_SIZE = pygame.Rect((0, 0, 1280, 736))
TILE_SIZE = 32
MAP_BORDER = (10000, 5000)
GRAVITY = pygame.Vector2((0, 0.4))
SCREEN = pygame.display.set_mode((1280, 736))
CHARACTER_SKINS = ""
INVENTORY_ITEMS = []
ALLOWED_LEVELS = 0
COINS = 0
RANDOM_NUMBER = 0
BULLETS = []
ENEMY_BULLETS= []
bullet_x = 0
bullet_y = 0

Base.screen = SCREEN

from gamestates import States
States.base = Base

class Menu(Base):
    background = pygame.transform.scale(pygame.image.load("Images/Background_images/menu_background.gif"),(1280, 736)).convert_alpha()

class Menu_start(Menu):

    def on_select(self):
        inventory_choice(item=0)
        map_choice(level=0)

    def draw(self):
        global CHARACTER_SKINS
        CHARACTER_SKINS = "Images/Sprites/SpriteBasic.png"

        SCREEN.blit(self.background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(80).render("ESCAPE THE LAB", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(580, 200))

        play_button = Button(image=pygame.transform.scale(image.load("Images/Rects/Map Rect.png"),(800, 220)), pos=(700, 450),
                             text_input="PLAY", font=get_font(200), base_color="#d7fcd4", hovering_color="White")


        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if play_button.checkForInput(menu_mouse_pos):
                    States.select("Menu_main")

        pygame.display.update()

class Menu_main(Menu):

    def draw(self):
        pygame.display.set_caption("Main Menu")

        SCREEN.blit(self.background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        controls_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 400),
                                text_input="Controls", font=get_font(70), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, controls_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(SCREEN)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if play_button.checkForInput(menu_mouse_pos):
                    States.select("Menu_play")
                if controls_button.checkForInput(menu_mouse_pos):
                    States.select("Menu_controls")
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()




class Menu_controls(Menu):
    def draw(self):
        pygame.display.set_caption("Controls")
        SCREEN.blit(self.background, (0, 0))
        credits_mouse_pos = pygame.mouse.get_pos()
        credit_text = get_font(150).render("CONTROLS", True, "#b68f40")
        credit_rect = credit_text.get_rect(center=(640, 100))
        info_text = get_font(40).render("Up arrow to shoot", True, "#b68f40")
        info_rect = credit_text.get_rect(center=(650, 300))
        info_text2 = get_font(40).render("Left arrow to go left", True, "#b68f40")
        info_rect2 = credit_text.get_rect(center=(650, 400))
        info_text3 = get_font(40).render("Right arrow to go right", True, "#b68f40")
        info_rect3 = credit_text.get_rect(center=(650, 500))
        info_text4 = get_font(40).render("Space button to jump", True, "#b68f40")
        info_rect4 = credit_text.get_rect(center=(650, 600))
        SCREEN.blit(credit_text, credit_rect)
        SCREEN.blit(info_text,info_rect)
        SCREEN.blit(info_text2, info_rect2)
        SCREEN.blit(info_text3, info_rect3)
        SCREEN.blit(info_text4, info_rect4)
        back_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(1050, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        back_button.changeColor(credits_mouse_pos)
        back_button.update(SCREEN)
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if back_button.checkForInput(credits_mouse_pos):
                    States.select("Menu_main")


class Menu_play(Menu):

    def draw(self):
        pygame.display.set_caption("Game Mode Selection")

        SCREEN.blit(self.background, (0, 0))

        play_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("GAME MODES", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))


        free_play_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(350, 300),
                                  text_input="Free Play", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        level_play_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(980, 300),
                                   text_input="Levels", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        shop_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(350, 550),
                             text_input="Shop", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [free_play_button, level_play_button, shop_button, quit_button]:
            button.changeColor(play_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if level_play_button.checkForInput(play_mouse_pos):
                    levels_window()
                elif free_play_button.checkForInput(play_mouse_pos):
                    States.select("Menu_freeplay")
                elif shop_button.checkForInput(play_mouse_pos):
                    shop_menu_overall()
                elif quit_button.checkForInput(play_mouse_pos):
                    States.select("Menu_main")



class Menu_freeplay(Menu):

    def draw(self):
        pygame.display.set_caption("Free Play Menu")

        shop_menu_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(self.background, (0, 0))
        menu_text = get_font(80).render("FREE PLAY MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))


        free_play_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 250),
                                  text_input="Free Play Normal", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        castle_free_play_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 450),
                                         text_input="Castle Free Play", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(640, 650),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [free_play_button, castle_free_play_button, quit_button]:
            button.changeColor(shop_menu_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if free_play_button.checkForInput(shop_menu_mouse_pos):
                    if ALLOWED_LEVELS >= 5:
                        random_number()
                        random_map_normal()
                    else:
                        not_completed_levels()
                if castle_free_play_button.checkForInput(shop_menu_mouse_pos):
                    if "Images/Free_Play_Shop/castle.png" in INVENTORY_ITEMS:
                        random_number()
                        random_map_castle()
                    else:
                        not_owned()
                if quit_button.checkForInput(shop_menu_mouse_pos):
                    States.select("Menu_play")

        pygame.image.save(SCREEN, "Images/screenshot_load_screen.jpg")



def levels_window():
    pygame.display.set_caption("Level Selection")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    basecolour0 = "#d7fcd4"
    basecolour1 =  "#d7fcd4"
    basecolour2 =  "#d7fcd4"
    basecolour3 =  "#d7fcd4"
    basecolour4 =  "#d7fcd4"
    basecolour5 =  "#d7fcd4"
    basecolour6 =  "#d7fcd4"

    if ALLOWED_LEVELS >= 1:
        basecolour0 = "#009E60"
    if ALLOWED_LEVELS >= 2:
        basecolour1 = "#009E60"
    if ALLOWED_LEVELS >= 3:
        basecolour2 = "#009E60"
    if ALLOWED_LEVELS >= 4:
        basecolour3 = "#009E60"
    if ALLOWED_LEVELS >= 5:
        basecolour4 = "#009E60"
    if ALLOWED_LEVELS >= 6:
        basecolour5 = "#009E60"
    if ALLOWED_LEVELS >= 7:
        basecolour6 = "#009E60"


    while 1:
        levels_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))





        level1_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(320, 100),
                               text_input="LeveL 1", font=get_font(75), base_color=basecolour0, hovering_color="White")

        level2_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(320, 250),
                               text_input="LeveL 2", font=get_font(75), base_color=basecolour1, hovering_color="White")

        level3_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(320, 400),
                               text_input="LeveL 3", font=get_font(75), base_color=basecolour2, hovering_color="White")

        level4_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(320, 550),
                               text_input="LeveL 4", font=get_font(75), base_color=basecolour3, hovering_color="White")

        level5_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(950, 100),
                               text_input="LeveL 5", font=get_font(75), base_color=basecolour4, hovering_color="White")

        level6_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(950, 250),
                               text_input="LeveL 6", font=get_font(75), base_color=basecolour5, hovering_color="White")

        level7_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(950, 400),
                               text_input="LeveL 7", font=get_font(75), base_color=basecolour6, hovering_color="White")

        back_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")


        for BUTTON in [level1_button, level2_button, level3_button, level4_button, level5_button, level6_button, level7_button, back_button]:
            BUTTON.changeColor(levels_mouse_pos)
            BUTTON.update(SCREEN)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if level1_button.checkForInput(levels_mouse_pos):
                    map_choice(level=1)
                if level2_button.checkForInput(levels_mouse_pos):
                    if ALLOWED_LEVELS >= 1:
                        map_choice(level=2)
                    else:
                        not_completed()

                if level3_button.checkForInput(levels_mouse_pos):
                    if ALLOWED_LEVELS >= 2:
                        map_choice(level=3)
                    else:
                        not_completed()
                if level4_button.checkForInput(levels_mouse_pos):
                    if ALLOWED_LEVELS >= 3:
                        map_choice(level=4)
                    else:
                        not_completed()
                if level5_button.checkForInput(levels_mouse_pos):
                    if ALLOWED_LEVELS >= 4:
                        map_choice(level=5)
                    else:
                        not_completed()
                if level6_button.checkForInput(levels_mouse_pos):
                    if ALLOWED_LEVELS >= 5:
                        map_choice(level=6)
                    else:
                        not_completed()
                if level7_button.checkForInput(levels_mouse_pos):
                    if ALLOWED_LEVELS >= 6:
                        map_choice(level=7)
                    else:
                        not_completed()
                if back_button.checkForInput(levels_mouse_pos):
                    play_window()
        pygame.image.save(SCREEN, "Images/screenshot_load_screen.jpg")
        pygame.display.update()

def shop_menu_overall():
    pygame.display.set_caption("Shop Window 2")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    while 1:
        shop_menu_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        menu_text = get_font(80).render("SHOP WINDOW", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))


        inventory_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 250),
                                       text_input="Inventory", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        shop_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 450),
                                       text_input="Shop", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(640, 650),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [inventory_button, shop_button, quit_button]:
            button.changeColor(shop_menu_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if inventory_button.checkForInput(shop_menu_mouse_pos):
                    inventory_window()
                if shop_button.checkForInput(shop_menu_mouse_pos):
                    shop_type_window()
                if quit_button.checkForInput(shop_menu_mouse_pos):
                    play_window()


        pygame.display.update()


def inventory_window():

    global CHARACTER_SKINS

    sprite1 = "Not Owned"
    sprite2 = "Not Owned"
    sprite3 = "Not Owned"
    sprite4 = "Not Owned"
    sprite5 = "Not Owned"
    sprite6 = "Not Owned"
    sprite7 = "Not Owned"

    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()

    sprite1_img = pygame.transform.scale(pygame.image.load("Images/Sprites/SpriteBasic.png"), (128, 128))
    sprite2_img = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite1.png"), (128, 128))
    sprite3_img = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite2.png"), (128, 128))
    sprite4_img = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite3.png"), (128, 128))
    sprite5_img = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite4.png"), (128, 128))
    sprite6_img = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite5.png"), (128, 128))
    sprite7_img = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite6.png"), (128, 128))

    while 1:
        SCREEN.blit(BG, (0, 0))
        pygame.display.set_caption("Inventory")
        inventory_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("INVENTORY", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        for i in INVENTORY_ITEMS:
            if i == "Images/Sprites/SpriteBasic.png":
                sprite1 = "Owned"
                if "Images/Sprites/SpriteBasic.png" == CHARACTER_SKINS:
                    sprite1 = "Selected"
            elif i == "Images/Sprites/Sprite1.png":
                sprite2 = "Owned"
                if "Images/Sprites/Sprite1.png" == CHARACTER_SKINS:
                    sprite2 = "Selected"
            elif i == "Images/Sprites/Sprite2.png":
                sprite3 = "Owned"
                if "Images/Sprites/Sprite2.png" == CHARACTER_SKINS:
                    sprite3 = "Selected"
            elif i == "Images/Sprites/Sprite3.png":
                sprite4 = "Owned"
                if "Images/Sprites/Sprite3.png" == CHARACTER_SKINS:
                    sprite4 = "Selected"
            elif i == "Images/Sprites/Sprite4.png":
                sprite5 = "Owned"
                if "Images/Sprites/Sprite4.png" == CHARACTER_SKINS:
                    sprite5 = "Selected"
            elif i == "Images/Sprites/Sprite5.png":
                sprite6 = "Owned"
                if "Images/Sprites/Sprite5.png" == CHARACTER_SKINS:
                    sprite6 = "Selected"
            elif i == "Images/Sprites/Sprite6.png":
                sprite7 = "Owned"
                if "Images/Sprites/Sprite6.png" == CHARACTER_SKINS:
                    sprite7 = "Selected"




        sprite_button1 = Button(image=sprite1_img, pos=(260, 240),
                                text_input=sprite1, font=get_font(20), base_color="red", hovering_color="White")

        sprite_button2 = Button(image=sprite2_img, pos=(460, 240),
                                text_input=sprite2, font=get_font(20), base_color="red", hovering_color="White")

        sprite_button3 = Button(image=sprite3_img, pos=(660, 240),
                                text_input=sprite3, font=get_font(20), base_color="red", hovering_color="White")

        sprite_button4 = Button(image=sprite4_img, pos=(860, 240),
                                text_input=sprite4, font=get_font(20), base_color="red", hovering_color="White")

        sprite_button5 = Button(image=sprite5_img, pos=(1060, 240),
                                text_input=sprite5, font=get_font(20), base_color="red", hovering_color="White")

        sprite_button6 = Button(image=sprite6_img, pos=(260, 380),
                                text_input=sprite6, font=get_font(20), base_color="red", hovering_color="White")

        sprite_button7 = Button(image=sprite7_img, pos=(460, 380),
                                text_input=sprite7, font=get_font(20), base_color="red", hovering_color="White")

        next_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="NEXT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(350, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [sprite_button1, sprite_button2, sprite_button3, sprite_button4, sprite_button5, sprite_button6, sprite_button7, next_button, quit_button]:
            button.changeColor(inventory_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if sprite_button1.checkForInput(inventory_mouse_pos):
                    if sprite1 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/SpriteBasic.png"
                        character_selected()
                    elif sprite1 == "Selected":
                        continue
                    else:
                        not_owned()
                if sprite_button2.checkForInput(inventory_mouse_pos):
                    if sprite2 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/Sprite1.png"
                        character_selected()
                    elif sprite2 == "Selected":
                        continue
                    else:
                        not_owned()
                if sprite_button3.checkForInput(inventory_mouse_pos):
                    if sprite3 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/Sprite2.png"
                        character_selected()
                    elif sprite3 == "Selected":
                        continue
                    else:
                        not_owned()
                if sprite_button4.checkForInput(inventory_mouse_pos):
                    if sprite4 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/Sprite3.png"
                        character_selected()
                    elif sprite4 == "Selected":
                        continue
                    else:
                        not_owned()
                if sprite_button5.checkForInput(inventory_mouse_pos):
                    if sprite5 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/Sprite4.png"
                        character_selected()
                    elif sprite5 == "Selected":
                        continue
                    else:
                        not_owned()
                if sprite_button6.checkForInput(inventory_mouse_pos):
                    if sprite6 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/Sprite5.png"
                        character_selected()
                    elif sprite6 == "Selected":
                        continue
                    else:
                        not_owned()
                if sprite_button7.checkForInput(inventory_mouse_pos):
                    if sprite7 == "Owned":
                        CHARACTER_SKINS = "Images/Sprites/Sprite6.png"
                        character_selected()
                    elif sprite7 == "Selected":
                        continue
                    else:
                        not_owned()
                if next_button.checkForInput(inventory_mouse_pos):
                    continue
                if quit_button.checkForInput(inventory_mouse_pos):
                    shop_menu_overall()


            pygame.display.update()


def shop_type_window():
    pygame.display.set_caption("Shop Window")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    while 1:
        shop_menu_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        menu_text = get_font(75).render("Character Shop", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))


        free_play_shop_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 250),
                                  text_input="Free Play Shop", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        character_shop_button = Button(image=pygame.image.load("Images/Rects/Map Rect.png"), pos=(640, 450),
                             text_input="Character Shop", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(640, 650),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [free_play_shop_button, character_shop_button, quit_button]:
            button.changeColor(shop_menu_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if free_play_shop_button.checkForInput(shop_menu_mouse_pos):
                    free_play_shop()
                if character_shop_button.checkForInput(shop_menu_mouse_pos):
                    shop_window1()
                if quit_button.checkForInput(shop_menu_mouse_pos):
                    shop_menu_overall()


        pygame.display.update()


def free_play_shop():
    pygame.display.set_caption("Free Play Shop")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    sprite1 = pygame.transform.scale(pygame.image.load("Images/Free_Play_Shop/Normal.png"), (200, 200))
    sprite2 = pygame.transform.scale(pygame.image.load("Images/Free_Play_Shop/castle.png"), (200, 200))
    while 1:

        shop_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        menu_text = get_font(150).render("SHOP", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(440, 100))
        shop_text = get_font(50).render("coins:", True, "#b68f40")
        shop_rect = shop_text.get_rect(center=(900, 100))
        coins_text = get_font(50).render(str(COINS), True, "#b68f40")
        coins_rect = shop_text.get_rect(center=(1200, 100))




        skin1_button = Button(image=sprite1, pos=(350, 300),
                              text_input="Not Implemented Yet", font=get_font(20), base_color="red", hovering_color="White")

        skin2_button = Button(image=sprite2, pos=(980, 300),
                              text_input="1000", font=get_font(75), base_color="red", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(350, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        next_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="NEXT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")



        for BUTTON in [skin1_button, skin2_button, quit_button, next_button]:
            BUTTON.changeColor(shop_mouse_pos)
            BUTTON.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(shop_text, shop_rect)
        SCREEN.blit(coins_text,coins_rect)


        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if skin1_button.checkForInput(shop_mouse_pos):
                    continue

                if skin2_button.checkForInput(shop_mouse_pos):
                    if ("Images/Free_Play_Shop/castle.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 1000:
                        cash(money=-1000)
                        sold()
                        inventory_choice(item=8)
                    else:
                        not_enough_money()
                if quit_button.checkForInput(shop_mouse_pos):
                    shop_type_window()

                if next_button.checkForInput(shop_mouse_pos):
                    continue


        pygame.display.update()


def shop_window1():
    pygame.display.set_caption("SHOP WINDOW 1")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    sprite1 = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite1.png"), (200, 200))
    sprite2 = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite2.png"), (200, 200))
    while 1:

        shop_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        menu_text = get_font(150).render("SHOP", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(440, 100))
        shop_text = get_font(50).render("coins:", True, "#b68f40")
        shop_rect = shop_text.get_rect(center=(900, 100))
        coins_text = get_font(50).render(str(COINS), True, "#b68f40")
        coins_rect = shop_text.get_rect(center=(1200, 100))




        skin1_button = Button(image=sprite1, pos=(350, 300),
                              text_input="700", font=get_font(75), base_color="red", hovering_color="White")

        skin2_button = Button(image=sprite2, pos=(980, 300),
                              text_input="2000", font=get_font(75), base_color="red", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(350, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        next_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="NEXT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")



        for BUTTON in [skin1_button, skin2_button, quit_button, next_button]:
            BUTTON.changeColor(shop_mouse_pos)
            BUTTON.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(shop_text, shop_rect)
        SCREEN.blit(coins_text,coins_rect)


        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if skin1_button.checkForInput(shop_mouse_pos):
                    if ("Images/Sprites/Sprite1.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 700:
                        cash(money=-700)
                        sold()
                        inventory_choice(item=1)

                    else:
                        not_enough_money()

                if skin2_button.checkForInput(shop_mouse_pos):
                    if ("Images/Sprites/Sprite2.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 2000:
                        cash(money=-2000)
                        sold()
                        inventory_choice(item=2)
                    else:
                        not_enough_money()
                if quit_button.checkForInput(shop_mouse_pos):
                    shop_type_window()

                if next_button.checkForInput(shop_mouse_pos):
                    shop_window2()


        pygame.display.update()


def shop_window2():
    pygame.display.set_caption("SHOP WINDOW 2")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    sprite1 = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite3.png"), (200, 200))
    sprite2 = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite4.png"), (200, 200))
    while 1:
        shop_mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        menu_text = get_font(150).render("SHOP", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(440, 100))
        shop_text = get_font(50).render("coins:", True, "#b68f40")
        shop_rect = shop_text.get_rect(center=(900, 100))
        coins_text = get_font(50).render(str(COINS), True, "#b68f40")
        coins_rect = shop_text.get_rect(center=(1200, 100))



        skin1_button = Button(image=sprite1, pos=(350, 300),
                              text_input="2800", font=get_font(75), base_color="red", hovering_color="White")

        skin2_button = Button(image=sprite2, pos=(980, 300),
                              text_input="3500", font=get_font(75), base_color="red", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(350, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        next_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="NEXT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [skin1_button, skin2_button, quit_button, next_button]:
            button.changeColor(shop_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(shop_text, shop_rect)
        SCREEN.blit(coins_text, coins_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if skin1_button.checkForInput(shop_mouse_pos):
                    if ("Images/Sprites/Sprite3.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 2800:
                        cash(money=-2800)
                        sold()
                        inventory_choice(item=4)
                    else:
                        not_enough_money()

                if skin2_button.checkForInput(shop_mouse_pos):
                    if ("Images/Sprites/Sprite4.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 3500:
                        cash(money=-3500)
                        sold()
                        inventory_choice(item=5)
                    else:
                        not_enough_money()
                if quit_button.checkForInput(shop_mouse_pos):
                    shop_window1()

                if next_button.checkForInput(shop_mouse_pos):
                    shop_window3()

        pygame.display.update()

def shop_window3():
    pygame.display.set_caption("SHOP WINDOW 3")
    BG = pygame.transform.scale(pygame.image.load("Images/Background_images/background.png"),
                                (1280, 736)).convert_alpha()
    sprite1 = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite5.png"), (200, 200))
    sprite2 = pygame.transform.scale(pygame.image.load("Images/Sprites/Sprite6.png"), (200, 200))

    while 1:
        SCREEN.blit(BG, (0, 0))
        shop_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(150).render("SHOP", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(440, 100))
        shop_text = get_font(50).render("coins:", True, "#b68f40")
        shop_rect = shop_text.get_rect(center=(900, 100))
        coins_text = get_font(50).render(str(COINS), True, "#b68f40")
        coins_rect = shop_text.get_rect(center=(1200, 100))



        skin1_button = Button(image=sprite1, pos=(350, 300),
                              text_input="4600", font=get_font(75), base_color="red", hovering_color="White")

        skin2_button = Button(image=sprite2, pos=(980, 300),
                              text_input="5000", font=get_font(75), base_color="red", hovering_color="White")

        quit_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(350, 550),
                             text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        next_button = Button(image=pygame.image.load("Images/Rects/Quit Rect.png"), pos=(950, 550),
                             text_input="NEXT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [skin1_button, skin2_button, quit_button, next_button]:
            button.changeColor(shop_mouse_pos)
            button.update(SCREEN)

        SCREEN.blit(menu_text, menu_rect)
        SCREEN.blit(shop_text, shop_rect)
        SCREEN.blit(coins_text, coins_rect)

        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if EVENT.type == pygame.MOUSEBUTTONDOWN:
                click()
                if skin1_button.checkForInput(shop_mouse_pos):
                    if ("Images/Sprites/Sprite5.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 4600:
                        cash(money=-4600)
                        sold()
                        inventory_choice(item=6)
                    else:
                        not_enough_money()

                if skin2_button.checkForInput(shop_mouse_pos):
                    if ("Images/Sprites/Sprite6.png" in INVENTORY_ITEMS) == True:
                        already_bought()
                    elif COINS >= 5000:
                        cash(money=-5000)
                        sold()
                        inventory_choice(item=7)
                    else:
                        not_enough_money()
                if quit_button.checkForInput(shop_mouse_pos):
                    shop_window2()

                if next_button.checkForInput(shop_mouse_pos):
                    continue
                    #shop_window4()
        pygame.display.update()






def get_font(size):
    return pygame.font.Font("Fonts/font.ttf", size)


def not_completed():
    SCREEN.fill((0, 255, 255))
    my_font = pygame.font.SysFont('Comic Sans MS', 100)
    font_render = my_font.render('Complete The Levels ', False, (0, 0, 0))
    font_render2 = my_font.render(' Before To Access', False, (0, 0, 0))
    SCREEN.blit(font_render, (200, 150))
    SCREEN.blit(font_render2, (200, 400))
    pygame.display.update()
    time.sleep(1.5)

def not_completed_levels():
    SCREEN.fill((0, 255, 255))
    my_font = pygame.font.SysFont('Comic Sans MS', 100)
    font_render = my_font.render('Complete Level 5', False, (0, 0, 0))
    font_render2 = my_font.render(' To Access Free Play', False, (0, 0, 0))
    SCREEN.blit(font_render, (200, 150))
    SCREEN.blit(font_render2, (200, 400))
    pygame.display.update()
    time.sleep(1.5)

def wasted():
    time.sleep(0.05)
    pygame.image.save(SCREEN, "Images/screenshot_death.jpg")
    music_effect(sound_effect=1)
    death_animation()
    time.sleep(0.3)
    level_music(level=0)
    remove_bullets()


def already_bought():
    previous_time = pygame.time.get_ticks()

    while 1:
        current_time = pygame.time.get_ticks()
        color = (255, 0, 0)
        SCREEN.fill(color, (150, 460, SCREEN.get_width() // 1.3, SCREEN.get_height() // 5))
        my_font = pygame.font.SysFont('Comic Sans MS', 130)
        font_render = my_font.render('Already Bought', False, (0, 0, 0))
        SCREEN.blit(font_render, (180, 420))
        pygame.display.update()

        if current_time - previous_time >= 500:
            break



def not_enough_money():
    previous_time = pygame.time.get_ticks()

    while 1:
        current_time = pygame.time.get_ticks()
        color = (255, 0, 0)
        SCREEN.fill(color, (150, 460, SCREEN.get_width() // 1.3, SCREEN.get_height() // 5))
        my_font = pygame.font.SysFont('Comic Sans MS', 150)
        font_render = my_font.render('Your Broke', False, (0, 0, 0))
        SCREEN.blit(font_render, (250, 420))
        pygame.display.update()

        if current_time - previous_time >= 500:
            break



def sold():
    previous_time = pygame.time.get_ticks()

    while 1:
        current_time = pygame.time.get_ticks()
        color = (0, 255, 255)
        SCREEN.fill(color, (150, 460, SCREEN.get_width() // 1.3, SCREEN.get_height() // 5))
        my_font = pygame.font.SysFont('Comic Sans MS', 150)
        font_render = my_font.render('Item Sold', False, (0, 0, 0))
        SCREEN.blit(font_render, (250, 420))
        pygame.display.update()

        if current_time - previous_time >= 500:
            break


def character_selected():
    previous_time = pygame.time.get_ticks()

    while 1:
        current_time = pygame.time.get_ticks()
        color = (0, 255, 255)
        SCREEN.fill(color, (150, 460, SCREEN.get_width() // 1.3, SCREEN.get_height() // 5))
        my_font = pygame.font.SysFont('Comic Sans MS', 100)
        font_render = my_font.render('Character Selected', False, (0, 0, 0))
        SCREEN.blit(font_render, (190, 440))
        pygame.display.update()

        if current_time - previous_time >= 500:
            inventory_window()


def inventory_choice(item):
    global INVENTORY_ITEMS


    INVENTORY_ITEMS.append((base.sprite_images[item]))


def not_owned():
    previous_time = pygame.time.get_ticks()

    while 1:
        current_time = pygame.time.get_ticks()
        color = (255, 0, 0)
        SCREEN.fill(color, (150, 460, SCREEN.get_width() // 1.3, SCREEN.get_height() // 5))
        my_font = pygame.font.SysFont('Comic Sans MS', 150)
        font_render = my_font.render('Not Owned', False, (0, 0, 0))
        SCREEN.blit(font_render, (250, 420))
        pygame.display.update()

        if current_time - previous_time >= 500:

            inventory_window()


def random_number():
    global RANDOM_NUMBER
    RANDOM_NUMBER = randint(75, 80)


class CameraAwareLayeredUpdates(pygame.sprite.LayeredUpdates):
    def __init__(self, target, world_size):
        super().__init__()
        self.target = target
        self.cam = pygame.Vector2(0, 0)
        self.world_size = world_size
        if self.target:
            self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target:
            x = -self.target.rect.center[0] + SCREEN_SIZE.width / 2
            y = -self.target.rect.center[1] + SCREEN_SIZE.height / 2
            self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.5
            self.cam.x = max(-(self.world_size.width - SCREEN_SIZE.width), min(0, self.cam.x))
            self.cam.y = max(-(self.world_size.height - SCREEN_SIZE.height), min(0, self.cam.y))

    def draw(self, surface):
        spritedict = self.spritedict
        surface_blit = surface.blit
        dirty = self.lostsprites
        self.lostsprites = []
        dirty_append = dirty.append
        init_rect = self._init_rect
        for spr in self.sprites():
            rec = spritedict[spr]
            newrect = surface_blit(spr.image, spr.rect.move(self.cam))
            if rec is init_rect:
                dirty_append(newrect)
            else:
                if newrect.colliderect(rec):
                    dirty_append(newrect.union(rec))
                else:
                    dirty_append(newrect)
                    dirty_append(rec)
            spritedict[spr] = newrect
        return dirty


def map_choice(level):
    level_music(level)
    if level == 1:
        main(Map = (open("Maps/map1")))
    if level == 2:
        main(Map = (open("Maps/map2")))
    if level == 3:
        main(Map = (open("Maps/map3")))
    if level == 4:
        main(Map = (open("Maps/map4")))
    if level == 5:
        main(Map = (open("Maps/map5")))
    if level == 6:
        main(Map = (open("Maps/map6")))
    if level == 7:
        main(Map = (open("Maps/map7")))




def allowed_maps(completed_maps):
    global ALLOWED_LEVELS
    if completed_maps > ALLOWED_LEVELS:
        ALLOWED_LEVELS = completed_maps

    return ALLOWED_LEVELS


def cash(money):
    global COINS
    COINS += money

def remove_bullets():
    global BULLETS
    global ENEMY_BULLETS
    BULLETS = []
    ENEMY_BULLETS = []



def random_map_castle():
    map_list2 = []
    map_list = [r"Map_Segments/segment_start",
                r"Map_Segments/segment_end"]

    segment_names = (r"Map_Segments/segment_1",
                     r"Map_Segments/segment_2",
                     r"Map_Segments/segment_3",
                     r"Map_Segments/segment_4",
                     r"Map_Segments/segment_5",
                     r"Map_Segments/segment_6",
                     r"Map_Segments/segment_7",
                     r"Map_Segments/segment_8",
                     r"Map_Segments/segment_9",
                     r"Map_Segments/segment_10",
                     r"Map_Segments/segment_11",
                     r"Map_Segments/segment_12",
                     r"Map_Segments/segment_13",
                     r"Map_Segments/segment_14",
                     r"Map_Segments/segment_15")


    map_list2.append(map_list[0])
    num_maps = (len(segment_names))-1

    for i in range(RANDOM_NUMBER):
        random_number2 = randint(0, num_maps)
        map_list2.append(segment_names[random_number2])

    map_list2.append(map_list[1])
    lines = []
    for map_segment in map_list2:
        with open(map_segment) as f:
            for line_num, line in enumerate(f):
                if line_num == len(lines):
                    lines.append(line.strip())
                else:
                    lines[line_num] += line.strip()


    with open("Maps/map_FreePlay", "w") as generated_map:
        generated_map.write(("\n".join(line for line in lines)))
        free_play_castle(segment=(open("Maps/map_FreePlay")))

def random_map_normal():
    map_list2 = []
    map_list = [r"Map_Segments/old_segments/segment_start",
                r"Map_Segments/old_segments/segment_end"]

    segment_names = (r"Map_Segments/old_segments/segment_1",
                     r"Map_Segments/old_segments/segment_2",
                     r"Map_Segments/old_segments/segment_3",
                     r"Map_Segments/old_segments/segment_4",
                     r"Map_Segments/old_segments/segment_5",
                     r"Map_Segments/old_segments/segment_6",
                     r"Map_Segments/old_segments/segment_7",
                     r"Map_Segments/old_segments/segment_8",
                     r"Map_Segments/old_segments/segment_9",
                     r"Map_Segments/old_segments/segment_10",
                     r"Map_Segments/old_segments/segment_11",
                     r"Map_Segments/old_segments/segment_12",
                     r"Map_Segments/old_segments/segment_13",
                     r"Map_Segments/old_segments/segment_14",
                     r"Map_Segments/old_segments/segment_15",
                     r"Map_Segments/old_segments/segment_16",
                     r"Map_Segments/old_segments/segment_17",
                     r"Map_Segments/old_segments/segment_18",
                     r"Map_Segments/old_segments/segment_19")



    map_list2.append(map_list[0])
    num_maps = (len(segment_names))-1
    #map_list2.append((segment_names[18]))

    for i in range(RANDOM_NUMBER):
        print(RANDOM_NUMBER)
        random_number2 = randint(0, num_maps)
        map_list2.append(segment_names[random_number2])
    map_list2.append(map_list[1])
    lines = []
    for map in map_list2:
        with open(map) as f:
            for line_num, line in enumerate(f):
                if line_num == len(lines):
                    lines.append(line.strip())
                else:
                    lines[line_num] += line.strip()



    with open("Maps/map_FreePlay", "w") as generated_map:
        generated_map.write(("\n".join(line for line in lines)))
        free_play_normal(segment=(open("Maps/map_FreePlay")))


def continue_free_map():
    random_number_2 = randint(3, 6)
    map_list2 = []

    segment_names = (r"Map_Segments/old_segments/segment_1",
                     r"Map_Segments/old_segments/segment_2",
                     r"Map_Segments/old_segments/segment_3",
                     r"Map_Segments/old_segments/segment_4",
                     r"Map_Segments/old_segments/segment_5",
                     r"Map_Segments/old_segments/segment_6",
                     r"Map_Segments/old_segments/segment_7",
                     r"Map_Segments/old_segments/segment_8",
                     r"Map_Segments/old_segments/segment_9",
                     r"Map_Segments/old_segments/segment_10",
                     r"Map_Segments/old_segments/segment_11",
                     r"Map_Segments/old_segments/segment_12",
                     r"Map_Segments/old_segments/segment_13",
                     r"Map_Segments/old_segments/segment_14",
                     r"Map_Segments/old_segments/segment_15",
                     r"Map_Segments/old_segments/segment_16",
                     r"Map_Segments/old_segments/segment_17",
                     r"Map_Segments/old_segments/segment_18",
                     r"Map_Segments/old_segments/segment_19")


    num_maps = (len(segment_names)) - 1
    for i in range (random_number_2):
        random_number2 = randint(0, num_maps)
        map_list2.append(segment_names[random_number2])
        lines = []
    for map in map_list2:
        with open(map) as f:
            for line_num, line in enumerate(f):
                if line_num == len(lines):
                    lines.append(line.strip())
                else:
                    lines[line_num] += line.strip()

    with open("Maps/map_FreePlay", "w") as generated_map:
        generated_map.write(("\n".join(line for line in lines)))
        print("check")





def free_play_castle(segment):
    global bullet_y
    global bullet_x
    background = pygame.transform.scale(pygame.image.load("Images/Background_images/free_play_background_castle.png"),
                                        (1280, 736)).convert_alpha()
    bullet_picture = pygame.transform.scale(pygame.image.load("Images/bullet.png"), (64, 32)).convert_alpha()
    time.sleep(0.3)
    SCREEN.fill((255, 0, 0))
    my_font = pygame.font.SysFont('Comic Sans MS', 200)
    font_render = my_font.render('LOADING...', False, (0, 0, 0))
    SCREEN.blit(font_render, (100, 150))
    pygame.display.update()
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Free Play Mode")
    timer = pygame.time.Clock()

    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE))
    level_width = MAP_BORDER[0] * TILE_SIZE
    level_height = MAP_BORDER[1] * TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(32, 0, level_width, level_height))

    # build the map_border
    x = y = 0
    for row in segment:
        for col in row:
            if col == "P":
                PlatBasicFree((x, y), platforms, entities)
            if col == "E":
                PlatExitFreeUp((x, y), platforms, entities)
            if col == "F":
                PlatSpeedF((x, y), platforms, entities)
            if col == "H":
                PlatSpeedH((x, y), platforms, entities)
            if col == "M":
                PlatSpeedM((x, y), platforms, entities)
            if col == "L":
                PlatSpeedL((x, y), platforms, entities)
            if col == "N":
                PlatNorm((x, y), platforms, entities)
            if col == "J":
                PlatJumpH((x, y), platforms, entities)
            if col == "G":
                PlatJumpM((x, y), platforms, entities)
            if col == "S":
                PlatNext((x, y), platforms, entities)
            if col == "=":
                PlatLevelEnd((x, y), platforms, entities)
            if col == "C":
                PlatCoins((x, y), platforms, entities)
            if col == "<":
                PlatExitFreeLeft((x, y), platforms, entities)
            if col == ">":
                PlatExitFreeRight((x, y), platforms, entities)
            if col == "e":
                PlatExitFreeDown((x, y), platforms, entities)
            if col == "S":
                PlatFreeStick((x, y), platforms, entities)
            if col == "0":
                PlatMovingCastle((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    free_play_music()


    while 1:

        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                level_music(level=0)
                remove_bullets()
                return

        bullet_x = player.rect[0]
        bullet_y = player.rect[1]



        entities.update()
        SCREEN.blit(background, (0, 0))
        for bullet in BULLETS:
            SCREEN.blit(bullet_picture, pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))
        entities.draw(screen)
        pygame.display.update()
        for p in platforms:
            for bullet in BULLETS:
                collide = bullet.colliderect(p.rect)

                if collide:
                    print(p.rect)
                    print(bullet)
                    BULLETS.remove(bullet)
        entities.draw(screen)
        pygame.display.update()
        timer.tick(60)

def free_play_normal(segment):
    global bullet_y
    global bullet_x
    bullet_picture = pygame.transform.scale(pygame.image.load("Images/bullet.png"), (64, 32)).convert_alpha()
    background = pygame.transform.scale(pygame.image.load("Images/Background_images/menu_background.png"),
                                        (1280, 736)).convert_alpha()

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Level Mode")
    timer = pygame.time.Clock()

    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE))
    level_width = MAP_BORDER[0] * TILE_SIZE
    level_height = MAP_BORDER[1] * TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))

    shop_text = get_font(50).render("coins:", True, "#b68f40")
    shop_rect = shop_text.get_rect(center=(180, 630))

    coins_rect = shop_text.get_rect(center=(180, 700))

    # build the map_border
    x = y = 0
    for row in segment:
        for col in row:
            if col == "=":
                PlatLevelEnd((x, y), platforms, entities)
            if col == "P":
                PlatBasic((x, y), platforms, entities)
            if col == "D":
                PlatEnemy((x, y), platforms, entities)
            if col == "E":
                PlatExitNorm((x, y), platforms, entities)
            if col == "F":
                PlatSpeedF((x, y), platforms, entities)
            if col == "H":
                PlatSpeedH((x, y), platforms, entities)
            if col == "M":
                PlatSpeedM((x, y), platforms, entities)
            if col == "L":
                PlatSpeedL((x, y), platforms, entities)
            if col == "N":
                PlatNormNorm((x, y), platforms, entities)
            if col == "J":
                PlatJumpH((x, y), platforms, entities)
            if col == "G":
                PlatJumpM((x, y), platforms, entities)
            if col == "2":
                PlatLevel2((x, y), platforms, entities)
            if col == "3":
                PlatLevel3((x, y), platforms, entities)
            if col == "4":
                PlatLevel4((x, y), platforms, entities)
            if col == "5":
                PlatLevel5((x, y), platforms, entities)
            if col == "6":
                PlatLevel6((x, y), platforms, entities)
            if col == "7":
                PlatLevel3((x, y), platforms, entities)
            if col == "0":
                PlatMoving((x, y), platforms, entities)
            if col == "C":
                PlatCoinsNorm((x, y), platforms, entities)
            if col == "S":
                PlatFreeStick((x, y), platforms, entities)
            if col == "0":
                PlatMoving((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    free_play_music()

    previous_time = pygame.time.get_ticks() + 3
    enemy_list = []
    counter = 0
    while 1:

        coins_text = get_font(50).render(str(COINS), True, "#b68f40")
        dead = False

        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                level_music(level=0)
                remove_bullets()
                return

        bullet_x = player.rect[0]
        bullet_y = player.rect[1]
        drawn_entities = []
        current_time = pygame.time.get_ticks()

        entities.update()
        screen.blit(background, (0, 0))
        for bullet in BULLETS:
            SCREEN.blit(bullet_picture, pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))
        for bullet in ENEMY_BULLETS:
            SCREEN.blit(pygame.transform.rotate(bullet_picture, -180),
                        pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))

        for platform in platforms:
            if platform.rect[0] - player.rect[0] < 1500:
                drawn_entities.append(platform)




        for b in range(len(ENEMY_BULLETS)):
            ENEMY_BULLETS[b][0] -= 6

        for p in drawn_entities:
            screen.blit(p.image, pygame.Rect(p.rect[0] + entities.cam[0],p.rect[1] + entities.cam[1], 32, 32))
            temp = str(p)
            if "PlatEnemy" in temp:
                if p not in enemy_list:
                    enemy_list.append(p)

            for bullet in ENEMY_BULLETS:
                if bullet.colliderect(p.rect):
                    ENEMY_BULLETS.remove(bullet)
                if bullet.colliderect(player):
                    dead = True

            for bullet in BULLETS:
                for bullet2 in ENEMY_BULLETS:
                    if bullet2.colliderect(bullet):
                        ENEMY_BULLETS.remove(bullet2)
                        BULLETS.remove(bullet)
                if bullet.colliderect(p.rect):
                    BULLETS.remove(bullet)
                    if "PlatEnemy" in temp:
                        enemy_list.remove(p)
                        p.kill()

            if current_time - previous_time > 4000:
                for enemy in enemy_list:
                    ENEMY_BULLETS.append(pygame.Rect(enemy.rect[0] - 100, enemy.rect[1], 32, 32))
                    shoot_sound()
                previous_time = current_time

            if (p.rect[0] - player.rect[0]) < -1500:
                if "PlatMoving" in temp:
                    continue
                else:
                    counter += 1
                    p.kill()

            if counter == 15:
                cash(money=randint(0, 5))
                counter = 0




        screen.blit(shop_text, shop_rect)
        screen.blit(coins_text, coins_rect)

        screen.blit(player.image, pygame.Rect(player.rect[0] + entities.cam[0], player.rect[1] + entities.cam[1], 32, 32))
        pygame.display.update()

        if dead == True:
            wasted()
            free_play_window()



        timer.tick(60)


def main(Map):
    global bullet_y
    global bullet_x
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE.size)
    pygame.display.set_caption("Level Mode")
    timer = pygame.time.Clock()
    background = pygame.transform.scale(pygame.image.load("Images/Background_images/menu_background.png"),
                                        (1280, 736)).convert_alpha()
    bullet_picture = pygame.transform.scale(pygame.image.load("Images/bullet.png"), (64, 32)).convert_alpha()
    platforms = pygame.sprite.Group()
    player = Player(platforms, (TILE_SIZE, TILE_SIZE))
    level_width = MAP_BORDER[0] * TILE_SIZE
    level_height = MAP_BORDER[1] * TILE_SIZE
    entities = CameraAwareLayeredUpdates(player, pygame.Rect(0, 0, level_width, level_height))
    # build the map_border

    x = y = 0
    for row in Map:
        for col in row:
            if col == "P":
                PlatBasic((x, y), platforms, entities)
            if col == "D":
                PlatEnemy((x, y), platforms, entities)
            if col == "E":
                PlatExit((x, y), platforms, entities)
            if col == "F":
                PlatSpeedF((x, y), platforms, entities)
            if col == "H":
                PlatSpeedH((x, y), platforms, entities)
            if col == "M":
                PlatSpeedM((x, y), platforms, entities)
            if col == "L":
                PlatSpeedL((x, y), platforms, entities)
            if col == "N":
                PlatNorm((x, y), platforms, entities)
            if col == "J":
                PlatJumpH((x, y), platforms, entities)
            if col == "G":
                PlatJumpM((x, y), platforms, entities)
            if col == "2":
                PlatLevel2((x, y), platforms, entities)
            if col == "3":
                PlatLevel3((x, y), platforms, entities)
            if col == "4":
                PlatLevel4((x, y), platforms, entities)
            if col == "5":
                PlatLevel5((x, y), platforms, entities)
            if col == "6":
                PlatLevel6((x, y), platforms, entities)
            if col == "7":
                PlatLevel3((x, y), platforms, entities)
            if col == "0":
                PlatMoving((x, y), platforms, entities)
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    previous_time = pygame.time.get_ticks()
    enemy_list = []

    while 1:

        dead = False

        for e in pygame.event.get():
            if e.type == QUIT:
                return
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                level_music(level=0)
                remove_bullets()
                return

        bullet_x = player.rect[0]
        bullet_y = player.rect[1]

        current_time = pygame.time.get_ticks()

        entities.update()
        screen.blit(background, (0, 0))

        for bullet in BULLETS:
            SCREEN.blit(bullet_picture, pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))
        for bullet in ENEMY_BULLETS:
            SCREEN.blit(pygame.transform.rotate(bullet_picture, -180), pygame.Rect(bullet[0] + entities.cam[0], bullet[1] + entities.cam[1], 32, 32))

        for b in range(len(ENEMY_BULLETS)):
            ENEMY_BULLETS[b][0] -= 6

        for p in platforms:
            temp = str(p)
            if "PlatEnemy" in temp:
                if p not in enemy_list:
                    enemy_list.append(p)

            for bullet in ENEMY_BULLETS:
                if bullet.colliderect(p.rect):
                    ENEMY_BULLETS.remove(bullet)
                if bullet.colliderect(player):
                    dead = True


            for bullet in BULLETS:
                for bullet2 in ENEMY_BULLETS:
                    if bullet2.colliderect(bullet):
                        ENEMY_BULLETS.remove(bullet2)
                        BULLETS.remove(bullet)
                if bullet.colliderect(p.rect):
                    BULLETS.remove(bullet)
                    if "PlatEnemy" in temp:
                        enemy_list.remove(p)
                        p.kill()



            if current_time - previous_time > 4000:
                for enemy in enemy_list:
                    ENEMY_BULLETS.append(pygame.Rect(enemy.rect[0] - 100, enemy.rect[1], 32, 32))
                    shoot_sound()
                previous_time = current_time


        entities.draw(screen)
        pygame.display.update()

        if dead == True:
            wasted()
            levels_window()

        timer.tick(60)


class Entity(pygame.sprite.Sprite):
    def __init__(self, color, pos, *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topright=pos)

    def update(self, **kwargs):
        if kwargs.get('x'):
            self.rect.x = kwargs.get('x')

class Bullet(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#5aa2e0"), pos)
        self.image = pygame.transform.scale(pygame.image.load("Images/bullets.png"), (32, 32)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(bullet_x, bullet_y)
        self.vel = pygame.math.Vector2(0, 0)
        self.damage = 10
        self.speed = 10

    def update(self):
        # Add the velocity to the position vector to move the sprite.
        self.pos += self.vel.x + self.speed
        self.rect.center = self.pos  # Update the rect pos.
        if self.rect.bottom <= 0:
            self.kill()

    def collide(self, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                Bullet.kill(self)


class Player(Entity):
    def __init__(self, platforms, pos, *groups):
        super().__init__(Color("#5aa2e0"), pos)
        self.image = pygame.transform.scale(pygame.image.load(CHARACTER_SKINS), (32, 32)).convert_alpha()
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.speed = 8
        self.jump_strength = 10
        self.right = False
        self.left = False
        self.previous_time = pygame.time.get_ticks()


    def update(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_SPACE] or pressed[K_w]
        left = pressed[K_LEFT] or pressed[K_a]
        right = pressed[K_RIGHT] or pressed[K_d]
        shoot = pressed[K_UP]
        quit = pressed[K_ESCAPE]

        if quit:
            pygame.quit()
            sys.exit()

        if up:
            if self.onGround:
                jump_effect()
                if self.left is True:
                    self.vel.y = -self.jump_strength
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.right is True:
                    self.vel.y = -self.jump_strength
                    self.image = pygame.transform.rotate(self.image, -90)
                else:
                    self.vel.y = -self.jump_strength

        if left:
            self.vel.x = -self.speed
            self.left = True
            self.right = False

        if right:
            self.vel.x = self.speed
            self.right = True
            self.left = False



        if not self.onGround:


            # only accelerate with gravity if in the air
            self.vel += GRAVITY


            # max falling speed
            if self.vel.y > 100:
                self.vel.y = 100



        if shoot:
            current_time = pygame.time.get_ticks()
            # fire when 500 ms have passed.
            if current_time - self.previous_time > 1000:
                BULLETS.append(pygame.Rect(bullet_x, bullet_y, 32, 32))
                shoot_sound()
                self.previous_time = current_time

        for b in range(len(BULLETS)):
            BULLETS[b][0] += 10


        if not (left or right):
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        # do x-axis collisions
        self.collide(self.vel.x, 0, self.platforms)
        # increment in y direction
        self.rect.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.vel.y, self.platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, PlatExit):
                    wasted()
                    levels_window()

                if isinstance(p, PlatMoving):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatMovingCastle):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatExitNorm):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatExitFreeUp):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatExitFreeLeft):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatExitFreeRight):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatExitFreeDown):
                    wasted()
                    free_play_window()

                if isinstance(p, PlatCoins):
                    cash(money=randint(0, 10))

                if isinstance(p, PlatCoinsNorm):
                    cash(money=randint(0, 10))


                if isinstance(p, PlatLevelEnd):
                    cash(money=RANDOM_NUMBER*randint(40, 80))
                    level_music(level=0)
                    free_play_window()

                if isinstance(p, PlatLevel2):
                    cash(money=10)
                    allowed_maps(completed_maps=1)
                    map_choice(level=2)

                if isinstance(p, PlatLevel3):
                    cash(money=20)
                    allowed_maps(completed_maps=2)
                    map_choice(level=3)

                if isinstance(p, PlatLevel4):
                    cash(money=30)
                    allowed_maps(completed_maps=3)
                    map_choice(level=4)

                if isinstance(p, PlatLevel5):
                    cash(money=40)
                    allowed_maps(completed_maps=4)
                    map_choice(level=5)

                if isinstance(p, PlatLevel6):
                    cash(money=50)
                    allowed_maps(completed_maps=5)
                    map_choice(level=6)

                if isinstance(p, PlatLevel7):
                    cash(money=60)
                    allowed_maps(completed_maps=8)
                    map_choice(level=7)

                if isinstance(p, PlatSpeedF):
                    self.speed = 300

                if isinstance(p, PlatSpeedH):
                    self.speed = 50
                if isinstance(p, PlatSpeedM):
                    self.speed = 16
                if isinstance(p, PlatSpeedL):
                    self.speed = 5


                if isinstance(p, PlatNorm):
                    self.speed = 8
                    self.jump_strength = 10

                if isinstance(p, PlatNormNorm):
                    self.speed = 8
                    self.jump_strength = 10

                if isinstance(p, PlatJumpH):
                    self.jump_strength = 30

                if isinstance(p, PlatJumpM):
                    self.jump_strength = 15


                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.vel.y = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom





class PlatMoving(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)
        self.speed = 6.5
        self.vel = pygame.Vector2((-2000, 0))
        self.onGround = False
        self.count = 0

    def update(self):
        self.vel.x += 1 * self.speed
        super().update(x=self.vel.x)



    def collide(self, platforms, xvel, yvel):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.vel.x *= -1
                super().update(x=self.vel.x)


class PlatEnemy(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatMovingCastle(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/spikes/Individual Spike.png"),(32, 32)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.speed = 7
        self.vel = pygame.Vector2((-8000, 0))
        self.onGround = False
        self.count = 0

    def update(self):
        self.vel.x += 1 * self.speed
        super().update(x=self.vel.x)



    def collide(self, platforms, xvel, yvel):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.vel.x *= -1
                super().update(x=self.vel.x)



class PlatLevelEnd(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)

class PlatFreeStick(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatLevel2(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatLevel3(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatLevel4(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatLevel5(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatLevel6(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatLevel7(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


class PlatBasic(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#10eb93"), pos, *groups)

class PlatCoinsNorm(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#10eb93"), pos, *groups)



class PlatBasicFree(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#10eb93"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/Background_images/wall_basic.png"), (32, 32)).convert_alpha()

class PlatCoins(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#10eb93"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/Background_images/wall_basic.png"), (32, 32)).convert_alpha()






class PlatExit(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)


class PlatExitNorm(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)



class PlatExitFreeUp(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/spikes/Individual Spike.png"), (32, 32)).convert_alpha()

class PlatExitFreeLeft(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/spikes/Individual Spike.png"), (32, 32)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)

class PlatExitFreeRight(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/spikes/Individual Spike.png"), (32, 32)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)

class PlatExitFreeDown(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#c40c0c"), pos, *groups)
        self.image = pygame.transform.scale(pygame.image.load("Images/spikes/Individual Spike.png"), (32, 32)).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)


class PlatSpeedF(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatSpeedH(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatSpeedM(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatSpeedL(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatNorm(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
        #self.image = pygame.transform.scale(pygame.image.load("Images/Background_images/wall_basic.png"), (32, 32)).convert_alpha()

class PlatNormNorm(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)



class PlatJumpH(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatJumpM(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatImmune(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)


class PlatNext(Entity):
    def __init__(self, pos, *groups):
        super().__init__(Color("#b154eb"), pos, *groups)


def level_music(level):
    music = ["Music/madirfan-hidden-place-extended-version-13891.ogg",
             "Music/this-minimal-technology-pure-12327.ogg",
             "Music/slow-trap-18565.ogg",
             "Music/bensound-summer_ogg_music.ogg",
             "Music/tropical-house-112360.ogg",
             "Music/sport-fashion-rock-95426.ogg",
             "Music/sport-fashion-rock-95426.ogg",
             "Music/sport-fashion-rock-95426.ogg "]
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.Channel(0).set_volume(0.3)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(music[level]))



def free_play_music():
    music = ["Music/madirfan-hidden-place-extended-version-13891.ogg",
             "Music/this-minimal-technology-pure-12327.ogg",
             "Music/slow-trap-18565.ogg",
             "Music/bensound-summer_ogg_music.ogg",
             "Music/tropical-house-112360.ogg",
             "Music/sport-fashion-rock-95426.ogg",
             "Music/sport-fashion-rock-95426.ogg",
             "Music/sport-fashion-rock-95426.ogg "]
    music_number = randint(1, 7)
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.Channel(0).set_volume(0.3)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(music[music_number]))



def music_effect(sound_effect):
    music = ["Music/gta-v-death-sound-effect-102.ogg"]
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.Channel(0).set_volume(1)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(music[sound_effect-1]))

def jump_effect():
    music = ["Music/jump.ogg"]
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(music[0]), maxtime=300)

def click():
    music = ["Music/click.ogg"]
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(music[0]), maxtime=250)

def shoot_sound():
    music = ["Music/shoot.wav"]
    pygame.mixer.pre_init()
    pygame.mixer.init()
    pygame.mixer.Channel(3).play(pygame.mixer.Sound(music[0]), maxtime=1000)

async def main():
    while States.draw():
        pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit(0)


States.select("Menu_start")

if __name__ == "__main__":
    asyncio.run(main())



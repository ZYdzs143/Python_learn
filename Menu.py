import pygame
from pygame.locals import*

#  抽象菜单类
class MenuAbstract(object):
    choice = 0  # 记录选项
    num = 0  # 选项数量
    #  选项位置
    rect = [Rect((225, 100, 150, 50)), Rect((225, 170, 150, 50)), Rect((225, 240, 150, 50)), Rect((225, 310, 150, 50))]
    #  选项图片
    start_img = pygame.image.load("./img/开始游戏.png")
    quit_img = pygame.image.load("./img/退出游戏.png")
    continue_img = pygame.image.load("./img/继续游戏.png")
    restart_img = pygame.image.load("./img/重新开始.png")
    hard_level = pygame.image.load("./img/难度选择.png")
    music = pygame.image.load("./img/音乐选项.png")
    easy = pygame.image.load("./img/简单.png")
    normal = pygame.image.load("./img/普通.png")
    hard = pygame.image.load("./img/困难.png")
    bgm_open = pygame.image.load("./img/背景音乐开.png")
    bgm_close = pygame.image.load("./img/背景音乐关.png")
    sound_open = pygame.image.load("./img/吃音效开.png")
    sound_close = pygame.image.load("./img/吃音效关.png")
    back = pygame.image.load("./img/返回上级.png")

    #  显示菜单
    def show_menu(self, screen):
        pass

    #  上下键选择选项
    def choose_menu(self, screen, key, num):
        if key == K_DOWN:
            pygame.draw.rect(screen, 'Cyan', self.rect[self.choice], 5)
            self.choice += 1
            if self.choice == num + 1:
                self.choice = 0
            pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)
        elif key == K_UP:
            pygame.draw.rect(screen, 'Cyan', self.rect[self.choice], 5)
            self.choice -= 1
            if self.choice == -1:
                self.choice = num
            pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)


#  开始界面一级菜单类
class Menu1Start(MenuAbstract):
    num = 3

    def show_menu(self, screen):
        screen.blit(self.start_img, self.rect[0])
        screen.blit(self.music, self.rect[1])
        screen.blit(self.hard_level, self.rect[2])
        screen.blit(self.quit_img, self.rect[3])
        pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)


#   暂停界面一级菜单类
class Menu1Pause(MenuAbstract):
    num = 2

    def show_menu(self, screen):
        screen.blit(self.continue_img, self.rect[0])
        screen.blit(self.music, self.rect[1])
        screen.blit(self.quit_img, self.rect[2])
        pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)


#  结束界面一级菜单类
class Menu1End(MenuAbstract):
    num = 3

    def show_menu(self, screen):
        screen.blit(self.restart_img, self.rect[0])
        screen.blit(self.music, self.rect[1])
        screen.blit(self.hard_level, self.rect[2])
        screen.blit(self.quit_img, self.rect[3])
        pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)


#  音乐界面二级菜单类
class Menu2Music(MenuAbstract):
    num = 2
    bgm = False  # 背景音乐开关
    eat_sound = False  # 吃东西音效开关

    def show_menu(self, screen):
        if self.bgm:
            screen.blit(self.bgm_open, self.rect[0])
        else:
            screen.blit(self.bgm_close, self.rect[0])
        if self.eat_sound:
            screen.blit(self.sound_open, self.rect[1])
        else:
            screen.blit(self.sound_close, self.rect[1])
        screen.blit(self.back, self.rect[2])
        pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)


#  难度界面二级菜单类
class Menu2Hard(MenuAbstract):
    num = 2

    def show_menu(self, screen):
        screen.blit(self.easy, self.rect[0])
        screen.blit(self.normal, self.rect[1])
        screen.blit(self.hard, self.rect[2])
        pygame.draw.rect(screen, 'BLACK', self.rect[self.choice], 5)

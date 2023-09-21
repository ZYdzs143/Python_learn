import sys
import random
from Menu import*
from collections import deque

Screen_Width = 600  # 窗口宽度
Screen_Height = 480  # 窗口长度
size = 20  # 小方格长宽


#  蛇类
class Snake:
    #  初始化蛇身坐标，速度，长度
    def __init__(self):
        self.snake_pos = deque([(300, 240), (320, 240), (340, 240)])  # 蛇尾--->蛇头
        self.snake_speed = 5
        self.snake_len = 3
        self.direct = random.choice([[1, 0], [0, 1], [0, -1]])
        self.score = 0

    #  移动方法
    def move(self, change, hard_level):
        #  此为一般移动方法，如果吃到食物就删掉蛇尾坐标，添加一个新的蛇头坐标
        #  难度二和三均不可穿墙，所以这亦是难度二或三对应的移动方法
        if not change:
            self.snake_pos.popleft()
        self.snake_pos.append((self.snake_pos[-1][0]+self.direct[0]*size, self.snake_pos[-1][1]+self.direct[1]*size))
        #  难度一移动方法，可以穿墙，如果蛇头撞墙就删掉蛇头坐标同时新增一个蛇头坐标
        if hard_level == 0:
            if self.snake_pos[-1][0] == Screen_Width:
                self.snake_pos.pop()
                self.snake_pos.append((0, self.snake_pos[-1][1]+self.direct[1]*size))
            elif self.snake_pos[-1][0] == -20:
                self.snake_pos.pop()
                self.snake_pos.append((Screen_Width-size, self.snake_pos[-1][1]+self.direct[1]*size))
            elif self.snake_pos[-1][1] == Screen_Height:
                self.snake_pos.pop()
                self.snake_pos.append((self.snake_pos[-1][0]+self.direct[0]*size, 2*size))
            elif self.snake_pos[-1][1] == size:
                self.snake_pos.pop()
                self.snake_pos.append((self.snake_pos[-1][0]+self.direct[0]*size, Screen_Height-size))

    #  遍历蛇身坐标，画蛇
    def draw_snake(self, screen):
        for s in self.snake_pos:
            pygame.draw.rect(screen, 'WHITE', pygame.Rect((s[0]+1, s[1]+1, size-1, size-1)))


#  食物类
class Food:
    #  初始化食物坐标, 并生成初始食物坐标
    def __init__(self, snake_pos):
        self.food_x = None
        self.food_y = None
        self.create_food(1, snake_pos)

    #  生成食物
    def create_food(self, change, snake_pos):
        #  change=True:吃到
        #  随机生成一个食物坐标，若与蛇身坐标重合，重新生成
        while change:
            self.food_x = size*random.randint(0, Screen_Width//size-1)
            self.food_y = size*random.randint(2, Screen_Height//size-1)
            if (self.food_x, self.food_y) not in snake_pos:
                break

    #  画食物
    def draw_food(self, screen):
        pygame.draw.rect(screen, 'RED', pygame.Rect(self.food_x, self.food_y, size, size))

    #  判断是否吃到食物
    def check_food(self, snake_pos):
        #  食物坐标==蛇头坐标，吃到食物，返回True
        return self.food_x == snake_pos[-1][0] and self.food_y == snake_pos[-1][1]


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('D:/music/WITCHES_DANCE.mp3')
        pygame.mixer.music.set_volume(0.1)
        self.sound = pygame.mixer.Sound('D:/music/吃东西.mp3')
        # 创建一个窗口,设置标题,填充背景颜色,画小方格
        self.screen = pygame.display.set_mode((Screen_Width, Screen_Height))
        pygame.display.set_caption('143贪吃蛇')
        self.screen.fill('LightBlue4')
        self.draw_line()
        # 实例化菜单类
        self.menu1s = Menu1Start()
        self.menu1p = Menu1Pause()
        self.menu1e = Menu1End()
        self.menu2m = Menu2Music()
        self.menu2h = Menu2Hard()
        # 实例化蛇类和食物类
        self.snake = Snake()
        self.food = Food(self.snake.snake_pos)
        # 实例化一个时钟类，用于贪吃蛇速度的具体实现
        self.clock = pygame.time.Clock()
        # b变量，防止移动中同时按下两个方向键导致直接game over的bug
        self.b = True
        # change变量，判断食物是否被吃
        self.change = False
        # 游戏开始变量，暂停变量，游戏结束变量
        self.pause = False
        self.game_start = False
        self.game_over = False
        #  菜单列表，确定当前是哪个菜单界面，5个位置分别对应[开始界面，暂停界面，结束界面，音乐二级界面，难度二级界面]
        self.menu_list = [1, 0, 0, 0, 0]
        #  显示开始界面的一级菜单
        self.menu1s.show_menu(self.screen)
        #  运行游戏
        self.running()

    #  重新开始游戏
    def restart(self):
        #  将蛇身坐标，长度，速度，分数等全部重新初始化
        self.snake.snake_pos = deque([(300, 240), (320, 240), (340, 240)])
        self.snake.snake_len = 3
        self.snake.snake_speed = 5
        self.snake.score = 0
        self.snake.direct = random.choice([[1, 0], [0, 1], [0, -1]])
        self.food.create_food(True, self.snake.snake_pos)

    #  控制背景音乐开关
    def music(self):
        if self.menu2m.bgm:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    #  吃到食物，更新速度，分数等信息，播放音效
    def score_ing(self, change):
        if change:
            if self.menu2m.eat_sound:
                self.sound.play()
            self.snake.snake_len += 1
            self.snake.score += 10
            #  困难难度，吃到食物速度减缓
            if self.menu2h.choice == 2:
                self.snake.snake_speed -= 0.2
            elif self.snake.snake_speed < 15.0:
                self.snake.snake_speed += 0.1
            #  创建一个新的食物坐标
            self.food.create_food(True, self.snake.snake_pos)
        #  困难难度，没吃到食物速度变快
        elif self.menu2h.choice == 2 and self.snake.snake_speed < 15.0:
            self.snake.snake_speed += 0.02

    #  打印文本信息
    def print_txt(self, txt, dx, pos):
        font = pygame.font.SysFont('SimHei', dx)
        text = font.render(txt, True, 'GREEN')
        self.screen.blit(text, pos)

    def draw_line(self):
        for x in range(size, Screen_Width, size):  # 竖线
            pygame.draw.line(self.screen, 'BLACK', (x, 40), (x, Screen_Height), 1)
        for y in range(2*size, Screen_Height, size):  # 横线
            pygame.draw.line(self.screen, 'BLACK', (0, y), (Screen_Width, y), 1)

    def draw_all(self):
        self.screen.fill('LightBlue4')
        self.snake.draw_snake(self.screen)
        self.food.draw_food(self.screen)
        self.draw_line()
        self.print_txt(f"得分: {self.snake.score}", 30, (440, 0))
        self.print_txt("速度:%.1f" % self.snake.snake_speed, 30, (0, 0))

    #  键盘处理，移动中按方向键控制移动，空格键暂停
    def handle_key(self, key):
        if self.b and key == K_UP and self.snake.direct[1] != 1:
            self.snake.direct = [0, -1]
            self.b = False
        elif self.b and key == K_DOWN and self.snake.direct[1] != -1:
            self.snake.direct = [0, 1]
            self.b = False
        elif self.b and key == K_LEFT and self.snake.direct[0] != 1:
            self.snake.direct = [-1, 0]
            self.b = False
        elif self.b and key == K_RIGHT and self.snake.direct[0] != -1:
            self.snake.direct = [1, 0]
            self.b = False
        elif key == K_SPACE:
            self.pause = True
            self.menu_list[self.menu_list.index(1)] = 0
            self.menu_list[1] = 1
            self.menu1p.show_menu(self.screen)  # 无需填充背景颜色

    #  根据不同的难度选择执行不同的判定条件判断是否游戏结束
    def check_game_over(self, hard_level):
        #  由于游戏结束判定是依据蛇头撞到了啥，所以先拿到蛇头
        snake_header = self.snake.snake_pos.pop()
        #  可以穿墙,蛇头撞到蛇身游戏结束
        if hard_level == 0:
            self.game_over = snake_header in self.snake.snake_pos
        #  不可穿墙，蛇头撞到墙或蛇身游戏结束
        elif hard_level == 1 or hard_level == 2:
            self.game_over = snake_header[1] == Screen_Height or snake_header[1] == 20 or snake_header[0] == \
                             Screen_Width or snake_header[0] == -20 or snake_header in self.snake.snake_pos
        #  将蛇头添加回来，否则会报错
        self.snake.snake_pos.append(snake_header)
        return self.game_over

    #  显示菜单界面后要执行选择菜单选项的函数，以及回车键确认选项执行具体的事件
    #  5个菜单界面分别对应5个选项函数和选项确认方法，利用menu_list来判断当前是哪个界面，并返回对应的函数，方便后续执行
    def real_choose(self):
        if self.menu_list[0] == 1:
            #  多返回一个菜单数量，因为choose函数需要一个num变量，不同菜单的num数量是不同的
            return self.menu1s.choose_menu, self.start_confirm, self.menu1s.num
        elif self.menu_list[1] == 1:
            return self.menu1p.choose_menu, self.pause_confirm, self.menu1p.num
        elif self.menu_list[2] == 1:
            return self.menu1e.choose_menu, self.end_confirm, self.menu1e.num
        elif self.menu_list[3] == 1:
            return self.menu2m.choose_menu, self.music_confirm, self.menu2m.num
        elif self.menu_list[4] == 1:
            return self.menu2h.choose_menu, self.hard_confirm, self.menu2h.num

    #  开始界面确认函数
    def start_confirm(self, key):
        if key == K_RETURN:
            #  选项一: 开始游戏
            if self.menu1s.choice == 0:
                self.game_start = True
            #  选项二: 显示音乐二级菜单界面
            elif self.menu1s.choice == 1:
                #  开始界面有4个菜单图片，但音乐二级菜单只有3张图片，所以在最后一个菜单位置画一个与背景颜色相同的矩形，然后画小方格
                #  这样做可以不用填充整个界面，防止游戏进行中显示二级菜单会将贪吃蛇和食物的画面一并填充掉
                pygame.draw.rect(self.screen, 'LightBlue4', self.menu1s.rect[3])
                self.draw_line()
                #  显示音乐二级界面
                self.menu2m.show_menu(self.screen)
                #  修改menu_list表示现在已经是音乐二级界面
                self.menu_list[0] = 0
                self.menu_list[3] = 1
            #  选项三: 显示难度二级界面，之后作用同上
            elif self.menu1s.choice == 2:
                pygame.draw.rect(self.screen, 'LightBlue4', self.menu1s.rect[3])
                self.draw_line()
                self.menu2h.show_menu(self.screen)
                self.menu_list[0] = 0
                self.menu_list[4] = 1
            #  选项四：退出游戏
            elif self.menu1s.choice == 3:
                pygame.quit()
                sys.exit()

    def pause_confirm(self, key):
        if key == K_RETURN:
            if self.menu1p.choice == 0:
                self.pause = False
            #  暂停界面3张图片，音乐二级界面也是3张，所以直接覆盖就好了，不用像之前一样
            elif self.menu1p.choice == 1:
                self.menu2m.show_menu(self.screen)
                self.menu_list[1] = 0
                self.menu_list[3] = 1
            elif self.menu1p.choice == 2:
                pygame.quit()
                sys.exit()

    def end_confirm(self, key):
        if key == K_RETURN:
            #  选项一：调用restart函数将蛇身等全部初始化，重新开始游戏
            if self.menu1e.choice == 0:
                self.game_over = False
                self.restart()
            elif self.menu1e.choice == 1:
                pygame.draw.rect(self.screen, 'LightBlue4', self.menu1e.rect[3])
                self.draw_line()
                self.menu2m.show_menu(self.screen)
                self.menu_list[2] = 0
                self.menu_list[3] = 1
            elif self.menu1e.choice == 2:
                pygame.draw.rect(self.screen, 'LightBlue4', self.menu1e.rect[3])
                self.draw_line()
                self.menu2h.show_menu(self.screen)
                self.menu_list[2] = 0
                self.menu_list[4] = 1
            elif self.menu1e.choice == 3:
                pygame.quit()
                sys.exit()

    def music_confirm(self, key):
        if key == K_RETURN:
            #  选项一: 更改bgm的值，用于背景音乐的开关，不返回上级界面
            if self.menu2m.choice == 0:
                self.menu2m.bgm = not self.menu2m.bgm
                self.music()
                self.menu2m.show_menu(self.screen)
            #  选项二：更改eat_sound的值，用于音效的开关，不返回上级界面
            elif self.menu2m.choice == 1:
                self.menu2m.eat_sound = not self.menu2m.eat_sound
                self.menu2m.show_menu(self.screen)
            #  选型三: 返回前一个一级界面，上一个界面的菜单图片数量都>=当前菜单图片数量，所以直接覆盖即可
            else:
                self.menu_list[3] = 0
                #  返回开始界面
                if self.menu1s.choice == 1:
                    self.menu1s.show_menu(self.screen)
                    self.menu_list[0] = 1
                #  返回暂停界面
                elif self.menu1p.choice == 1:
                    self.menu1p.show_menu(self.screen)
                    self.menu_list[1] = 1
                #  返回结束界面
                elif self.menu1e.choice == 1:
                    self.menu1e.show_menu(self.screen)
                    self.menu_list[2] = 1

    def hard_confirm(self, key):
        if key == K_RETURN:
            #  作用同音乐二级界面，但直接返回上级界面
            self.menu_list[self.menu_list.index(1)] = 0
            if self.menu1s.choice == 2:
                self.menu1s.show_menu(self.screen)
                self.menu_list[0] = 1
            elif self.menu1e.choice == 2:
                self.menu1e.show_menu(self.screen)
                self.menu_list[2] = 1

    def running(self):
        while True:
            self.clock.tick(self.snake.snake_speed)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    #  开始界面，暂停界面，结束界面，执行相应的选择函数和确认函数
                    if not self.game_start or self.pause or self.game_over:
                        choose, confirm, num = self.real_choose()
                        choose(self.screen, event.key, num)
                        confirm(event.key)
                    else:
                        self.handle_key(event.key)
            #  开始游戏
            if self.game_start and not self.pause and not self.game_over:
                self.b = True  # 将b变量设置为True，否则下次移动无效
                #  蛇身坐标移动
                self.snake.move(self.change, self.menu2h.choice)
                #  判断是否吃到食物
                self.change = self.food.check_food(self.snake.snake_pos)
                #  吃到食物更改相应的信息
                self.score_ing(self.change)
                #  画新的界面
                self.draw_all()
                #  判断是否游戏结束
                if self.check_game_over(self.menu2h.choice):
                    #  游戏结束，显示结束界面
                    self.menu_list[self.menu_list.index(1)] = 0
                    self.menu_list[2] = 1
                    self.menu1e.show_menu(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()

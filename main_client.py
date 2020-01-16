import pygame
from pygame.locals import *
import random
import math


class Unit:
    """
    Класс, необходимый для создания платформ и других объектов.
    Обладает функцией для рендеринга картинки
    """
    def __init__(self, x, y, direction, num, obj, img=None, color=None, spring=None):
        self.x = x
        self.y = y
        self.obj = obj
        self.red = False
        self.jumped = False
        self.spring_x = self.x + random.randint(5, 20)
        self.spring_y = self.y - 25
        self.direction = direction
        if not (spring is None):
            self.spring = spring
        if not (color is None):
            self.color = color
        if obj == 'ground':
            self.img = img
            if len(img) == 2:
                self.red = True
            self.sprite = img[0]
            self.width = self.sprite.get_width()
            self.height = self.sprite.get_height()

    def render(self, window):
        if self.spring:
            if self.jumped:
                window.blit(pygame.image.load('game_files/jump_2.png').convert_alpha(),
                            (self.spring_x, self.spring_y - 24))
            else:
                window.blit(pygame.image.load('game_files/jump_1.png').convert_alpha(),
                            (self.spring_x, self.spring_y))

        if self.color == 'blue':
            if self.direction:
                self.x += 5
                self.spring_x += 5
            else:
                self.x -= 5
                self.spring_x -= 5
            if self.x >= 422:
                self.direction = 0
            elif self.x <= 0:
                self.direction = 1

        window.blit(self.sprite,
                    (self.x, self.y))


class AnimatedSprite(pygame.sprite.Sprite):
    """
    Класс, взятый из учебника яндекс лицея, необходимый для смены спрайта игрока.
    """
    def __init__(self, sheet, columns, rows):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(-100, -100)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(-100, -100, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Hero:
    """
    Класс главного героя, содержит функции:
    рисование главного героя,
    коллизия с другими предметами/врагами,
    физика прыжка,
    установка нужного спрайта,
    смерть персонажа при столкновении с врагом(враг должен находится сверху)
    """

    def __init__(self, x, y, direction, num_id=None):
        """
        Входные данные для создания персонажа

        :param x:
        :param y:
        :param direction:
        :param num_id:
        """
        self.K_MOVE = 0.7
        self.jump_force = 0
        self.x = x
        self.y = y
        self.onGround = False
        self.spring_y = False
        self.onSpring = False
        self.hero_death = False
        self.sprite = pygame.image.load('game_files/dodle_left.png').convert_alpha()
        if not (num_id is None):
            self.num_id = num_id
        else:
            self.num_id = 25
        self.direction = direction
        self.height = 80
        self.width = 80
        self.speed = 15
        self.jump = 400
        self.obj = 'hero'

    def collision(self, unit):
        """
        Коллизия с предметами, на вход подается класс.

        :param unit:
        :return:
        """
        if unit.obj == 'enemy':
            if self.x <= unit.x <= (self.x + self.width) or unit.x <= self.x <= (unit.x + unit.width):
                if self.y <= unit.y <= (self.y + self.height) or unit.y <= self.y <= (unit.y + unit.height):
                    self.death()
                    return True

        elif unit.obj == 'ground':
            if self.x + self.width >= unit.x >= self.x or unit.x + unit.width >= self.x >= unit.x:
                if unit.y + 8 <= self.y + self.height < unit.y + unit.height:
                    if self.down:
                        self.onGround = True
                        second_jump = unit.jumped
                        unit.jumped = True

                        if unit.red:
                            unit.sprite = unit.img[1]
                        self.y = unit.y - self.height
                        if unit.spring:
                            self.onSpring = True
                            self.y -= 24
                        if not second_jump:
                            return True
        return False

    def set_sprite(self, img):
        """
        Установка спрайта, на вход картинка
        :param img:
        :return:
        """
        self.sprite = img

    def move(self, forces, keys, UNITLIST=None):
        """
        Передвижение персонажа.
        Физика прыжков, сила гравитации, передвижение вправо и влево

        :param forces:
        :param keys:
        :param UNITLIST:
        :return:
        """
        result_force = [0, 0]

        for force in forces:
            result_force[0] += force[0]
            result_force[1] += force[1]

        result_force[1] += self.jump_force
        self.x += result_force[0] * self.K_MOVE / 5
        self.y += result_force[1] * self.K_MOVE / 5

        if keys[pygame.K_a]:
            self.x -= self.speed * self.K_MOVE
            self.sprite = pygame.image.load('game_files/dodle_left.png').convert_alpha()
        elif keys[pygame.K_d]:
            self.x += self.speed * self.K_MOVE
            self.sprite = pygame.image.load('game_files/dodle_right.png').convert_alpha()

        if self.onGround:
            if self.onSpring:
                self.onSpring = False
                self.onGround = False
                self.jump_force = self.jump
            else:
                self.onGround = False
                self.jump_force = self.jump / 2

        # for jump
        if self.jump_force > 20:
            self.y -= self.jump_force / 2.3
            self.jump_force -= self.jump_force / 10
            self.down = False
        else:
            self.down = True
        if self.y < 0:
            self.y = 0
        if self.x < 0:
            self.x = 0
        elif self.x > (532 - self.width):
            self.x = 532 - self.width
        for i in range(len(UNITLIST)):
            if self.collision(UNITLIST[i]):
                return UNITLIST[i]
        return False

    def render(self, window):
        """
        Рисование персонажа на игровом поле
        :param window:
        :return:
        """
        window.blit(self.sprite, (self.x, self.y))

    def death(self):
        """
        Смерть персонажа при столкновении с врагом(враг должен находится над персонажем)
        :return:
        """
        self.hero_death = True


class Platform(Unit):
    """
    Класс платформы, заимствует все функции из класса UNIT
    Отвечает за создание платформ разного цвета
    """
    def __init__(self, x, y, image, num, spring):
        colors = ['green',
                  'blue',
                  'red']
        Unit.__init__(self, x, y, num, 0, 'ground', img=image, color=colors[num], spring=spring)


class Weapon:
    """
    Класс для работы с оружием(дулом у персонажа)
    Функции:
    Смена спрайта у игрока в зависимости от выстрела,
    Коллизия с врагами(враги умирают, при столкновении с пулей),
    Физика движения пули,
    Рисование спрайта на игровом поле
    """
    def __init__(self, hero_x, hero_y, mouse_pos):
        self.forces = [(0, 9 * 10)]
        self.K_MOVE = 0.8
        self.spring_y = 0
        self.start_x = hero_x + 40
        self.start_y = hero_y + 30
        self.x = self.start_x - 7.5
        self.y = self.start_y - 7.5
        self.end_x = mouse_pos[0]
        self.end_y = mouse_pos[1]
        self.width = 15
        self.height = 15
        self.bullet_sprite = pygame.image.load('game_files/bullet.png').convert_alpha()
        self.bullet_speed = 200
        self.obj = 'bullet'
        self.angle = 0

    def render_shot_pic(self):
        """
        Меняет спрайт у персонажа в зависимости от
        угла между начальными координатами персонажа и мышкой
        :return:
        """
        try:
            angle = (self.start_y - self.end_y) / (self.start_x - self.end_x)
        except:
            return pygame.image.load('game_files/doodle_77_left.png')

        self.angle = abs(math.degrees(math.atan(angle)) - 90)

        if 0 < self.angle < 22.5:
            return pygame.image.load('game_files/doodle_77_left.png')
        elif 22.5 <= self.angle < 45:
            return pygame.image.load('game_files/doodle_45_left.png')
        elif 45 <= self.angle < 77.5:
            return pygame.image.load('game_files/doodle_22_left.png')
        elif 77.5 <= self.angle < 90:
            return pygame.image.load('game_files/dodle_left.png')
        elif self.angle > 180:
            return pygame.image.load('game_files/doodle_90.png')
        elif 90 < self.angle <= 112.5:
            return pygame.image.load('game_files/dodle_right.png')
        elif 112.5 < self.angle <= 135:
            return pygame.image.load('game_files/doodle_22_right.png')
        elif 135 < self.angle <= 157.5:
            return pygame.image.load('game_files/doodle_45_right.png')
        elif 157.5 < self.angle < 180:
            return pygame.image.load('game_files/doodle_77_right.png')

    def collision(self, enemy):
        """
        Столкновение с врагом.
        Пуля и враг при столкновении исчезают.
        На вход подается список состоящий из объкектов врагов.
        :param enemy:
        :return:
        """
        for unit in enemy:
            if self.x + self.width >= unit.x >= self.x or unit.x + unit.width >= self.x >= unit.x:
                if unit.y <= self.y + self.height < unit.y + unit.height:
                    return unit
        return False

    def move_bullet(self, forces):
        """
        Передвижение пули в соответсвии с законами физики.
        На вход подается сила притяжения и другие действующие на пулю силы.
        :param forces:
        :return:
        """
        result_force = [0, 0]
        for force in forces:
            result_force[0] += force[0]
            result_force[1] += force[1]

        result_force[1] += self.bullet_speed
        self.x += result_force[0] * self.K_MOVE / 5
        self.y += result_force[1] * self.K_MOVE / 5

        if self.bullet_speed > 20:
            self.y -= self.bullet_speed / 2
            self.bullet_speed -= self.bullet_speed / 10
        if self.angle > 90:
            self.x += 15
            self.y -= 20
        elif self.angle > 0:
            self.x -= 15
            self.y -= 20

    def render(self, window):
        """
        Рисование спрайта пули.
        Вызывается функция для ее передвижения и смены координат
        :param window:
        :return:
        """
        self.move_bullet(self.forces)
        window.blit(self.bullet_sprite, (self.x, self.y))


class Enemy:
    """
    Класс для изображения на поле Врага.
    Используется класс AnimatedSprite, для создания анимации движения врага
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 52
        self.width = 52
        self.spring_y = 0
        self.enemy = AnimatedSprite(pygame.image.load("game_files/enemy.png").convert_alpha(), 5, 2)
        self.obj = 'enemy'

    def render(self, window):
        """
        Рисование спрайта врага.
        Вызывается обновление спрайта у врага.
        :param window:
        :return:
        """
        window.blit(self.enemy.image, (self.x, self.y))
        self.enemy.update()


class Client:
    """
    Класс пользователя.
    Отвечает за обработку и вывод изображения для пользователя.
    Также отвечает за рисования стартовых и последующих платформ
    """
    def __init__(self):
        self.plats = []
        self.UNITLIST = []
        self.all_bullets = []
        self.enemy = []
        self.account = 0
        pygame.init()
        pygame.display.set_caption("Doodle jump")
        pygame.mouse.set_visible(False)
        window = pygame.display.set_mode((532, 850))
        pygame.mixer.music.load('game_files/music.mp3')
        pygame.mixer.music.play()
        self.bg = pygame.image.load("game_files/background.png").convert_alpha()
        self.MANUAL_CURSOR = pygame.image.load('game_files/arrow.png').convert_alpha()
        self.solo_game(window)

    def restart_game(self, window):
        """
        Перезапуск игры при нажатии на кнопку 'r'
        :param window:
        :return:
        """
        self.plats = []
        self.UNITLIST = []
        self.all_bullets = []
        self.enemy = []
        self.account = 0
        pygame.mixer.music.load('game_files/music.mp3')
        pygame.mixer.music.play()
        self.solo_game(window)

    def solo_game(self, window):
        """
        Одиночная игра.
        Функция отвечает за рисование всех объектов на поле
        :param window:
        :return:
        """
        clock = pygame.time.Clock()
        x = 250
        y = 600
        player = Hero(x, y, 0)
        run = True
        wait_between_bullets = 5
        cost = 1500
        while run:
            clock.tick(60)
            window.blit(self.bg, (0, 0))
            window.blit(self.MANUAL_CURSOR, (pygame.mouse.get_pos()))
            pygame.display.set_caption(f"Your score - {str(self.account)}")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif (event.type == pygame.MOUSEBUTTONDOWN and
                      pygame.mouse.get_pos()[1] < (player.y + 20) and wait_between_bullets > 15):
                    wait_between_bullets = 0
                    bullet = Weapon(player.x, player.y,
                                    pygame.mouse.get_pos())
                    player.set_sprite(bullet.render_shot_pic())
                    self.all_bullets.append(bullet)

            self.add_platforms()
            wait_between_bullets += 1
            self.bullets_collision()

            if self.account > cost:
                self.create_enemy()
                cost += random.randint(400, 2000)
                
            for enemy in self.enemy:
                if enemy.y > 860:
                    del enemy
                    continue
                if enemy not in self.UNITLIST:
                    self.UNITLIST.append(enemy)            

            if pygame.key.get_pressed():
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.restart_game(window)
                    return
                answer = player.move([(0, 7 * 10)], pygame.key.get_pressed(), UNITLIST=self.UNITLIST)
                if answer:
                    if player.hero_death:
                        self.death(window)
                        return
                    elif answer.obj == 'ground' and answer.spring:
                        self.account += random.randint(150, 1000)
                    else:
                        self.account += random.randint(50, 200)

            self.UNITLIST.extend(self.all_bullets)
            self.UNITLIST.append(player)

            if player.y < 450:
                coord = 25
                for unit in self.UNITLIST:
                    unit.y += coord
                    unit.spring_y += coord

            for unit in self.UNITLIST:
                unit.render(window)
            pygame.display.update()
            if player.y > 770:
                self.death(window)
                return
            self.UNITLIST = []
        pygame.quit()

    def death(self, window):
        """
        Функция, вызывающаяся при смерти героя.
        Рисует окно с результатами игры
        :param window:
        :return:
        """
        clock = pygame.time.Clock()
        for i in range(30):
            clock.tick(60)
            window.blit(self.bg, (0, 0))
            window.blit(self.MANUAL_CURSOR, (pygame.mouse.get_pos()))
            for unit in self.UNITLIST:
                if unit.obj != 'hero':
                    unit.y -= 10
                    unit.spring_y -= 10
                else:
                    unit.y -= 2
            for unit in self.UNITLIST:
                unit.render(window)
            pygame.display.update()
        for i in range(10):
            clock.tick(60)
            window.blit(self.bg, (0, 0))
            window.blit(self.MANUAL_CURSOR, (pygame.mouse.get_pos()))
            for unit in self.UNITLIST:
                if unit.obj == 'hero':
                    unit.y += 2
            for unit in self.UNITLIST:
                unit.render(window)
            pygame.display.update()
        window.blit(self.bg, (0, 0))
        window.blit(self.MANUAL_CURSOR, (pygame.mouse.get_pos()))
        font = pygame.font.Font(None, 40)
        text = font.render("You're dead", True, (0, 0, 0))
        score_text = font.render(f"Your score: {str(self.account)}", True, (0, 0, 0))
        restart = font.render("If you want to play again", True, (0, 0, 0))
        add_restart = font.render(" click the 'R'button", True, (0, 0, 0))
        window.blit(text, (50, 50))
        window.blit(score_text, (50, 100))
        window.blit(restart, (50, 150))
        window.blit(add_restart, (50, 200))
        pygame.display.update()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart_game(window)
                    return

    def create_enemy(self):
        """
        Функция по созданию и размещению игроков на игровом поле
        :return:
        """
        green_plat = [pygame.image.load("game_files/green_platform.png").convert_alpha()]
        enemy_plat_y = self.plats[-1].y

        for i in range(5):
            spring = False
            random_number = random.randint(1, 10)
            if random_number % 2 == 0:
                self.plats.append(Platform(120 * i,
                                           enemy_plat_y - 250,
                                           green_plat, 0,
                                           spring))
                self.enemy.append(Enemy(120 * i + 25, enemy_plat_y - 302))
                self.UNITLIST.append(self.plats[-1])
                self.UNITLIST.append(self.enemy[-1])

    def bullets_collision(self):
        """
        Функция, которая проверяет вышла ли
        пуля за границы игрового поля и проверка на столкновение с врагами
        :return:
        """
        for bullet in self.all_bullets:
            if bullet.x < 0 or bullet.y < 0 or bullet.x > 532 or bullet.y > 850:
                del bullet
                continue
            answer = bullet.collision(self.enemy)
            if answer:
                del bullet
                self.account += random.randint(500, 1500)
                for i in range(len(self.enemy)):
                    if self.enemy[i].x == answer.x and self.enemy[i].y == answer.y:
                        self.enemy.pop(i)
                        break

    def add_platforms(self):
        """
        Функция для создания платформ и размещения их в рандомном порядке по игровому полю
        :return:
        """
        green_plat = [pygame.image.load("game_files/green_platform.png").convert_alpha()]
        blue_plat = [pygame.image.load("game_files/blue_platform.png").convert_alpha()]
        red_plat = [pygame.image.load("game_files/red_platform.png").convert_alpha(),
                    pygame.image.load("game_files/broken_red_platform.png").convert_alpha()]
        colors_of_plats = [green_plat,
                           blue_plat,
                           red_plat]
        spring = False
        spring_num = [random.randint(0, 24),
                      random.randint(0, 24),
                      random.randint(0, 24)]

        for i in range(len(self.plats)):
            if self.plats[i].y > 850 or (self.plats[i].red and self.plats[i].jumped):
                self.plats.pop(i)
                num_of_plat = random.randint(0, 2)
                if i in spring_num and num_of_plat != 2:
                    spring = True
                self.plats.append(Platform(random.randint(0, 422),
                                           self.plats[-1].y - random.randint(50, 200),
                                           colors_of_plats[num_of_plat],
                                           num_of_plat,
                                           spring))
                spring = False

        if len(self.plats) == 0:
            n = 10
            for i in range(5):
                self.plats.append(Platform(120 * i, 800,
                                           green_plat, 0,
                                           spring))
            for i in range(n):
                num_of_plat = random.randint(0, 2)
                if i in spring_num and num_of_plat != 2:
                    spring = True
                self.plats.append(Platform(random.randint(0, 422),
                                           self.plats[-1].y - random.randint(50, 200),
                                           colors_of_plats[num_of_plat],
                                           num_of_plat,
                                           spring))
                spring = False

        self.UNITLIST.extend(self.plats)


if __name__ == "__main__":
    client = Client()

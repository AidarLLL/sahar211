import pygame

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Настройки экрана
width, height = 900, 450
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("DinosaurFullGame")

# Загрузка и масштабирование изображений
dino_img = pygame.image.load("dino.png")
obstacle_img = pygame.image.load("cactus.png")
ground_img = pygame.image.load("ground.png")

dino_img = pygame.transform.scale(dino_img, (60, 60))
obstacle_img = pygame.transform.scale(obstacle_img, (30, 60))
ground_img = pygame.transform.scale(ground_img, (width, 90))


class Dinosaur:
    def __init__(self):
        self.image = dino_img
        self.x = 50
        self.y = height - self.image.get_height() - 50
        self.vel_y = 0
        self.gravity = 1.5  # Немного увеличим гравитацию для плавности
        self.jump_height = -20
        self.is_jumping = False
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def update(self):
        if self.is_jumping:
            self.vel_y += self.gravity
            self.y += self.vel_y
            
            # Проверка приземления
            floor_y = height - self.image.get_height() - 50
            if self.y >= floor_y:
                self.y = floor_y
                self.is_jumping = False
                self.vel_y = 0
                
        # Важно: обновляем хитбокс вслед за координатами!
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel_y = self.jump_height
           

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self):
        self.image = obstacle_img
        self.x = width
        self.y = height - self.image.get_height() - 50
        self.base_vel = 12
        self.vel = self.base_vel
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

    def update(self, score):
        # Увеличение скорости в зависимости от очков
        self.vel = self.base_vel + (score // 5) * 0.5
        self.x -= self.vel
        self.rect.topleft = (self.x, self.y)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Ground:
    def __init__(self):
        self.image = ground_img
        self.x = 0
        self.y = height - 100
        self.vel = 6

    def update(self):
        self.x -= self.vel
        if self.x <= -width:
            self.x = 0

    def draw(self, win):
        # Отрисовка двух картинок земли для бесшовного эффекта
        win.blit(self.image, (self.x, self.y))
        win.blit(self.image, (self.x + width, self.y))


def main():
    clock = pygame.time.Clock()
    
    # Попробуем загрузить стандартный шрифт, если указанного файла нет в папке
    try:
        font = pygame.font.Font("PressStart2P-Regular.ttf", 30)
    except IOError:
        font = pygame.font.SysFont("monospace", 30, bold=True)

    try:
        pygame.mixer.music.play(-1)
    except:
        pass

    run = True
    game_active = False
    initial_start = True

    score = 0
    record = 0

    dino = Dinosaur()
    obstacle = Obstacle()
    ground = Ground()

    while run:
        clock.tick(30)
        win.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_active:
                        # Перезапуск игры
                        dino = Dinosaur()
                        obstacle = Obstacle()
                        ground = Ground()
                        score = 0
                        game_active = True
                        initial_start = False
                    else:
                        dino.jump()

        if game_active:
            # Обновление логики игры
            dino.update()
            obstacle.update(score)
            ground.update()

        

            # Начисление очков, если препятствие пролетело мимо
            if obstacle.x < -obstacle.image.get_width():
                score += 1
                if score > record:
                    record = score
                obstacle = Obstacle()  # Создаем новое препятствие

            # Отрисовка игровых объектов
            ground.draw(win)
            dino.draw(win)
            obstacle.draw(win)

            # Вывод счета
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            record_text = font.render(f"Record: {record}", True, (0, 0, 0))
            win.blit(score_text, (10, 10))
            win.blit(record_text, (width - 290, 10))
            
        else:
            # Отрисовка экранов меню и Game Over
            if initial_start:
                start_text = font.render("To Start Press Space", True, (0, 0, 0))
                win.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2))
            else:
                # Отрендерим старую сцену на заднем фоне (чтобы не было пустого экрана)
                ground.draw(win)
                dino.draw(win)
                obstacle.draw(win)
                
                game_over_text = font.render("Wanna try again?", True, (0, 0, 0))
                game_over_text2 = font.render("Press Space to Start", True, (0, 0, 0))
                
                win.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
                win.blit(game_over_text2, (width // 2 - game_over_text2.get_width() // 2, height // 2 + 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
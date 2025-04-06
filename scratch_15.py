import pygame, random
from pygame.math import Vector2
import pickle  # 用來儲存和讀取最高分數

pygame.init()

# 常數設置
background = (0, 0, 0)
cell = 20
cellnum = 20
width = cell * cellnum
height = cell * cellnum
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("snake snack!")
clock = pygame.time.Clock()
fps = 60
Update = pygame.USEREVENT
min_speed = 50  # 设置最小速度


# 載入最高分數
def load_high_score():
    try:
        with open("high_score.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return 0  # 若檔案不存在，回傳 0


# 儲存最高分數
def save_high_score(score):
    with open("high_score.pkl", "wb") as f:
        pickle.dump(score, f)


class Snack():
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize([])

    def draw(self):
        snack_set = pygame.Rect(self.x * cell, self.y * cell, cell, cell)
        pygame.draw.rect(screen, (129, 180, 130), snack_set)  # 绿色果实

    def randomize(self, snake_body):
        while True:
            self.x = random.randint(0, cellnum - 1)
            self.y = random.randint(0, cellnum - 1)
            self.pos = Vector2(self.x, self.y)
            if self.pos not in snake_body:
                break


class Snack1():
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.randomize1([])

    def draw(self):
        snack_set = pygame.Rect(self.x * cell, self.y * cell, cell, cell)
        pygame.draw.rect(screen, (255, 255, 255), snack_set)  # 白色果实

    def randomize1(self, snake_body):
        while True:
            self.x = random.randint(0, cellnum - 1)
            self.y = random.randint(0, cellnum - 1)
            self.pos = Vector2(self.x, self.y)
            if self.pos not in snake_body:
                break


class Snake():
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.way = Vector2(0, 0)
        self.new_body = False

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10), Vector2(4, 10)]
        self.way = Vector2(0, 0)

    def add(self):
        self.new_body = True

    def remove(self):
        if len(self.body) > 4:
            self.body.pop()

    def move(self):
        if self.new_body:
            self.body.insert(0, self.body[0] + self.way)
            self.new_body = False
        else:
            if self.way != Vector2(0, 0):
                self.body.pop(-1)
                self.body.insert(0, self.body[0] + self.way)

    def draw(self):
        for i, part in enumerate(self.body):
            color = (0, 0, 255) if i == 0 else (0, 0, 180)
            snake_set = pygame.Rect(part.x * cell, part.y * cell, cell, cell)
            pygame.draw.rect(screen, color, snake_set)


class Main():
    def __init__(self):
        self.snake = Snake()
        self.snack = Snack()
        self.snack1 = Snack1()
        self.score = 0
        self.green_fruit_count = 0  # 計算吃到的綠色果實數量
        self.snake_speed = 150
        self.game_over = False
        self.game_started = False  # 新增變數，判斷遊戲是否已開始

        self.snack.randomize(self.snake.body)
        self.snack1.randomize1(self.snake.body)

        # 載入最高分數
        self.high_score = load_high_score()

    def fail(self):
        head = self.snake.body[0]
        # 判断蛇是否撞墙或撞到自身
        if not (0 <= head.x < cellnum and 0 <= head.y < cellnum):
            return True
        if head in self.snake.body[1:]:
            return True
        return False

    def update(self):
        self.snake.move()
        self.eat()
        if self.fail():
            self.game_over = True
            pygame.time.set_timer(Update, 0)
            self.draw()
            self.game_over_screen()

    def game_over_screen(self):
        font = pygame.font.SysFont("Arial", 50)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        rect = game_over_text.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(game_over_text, rect)

        restart_text = font.render("Click to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(restart_text, restart_rect)

        pygame.display.update()

    def reset_game(self):
        self.snake.reset()
        self.snack.randomize(self.snake.body)
        self.snack1.randomize1(self.snake.body)
        self.score = 0
        self.green_fruit_count = 0  # 重置綠色果實計數
        self.snake_speed = 150
        pygame.time.set_timer(Update, self.snake_speed)
        self.game_over = False

    def eat(self):
        head = self.snake.body[0]
        if self.snack.pos == head:
            # 绿色果实：蛇减短一节并减速
            self.snake.remove()
            self.snake_speed = min(self.snake_speed + 20, 1000)
            self.snack.randomize(self.snake.body)

            # 增加綠色果實計數
            self.green_fruit_count += 1
            if self.green_fruit_count >= 3:
                # 吃到三個綠色果實，遊戲結束
                self.game_over = True
                pygame.time.set_timer(Update, 0)
        if self.snack1.pos == head:
            # 白色果实：增加分数、蛇增长一节并加速
            self.score += 1
            self.snake.add()
            self.snake_speed = max(min_speed, self.snake_speed - 5)  # 保证速度不会低于最小值
            pygame.time.set_timer(Update, self.snake_speed)
            self.snack1.randomize1(self.snake.body)

            # 更新最高分數
            if self.score > self.high_score:
                self.high_score = self.score
                save_high_score(self.high_score)

    def draw(self):
        self.snake.draw()
        self.snack.draw()
        self.snack1.draw()


        # 顯示最高分數、目前分數和綠色果實數量
        self.display_right_corner_info()

    def display_score(self):
        text = str(self.score)
        score_font = pygame.font.SysFont(None, 25)  # 縮小字體
        surface = score_font.render(text, True, (255, 255, 255))
        x = int(cell * cellnum - 60)
        y = int(cell * cellnum - 40)
        rect = surface.get_rect(center=(x, y))
        screen.blit(surface, rect)

    def display_right_corner_info(self):
        # 顯示三個資訊：最高分數、目前分數、綠色果實數量
        font = pygame.font.SysFont(None, 20)  # 縮小字體

        # 顯示最高分數
        high_score_text = f"High: {self.high_score}"
        surface = font.render(high_score_text, True, (255, 255, 255))
        x = width - 10  # 讓文字靠近右邊界
        y = 10  # 靠近上邊界
        rect = surface.get_rect(topright=(x, y))
        screen.blit(surface, rect)

        # 顯示目前分數
        score_text = f"Score: {self.score}"
        surface = font.render(score_text, True, (255, 255, 255))
        y += 20  # 稍微下移
        rect = surface.get_rect(topright=(x, y))
        screen.blit(surface, rect)

        # 顯示綠色果實數量
        green_fruit_text = f"Green: {self.green_fruit_count}"
        surface = font.render(green_fruit_text, True, (255, 255, 255))
        y += 20  # 稍微下移
        rect = surface.get_rect(topright=(x, y))
        screen.blit(surface, rect)

    def game_instructions(self):
        # 使用支援中文的字體
        font = pygame.font.Font("TaipeiSans.ttf", 15)  # 調整字體大小

        # 各段說明文字
        instructions_text = font.render("歡迎來到貪食蛇！", True, (255, 255, 255))
        controls_text = font.render("控制方式：使用方向鍵（上下左右）來控制蛇的移動方向", True, (255, 255, 255))
        rules_text = font.render("遊戲規則：", True, (255, 255, 255))
        rule1_text = font.render("1. 吃掉白色果實，蛇會增加一節身體並加速，分數加1", True, (255, 255, 255))
        rule2_text = font.render("2. 吃掉綠色果實，蛇會減少一節身體並減速", True, (255, 255, 255))
        rule3_text = font.render("3. 碰到牆壁、自己或吃到三個綠色果實遊戲結束", True, (255, 255, 255))
        start_text = font.render("點擊滑鼠以開始遊戲", True, (255, 0, 0))
        good_luck_text = font.render("祝您好運，遊戲愉快！", True, (255, 255, 255))

        # 清空畫面並顯示說明文字
        screen.fill(background)

        # 說明標題（"歡迎來到貪貪蛇"）
        screen.blit(instructions_text, (width // 2 - instructions_text.get_width() // 2, height // 7))

        # 控制方式文字
        screen.blit(controls_text, (width // 2 - controls_text.get_width() // 2, height // 4))

        # 遊戲規則標題
        screen.blit(rules_text, (width // 2- rules_text.get_width() // 2, height // 3))

        # 規則內容（條列說明）
        screen.blit(rule1_text, (width // 2 - rule1_text.get_width() // 2, height // 3+ 40))
        screen.blit(rule2_text, (width // 2.4 - rule2_text.get_width() // 2, height // 3 + 80))
        screen.blit(rule3_text, (width // 2.2 - rule3_text.get_width() // 2, height // 3 + 120))

        # 開始遊戲提示
        screen.blit(start_text, (width // 2.05 - start_text.get_width() // 2, height // 1.1))

        # 祝福語
        screen.blit(good_luck_text, (width // 2 - good_luck_text.get_width() // 2, height // 1.3))

        pygame.display.update()  # 更新畫面


# 主循環
main_ = Main()
running = True

# 顯示遊戲說明頁面，直到玩家點擊
while running:
    clock.tick(fps)
    if not main_.game_started:
        main_.game_instructions()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # 點擊開始遊戲
            if not main_.game_started:
                main_.game_started = True  # 開始遊戲
                pygame.time.set_timer(Update, main_.snake_speed)

        if event.type == pygame.KEYDOWN:
            if not main_.game_over and main_.game_started:
                if event.key == pygame.K_LEFT and main_.snake.way.x != 1:
                    main_.snake.way = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_.snake.way.x != -1:
                    main_.snake.way = Vector2(1, 0)
                if event.key == pygame.K_UP and main_.snake.way.y != 1:
                    main_.snake.way = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_.snake.way.y != -1:
                    main_.snake.way = Vector2(0, 1)

        if event.type == pygame.MOUSEBUTTONDOWN:  # 监听鼠标点击
            if main_.game_over:
                main_.reset_game()

        if event.type == Update and not main_.game_over and main_.game_started:
            main_.update()

    if main_.game_started:
        screen.fill(background)
        main_.draw()

        # 如果遊戲結束，顯示遊戲結束畫面
        if main_.game_over:
            main_.game_over_screen()

    pygame.display.update()

pygame.quit()
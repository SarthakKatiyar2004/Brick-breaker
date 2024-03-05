import pygame, sys
from random import randrange as rnd

WIDTH, HEIGHT = 1280, 720
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker by Sarthak Katiyar")


background = pygame.image.load("BG.jpg")
def get_font(size):
    return pygame.font.Font("font.ttf", size)

mode = "menu"

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
               
def display_score(score, screen):
    font = get_font(25)
    score_text = font.render("Score   " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def play():
    fps = 60
    paddle_w = 100
    paddle_h = 25
    paddle_speed = 2
    paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
    score = 0

    ball_radius = 15
    ball_speed = 1
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
    dx, dy = 1, -1
    block_list = [pygame.Rect(5 + 80*i, 35 + 30*j, 75, 25) for i in range(16) for j in range(5)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(16) for j in range(5)]

    def detect_collision(dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.blit(background, (0, 0))


        [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(screen, pygame.Color('black'), paddle)
        pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)

        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

        if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
            dx = -dx

        if ball.centery < ball_radius:
            dy = -dy

        if ball.colliderect(paddle) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, paddle)

        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            score += 10
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
        
            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(screen, hit_color, hit_rect)
            fps += 2

        if ball.bottom > HEIGHT: 
            global mode; mode = "game_over"
            main_menu()
        elif not len(block_list):
            mode = "you_won"
            main_menu()


        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and paddle.left > 0:
            paddle.left -= paddle_speed
        if key[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.right += paddle_speed

        display_score(score, screen)
        pygame.display.flip()

def main_menu():
    mode = "menu"
    settings_clicked = False
    
    while True:
        screen.blit(background, (0, 0))

        if mode == "menu":
            if settings_clicked == True:
                TITLE = get_font(100).render("SETTINGS", True, "#CCA300")
            TITLE = get_font(100).render("BRICK BREAKER", True, "#CCA300")
        elif mode == "game_over":
            TITLE = get_font(100).render("GAME OVER!", True, "#b68f40")
        elif mode == "you_won":
            TITLE = get_font(100).render("YOU WON!!!", True, "#b68f40")

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_RECT = TITLE.get_rect(center=(640, 150))

        SETTINGS = pygame.image.load("Settings.png")
        BUTTON_ONE = Button(image=pygame.image.load("rect.png"), pos=(640, 340), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Green")
        BUTTON_TWO = Button(image=pygame.image.load("rect.png"), pos=(640, 500), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Red")
        LOGO = Button(image=pygame.image.load("logo.png"), pos=(640, 650), text_input="", font=get_font(0), base_color="#d7fcd4", hovering_color="White")
        screen.blit(TITLE, MENU_RECT)

        SETTINGS_BUTTON = Button(image=SETTINGS, pos=(WIDTH - 30, 20), text_input="", font=get_font(0), base_color="#d7fcd4", hovering_color="White")

        for button in [BUTTON_ONE, BUTTON_TWO, SETTINGS_BUTTON, LOGO]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_ONE.checkForInput(MENU_MOUSE_POS):
                    play()

                if BUTTON_TWO.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                
                if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    settings_clicked = True

        pygame.display.update()


main_menu()



main_menu()
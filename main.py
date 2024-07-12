import pygame as pg
import math
import random

# Game Variables
pg.font.init()
WIDTH = 900
HEIGHT = 700
screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()
font = pg.font.SysFont("comicsans", 30, True, True)
menu_font = pg.font.SysFont('arial', 40)
game_state = "Start_menu"

# Draw game main menu
def draw_start_menu():
    screen.fill((0,255,155))
    title = menu_font.render('Endure', True, (255,255,255))
    start_button = menu_font.render('Start', True, (255,255,255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2-title.get_height()//2-200))
    screen.blit(start_button, (WIDTH//2 - start_button.get_width()//2, HEIGHT//2-start_button.get_height()//2))
    pg.mouse.set_visible(True)
    pg.display.update()

# Game over screen
def draw_game_over():
    screen.fill((0,0,0))
    game_over = menu_font.render("Game Over", True, (255,0,0))
    screen.blit(game_over, (WIDTH//2-game_over.get_width()//2, HEIGHT//2-120))
    pg.mouse.set_visible(True)
    pg.display.update()

def PauseGame():
    screen.fill((50, 200, 180))
    text = font.render("Score: " + str(player.score), 1, (0,0,0))
    health = font.render("Health: " + str(player.health), 1, (0,0,0))
    pause = menu_font.render("PAUSED", True, (255,255,255))
    screen.blit(pause, (WIDTH//2 - pause.get_width()//2, 0))
    player.draw(screen)
    screen.blit(text, (0, 15))
    screen.blit(health, (WIDTH-150, 15))
    pg.mouse.set_visible(True)
    for alien in aliens:
        alien.draw(screen)
        alien.speed = 0
    player.speed = 0
    pg.display.update()

# Spawning enemies
dt = 0
timer = 1

# Player Variables
player_y_pos = HEIGHT//2
player_x_pos = WIDTH//2
player_speed = 2
player_health = 100
max_health = 100
class Player:
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.score = 0
        self.player_img = pg.image.load("/home/judi/Documents/programming/waves/assets/characters/robot.png")
        self.hitbox = (self.x+3, self.y, 25, 32)
        self.health = health
        self.speed = 2
    
    def draw(self, screen):
        screen.blit(self.player_img, (self.x, self.y))
        self.hitbox = (self.x+3, self.y, 25, 32)
        #pg.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        self.health -= 10

# Cursor
pg.mouse.set_visible(False)
cursor_img = pg.image.load("/home/judi/Documents/programming/waves/assets/objects/rectacle.png")
cursor_img_rect = cursor_img.get_rect()

# Bullet variables
bullet_speed = 3
bullet_limit = 5
bullet_damage = 2
bullets = []
class Bullets:
    def __init__(self, x, y, bullet_speed):
        self.pos = (x, y)
        self.bullet_img = pg.image.load("/home/judi/Documents/programming/waves/assets/objects/energy_orb.png")
        mx, my = pg.mouse.get_pos()
        self.dir = (mx-x-18, my-y-18)
        self.radius = 5
        self.hitbox = (self.pos[0]+self.radius, self.pos[1]+self.radius, 20, 20)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, 1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)

        self.bullet = pg.Surface((7, 2)).convert_alpha()
        self.speed = bullet_speed

    def update(self):
        self.pos = (self.pos[0]+self.dir[0]*self.speed,
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, screen):
        screen.blit(self.bullet_img, self.pos)
        self.hitbox = (self.pos[0]+5, self.pos[1]+5, 20, 20)
        #pg.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

# Alien variables
def rand_x():
    return random.randint(0, WIDTH)

def rand_y():
    foo = [0, HEIGHT]
    return random.choice(foo)
aliens = []
class Aliens:
    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.image = pg.image.load("/home/judi/Documents/programming/waves/assets/characters/alien.png")
        self.rect = self.image.get_rect()
        self.speed = 1
        self.hitbox = (self.x+3, self.y, 25, 32)
        self.width = 25
        self.health = 6
        self.visible = True
    
    def move_towards_player(self, players_x, players_y):
        dx, dy = players_x-self.x, players_y-self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            dist = 1
        dx, dy = dx/dist, dy/dist
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x, self.y))
            self.hitbox = (self.x+3, self.y, 25, 32)

            # Health Bar
            pg.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1]- 10, 25, 10))
            pg.draw.rect(screen, (0, 255, 0), (self.hitbox[0], self.hitbox[1]- 10, self.width, 10))
            #pg.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        if self.health <= 0:
            self.visible = False
        else:
            self.health -= bullet_damage
            self.width -= 5*bullet_damage

# Make Alien follow player:
def alien_follow():
    for alien in aliens:
        alien.draw(screen)
        alien.speed = 1
        alien.move_towards_player(player.x, player.y)

# Creating bullets
def shoot_bullet():
    bullet = Bullets(player.x, player.y, bullet_speed)
    bullets.append(bullet)

# Updating Game
def redrawGameWindow():
    screen.fill((50, 200, 180))
    text = font.render("Score: " + str(player.score), 1, (0,0,0))
    health = font.render("Health: " + str(player.health), 1, (0,0,0))
    player.draw(screen)
    player.speed = 2

    # Update aliens to follow player
    alien_follow()

    cursor_img_rect.center = pg.mouse.get_pos()
    screen.blit(cursor_img, cursor_img_rect)

    screen.blit(text, (0, 15))
    screen.blit(health, (WIDTH-150, 15))
    
    # Update and Draw bulllets to screen
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw bulllets to screen and check collisions
    for bullet in bullets[:]:
        bullet.update()
        for alien in aliens:
            if (bullet.pos[1] - bullet.radius*2 < alien.hitbox[1] + alien.hitbox[3]) and (bullet.pos[1] + bullet.radius*2 > alien.hitbox[1]):
                if (bullet.pos[0] + bullet.radius*2 > alien.hitbox[0]) and (bullet.pos[0] - bullet.radius*2 < alien.hitbox[0] + alien.hitbox[2]):
                    alien.hit()
                    player.score += 1
                    if bullet in bullets:
                        bullets.pop(bullets.index(bullet))
                    if alien.health <= 0:
                        aliens.pop(aliens.index(alien))
            if not screen.get_rect().collidepoint(bullet.pos):
                try:
                    bullets.remove(bullet)
                except:
                    pass

    # Check for player collisions:
    for alien in aliens:
        if (alien.y < player.hitbox[1] + player.hitbox[3]) and (alien.y > player.hitbox[1]):
            if (alien.x + 20 > player.hitbox[0]) and (alien.x < player.hitbox[0] + player.hitbox[2]):
                player.hit()
                aliens.pop(aliens.index(alien))

    # Updating screen
    pg.display.update()

player = Player(player_x_pos, player_y_pos, player_health)

# Main Game Loop
run = True
while run:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        if event.type == pg.MOUSEBUTTONUP and len(bullets) < bullet_limit:
            shoot_bullet()
    
    # Move player
    keys = pg.key.get_pressed()
    if keys[pg.K_w] and player.y>=0:
        player.y-=player.speed
    if keys[pg.K_s] and player.y<=HEIGHT-34:
        player.y+=player.speed
    if keys[pg.K_d] and player.x<=WIDTH-30:
        player.x+=player.speed
    if keys[pg.K_a] and player.x>=0:
        player.x-=player.speed

    if game_state == "Start_menu":
        draw_start_menu()
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            game_state = "Game"
    if game_state == "Game":
        redrawGameWindow()
        timer -= dt
        if timer <= 0:
            aliens.append(Aliens(rand_x(), rand_y()))
            timer = 1
        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            game_state = "Pause"
        if player.health <= 0:
            game_state = "Game_over"
        dt = clock.tick(45)/1000
    if game_state == "Pause":
        PauseGame()
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            game_state = "Game"
        if keys[pg.K_q]:
            run = False
    if game_state == "Game_over":
        draw_game_over()
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            game_state = "Game"
            player.health = 100
            player.score = 0
            player.x = WIDTH//2
            player.y = HEIGHT//2
            del aliens[:]
        if keys[pg.K_q]:
            run = False

pg.quit()

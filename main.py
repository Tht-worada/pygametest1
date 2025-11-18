import pygame
import Ingame

pygame.init()

# --- Set up ---
pygame.display.set_caption("BINGO by Thankhun888")
info = pygame.display.Info()
width, height = 1280,720
screen = pygame.display.set_mode((width, height))


# --- Colors ---
darkbrown = (41, 39, 37)
white = (255, 255, 255)
blue = (56, 182, 255)
red = (255, 87, 87)

# --- Load images ---
play_img = pygame.image.load('ImgAsset/playimg.png').convert_alpha()
credits_img = pygame.image.load('ImgAsset/creditsimg.png').convert_alpha()
quit_img = pygame.image.load('ImgAsset/quitimg.png').convert_alpha()
back_img = pygame.image.load('ImgAsset/backimg.png').convert_alpha()
logo_img = pygame.image.load('ImgAsset/logoimg.png').convert_alpha()
bg_img = pygame.image.load('ImgAsset/bgimg_mainmenu.jpg').convert_alpha()
idea = pygame.image.load('ImgAsset/idea.png').convert_alpha()
vin = pygame.image.load('ImgAsset/vin.png').convert_alpha()
taan = pygame.image.load('ImgAsset/taan.png').convert_alpha()

# --- Button class ---
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.offset_x = 0.0
        self.target_offset = 0.0

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.target_offset = 20
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        else:
            self.target_offset = 0

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Smooth hover
        speed = 0.03
        self.offset_x += (self.target_offset - self.offset_x) * speed

        screen.blit(self.image, (self.rect.x + self.offset_x, self.rect.y))
        return action

# --- Text class ---
class TextObject:
    def __init__(self, text, font, color, x, y):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# --- Buttons ---
play_btn = Button(90, 320, play_img)
credits_btn = Button(90, 430, credits_img)
quit_btn = Button(90, 550, quit_img)
back_btn = Button(15, 50, back_img)

# --- Music ---
mainmenu_music = pygame.mixer.music
mainmenu_music.load("SFX/mainmenu.mp3")
mainmenu_music.play(-1, 0)
mainmenu_music.set_volume(0.5)
click_sfx = pygame.mixer.Sound("SFX/click.mp3")

# --- Font ---
h1font = pygame.font.SysFont("Montserrat Thin", 80)
h2font = pygame.font.SysFont("Montserrat Thin", 45)
h3font = pygame.font.SysFont("Montserrat Thin", 35)

# --- Game display ---
def play():
    mainmenu_music.stop()
    Ingame.run_game()

def credits():
    # สร้าง text
    head1 = TextObject("CREDITS", h1font, white, 470, 50)

    role1 = TextObject("Coding", h2font, red, 300, 150)
    role2 = TextObject("Design / Sound", h2font, red, 300, 300)
    role3 = TextObject("Testing", h2font, red, 300, 500)

    name1 = TextObject("- Phanyakorn Inthasombat", h3font, white, 300, 220)
    name2 = TextObject("- Prawin Muadsuk", h3font, white, 300, 370)
    name1_dup = TextObject("- Phanyakorn Inthasombat", h3font, white, 300, 420)

    name3 = TextObject("- Thaankhun Suchada", h3font, white, 300, 570)
    name2_dup = TextObject("- Prawin Muadsuk", h3font, white, 300, 620)
    
    running = True
    while running:
        screen.fill(darkbrown)
        
        # วาดข้อความทั้งหมด
        head1.draw(screen)

        role1.draw(screen)
        name1.draw(screen)

        role2.draw(screen)
        name2.draw(screen)
        name1_dup.draw(screen)

        role3.draw(screen)
        name3.draw(screen)
        name2_dup.draw(screen)

        # แสดงผลรูปภาพ
        screen.blit(idea, (850,150))
        screen.blit(vin, (850, 330))
        screen.blit(taan, (850, 520))
        
        # ปุ่มกลับไป main menu
        if back_btn.draw():
            click_sfx.play()
            return
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # กด กากบาทขวาบน ออกเกม
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # กด ESC ออกเกม
                running = False
            
        pygame.display.update()


def main_menu():
    running = True
    while running:
        screen.fill(darkbrown)

        # Draw background
        screen.blit(bg_img, (0, 0))

        # Draw buttons
        if play_btn.draw():
            click_sfx.play()
            play()
        if credits_btn.draw():
            click_sfx.play()
            credits()
        if quit_btn.draw():
            running = False

        # Draw logo
        screen.blit(logo_img, (80, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # กด กากบาทขวาบน ออกเกม
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # กด ESC ออกเกม
                running = False

        pygame.display.update()
    pygame.quit()

# --- Start game ---
main_menu()
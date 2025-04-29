import pygame
import math
import random
import time

class HangmanGame:
    def __init__(self, width, height):
        #inkapsuliavimas
        self.width = width
        self.height = height
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hangman Game!")
        
        # mygtuku duomenys
        self.RADIUS = 20
        self.GAP = 15
        self.letters = []
        self.startx = round((self.width - (self.RADIUS * 2 + self.GAP) * 13) / 2)
        self.starty = 400
        self.A = 65
        for i in range(26):
            x = self.startx + self.GAP * 2 + ((self.RADIUS * 2 + self.GAP) * (i % 13))
            y = self.starty + ((i // 13) * (self.GAP + self.RADIUS * 2))
            self.letters.append([x, y, chr(self.A + i), True])

        # Sriftai
        self.LETTER_FONT = pygame.font.SysFont('timesnewroman', 40)
        self.WORD_FONT = pygame.font.SysFont('timesnewroman', 60)
        self.TITLE_FONT = pygame.font.SysFont('timesnewroman', 70)

        # Kraunamos nuotraukos
        self.images = []
        for i in range(7):
            image = pygame.image.load("basic" + str(i) + ".png")
            self.images.append(image)

        # game variables
        self.hangman_status = 0
        self.words = self.load_words_from_file("words.txt")  # Krauname zodzius is failo
        self.word = random.choice(self.words)  # Renkamas atsitiktinis zodis
        self.guessed = []

        # Spalvos
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.start_time = time.time()  # Leidzia pradeti skaiciuoti likusi laika kai zaidimas yra paleidziamas
    # IMAME ZODZIUS IS TXT FAILO
    def load_words_from_file(self, file_name):
        
        try:
            with open(file_name, 'r') as file:
                words = [line.strip() for line in file.readlines()]
            return words
        except FileNotFoundError:
            print(f"Error: {file_name} not found!")
            return []

    def draw(self):
        # zaidimo piesimas yra abraktuotas nuo vartotojo
        self.win.fill(self.WHITE)
        # Piesiame/spausdiname pavadinima
        text = self.TITLE_FONT.render("HANGMAN GAME", 1, self.BLACK)
        self.win.blit(text, (self.width / 2 - text.get_width() / 2, 20))

        # Piesiame/spausdinam zodi
        display_word = ""
        for letter in self.word:
            if letter in self.guessed:
                display_word += letter + " "
            else:
                display_word += "_ "
    
        word_width = self.WORD_FONT.size(display_word)[0]
        word_x = (self.width - word_width) / 2  # Centruojame zodi viduryje

        text = self.WORD_FONT.render(display_word, 1, self.BLACK)
        self.win.blit(text, (word_x, 200))

        # Piesiame/spausdinam raidziu mygtukus
        for letter in self.letters:
            x, y, ltr, visible = letter
            if visible:
                pygame.draw.circle(self.win, self.BLACK, (x, y), self.RADIUS, 3)
                text = self.LETTER_FONT.render(ltr, 1, self.BLACK)
                self.win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        self.win.blit(self.images[self.hangman_status], (40, 100))

        self.display_timer()

        pygame.display.update()

    def display_message(self, message):
        pygame.time.delay(1000)
        self.win.fill(self.WHITE)
        text = self.WORD_FONT.render(message, 1, self.BLACK)
        self.win.blit(text, (self.width / 2 - text.get_width() / 2, self.height / 2 - text.get_height() / 2))

        if self.hangman_status == 6 or message.startswith("Time's up"):
            lost_message = f"The word was: {self.word}"
            lost_text = self.WORD_FONT.render(lost_message, 1, self.BLACK)
            self.win.blit(lost_text, (self.width / 2 - lost_text.get_width() / 2, self.height / 2 + 50))

        pygame.display.update()
        pygame.time.delay(3000)

    def display_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, 60 - int(elapsed_time))  # 60 sekundziu laikmatis kuris uztikrina kad tai nenueitu i minusa
        
        pygame.draw.circle(self.win, self.BLACK, (self.width - 80, self.height - 50), 40, 3)  # nupiesiame apskritima laikmaciui ir nustatome kad jis butu apacioje desinej
    
        # Piesiame likusi laika kaip teksta
        timer_text = self.LETTER_FONT.render(f"{remaining_time}s", 1, self.BLACK)
    
        # Centruojame teksta viduryje apskritimo
        text_x = self.width - timer_text.get_width() - 52  # horizontaliai
        text_y = self.height - 50 - timer_text.get_height() / 2  # vertikaliai
    
        self.win.blit(timer_text, (text_x, text_y))  # statome teksta viduryje apskritimo



    def main(self):
        FPS = 60
        clock = pygame.time.Clock()
        run = True
        start_time = time.time()
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    m_x, m_y = pygame.mouse.get_pos()
                    for letter in self.letters:
                        x, y, ltr, visible = letter
                        if visible:
                            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                            if dis < self.RADIUS:
                                letter[3] = False
                                self.guessed.append(ltr)
                                if ltr not in self.word:
                                    self.hangman_status += 1

            self.draw()

            won = True
            for letter in self.word:
                if letter not in self.guessed:
                    won = False
                    break

            if won:
                self.display_message("You WON!")
                break

            if self.hangman_status == 6:
                self.display_message("You LOST!")
                break

            # Jei laikas baigiasi, zaidimas pralaimimas
            elapsed_time = time.time() - start_time
            if elapsed_time > 60:
                self.display_message("Time's up! You LOST!")
                break


class AdvancedHangman(HangmanGame):
    def __init__(self, width, height):    
    #Raktinis žodis super() AdvancedHangman klasėje rodo polimorfizmą:
        super().__init__(width, height) #paveldejimas is hangmangame klases
        self.words = self.load_words_from_file("advancedwords.txt")
        self.word = random.choice(self.words)
        self.load_advanced_images()
    def load_advanced_images(self):
        self.images = [pygame.image.load(f"hangman{i}.png") for i in range(7)] # nuotraukos ikelimas yra abstraktuotas
def show_mode_selection():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Select Game Mode")
    font = pygame.font.SysFont('timesnewroman', 60)
    white = (255, 255, 255)
    black = (0, 0, 0)

    basic_btn = pygame.Rect(75, 250, 400, 100)
    adv_btn = pygame.Rect(500, 250, 400, 100)
    mode_btn= pygame.Rect(240, 50, 265, 100)
    mode1_btn= pygame.Rect(500, 50, 265, 100)

    while True:
        screen.fill(white)
        pygame.draw.ellipse(screen, (0, 100, 255), basic_btn)
        pygame.draw.ellipse(screen, (255, 0, 0), adv_btn)
        pygame.draw.rect(screen,(0,100,255), mode_btn)
        pygame.draw.rect(screen,(255,0,0), mode1_btn)

        header_font = pygame.font.SysFont('timesnewroman', 50)
        header_text = header_font.render("CHOOSE GAME MODE", True, black)
        screen.blit(header_text, (screen.get_width() / 2 - header_text.get_width() / 2, 75))   
    
        basic_text = font.render("BASIC", True, white)
        adv_text = font.render("ADVANCED", True, white)
        screen.blit(basic_text, (basic_btn.x + 110, basic_btn.y + 15))
        screen.blit(adv_text, (adv_btn.x + 45, adv_btn.y + 15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                if basic_btn.collidepoint(m_x, m_y):
                    game = HangmanGame(1000, 600)
                    game.main()
                    return
                elif adv_btn.collidepoint(m_x, m_y):
                    game = AdvancedHangman(1000, 600)  # For now same as basic
                    game.main()
                    return

if __name__ == "__main__":
    show_mode_selection()
    pygame.quit()

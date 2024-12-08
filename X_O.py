import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Определение размеров окна
SIZE = 600
EXTRA_HEIGHT = 150
WINDOW_HEIGHT = SIZE + EXTRA_HEIGHT
ROWS, COLS = 3, 3
SQUARE_SIZE = SIZE // COLS

# Звуковые файлы
pygame.mixer.init()
try:
    move_sound = pygame.mixer.Sound('move_sound.wav')  # Звук хода
    draw_sound = pygame.mixer.Sound('draw_sound.wav')  # Звук ничьей
    x_winner_sound = pygame.mixer.Sound('x_winner.wav')  # Озвучка победы X
    o_winner_sound = pygame.mixer.Sound('o_winner.wav')  # Озвучка победы O
    pygame.mixer.music.load('background_music.mp3')  # Фоновая музыка
except pygame.error as e:
    print(f"Ошибка загрузки звуков: {e}")
    move_sound = draw_sound = x_winner_sound = o_winner_sound = None

# Шрифт
font = pygame.font.Font(None, 50)  # Стандартный шрифт Pygame

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((SIZE, WINDOW_HEIGHT))
        pygame.display.set_caption('Крестики-нолики')
        self.grid = [[None] * COLS for _ in range(ROWS)]
        self.player = "X"
        self.winner = None
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.sound_enabled = True
        self.mode = "PvP"  # Режим игры по умолчанию: PvP
        pygame.mixer.music.play(-1)  # Запускаем фоновую музыку

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col]:
                    label = font.render(self.grid[row][col], True, RED if self.grid[row][col] == "X" else BLUE)
                    self.screen.blit(label, (col * SQUARE_SIZE + 50, row * SQUARE_SIZE + 25))

    def draw_lines(self):
        for i in range(1, ROWS):
            pygame.draw.line(self.screen, BLACK, (0, i * SQUARE_SIZE), (SIZE, i * SQUARE_SIZE), 2)
            pygame.draw.line(self.screen, BLACK, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SIZE), 2)

    def draw_turn_indicator(self):
        text = f"Ход: {'Крестики' if self.player == 'X' else 'Нолики'}"
        label = font.render(text, True, BLACK)
        self.screen.blit(label, (SIZE // 2 - label.get_width() // 2, SIZE + 20))

    def draw_scores(self):
        score_text = f"X: {self.scores['X']} | O: {self.scores['O']} | Ничьи: {self.scores['Draw']}"
        label = font.render(score_text, True, BLACK)
        self.screen.blit(label, (SIZE // 2 - label.get_width() // 2, SIZE + 60))

    def draw_menu_button(self):
        # Кнопка "Главное меню"
        menu_button = font.render("Главное меню", True, RED)
        self.screen.blit(menu_button, (10, SIZE + 90))
        return menu_button

    def check_winner(self):
        # Проверка строк и столбцов
        for i in range(ROWS):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] and self.grid[i][0]:
                return self.grid[i][0]
            if self.grid[0][i] == self.grid[1][i] == self.grid[2][i] and self.grid[0][i]:
                return self.grid[0][i]

        # Проверка диагоналей
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0]:
            return self.grid[0][0]
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2]:
            return self.grid[0][2]

        # Проверка на ничью
        if all(all(cell is not None for cell in row) for row in self.grid):
            return "Draw"

        return None

    def handle_click(self, mouseX, mouseY):
        # Проверяем, находится ли клик в пределах сетки
        if mouseX >= SIZE or mouseY >= SIZE:
            return  # Игнорируем клик за пределами игрового поля

        clicked_row = mouseY // SQUARE_SIZE
        clicked_col = mouseX // SQUARE_SIZE

        if not self.grid[clicked_row][clicked_col]:
            self.grid[clicked_row][clicked_col] = self.player
            if self.sound_enabled and move_sound:
                move_sound.play()
            self.winner = self.check_winner()
            if not self.winner:
                self.player = "O" if self.player == "X" else "X"

    def ai_move(self):
        time.sleep(0.5)
        for row in range(ROWS):
            for col in range(COLS):
                if not self.grid[row][col]:
                    self.grid[row][col] = "O"
                    if self.sound_enabled and move_sound:
                        move_sound.play()
                    self.winner = self.check_winner()
                    self.player = "X"
                    return

    def reset_game(self):
        self.grid = [[None] * COLS for _ in range(ROWS)]
        self.winner = None
        self.player = "X"

    def main_menu(self):
        while True:
            self.screen.fill(WHITE)
            title = font.render("Крестики-нолики", True, BLACK)
            self.screen.blit(title, (SIZE // 2 - title.get_width() // 2, SIZE // 4))

            pvp_button = font.render("PvP (Игрок против Игрока)", True, GREEN)
            pve_button = font.render("PvE (Игрок против Компьютера)", True, GREEN)
            sound_button = font.render(f"Звук: {'Вкл' if self.sound_enabled else 'Выкл'}", True, BLUE)

            self.screen.blit(pvp_button, (SIZE // 2 - pvp_button.get_width() // 2, SIZE // 2 - 80))
            self.screen.blit(pve_button, (SIZE // 2 - pve_button.get_width() // 2, SIZE // 2))
            self.screen.blit(sound_button, (SIZE // 2 - sound_button.get_width() // 2, SIZE // 2 + 80))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    # Кнопка PvP
                    if SIZE // 2 - pvp_button.get_width() // 2 < mouseX < SIZE // 2 + pvp_button.get_width() // 2:
                        if SIZE // 2 - 80 < mouseY < SIZE // 2 - 80 + pvp_button.get_height():
                            self.mode = "PvP"
                            return
                    # Кнопка PvE
                    if SIZE // 2 - pve_button.get_width() // 2 < mouseX < SIZE // 2 + pve_button.get_width() // 2:
                        if SIZE // 2 < mouseY < SIZE // 2 + pve_button.get_height():
                            self.mode = "PvE"
                            return
                    # Кнопка звука
                    if SIZE // 2 - sound_button.get_width() // 2 < mouseX < SIZE // 2 + sound_button.get_width() // 2:
                        if SIZE // 2 + 80 < mouseY < SIZE // 2 + 80 + sound_button.get_height():
                            self.toggle_sound()

    def main_loop(self):
        self.main_menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.toggle_sound()  # Клавиша S для звука
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    # Проверяем, нажата ли кнопка "Главное меню"
                    menu_button = self.draw_menu_button()
                    if 10 < mouseX < 10 + menu_button.get_width() and SIZE + 90 < mouseY < SIZE + 90 + menu_button.get_height():
                        self.main_menu()
                        return
                    if not self.winner:
                        self.handle_click(mouseX, mouseY)
                        if self.mode == "PvE" and self.player == "O" and not self.winner:
                            self.ai_move()

            if self.winner:
                if self.winner == "X":
                    self.scores["X"] += 1
                    if self.sound_enabled and x_winner_sound:
                        x_winner_sound.play()
                elif self.winner == "O":
                    self.scores["O"] += 1
                    if self.sound_enabled and o_winner_sound:
                        o_winner_sound.play()
                elif self.winner == "Draw":
                    self.scores["Draw"] += 1
                    if self.sound_enabled and draw_sound:
                        draw_sound.play()

                time.sleep(2)
                self.reset_game()

            self.screen.fill(WHITE)
            self.draw_lines()
            self.draw_grid()
            self.draw_turn_indicator()
            self.draw_scores()
            self.draw_menu_button()
            pygame.display.flip()

if __name__ == "__main__":
    game = TicTacToe()
    game.main_loop()

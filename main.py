import pygame
import MatchGameBase
from random import randrange
from random import choice


class ColummnsGameDrawGame:
    def __init__(self) -> None:
        """Initalizes Vital variables"""
        self.grey = pygame.Color(52, 57, 59) #Grey
        self.s_jewel = pygame.Color(44, 119, 94) #Green
        self.t_jewel = pygame.Color(123, 239, 21) #Lime
        self.v_jewel = pygame.Color(239, 130, 21) #Orange
        self.w_jewel = pygame.Color(202, 45, 255) #Purple
        self.x_jewel = pygame.Color(10, 45, 255) #Blue
        self.y_jewel = pygame.Color(45, 171, 255) #Light Blue
        self.z_jewel = pygame.Color(255, 45, 45) #Red

        self.clear = pygame.Color(255, 255, 255) #White
        self.yellow = pygame.Color(249, 241, 0) #Yellow
        self.teal = pygame.Color(0, 237, 249)  #Teal
        self.dimensions = (700, 800)

    def create_window(self, size:(int, int)) -> "surface":
        """Creates the windows and returns it as a variable"""
        surface = pygame.display.set_mode(size, pygame.RESIZABLE)
        surface.fill(pygame.Color(134, 205, 249))

        return surface

    def create_board_in_window(self, surface) -> "surface":
        """Draw the entire board"""
        increase = 0

        frac_x = self.dimensions[0] * (2/7) #200
        frac_y = self.dimensions[1] * (1/8) #100

        frac_x2 = self.dimensions[0] * (3/7) #300
        frac_y2 = self.dimensions[1] * (13/16) #650

        "Draw the border"
        pygame.draw.rect(surface, self.grey, (frac_x, frac_y, frac_x2, frac_y2), 3)

        frac_x = self.dimensions[0] * (5/14) #250
        frac_y = self.dimensions[1] * (1/8) #100

        frac_y2 = self.dimensions[1] * (15/16) #750

        "Draw the grids"
        for num in range(5):
            pygame.draw.line(surface, self.grey, (frac_x + increase, frac_y), (frac_x + increase, frac_y2), 4)
            increase += self.dimensions[0] * (1 / 14)  # 50

        increase = 0
        frac_x = self.dimensions[0] * (2/7) #200
        frac_y = self.dimensions[1] * (3/16) #150

        frac_x2 = self.dimensions[0] * (5/7) #500

        for num in range(12):
            pygame.draw.line(surface, self.grey, (frac_x, frac_y + increase), (frac_x2, frac_y + increase), 4)
            increase += self.dimensions[1] * (1 / 16)  # 50

        return surface

    def draw_jewels(self, surface, jewel_locations) -> "surface":
        "Draw the jewels"
        for jewel in jewel_locations:
            if not jewel[-1]:
                if jewel[4].isupper():
                    pygame.draw.rect(jewel[0], jewel[1], jewel[2], jewel[3])
                    pygame.draw.rect(jewel[0], self.grey, jewel[2], 2)

                elif jewel[5]:
                    pygame.draw.rect(jewel[0], jewel[1], jewel[2], jewel[3])
                    pygame.draw.rect(jewel[0], self.yellow, jewel[2], 4)

                elif not jewel[5]:
                    pygame.draw.rect(jewel[0], jewel[1], jewel[2], jewel[3])
                    pygame.draw.rect(jewel[0], self.clear, jewel[2], 4)

            elif jewel[-1]:
                pygame.draw.rect(jewel[0], jewel[1], jewel[2], jewel[3])
                pygame.draw.rect(jewel[0], self.teal, jewel[2], 4)

        return surface

    def jewel_position(self, surface, game_state, consider_matching) -> ["Jewels"]:
        """Return a list containing the positions of each jewel in gamestate"""
        jewel_locations = []
        frac_x1 = self.dimensions[0] * (2/7) #200
        frac_y1 = self.dimensions[1] * (1/8) #100
        frac_x2 = self.dimensions[0] * (1/14) #50
        frac_y2 = self.dimensions[1] * (1/16) #50

        for row in range(len(game_state) - 1):
            for column in range(len(game_state[row])):
                if game_state[row][column].upper() == "S":
                    jewel_locations.append([surface, self.s_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])
                elif game_state[row][column].upper() == "T":
                    jewel_locations.append([surface, self.t_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])
                elif game_state[row][column].upper() == "V":
                    jewel_locations.append([surface, self.v_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])
                elif game_state[row][column].upper() == "W":
                    jewel_locations.append([surface, self.w_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])
                elif game_state[row][column].upper() == "X":
                    jewel_locations.append([surface, self.x_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])
                elif game_state[row][column].upper() == "Y":
                    jewel_locations.append([surface, self.y_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])
                elif game_state[row][column].upper() == "Z":
                    jewel_locations.append([surface, self.z_jewel, (frac_x1 + (frac_x2 * row), frac_y1 + (frac_y2 * column), frac_x2, frac_y2), 0, game_state[row][column], game_state[-1][-1], False])

            for jewel in range(len(jewel_locations) - 1):
                if jewel_locations[jewel][4].islower() and consider_matching:
                    jewel_locations[jewel][-1] = True

        return jewel_locations


class ColummnsGameBrain:
    def __init__(self):
        """Initializes Vital Variables"""
        self.game = MatchGameBase.ColumnsGame()
        self.draw = ColummnsGameDrawGame()
        self.board_size = self.game.user_input(13, 6)
        self.game_state = self.game.create_board(self.board_size)
        self.JEWELS = ["S", "T", "V", "W", "X", "Y", "Z"]

    def _generate_faller(self, game_state) -> "Faller":
        """Generates and returns a faller"""
        row = randrange(5) + 1

        jewels = " "
        for num in range(3):
            jewel = choice(self.JEWELS)
            jewels += f"{jewel} "

        faller = str(row) + jewels

        return self.game.create_faller(game_state, faller.split())

    def run_game(self) -> None:
        """Run the game"""
        clock = pygame.time.Clock()
        special_event = 0

        running = True
        pygame.init()

        surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
        self.game_state = self._generate_faller(self.game_state)
        self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, False))
        pygame.display.flip()

        while running:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        self.game_state = self.game._rotate_faller(self.game_state)
                        pygame.display.get_surface()
                        surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
                        self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, False))
                        pygame.display.flip()
                    elif key[pygame.K_RIGHT]:
                        self.game_state = self.game._shift_faller(self.game_state, "RIGHT")
                        pygame.display.get_surface()
                        surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
                        self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, False))
                        pygame.display.flip()
                    elif key[pygame.K_LEFT]:
                        self.game_state = self.game._shift_faller(self.game_state, "LEFT")
                        pygame.display.get_surface()
                        surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
                        self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, False))
                        pygame.display.flip()
                    elif key[pygame.K_d]:
                        self.game_state = self.game._drop_faller(self.game_state)
                        pygame.display.get_surface()
                        surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
                        self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, False))
                        pygame.display.flip()
                if event.type == pygame.VIDEORESIZE:
                    self.draw.dimensions = event.size
                    self.draw.create_window(self.draw.dimensions)

            if self.game_state == "QUIT":
                running = False

            special_event += 1
            if special_event == 30:
                self.game_state = self.game._drop_faller(self.game_state)
                pygame.display.get_surface()
                surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
                self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, False))

                if self.game_state[-1] == [0, [], 0, False]:
                    new_game_state = self.game.check_for_clear(self.game_state)
                    if new_game_state != self.game_state:
                        self.game_state = new_game_state
                        pygame.display.get_surface()
                        surface = self.draw.create_board_in_window(self.draw.create_window(self.draw.dimensions))
                        self.draw.draw_jewels(surface, self.draw.jewel_position(surface, self.game_state, True))

                    else:
                        self.game_state = self._generate_faller(self.game_state)
                special_event = 0
                pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = ColummnsGameBrain()
    game.run_game()
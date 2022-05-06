from collections import namedtuple
import copy


class ColumnsContentError(Exception):
    pass


class ColumnsGame:
    def __init__(self) -> None:
        """"Initialize important variables"""
        self.JEWELS = ["S", "T", "V", "W", "X", "Y", "Z", " "]
        self.game_board = []
        self.user_input = namedtuple("user_input", ["columns", "rows"])

    def create_board(self, user_input) -> list:
        """Use user input in order to create the 2D list for the game board"""
        for num in range(user_input.rows):
            self.game_board.append([])

        for row in self.game_board:
            for num in range(user_input.columns):
                row.append(" ")

        """EXPLANATION: The first index is the row this faller will be on the 2nd index is the contents of the faller
        the third index is the stage from 2-0 that the faller is in and the final index is whether or not the faller is frozen"""
        self.game_board.append([0, [], 0, False])

        return self.game_board

    def obtain_board_inputs(self) -> "namedtuple":
        """Obtain input from the user (rows and columns)"""
        rows = int(input())
        columns = int(input())

        return self.user_input(rows, columns)

    def board_contents(self, game_board) -> "Game Board":
        """Allow user to pre-fill board if they want and return the filled or non-filled board"""
        user_input = input()
        if user_input == "EMPTY":
            return game_board
        if user_input == "CONTENTS":
            content = []
            for row in range(len(game_board) - 1):
                content.append([])
                for num in range(len(game_board[row])):
                    content[row].append(" ")

            for row in range(len(game_board) - 1):
                user_input = input()
                jewel = 0
                while jewel != len(user_input):
                    content[jewel][row] = user_input[jewel]
                    jewel += 1

            for a in range(len(game_board) - 1):
                game_board[a] = content[a]

            return game_board

    def print_board(self, game_state, matching:bool) -> None:
        """Prints out the game board for the user"""
        row_number = 0
        column_number = 0



        while column_number != len(game_state[0]):
            print("|", end="")

            for row in range(len(game_state) - 1):

                if matching and game_state[row_number][column_number].islower():
                    print("*" + str(game_state[row_number][column_number]).upper() + "*", end="")

                elif game_state[row_number][column_number].islower() and not game_state[-1][-1]:
                    print("[" + game_state[row_number][column_number].upper() + "]", end="")

                elif game_state[row_number][column_number].islower() and game_state[-1][-1]:
                    print("|" + game_state[row_number][column_number].upper() + "|", end="")

                else:
                    print(" " + game_state[row_number][column_number] + " ", end="")
                row_number += 1

            row_number = 0
            column_number += 1
            print("|", end="")
            print()
            if column_number >= len(game_state[0]):
                column_number = len(game_state[0])

        dashes = " "
        if len(game_state) - 1 > len(game_state[0]):
            for length in range(len(game_state[0]) * 4 - 1):
                dashes += "-"
            dashes += " "
        else:
            for length in range(len(game_state) * 3 - 3):
                dashes += "-"
            dashes += " "
        print(dashes)

    def check_user_input(self, game_state) -> "namedtuple":
        user_input = input()

        if user_input == "":
            return self._drop_faller(game_state)

        command = user_input.split()[0]
        sub_command = user_input.split()[1::]

        if command == "F":
            return self.create_faller(game_state, sub_command)
        elif command == "R":
            return self._rotate_faller(game_state)
        elif command == "<":
            return self._shift_faller(game_state, 'LEFT')
        elif command == ">":
            return self._shift_faller(game_state, 'RIGHT')
        elif command == "Q":
            return "QUIT"

    def create_faller(self, game_state, sub_command) -> "Game Board":
        """Takes information from the sub command to return a list containing the faller"""
        if game_state[-1] != [0, [], 0, False]:
            return game_state

        valid_jewels = self._check_jewel_validity(sub_command[1::])
        faller = [int(sub_command[0]) - 1, valid_jewels, 1, False]
        game_state[-1] = faller

        if game_state[faller[0]][0] != " " and game_state[faller[0]][0].isupper():
            print("GAME OVER")
            game_state = "QUIT"
            return game_state

        game_state[faller[0]][0] = faller[1][-1]
        if game_state[faller[0]][1] != " " and game_state[faller[0]][1].isupper():
            faller[-1] = True
            game_state[-1] = faller
            return game_state

        return game_state

    def _check_jewel_validity(self, jewels) -> ["jewels"]:
        """Takes a list of jewels and checks if the jewels in that list are all valid and if so return that list"""
        valid_jewels = []
        for jewel in jewels:
            if jewel in self.JEWELS:
                valid_jewels.append(jewel.lower())

        if len(valid_jewels) != 3:
            print("AN ERROR HAS OCCURED")
        else:
            return valid_jewels

    def _drop_faller(self, game_state) -> "Game Board":

        if game_state[-1] != [0, [], 0, False]:
            faller = [game_state[-1][0], game_state[-1][1], game_state[-1][2], game_state[-1][3]]
        else:
            for row in range(len(game_state) - 1):
                for column in range(len(game_state[row])):
                    if game_state[row][column].islower():
                        game_state[row][column] = " "

            game_state = self.drop_jewels(game_state)
            return game_state

        if self.check_for_player_loss(game_state, game_state[-1]):
            print("GAME OVER")
            return "QUIT"

        if self._check_drop_validity(game_state, faller):
            return self._complete_freeze(game_state)

        for piece in reversed(range(len(game_state[faller[0]]))):
            if game_state[faller[0]][piece] != " " and game_state[faller[0]][piece].islower():
                game_state[faller[0]][piece + 1] = game_state[faller[0]][piece]
                if faller[2] == -1:
                    game_state[faller[0]][piece] = " "
                    if self._check_drop_validity(game_state, faller):
                        faller[-1] = True
                        game_state[-1] = faller
                        return game_state
                    return game_state

                game_state[faller[0]][piece] = faller[1][faller[2]]
                faller[2] -= 1

        if game_state[faller[0]][2] != " " and game_state[faller[0]][2].isupper():
            faller[-1] = True
            game_state[-1] = faller
            return game_state

        if self._check_drop_validity(game_state, faller):
            if faller[2] == -1:
                faller[-1] = True
                game_state[-1] = faller
            return game_state

        return game_state

    def _rotate_faller(self, game_state) -> "Game State":
        if game_state[-1] != [0, [], 0, False]:
            faller = game_state[-1]
        else:
            return game_state

        swap_jewels = []

        swap_jewels.append(game_state[-1][1][2])
        swap_jewels.append(game_state[-1][1][0])
        swap_jewels.append(game_state[-1][1][1])


        new_column = game_state[faller[0]]

        count = 0
        for spot in game_state[faller[0]]:
            if spot.islower():
                count += 1

        if count == 1:
            for index_num in range(2, 1, -1):
                jewel = game_state[faller[0]].index(game_state[-1][1][index_num])
                new_column[jewel] = swap_jewels[index_num]
        elif count == 2:
            for index_num in range(2, 0, -1):
                jewel = game_state[faller[0]].index(game_state[-1][1][index_num])
                new_column[jewel] = swap_jewels[index_num]

        else:
            temp = 2
            for index_num in reversed(range(len(new_column))):
                if new_column[index_num].islower():
                    new_column[index_num] = swap_jewels[temp]
                    temp -= 1

        game_state[-1][1] = swap_jewels
        game_state[faller[0]] = new_column
        return game_state

    def _shift_faller(self, game_state, shift_location) -> "Game Board":
        if game_state[-1] != [0, [], 0, False]:
            faller = game_state[-1]
        else:
            return game_state

        count = 0
        for spot in game_state[faller[0]]:
            if spot.islower():
                count += 1

        check = 0
        check2 = 0
        if shift_location == "RIGHT":
            old_column = game_state[faller[0]][:]
            new_column = game_state[faller[0] + 1][:]
            location = faller[0] + 1
        elif shift_location == "LEFT":
            old_column = game_state[faller[0]][:]
            new_column = game_state[faller[0] -1][:]
            location = faller[0] - 1

        for index_num in reversed(range(len(game_state[faller[0]]))):
            if location < 0 or location > len(game_state) - 2:
                return game_state

            if count < 3:
                check2 = 2
                if game_state[faller[0]][index_num].islower():
                    if game_state[faller[0]][index_num].islower():
                        jewel = index_num

                        if check2 != count:
                            check2 -= 1

                        if game_state[location][jewel] != " ":
                            print("UNABLE TO MOVE")
                            return game_state

                        elif game_state[location][jewel] == " ":
                            new_column[index_num] = old_column[index_num]
                            old_column[index_num] = " "
                            check += 1

            elif game_state[faller[0]][index_num].islower():
                jewel = index_num
                check2 += 1

                if game_state[location][jewel] != " ":
                    return game_state

                elif game_state[location][jewel] == " ":
                    new_column[index_num] = old_column[index_num]
                    old_column[index_num] = " "
                    check += 1

            if check == count:
                game_state[faller[0]] = old_column
                game_state[location] = new_column
                if shift_location == "RIGHT":
                    faller[0] += 1
                elif shift_location == "LEFT":
                    faller[0] -= 1

                if not self._check_drop_validity(game_state, faller):
                    faller[-1] = False
                    faller[2] = 1

                if index_num + 1 < len(game_state[faller[0]]) - 1 and faller[-1] == False:
                    if game_state[faller[0]][index_num + 1] != " ":
                        if self._check_drop_validity(game_state, faller):
                            faller[-1] = True
                            game_state[-1] = faller

                return game_state

        return game_state

    def _complete_freeze(self, game_state) -> "Game State":
        for row in range(len(game_state) - 1):
            for column in range(len(game_state[0])):
                game_state[row][column] = game_state[row][column].upper()
        game_state[-1] = [0, [], 0, False]
        return game_state

    def _check_drop_validity(self, game_state, faller) -> bool:
            x = -1
            for n in reversed(range(len(game_state[faller[0]]))):
                if x == -1:
                    if game_state[faller[0]][n].islower():
                        x = n
            if not (x + 1) > int(len(game_state[faller[0]]) - 1):
                if x == -1:
                    return True
                return game_state[faller[0]][x + 1] != " "

            else:
                return True

    def check_for_player_loss(self, game_state, faller) -> bool:

        if faller == [0, [], 0, False]:
            return False

        x = -1
        for n in reversed(range(len(game_state[faller[0]]))):
            if x == -1:
                if game_state[faller[0]][n].islower():
                    x = n

        if x >= 2:
            return False

        return game_state[faller[0]][x + 1] != " " and (x == 1 or x == 0)

    def drop_jewels(self, game_state) -> "Game Board":
        """Control the dropping of jewels into empty space"""
        potential_clear = False
        check = 0

        empty_check = 0
        for row in range(len(game_state) - 1):
            for column in game_state[row]:
                empty_check += column.count(" ")

        if empty_check == (len(game_state) - 1) * len(game_state[0]):
            return game_state

        while not potential_clear:
            for row in range(len(game_state) - 1):
                finished = False

                while not finished:
                    for column in range(len(game_state[0]) - 1):
                        if game_state[row][column] != " ":
                            if game_state[row][column + 1] == " ":
                                game_state[row][column + 1] = game_state[row][column]
                                game_state[row][column] = " "
                                check = 0
                            else:
                                check += 1
                        if check > len(game_state[0]) * len(game_state):
                            finished = True
                            check = 0
                        if game_state[row][column] in self.JEWELS and game_state[row][column + 1] == " ":
                            check += 1

            potential_clear = True

        return game_state

    def check_for_clear(self, game_state) -> "Pseudo Game Board":
        count = 1
        index_num_row = 0
        index_num_column = 0
        check = 0
        lower_check = 0
        temp = 1
        temp_check1 = True
        temp_check2 = True
        jewels = ["S", "T", "V", "W", "X", "Y", "Z"]

        pseudo_original_game_state = copy.deepcopy(game_state)
        pseudo_game_state = copy.deepcopy(game_state)

        rows = len(pseudo_game_state) - 2
        columns = len(pseudo_game_state[0]) - 1

        """HORIZONTAL/VERTICAL"""
        while check < rows + 1:

            if index_num_row > rows:
                index_num_row = 0

            if pseudo_game_state[index_num_row][index_num_column] != " " and pseudo_game_state[index_num_row][index_num_column].upper() in jewels:
                jewel_check = pseudo_game_state[index_num_row][index_num_column]

                """UP/DOWN"""
                while temp_check1 and temp_check2:
                    if index_num_column + temp <= columns:
                        if pseudo_game_state[index_num_row][index_num_column + temp].upper() == jewel_check:
                            pseudo_game_state[index_num_row][index_num_column + temp] = pseudo_game_state[index_num_row][index_num_column + temp].lower()
                            count += 1
                        else:
                            temp_check1 = False
                    else:
                        temp_check1 = False

                    if index_num_column - temp <= columns:
                        if pseudo_game_state[index_num_row][index_num_column - temp].upper() == jewel_check:
                            pseudo_game_state[index_num_row][index_num_column - temp] = pseudo_game_state[index_num_row][index_num_column - temp].lower()
                            count += 1
                        else:
                            temp_check2 = False
                    else:
                        temp_check2 = False

                    temp += 1

                if count < 3:
                    pseudo_game_state = copy.deepcopy(pseudo_original_game_state)
                    count = 1

                if count >= 3:
                    pseudo_game_state[index_num_row][index_num_column] = pseudo_game_state[index_num_row][index_num_column].lower()
                    pseudo_original_game_state = pseudo_game_state
                    count = 1
                    check = 0

                temp = 1
                temp_check1 = True
                temp_check2 = True

                """LEFT/RIGHT"""
                while temp_check1 and temp_check2:
                    if index_num_row + temp <= rows:
                        if pseudo_game_state[index_num_row + temp][index_num_column].upper() == jewel_check:
                            pseudo_game_state[index_num_row + temp][index_num_column] = pseudo_game_state[index_num_row + temp][index_num_column].lower()
                            count += 1
                        else:
                            temp_check1 = False
                    else:
                        temp_check1 = False

                    if index_num_row - temp <= rows and index_num_row - temp >= 0:
                        if pseudo_game_state[index_num_row - temp][index_num_column].upper() == jewel_check:
                            pseudo_game_state[index_num_row - temp][index_num_column] = pseudo_game_state[index_num_row - temp][index_num_column].lower()
                            count += 1
                        else:
                            temp_check2 = False
                    else:
                        temp_check2 = False

                    temp += 1

                if count < 3:
                    count = 1
                    pseudo_game_state = copy.deepcopy(pseudo_original_game_state)

                if count >= 3:
                    pseudo_game_state[index_num_row][index_num_column] = pseudo_game_state[index_num_row][index_num_column].lower()
                    pseudo_original_game_state = pseudo_game_state
                    count = 1
                    check = 0

                temp = 1
                temp_check1 = True
                temp_check2 = True

                """DIAGONAL"""
                while temp_check1 and temp_check2:
                    if (0 <= index_num_row - temp <= rows and index_num_row + temp <= rows) and index_num_column + temp <= columns:
                        if pseudo_game_state[index_num_row - temp][index_num_column + temp].upper() == jewel_check:
                            pseudo_game_state[index_num_row - temp][index_num_column + temp] = pseudo_game_state[index_num_row - temp][index_num_column + temp].lower()
                            count += 1
                        elif pseudo_game_state[index_num_row + temp][index_num_column + temp].upper() == jewel_check:
                            pseudo_game_state[index_num_row + temp][index_num_column + temp] = pseudo_game_state[index_num_row + temp][index_num_column + temp].lower()
                            count += 1
                        else:
                            temp_check1 = False
                    else:
                        temp_check1 = False

                    if (0 <= index_num_row - temp <= rows and index_num_row + temp <= rows) and index_num_column - temp <= columns:
                        if pseudo_game_state[index_num_row - temp][index_num_column - temp].upper() == jewel_check:
                            pseudo_game_state[index_num_row - temp][index_num_column - temp] = pseudo_game_state[index_num_row - temp][index_num_column - temp].lower()
                            count += 1
                        elif pseudo_game_state[index_num_row + temp][index_num_column - temp].upper() == jewel_check:
                            pseudo_game_state[index_num_row + temp][index_num_column - temp] = pseudo_game_state[index_num_row + temp][index_num_column - temp].lower()
                            count += 1
                        else:
                            temp_check2 = False
                    else:
                        temp_check2 = False

                    temp += 1

                temp = 1
                temp_check1 = True
                temp_check2 = True

                if count < 3:
                    count = 1
                    pseudo_game_state = copy.deepcopy(pseudo_original_game_state)
                    index_num_column += 1

                if count >= 3:
                    pseudo_game_state[index_num_row][index_num_column] = pseudo_game_state[index_num_row][index_num_column].lower()
                    pseudo_original_game_state = pseudo_game_state
                    count = 1
                    check = 0

            else:
                index_num_column += 1

            if index_num_column > columns:
                index_num_row += 1
                index_num_column = 0
                check += 1

        return pseudo_original_game_state


def run_game() -> "game_state":
    game = ColumnsGame()
    game_state = game.create_board(game.obtain_board_inputs())
    game_state = game.board_contents(game_state)
    game_state = game.drop_jewels(game_state)

    while True:
        if game_state[-1] == [0, [], 0, False]:
            new_game_state = game.check_for_clear(game_state)
            if new_game_state != game_state:
                game.print_board(new_game_state, True)
                game_state = new_game_state
            else:
                game.print_board(game_state, False)
        else:
            game.print_board(game_state, False)

        game_state = game.check_user_input(game_state)
        if game_state == "QUIT":
            return


if __name__ == "__main__":
    run_game()
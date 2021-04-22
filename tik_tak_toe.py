
import random
import os
from typing import Union


# Function to clear output
def clear_output():
    if os.name == 'posix':
    # for mac and linux, os.name is 'posix'
        os.system('clear')
    else:
    # for windows users, os.name is 'nt'
        os.system('cls')


# Players
class Player:

    def __init__(self, avatar: str, name=None) -> None:
        self.name = name
        self.avatar = avatar
        self.statistics = { 'wins': 0, 'losses': 0, 'draws': 0 }

    def __str__(self) -> str:
        return f'Player {self.name} ({self.avatar})'

    # Update whether player wins or loses
    def update_stats(self, stat: str) -> None:
        if stat == 'win':
            self.statistics['wins'] += 1
        if stat == 'loss':
            self.statistics['losses'] += 1
        if stat == 'draw':
            self.statistics['draws'] += 1

    # Show Player statistics
    def get_stats(self):
        return f'{self.__str__()} : \t wins= { self.statistics["wins"] } , draws= {self.statistics["draws"]}, losses= {self.statistics["losses"]} \
                : Games played: {sum([self.statistics["wins"], self.statistics["losses"], self.statistics["draws"] ])} '


# Function to set players
def set_player(num: int) -> str:
    accept = False
    player_name = ''

    while not accept:
        player_name = input(f'Enter player { num } name: ')
        if len(player_name) < 1:
            print(f'Sorry, player {num} name cannot be blank.')
            continue

        choice = 'wrong'
        while choice not in ('Y', 'y', 'N', 'n'):
            choice = input(f'Accept the username: {player_name} : ? (Y or N) ')
            if choice not in ('Y', 'y', 'N', 'n'):
                print('Please enter a valid choice.')

        if choice in ('Y', 'y'):
            accept = True

    return player_name


# Function to accept user choice
def user_choice() -> int:
    choice = 'wrong'
    acceptable_input = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    while choice not in acceptable_input:
        choice = input('Pick a position 1-9 (reference number-pad on a full-sized keyboard) ')

        if choice not in acceptable_input:
            print('Sorry, invalid choice ')

    return int(choice)



# Check if a player has won a game or if there are no more open positions
def check_board(board, avatar: str):
    won = False
    has_open_positons = False

    # winning_options = [
    #             [1, 2, 3], [1, 4, 7], [1, 5, 9],
    #             [2, 5, 8], [3, 5, 7], [3, 6, 9],
    #             [4, 5, 6], [7, 8, 9]
    #         ]

    if  board[1] == board [2] == board[3] == avatar:
        won = True
    elif  board[1] == board [4] == board[7] == avatar:
        won = True
    elif  board[1] == board [5] == board[9] == avatar:
        won = True
    elif  board[2] == board [5] == board[8] == avatar:
        won = True
    elif  board[3] == board [5] == board[7] == avatar:
        won = True
    elif  board[3] == board [6] == board[9] == avatar:
        won = True
    elif  board[4] == board [5] == board[6] == avatar:
        won = True
    elif  board[7] == board [8] == board[9] == avatar:
        won = True

    for i in range(1,10):
        if board[i] not in ('X', 'O'):
            has_open_positons = True
            break

    return (has_open_positons, won)


# Function to update board
def update_game_board(board, position: int, avatar: str) -> Union[list[str], bool]:

    if board[position] != ' ':
        print(f'Board position has already been taken. Please make another choice. ')
        return False

    board[position] = avatar

    return board


# Reset Board
def reset_board() -> list[str]:
    board =  [' ',] * 10

    return board


# Game-on choice (ask user if they want to keep on playing)
def gameon_choice() -> bool:
    choice = 'wrong'

    while choice not in ('Y', 'N', 'y', 'n'):
        choice = input('Quit game? (Y or N) ')

        if choice not in ('Y', 'N', 'y', 'n'):
            print('Sorry, please choose Y or N ')

    return True if choice in ('Y', 'y') else False


# Function to display the game
def display_game_board(board):
    clear_output()
    print(f"""
             {board[7]} | {board[8]} | {board[9]}
            -----------
             {board[4]} | {board[5]} | {board[6]}
            -----------
             {board[1]} | {board[2]} | {board[3]}
            """)


def main():

    player1 = Player('X')
    player2 = Player('O')

    player1.name = set_player(1)

    player2.name = set_player(2)

    players = [player1, player2]

    clear_output()

    board = reset_board()

    game_over = False
    
    is_first_player_selected = False

    won, has_open_positions = False, True

    while not game_over:
        if not is_first_player_selected:
            flip = random.randint(0,1)

            if flip == 1:
                players.reverse()
            
            is_first_player_selected = True

            clear_output()

            print(f'{players[0]} is playing first \n')

            input('Enter any key to continue: ')

            while not won and has_open_positions:

                display_game_board(board)
                player = players[0]
                position = user_choice()

                valid_position = False
                while not valid_position:
                    temp_board = update_game_board(board, position, player.avatar)
                    if temp_board != False:
                        board = temp_board
                        valid_position = True

                # Check if player won or board complete
                has_open_positions, won = check_board(board, player.avatar)
                if won:
                    display_game_board(board)
                    print(f'Player {player} WON !!')
                    player.update_stats('win')
                    players[1].update_stats('loss')

                    break
                if not has_open_positions:
                    display_game_board(board)
                    print(f'Game is DRAW')
                    player.update_stats('draw')
                    players[1].update_stats('draw')

                    break

                # switch between players so long as the game is not won 
                # and there are still open moves on the board
                players.reverse()

            for player in players:
                print(f'{player} : {player.get_stats()}')

            game_over = gameon_choice()
            if not game_over:
                board = reset_board()
                is_first_player_selected = False
                won, has_open_positions = False, True
                continue



if __name__=='__main__':
    main()

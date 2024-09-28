'''
Name: Project 1 - Battleship Game
Description: Simple Battleship game made in python
Inputs: Players provide coordinates for ship placement and attacks (e.g., A1 for column A and row 1). For ships 
longer than one grid space, players specify a direction (H for horizontal, V for vertical).
Outputs: The game board is updated and displayed after each turn, showing hits, misses, and the 
positions of the player's ships.
Collaborators/Sources: 
Michael Oliver, Peter Pham, Jack Youngquist, Andrew Uriell, Ian Wilson, ChatGPT
Aug 31 2024
'''
import os
import random

# ANSI Coloring for text
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
DEFAULT = '\033[0m'

# tracks respective player's attacks and current board using a 2D list
p1_game_board = [[' ']*10 for _ in range(10)] # track player's board incuding ship placement and enemy attacks
p1_attack_board = [[' ']*10 for _ in range(10)] #track where player one has fired from their pov
p2_game_board = [[' ']*10 for _ in range(10)]
p2_attack_board = [[' ']*10 for _ in range(10)]

# x and y axis for accessing the game boards
x = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9}
y = [str(num) for num in range(1,11)]

p1_ships = {} # Dictionary to store Player 1 ships
p2_ships = {} # Dictionary to store Player 2 ships

ai_targets = [] # List for medium AI target tracking

# system function to clear the terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_single_board(game_board):
    print(f"{'':<3}{BLUE}| ",end='')
    for letter in 'ABCDEFGHIJ':
        print(f'{YELLOW}{letter}{BLUE} | ',end='')
    print('')
    for index, row in enumerate(game_board):
        print(f'{"-"*45}')
        string = ''
        for cell in row:
            string = string + f' {cell} |'
        print(f"{YELLOW}{index+1:>2}{BLUE} |{string}")
    print(DEFAULT)

def print_full_board(attack_board, game_board):
    # Print both the attack board and the player's own board side by side
    print(f'{RED}Attack board:{DEFAULT}\t\t\t\t\t\t{GREEN}Your board:{DEFAULT}\n')
    string = f'{"":<3}{BLUE}| '
    for letter in 'ABCDEFGHIJ':
        string += (f'{YELLOW}{letter}{BLUE} | ')
    string += '\t\t'
    string += f'{"":<3}{BLUE}| '
    for letter in 'ABCDEFGHIJ':
        string += (f'{YELLOW}{letter}{BLUE} | ')
    string += '\n'

    for index, (attack_board_row, game_board_row) in enumerate(zip(attack_board, game_board)):
        string += f'{"-"*45}\t\t{"-"*45}\n'

        cell_row = ''
        for cell_value in attack_board_row:
            cell_row = cell_row + f' {cell_value} |'
        string += f'{YELLOW}{index+1:>2}{BLUE} |{cell_row}\t\t'

        cell_row = ''
        for cell_value in game_board_row:
            cell_row = cell_row + f' {cell_value} |'
        string += f'{YELLOW}{index+1:>2}{BLUE} |{cell_row}\n'

    print(string, end=f'{DEFAULT}\n')

# Parameters: The players board, which player is being reffered to, the disctionary of that players ships
# ChatGPT was used to split one ship placement function into two separate fundtions to query and validate ship placement.
def query_ship_placement(game_board, player, player_ships):
    for ship, size in ships:
        while True:
            print_single_board(game_board)
            print(f'Player {player}, place your {ship} of size {size} [e.g., A1]:')
            start_pos = input('Enter the starting position:\n').lower()

            if size != 1:
                direction = input('Enter direction (H for horizontal, V for vertical):\n').lower()
                if direction == 'h':
                    horiz_dir = input('Enter horizontal direction (R for right, L for left):\n').lower()
                    vert_dir = None
                elif direction == 'v':
                    horiz_dir = None
                    vert_dir = input('Enter vertical direction (U for up, D for down):\n').lower()
                else:
                    print(f"Invalid direction input! Please enter 'H' for horizontal or 'V' for vertical.") # If invalid input, reprompt
                    continue
                
                if validate_ship_placement(start_pos, size, game_board, direction, horiz_dir, vert_dir):
                    place_ship(start_pos, size, game_board, player_ships, ship, direction, horiz_dir, vert_dir)
                    break
                else:
                    print(f'Invalid placement for {ship}. Try again.')
            else:
                if validate_ship_placement(start_pos, size, game_board):
                    place_ship(start_pos, size, game_board, player_ships, ship)
                    break
                else:
                    print(f'Invalid placement for {ship}. Try again.')

def validate_ship_placement(start_pos, size, game_board, direction=None, horiz_dir=None, vert_dir=None):
    if start_pos[0] in x and start_pos[1:] in y: # Verifies position is within the board dimensions
        col = x[start_pos[0]]  # Convert column letter to index
        row = int(start_pos[1:]) - 1  # Convert row number to index (0-based)

        if direction == 'h':  # Horizontal placement
            if horiz_dir == 'r':
                if col + size > 10:  # Out of bounds in column direction
                    return False
                for i in range(size):
                    if game_board[row][col + i] != ' ':  # Check overlap
                        return False
            elif horiz_dir == 'l':
                if col - size + 1 < 0:  # Out of bounds in column direction
                    return False
                for i in range(size):
                    if game_board[row][col - i] != ' ':  # Check overlap
                        return False
            elif horiz_dir != 'r' and horiz_dir != 'l': # Check for bad input. If there is bad input, reprompt user
                return False
            return True
        #need to check for good input

        elif direction == 'v':  # Vertical placement
            if vert_dir == 'd':
                if row + size > 10:  # Out of bounds in row direction
                    return False
                for i in range(size):
                    if game_board[row + i][col] != ' ':  # Check overlap
                        return False
            elif vert_dir == 'u':
                if row - size + 1 < 0:  # Out of bounds in row direction
                    return False
                for i in range(size):
                    if game_board[row - i][col] != ' ':  # Check overlap
                        return False
            elif vert_dir == 'd' and vert_dir == 'u': # Check for bad input. If there is bad input, reprompt user
                return False
            return True
        
        # Ships of size 1
        elif direction == None:
            return True
        
        raise BaseException(f'Unable to validate ship placement: {direction} {horiz_dir} {vert_dir}')
    else:
        return False

def place_ship(start_pos, size, game_board, player_ships, ship_name,  direction=None, horiz_dir=None, vert_dir=None):
    col = x[start_pos[0]]  # Convert column letter to index
    row = int(start_pos[1:]) - 1  # Convert row number to index (0-based)
    coordinates = [] # Holds the ships coordinates

    if direction == 'h':  # Horizontal placement
        if horiz_dir == 'r':
            for i in range(size):
                game_board[row][col + i] = 'S'
                coordinates.append((row, col + i)) # Track the ships position
        elif horiz_dir == 'l':
            for i in range(size):
                game_board[row][col - i] = 'S'
                coordinates.append((row, col - i)) # Track the ships position

    elif direction == 'v':  # Vertical placement
        if vert_dir == 'd':
            for i in range(size):
                game_board[row + i][col] = 'S'
                coordinates.append((row + i, col)) # Track the ships position
        elif vert_dir == 'u':
            for i in range(size):
                game_board[row - i][col] = 'S'
                coordinates.append((row - i, col)) # Track the ships position

    # ships of size 1
    elif direction == None:
        game_board[row][col] = 'S'
        coordinates.append((row, col)) # Track the ships position

    player_ships[ship_name] = coordinates # Add the coordinates of the ships to the players ship dictionary

# Check to see if a players ship is destoryed
def check_ship_destroyed(player_ships, game_board):
    for ship, positions in player_ships.items():
        destroyed = all(game_board[row][col] == f'{RED}X{BLUE}' for row, col in positions)
        if destroyed:
            print(f"{RED}{ship} has been destroyed!{DEFAULT}")
            del player_ships[ship]
            break

# Check if a player has won the game
def check_winner(player_ships):
    if len(player_ships) == 0:
        return True
    return False

def check_attack(attack_pos, game_board): # returns True if valid move
    if attack_pos[0] in x and attack_pos[1:] in y:
        attack_col = x[attack_pos[0]]
        attack_row = int(attack_pos[1:]) - 1
        # check for already attacked positions
        if game_board[attack_row][attack_col] in (' ', 'S'):
            return True
        else:
            print(f'Cell has already been attacked!')
            return False
    else:
        print(f'Please enter a valid cell to attack! [A1]')
        return False

def game_setup():
    global opponent_type
    global ai_difficulty
    # Ask for the number of ships
    while True:
        try:
            number_of_ships = int(input('How many ships should be used? (1-5):\n'))
            if 1 <= number_of_ships <= 5:
                break
            else:
                print(f'Please select a valid number of ships between 1 and 5!\n')
        except ValueError:
            print(f'Input must be a valid number!')

    ship_sizes = {"Liberty": 1, "Destroyer": 2, "Submarine": 3, "Battleship": 4, "Carrier": 5}
    global ships
    ships = list(ship_sizes.items())[:number_of_ships]  # Only take the required number of ships

    # Ask the user whether to play against a human or AI
    while True:
        opponent_choice = input('Do you want to play against a human or AI? Enter "H" for human, "AI" for AI opponent:\n').lower()
        if opponent_choice == 'h':
            opponent_type = 'human'
            break
        elif opponent_choice == 'ai':
            opponent_type = 'AI'
            break
        else:
            print('Please enter "H" for human or "AI" for AI opponent.')

    # If playing against AI, ask for difficulty level
    if opponent_type == 'AI':
        while True:
            ai_level = input('Select AI difficulty level - Easy (E), Medium (M), Hard (H):\n').lower()
            if ai_level == 'e':
                ai_difficulty = 'easy'
                break
            elif ai_level == 'm':
                ai_difficulty = 'medium'
                break
            elif ai_level == 'h':
                ai_difficulty = 'hard'
                break
            else:
                print('Please enter "E" for Easy, "M" for Medium, or "H" for Hard.')
    else:
        ai_difficulty = None # Not playing against AI

    # Player 1 game board setup
    query_ship_placement(p1_game_board, 1, p1_ships)
    clear_screen()

    if opponent_type == 'human':
        # Player 2 game board setup
        query_ship_placement(p2_game_board, 2, p2_ships)
    else:
        # AI places ships randomly
        place_ai_ships(p2_game_board, p2_ships)
        print('AI has placed its ships.')
        input('Press Enter to continue.')

def place_ai_ships(game_board, player_ships):
    # AI places ships randomly
    for ship, size in ships:
        while True:
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            direction = random.choice(['h', 'v'])
            if direction == 'h':
                horiz_dir = random.choice(['r', 'l'])
                vert_dir = None # No vertical direction needed
            else:
                vert_dir = random.choice(['u', 'd'])
                horiz_dir = None # No horizontal direction needed

            start_col_letter = list(x.keys())[list(x.values()).index(col)] # Convert column index to letter
            start_pos = start_col_letter + str(row + 1) # Construct start position string

            if validate_ship_placement(start_pos, size, game_board, direction, horiz_dir, vert_dir):
                place_ship(start_pos, size, game_board, player_ships, ship, direction, horiz_dir, vert_dir)
                break

def process_attack(attack_row, attack_col, attacker_attack_board, defender_game_board, defender_ships):
    # Process an attack on the given coordinates, updates boards and checks for ship destruction.
    if defender_game_board[attack_row][attack_col] == 'S':
        # If the defender has a ship at the attack position
        defender_game_board[attack_row][attack_col] = f'{RED}X{BLUE}'
        attacker_attack_board[attack_row][attack_col] = f'{RED}X{BLUE}'
        check_ship_destroyed(defender_ships, defender_game_board)
        return True # Indicate a hit
    else:
        # If the attack misses
        defender_game_board[attack_row][attack_col] = f'{RED}O{BLUE}'
        attacker_attack_board[attack_row][attack_col] = f'{RED}O{BLUE}'
        return False # Indicate a miss

def player_turn(player_num, attacker_attack_board, attacker_game_board, defender_game_board, defender_ships):
    # Handle a player's turn by getting attack input and processing the attack
    clear_screen()
    print_full_board(attacker_attack_board, attacker_game_board)
    while True:
        attack_pos = input(f'{RED}Player {player_num}{DEFAULT}: Which cell would you like to attack? [A1]:\n').lower()
        if attack_pos[0] not in x or attack_pos[1:] not in y:
            print(f'Please enter a valid cell!')
            continue
        attack_col = x[attack_pos[0]]
        attack_row = int(attack_pos[1:]) - 1
        if check_attack(attack_pos, defender_game_board):
            hit = process_attack(attack_row, attack_col, attacker_attack_board, defender_game_board, defender_ships)
            if hit:
                shot = "Hit!"
            else:
                shot = "Miss"
            break
    clear_screen()
    print_full_board(attacker_attack_board, attacker_game_board)
    print(shot)
    input("Press enter to end turn: ")

def run_game():
    while True:
        # Player 1 turn
        player_turn(1, p1_attack_board, p1_game_board, p2_game_board, p2_ships)

        # Check if Player 1 has won
        if check_winner(p2_ships):
            print(f"Player 1 Wins!{DEFAULT}\n")
            break
        elif check_winner(p1_ships):
            if opponent_type == 'AI':
                print(f"AI Wins!{DEFAULT}\n")
            else:
                print(f"Player 2 Wins!{DEFAULT}\n")
            break

        if opponent_type == 'human':
            input("Press enter to begin turn player 2: ")
            # Player 2 turn
            player_turn(2, p2_attack_board, p2_game_board, p1_game_board, p1_ships)
        else:
            # AI's turn
            clear_screen()
            print(f"{RED}AI's Turn{DEFAULT}\n")
            ai_attack(p2_attack_board, p1_game_board, p1_ships)
            input("Press Enter to continue: ")

        # Check if Player 2 has won
        if check_winner(p1_ships):
            if opponent_type == 'AI':
                print(f"AI Wins!{DEFAULT}\n")
            else:
                print(f"Player 2 Wins!{DEFAULT}\n")
            break
        elif check_winner(p2_ships):
            print(f"Player 1 Wins!{DEFAULT}\n")
            break

def ai_attack(attack_board, opponent_game_board, opponent_ships):
    if ai_difficulty == 'easy':
        # AI fires randomly every turn
        while True:
            attack_row = random.randint(0, 9)
            attack_col = random.randint(0, 9)
            if opponent_game_board[attack_row][attack_col] in (' ', 'S'):
                hit = process_attack(attack_row, attack_col, attack_board, opponent_game_board, opponent_ships)
                if hit:
                    shot = "AI hits your ship!"
                else:
                    shot = "AI misses."
                break
    elif ai_difficulty == 'medium':
        # AI fires randomly until it hits a ship then fires in orthogonally adjacent spaces to find other hits until a ship is sunk
        global ai_targets
        if ai_targets:
            # AI has targets to attack
            attack_row, attack_col = ai_targets.pop(0) # Get next target from list
            if opponent_game_board[attack_row][attack_col] in (' ', 'S'):
                hit = process_attack(attack_row, attack_col, attack_board, opponent_game_board, opponent_ships)
                if hit:
                    shot = "AI hits your ship!"
                    add_adjacent_targets(attack_row, attack_col, opponent_game_board)
                else:
                    shot = "AI misses."
            else:
                # Cell already attacked, pick next target
                ai_attack(attack_board, opponent_game_board, opponent_ships) # Recursive call to attack again
                return
        else:
            # AI fires randomly
            while True:
                attack_row = random.randint(0, 9)
                attack_col = random.randint(0, 9)
                if opponent_game_board[attack_row][attack_col] in (' ', 'S'):
                    hit = process_attack(attack_row, attack_col, attack_board, opponent_game_board, opponent_ships)
                    if hit:
                        shot = "AI hits your ship!"
                        add_adjacent_targets(attack_row, attack_col, opponent_game_board)
                    else:
                        shot = "AI misses."
                    break
    elif ai_difficulty == 'hard':
        # AI knows where all your ships are and lands a hit every turn
        for row in range(10):
            for col in range(10):
                if opponent_game_board[row][col] == 'S':
                    # Hit this ship
                    hit = process_attack(row, col, attack_board, opponent_game_board, opponent_ships)
                    shot = "AI hits your ship!"
                    print(shot)
                    return
        # If no ships found, fire randomly
        while True:
            attack_row = random.randint(0, 9)
            attack_col = random.randint(0, 9)
            if opponent_game_board[attack_row][attack_col] == ' ':
                hit = process_attack(attack_row, attack_col, attack_board, opponent_game_board, opponent_ships)
                shot = "AI misses."
                break

    print(shot)

def add_adjacent_targets(row, col, opponent_game_board):
    # Add orthogonally adjacent positions to ai_targets if they are within bounds and not already attacked
    adjacent_positions = [
        (row -1, col), # Up
        (row +1, col), # Down
        (row, col -1), # Left
        (row, col +1) # Right
    ]
    for r, c in adjacent_positions:
        if 0 <= r < 10 and 0 <= c <10:
            if opponent_game_board[r][c] not in (f'{RED}X{BLUE}', f'{RED}O{BLUE}'):
                ai_targets.append((r, c)) # Add position to ai_targets list

def main():
    game_setup()
    run_game()

if __name__ == '__main__':
    main()
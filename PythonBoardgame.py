
# Fox and Hounds
# Language: Python
# Paradigm: Procedural Programming
# Customisation 1: AI Opponent
# Customisation 2: Move Suggestion

# Joseph Cihlar 23467706

import random

BOARD_SIZE = 8

# Create an empty board
board = [["." for col in range(BOARD_SIZE)]
         for row in range(BOARD_SIZE)]

# Place the four hounds
for col in range(1, BOARD_SIZE, 2):
    board[0][col] = "H"

# Place the fox
board[7][4] = "F"


# Display the game board
def display_board():
    print("\n     a b c d e f g h")
    print("   -----------------")

    for row in range(BOARD_SIZE):
        print(row + 1, " |", end=" ")

        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")

        print()
    print()


# Convert a coordinate such as e8 to row and column
def get_position(square):
    if len(square) != 2:
        return None

    col = ord(square[0].lower()) - ord("a")

    if not square[1].isdigit():
        return None

    row = int(square[1]) - 1

    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return row, col

    return None


# Get all legal moves for a piece
def get_legal_moves(row, col, piece):
    moves = []

    if piece == "F":
        row_directions = [-1, 1]
    elif piece == "H":
        row_directions = [1]
    else:
        return moves

    for row_change in row_directions:
        for col_change in [-1, 1]:

            new_row = row + row_change
            new_col = col + col_change

            if (0 <= new_row < BOARD_SIZE and
                    0 <= new_col < BOARD_SIZE):

                if board[new_row][new_col] == ".":
                    moves.append((new_row, new_col))

    return moves


# Move a piece if the move is legal
def move_piece(start, end, player):
    start_pos = get_position(start)
    end_pos = get_position(end)

    if start_pos is None or end_pos is None:
        print("Invalid square! Use coordinates such as e8 or d7.")
        return False

    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = board[start_row][start_col]

    if player == "Fox" and piece != "F":
        print("You must select the fox.")
        return False

    if player == "Hounds" and piece != "H":
        print("You must select a hound.")
        return False

    legal_moves = get_legal_moves(
        start_row, start_col, piece
    )

    if (end_row, end_col) not in legal_moves:
        print("Invalid move! Pieces move diagonally one square.")
        return False

    board[end_row][end_col] = piece
    board[start_row][start_col] = "."

    return True


# Find the fox's position
def find_fox():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == "F":
                return row, col

    return None


# Customisation 2: Suggest a random legal fox move
def suggest_move():
    fox_position = find_fox()

    if fox_position is None:
        print("Fox not found!")
        return

    row, col = fox_position

    legal_moves = get_legal_moves(row, col, "F")

    if not legal_moves:
        print("No legal moves available!")
        return

    suggested_row, suggested_col = random.choice(legal_moves)

    start = chr(col + ord("a")) + str(row + 1)
    end = chr(suggested_col + ord("a")) + str(suggested_row + 1)

    print("Suggested move:", start, "to", end)
    print("This is a legal move, but not necessarily the best move.")


# Check if the fox has reached the top row
def fox_has_won():
    for col in range(BOARD_SIZE):
        if board[0][col] == "F":
            return True

    return False


# Check if the fox is trapped
def fox_is_trapped():
    fox_position = find_fox()

    if fox_position is None:
        return True

    row, col = fox_position
    legal_moves = get_legal_moves(row, col, "F")

    return len(legal_moves) == 0


# Check if any hound can move
def hounds_have_moves():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            if board[row][col] == "H":
                if get_legal_moves(row, col, "H"):
                    return True

    return False


# Convert row and column into game coordinates
def position_to_square(position):
    row, col = position

    letter = chr(col + ord("a"))
    number = str(row + 1)

    return letter + number


# Customisation 1: AI opponent
def ai_hound_move():
    possible_moves = []

    # Find every legal hound move
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            if board[row][col] == "H":
                legal_moves = get_legal_moves(row, col, "H")

                for move in legal_moves:
                    possible_moves.append(((row, col), move))

    if not possible_moves:
        print("The AI has no legal moves remaining.")
        return False

    best_moves = []
    best_score = float("-inf")

    # Test each possible AI move
    for start, end in possible_moves:
        start_row, start_col = start
        end_row, end_col = end

        # Temporarily move a hound
        board[start_row][start_col] = "."
        board[end_row][end_col] = "H"

        # Count how many moves the fox has available
        fox_row, fox_col = find_fox()
        fox_moves = get_legal_moves(fox_row, fox_col, "F")

        # Fewer fox moves gives the AI a higher score
        score = -len(fox_moves)

        # Restore the board
        board[start_row][start_col] = "H"
        board[end_row][end_col] = "."

        if score > best_score:
            best_score = score
            best_moves = [(start, end)]

        elif score == best_score:
            best_moves.append((start, end))

    # Randomly choose between equally good moves
    start, end = random.choice(best_moves)

    start_square = position_to_square(start)
    end_square = position_to_square(end)

    print("AI moves:", start_square, "to", end_square)

    return move_piece(start_square, end_square, "Hounds")


# Process player input
def parse_move(text):
    text = text.lower()
    text = text.replace("-", " ")
    text = text.replace(",", " ")
    text = text.replace("to", " ")

    parts = text.split()

    # Allow e8d7 as well as e8 d7
    if len(parts) == 1 and len(parts[0]) == 4:
        parts = [parts[0][:2], parts[0][2:]]

    return parts


# Main game
def play_game():
    current_player = "Fox"

    print("================================")
    print("         FOX AND HOUNDS")
    print("================================")

    print("You control the Fox (F)")
    print("The AI controls the Hounds (H)")
    print("Empty squares are represented by .")

    print("\nGame Rules:")
    print("- Fox moves diagonally forwards or backwards.")
    print("- Hounds move diagonally downwards only.")
    print("- Fox wins by reaching the top row.")
    print("- Hounds win by trapping the fox.")
    print("- Fox also wins if the hounds cannot move.")

    print("\nCommands:")
    print("- Enter a move such as e8 d7")
    print("- Type hint for a suggested move")
    print("- Type q to quit")

    while True:
        display_board()

        # Check the winning conditions
        if fox_has_won():
            print("Congratulations! The Fox wins!")
            break

        if fox_is_trapped():
            print("The AI wins! The fox is trapped.")
            break

        if not hounds_have_moves():
            print("The Hounds have no moves left!")
            print("The Fox wins!")
            break

        # Computer-controlled hounds
        if current_player == "Hounds":
            print("AI is thinking...")

            if ai_hound_move():
                current_player = "Fox"

            continue

        # Human-controlled fox
        print("Your turn - Fox")

        raw = input(
            "Enter your move (hint or q): "
        ).strip().lower()

        if raw == "q":
            print("Game ended.")
            break

        if raw == "hint":
            suggest_move()
            continue

        move = parse_move(raw)

        if len(move) != 2:
            print("Enter two squares, e.g. e8 d7.")
            continue

        if move_piece(move[0], move[1], current_player):
            current_player = "Hounds"


# Start the program
if __name__ == "__main__":
    play_game()

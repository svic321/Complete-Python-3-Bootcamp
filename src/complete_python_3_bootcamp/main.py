RESET = "\033[0m"
BOLD = "\033[1m"
WIN_COLOR = "\033[92m"
BOARD_POSITIONS = tuple(range(1, 10))
TOP_DOWN_LAYOUT = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
KEYPAD_LAYOUT = ((7, 8, 9), (4, 5, 6), (1, 2, 3))
DISPLAY_LAYOUT = TOP_DOWN_LAYOUT
AVAILABLE_COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}
WINNING_COMBOS = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    (1, 5, 9),
    (3, 5, 7),
)
def print_board(
    board: list[str | None],
    winning_positions: list[int] | None = None,
    player_colors: dict[str, str] | None = None,
    layout: tuple[tuple[int, int, int], ...] = DISPLAY_LAYOUT,
):
    """
    Prints the tic-tac-toe board with optional highlighting of winning positions.

    Args:
        board: The game board
        winning_positions: List of positions that form the winning combination (e.g., [1, 2, 3])
    """
    winning_positions = set(winning_positions or [])

    def format_cell(pos):
        cell = board[pos] if board[pos] is not None else str(pos)
        formatted = f"{cell:^9}"
        color = player_colors.get(cell) if player_colors else None
        if pos in winning_positions:
            color = color or WIN_COLOR
            return f"{BOLD}{color}{formatted}{RESET}"
        return f"{color}{formatted}{RESET}" if color else formatted

    print(
        "\n"
        + "\n".join(f"|{'|'.join(format_cell(pos) for pos in row)}|" for row in layout)
        + "\n"
    )


def has_won(board: list[str | None]) -> tuple[bool, list[int]]:
    """
    Checks if there's a winning combination on the board.

    Returns:
        Tuple of (has_won, winning_positions)
    """
    for combo in WINNING_COMBOS:
        if (
            board[combo[0]] == board[combo[1]] == board[combo[2]]
            and board[combo[0]] is not None
        ):
            return True, combo

    return False, []


def select_player(
    num_players: int = 2,
    available_colors: dict[str, str] | None = None,
) -> tuple[dict[int, str], dict[str, str]]:
    """
    Interactively prompts each player to select their character.

    Args:
        num_players: Number of players (default: 2)

    Returns:
        Tuple containing the player characters and their ANSI colors.
    """
    if available_colors is None:
        available_colors = AVAILABLE_COLORS

    players = {}
    player_colors = {}
    used_chars = set()
    used_colors = set()

    for player_num in range(1, num_players + 1):
        while True:
            char = input(f"Player {player_num}, choose your character: ").lower()

            if not char:
                print("Character cannot be empty. Try again.")
                continue

            if len(char) > 1:
                print("Please enter only one character.")
                continue

            if not char.isalpha():
                print("Please enter only single letters")
                continue

            if char in used_chars:
                print(f"'{char}' is already taken. Choose a different character.")
                continue

            color = input(
                f"Player {player_num}, choose a color "
                f"({', '.join(available_colors)}) or press Enter to skip: "
            ).lower()

            if color and color not in available_colors:
                print("That color is not available. Try again.")
                continue

            if color in used_colors:
                print(f"'{color}' is already taken. Choose a different color.")
                continue

            used_chars.add(char)
            players[player_num] = char
            if color:
                used_colors.add(color)
                player_colors[char] = available_colors[color]
            break

    return players, player_colors


def main() -> None:
    board: list[str | None] = [None] * (len(BOARD_POSITIONS) + 1)
    print_board(board)
    players, player_colors = select_player()
    player_chars = set(players.values())

    while True:
        for player, char in players.items():
            while True:  # Keep asking until valid position is selected
                position = int(
                    input(f"Player {player} using {char!r} select a coordinate [1-9]: ")
                )
                if board[position] in player_chars:
                    print(
                        f"cell is already filled with {board[position]!r}. Select other cell"
                    )
                    continue  # Re-ask this player for input
                break  # Exit while loop when valid position is selected
            board[position] = char

            won, winning_pos = has_won(board)
            if won:
                print_board(
                    board, winning_positions=winning_pos, player_colors=player_colors
                )
                print(f"Congrats player {player} using {char!r}, you won!!!")
                break
            print_board(board, player_colors=player_colors)

            if all(board[position] is not None for position in BOARD_POSITIONS):
                print("The game is a draw: the board is full.")
                return
        else:
            continue
        break


if __name__ == "__main__":
    main()

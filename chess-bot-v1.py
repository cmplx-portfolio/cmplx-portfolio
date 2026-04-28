import random

EMPTY = 0
PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 1, 2, 3, 4, 5, 6
WHITE, BLACK = 1, -1

INITIAL_BOARD = [
    [-ROOK, -KNIGHT, -BISHOP, -QUEEN, -KING, -BISHOP, -KNIGHT, -ROOK],
    [-PAWN]*8,
    [EMPTY]*8,
    [EMPTY]*8,
    [EMPTY]*8,
    [EMPTY]*8,
    [PAWN]*8,
    [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK],
]

PIECE_SYMBOLS = {
    PAWN: 'P', KNIGHT: 'N', BISHOP: 'B', ROOK: 'R', QUEEN: 'Q', KING: 'K',
    -PAWN: 'p', -KNIGHT: 'n', -BISHOP: 'b', -ROOK: 'r', -QUEEN: 'q', -KING: 'k',
    EMPTY: '.'
}

PIECE_LETTERS = {KNIGHT: 'N', BISHOP: 'B', ROOK: 'R', QUEEN: 'Q', KING: 'K'}

def copy_board(board):
    return [row[:] for row in board]

def in_bounds(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def piece_color(piece):
    if piece > 0:
        return WHITE
    if piece < 0:
        return BLACK
    return None

def col_to_file(c):
    return chr(ord('a') + c)

def row_to_rank(r):
    return str(8 - r)

def square_name(r, c):
    return col_to_file(c) + row_to_rank(r)

def parse_square(s):
    c = ord(s[0]) - ord('a')
    r = 8 - int(s[1])
    return r, c

def get_pawn_moves(board, r, c, color):
    moves = []
    direction = -1 if color == WHITE else 1
    start_row = 6 if color == WHITE else 1
    nr = r + direction
    if in_bounds(nr, c) and board[nr][c] == EMPTY:
        moves.append((r, c, nr, c))
        if r == start_row:
            nr2 = r + 2 * direction
            if in_bounds(nr2, c) and board[nr2][c] == EMPTY:
                moves.append((r, c, nr2, c))
    for dc in [-1, 1]:
        nc = c + dc
        if in_bounds(nr, nc) and board[nr][nc] != EMPTY and piece_color(board[nr][nc]) != color:
            moves.append((r, c, nr, nc))
    return moves

def get_sliding_moves(board, r, c, color, directions):
    moves = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        while in_bounds(nr, nc):
            if board[nr][nc] == EMPTY:
                moves.append((r, c, nr, nc))
            elif piece_color(board[nr][nc]) != color:
                moves.append((r, c, nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc
    return moves

def get_step_moves(board, r, c, color, deltas):
    moves = []
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc) and piece_color(board[nr][nc]) != color:
            moves.append((r, c, nr, nc))
    return moves

def get_piece_moves(board, r, c):
    piece = board[r][c]
    color = piece_color(piece)
    pt = abs(piece)
    if pt == PAWN:
        return get_pawn_moves(board, r, c, color)
    if pt == KNIGHT:
        return get_step_moves(board, r, c, color, [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)])
    if pt == BISHOP:
        return get_sliding_moves(board, r, c, color, [(-1,-1),(-1,1),(1,-1),(1,1)])
    if pt == ROOK:
        return get_sliding_moves(board, r, c, color, [(-1,0),(1,0),(0,-1),(0,1)])
    if pt == QUEEN:
        return get_sliding_moves(board, r, c, color, [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)])
    if pt == KING:
        return get_step_moves(board, r, c, color, [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])
    return []

def get_all_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            if piece_color(board[r][c]) == color:
                moves.extend(get_piece_moves(board, r, c))
    return moves

def apply_move(board, move):
    b = copy_board(board)
    r1, c1, r2, c2 = move
    b[r2][c2] = b[r1][c1]
    b[r1][c1] = EMPTY
    if abs(b[r2][c2]) == PAWN and (r2 == 0 or r2 == 7):
        b[r2][c2] = QUEEN * piece_color(b[r2][c2])
    return b

def find_king(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c] == KING * color:
                return r, c
    return None

def is_in_check(board, color):
    king_pos = find_king(board, color)
    if not king_pos:
        return True
    for move in get_all_moves(board, -color):
        if (move[2], move[3]) == king_pos:
            return True
    return False

def get_legal_moves(board, color):
    legal = []
    for move in get_all_moves(board, color):
        nb = apply_move(board, move)
        if not is_in_check(nb, color):
            legal.append(move)
    return legal

def move_to_notation(board, move, legal_moves):
    r1, c1, r2, c2 = move
    piece = board[r1][c1]
    pt = abs(piece)
    color = piece_color(piece)
    captured = board[r2][c2] != EMPTY
    nb = apply_move(board, move)
    in_check = is_in_check(nb, -color)
    opp_moves = get_legal_moves(nb, -color)
    checkmate = in_check and len(opp_moves) == 0
    suffix = '#' if checkmate else ('+' if in_check else '')

    if pt == PAWN:
        if captured:
            notation = col_to_file(c1) + 'x' + square_name(r2, c2)
        else:
            notation = square_name(r2, c2)
        if r2 == 0 or r2 == 7:
            notation += '=Q'
        return notation + suffix

    letter = PIECE_LETTERS[pt]
    ambiguous_from = []
    for m in legal_moves:
        if m == move:
            continue
        if board[m[0]][m[1]] == piece and (m[2], m[3]) == (r2, c2):
            ambiguous_from.append((m[0], m[1]))

    disambig = ''
    if ambiguous_from:
        same_file = [pos for pos in ambiguous_from if pos[1] == c1]
        same_rank = [pos for pos in ambiguous_from if pos[0] == r1]
        if not same_file:
            disambig = col_to_file(c1)
        elif not same_rank:
            disambig = row_to_rank(r1)
        else:
            disambig = square_name(r1, c1)

    capture_str = 'x' if captured else ''
    return letter + disambig + capture_str + square_name(r2, c2) + suffix

def print_board(board, player_color):
    print()
    if player_color == WHITE:
        print("    a b c d e f g h")
        print("   -----------------")
        for i, row in enumerate(board):
            print(f" {8-i} | " + ' '.join(PIECE_SYMBOLS[p] for p in row))
    else:
        print("    h g f e d c b a")
        print("   -----------------")
        for i in range(7, -1, -1):
            print(f" {8-i} | " + ' '.join(PIECE_SYMBOLS[p] for p in reversed(board[i])))
    print()

def parse_human_move(text, board, color, legal_moves):
    text = text.strip()
    legal_set = {(m[0], m[1], m[2], m[3]) for m in legal_moves}
    if len(text) >= 4:
        try:
            r1, c1 = parse_square(text[0:2])
            r2, c2 = parse_square(text[2:4])
            if (r1, c1, r2, c2) in legal_set:
                return (r1, c1, r2, c2)
        except:
            pass
    for move in legal_moves:
        try:
            notation = move_to_notation(board, move, legal_moves)
            clean = notation.replace('+', '').replace('#', '')
            if clean.lower() == text.lower() or notation.lower() == text.lower():
                return move
        except:
            pass
    return None

def bot_move(board, color):
    moves = get_legal_moves(board, color)
    if not moves:
        return None
    return random.choice(moves)

def print_move_log(move_log):
    print("\n--- Move History ---")
    line = ''
    for entry in move_log:
        line += entry + '  '
        if len(line) > 60:
            print(line.strip())
            line = ''
    if line.strip():
        print(line.strip())
    print()

def play():
    print("=" * 45)
    print("      CHESS  --  Human vs Random Bot")
    print("=" * 45)
    color_input = input("Play as White or Black? (w/b): ").strip().lower()
    player_color = WHITE if color_input != 'b' else BLACK
    bot_color = -player_color
    color_name = {WHITE: 'White', BLACK: 'Black'}

    board = copy_board(INITIAL_BOARD)
    current = WHITE
    move_number = 1
    move_log = []
    white_notation = None

    while True:
        legal_moves = get_legal_moves(board, current)

        if not legal_moves:
            print_board(board, player_color)
            print_move_log(move_log)
            if is_in_check(board, current):
                winner = color_name[-current]
                print(f"  Checkmate! {winner} wins!")
            else:
                print("  Stalemate! It's a draw.")
            break

        if current == player_color:
            print_board(board, player_color)
            if is_in_check(board, current):
                print("  *** CHECK! You must get out of check. ***")
            print(f"  Move {move_number} | You are {color_name[player_color]}")
            print("  Enter move (e.g. e2e4 or Nf3 or e4): ", end='')
            user_input = input().strip()
            if user_input.lower() in ('q', 'quit', 'exit'):
                print("  Game aborted.")
                break
            move = parse_human_move(user_input, board, current, legal_moves)
            if move is None:
                print("  !! Invalid move. Try coordinate format like e2e4 or algebraic like Nf3.\n")
                continue
            notation = move_to_notation(board, move, legal_moves)
            board = apply_move(board, move)
            if current == WHITE:
                white_notation = notation
                print(f"  >> You played: {move_number}. {notation}")
            else:
                entry = f"{move_number}. {white_notation} {notation}" if white_notation else f"{move_number}... {notation}"
                move_log.append(entry)
                print(f"  >> You played: {move_number}... {notation}")
                white_notation = None
                move_number += 1
        else:
            move = bot_move(board, current)
            if move is None:
                break
            notation = move_to_notation(board, move, legal_moves)
            board = apply_move(board, move)
            if current == WHITE:
                white_notation = notation
                print(f"  >> Bot played:  {move_number}. {notation}")
            else:
                entry = f"{move_number}. {white_notation} {notation}" if white_notation else f"{move_number}... {notation}"
                move_log.append(entry)
                print(f"  >> Bot played:  {move_number}... {notation}")
                white_notation = None
                move_number += 1

        current = -current

    print_move_log(move_log)

if __name__ == "__main__":
    play()
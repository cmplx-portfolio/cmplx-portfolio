import random
import time

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

PIECE_VALUES = {
    PAWN: 100,
    KNIGHT: 320,
    BISHOP: 330,
    ROOK: 500,
    QUEEN: 900,
    KING: 20000
}

PAWN_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0],
]

KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50],
]

BISHOP_TABLE = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20],
]

ROOK_TABLE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0],
]

QUEEN_TABLE = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20],
]

KING_MID_TABLE = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20],
]

KING_END_TABLE = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50],
]

PIECE_TABLES_MID = {
    PAWN: PAWN_TABLE,
    KNIGHT: KNIGHT_TABLE,
    BISHOP: BISHOP_TABLE,
    ROOK: ROOK_TABLE,
    QUEEN: QUEEN_TABLE,
    KING: KING_MID_TABLE,
}

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

def is_endgame(board):
    queens = sum(1 for r in board for p in r if abs(p) == QUEEN)
    minors = sum(1 for r in board for p in r if abs(p) in (KNIGHT, BISHOP, ROOK))
    return queens == 0 or (queens <= 2 and minors <= 2)

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

def get_piece_square_value(pt, r, c, color, endgame=False):
    if pt == KING and endgame:
        table = KING_END_TABLE
    else:
        table = PIECE_TABLES_MID.get(pt)
    if table is None:
        return 0
    return table[r][c] if color == WHITE else table[7 - r][c]

def count_mobility(board, color):
    return len(get_all_moves(board, color))

def count_doubled_pawns(board, color):
    penalty = 0
    pawn = PAWN * color
    for c in range(8):
        col_pawns = sum(1 for r in range(8) if board[r][c] == pawn)
        if col_pawns > 1:
            penalty += (col_pawns - 1) * 20
    return penalty

def count_isolated_pawns(board, color):
    penalty = 0
    pawn = PAWN * color
    files_with_pawns = set()
    for c in range(8):
        for r in range(8):
            if board[r][c] == pawn:
                files_with_pawns.add(c)
    for c in files_with_pawns:
        neighbors = {c - 1, c + 1}
        if not neighbors & files_with_pawns:
            penalty += 25
    return penalty

def evaluate_board(board):
    endgame = is_endgame(board)
    score = 0
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == EMPTY:
                continue
            color = piece_color(piece)
            pt = abs(piece)
            val = PIECE_VALUES[pt] + get_piece_square_value(pt, r, c, color, endgame)
            score += val * color

    w_mob = count_mobility(board, WHITE)
    b_mob = count_mobility(board, BLACK)
    score += (w_mob - b_mob) * 5

    score -= count_doubled_pawns(board, WHITE)
    score += count_doubled_pawns(board, BLACK)
    score -= count_isolated_pawns(board, WHITE)
    score += count_isolated_pawns(board, BLACK)

    return score

def order_moves(board, moves, color):
    def move_priority(move):
        r1, c1, r2, c2 = move
        captured = board[r2][c2]
        priority = 0
        if captured != EMPTY:
            attacker_val = PIECE_VALUES[abs(board[r1][c1])]
            victim_val = PIECE_VALUES[abs(captured)]
            priority += victim_val - attacker_val // 10
        nb = apply_move(board, move)
        if is_in_check(nb, -color):
            priority += 50
        return priority
    return sorted(moves, key=move_priority, reverse=True)

def alpha_beta(board, depth, alpha, beta, maximizing):
    color = WHITE if maximizing else BLACK
    legal = get_legal_moves(board, color)

    if not legal:
        if is_in_check(board, color):
            return -99999 if maximizing else 99999
        return 0

    if depth == 0:
        return evaluate_board(board)

    ordered = order_moves(board, legal, color)

    if maximizing:
        value = -999999
        for move in ordered:
            nb = apply_move(board, move)
            value = max(value, alpha_beta(nb, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = 999999
        for move in ordered:
            nb = apply_move(board, move)
            value = min(value, alpha_beta(nb, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def get_ranked_moves_ab(board, color, depth=3):
    legal = get_legal_moves(board, color)
    if not legal:
        return []
    ordered = order_moves(board, legal, color)
    scored = []
    maximizing = (color == WHITE)
    for move in ordered:
        nb = apply_move(board, move)
        score = alpha_beta(nb, depth - 1, -999999, 999999, not maximizing)
        scored.append((score, move))
    scored.sort(key=lambda x: x[0], reverse=maximizing)
    return scored

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

def explain_move(board, move, legal_moves, color):
    r1, c1, r2, c2 = move
    pt = abs(board[r1][c1])
    captured = board[r2][c2]
    nb = apply_move(board, move)
    reasons = []
    if captured != EMPTY:
        cap_val = PIECE_VALUES[abs(captured)]
        mover_val = PIECE_VALUES[pt]
        if cap_val >= mover_val:
            reasons.append(f"wins {cap_val} cp of material")
        else:
            reasons.append("captures a piece")
    if is_in_check(nb, -color):
        opp_moves = get_legal_moves(nb, -color)
        if not opp_moves:
            reasons.append("delivers checkmate!")
        else:
            reasons.append("gives check")
    if pt == PAWN and (r2 == 1 or r2 == 6):
        reasons.append("reaches promotion rank")
    if pt in (KNIGHT, BISHOP) and r1 in (0, 7):
        reasons.append("develops a piece")
    center = {(3,3),(3,4),(4,3),(4,4)}
    if (r2, c2) in center and pt in (PAWN, KNIGHT):
        reasons.append("controls the center")
    if not reasons:
        reasons.append("best positional improvement")
    return ', '.join(reasons)

def grade_move(played_score, best_score, color):
    diff = (best_score - played_score) * color
    if diff <= 10:
        return "Excellent!", "✓"
    elif diff <= 50:
        return "Good move", "~"
    elif diff <= 150:
        return "Inaccuracy", "?"
    elif diff <= 400:
        return "Mistake", "??"
    else:
        return "Blunder", "??!"

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

def print_move_log(move_log):
    print("\n--- Move History ---")
    line = ''
    for entry in move_log:
        line += entry + '  '
        if len(line) > 64:
            print(line.strip())
            line = ''
    if line.strip():
        print(line.strip())
    print()

def print_review(board_before, move_played, legal_moves_before, best_move, best_score, player_color):
    if move_played is None or best_move is None:
        return
    played_notation = move_to_notation(board_before, move_played, legal_moves_before)
    best_notation = move_to_notation(board_before, best_move, legal_moves_before)
    nb_played = apply_move(board_before, move_played)
    played_score = evaluate_board(nb_played) * player_color
    best_cp = best_score * player_color
    label, symbol = grade_move(played_score, best_cp, 1)
    print(f"  ┌─ Last Turn Review ────────────────────────────")
    print(f"  │  You played:  {played_notation} {symbol}  ({label})")
    if move_played != best_move:
        reason = explain_move(board_before, best_move, legal_moves_before, player_color)
        print(f"  │  Best was:    {best_notation}  ({reason})")
        print(f"  │  Score diff:  {abs(best_cp - played_score)} cp lost")
    else:
        print(f"  │  That WAS the best move — perfect!")
    print(f"  └───────────────────────────────────────────────")

def play():
    print("=" * 56)
    print("    CHESS v4  --  Human vs Alpha-Beta Bot")
    print("    3-ply search with move ordering & pawn structure.")
    print("    Hints + last turn review every move.")
    print("    Bot plays 2nd best move.")
    print("=" * 56)
    color_input = input("Play as White or Black? (w/b): ").strip().lower()
    player_color = WHITE if color_input != 'b' else BLACK
    color_name = {WHITE: 'White', BLACK: 'Black'}

    board = copy_board(INITIAL_BOARD)
    current = WHITE
    move_number = 1
    move_log = []
    white_notation = None

    last_player_board = None
    last_player_move = None
    last_player_legal_moves = None
    last_player_best_move = None
    last_player_best_score = None

    while True:
        legal_moves = get_legal_moves(board, current)

        if not legal_moves:
            print_board(board, player_color)
            print_move_log(move_log)
            if is_in_check(board, current):
                print(f"  Checkmate! {color_name[-current]} wins!")
            else:
                print("  Stalemate! It's a draw.")
            break

        if current == player_color:
            print_board(board, player_color)

            if last_player_move is not None:
                print_review(
                    last_player_board,
                    last_player_move,
                    last_player_legal_moves,
                    last_player_best_move,
                    last_player_best_score,
                    player_color
                )
                print()

            print("  Thinking...", end='', flush=True)
            t0 = time.time()
            ranked = get_ranked_moves_ab(board, player_color, depth=3)
            elapsed = time.time() - t0
            print(f"\r  Analyzed {len(ranked)} moves in {elapsed:.2f}s")

            if ranked:
                best_score_now, best_move_now = ranked[0]
                best_notation_now = move_to_notation(board, best_move_now, legal_moves)
                reason_now = explain_move(board, best_move_now, legal_moves, player_color)
                cp = best_score_now * player_color
                print(f"  Hint  >> Best move: {best_notation_now}  ({reason_now})  [{cp:+d} cp]")

            if is_in_check(board, current):
                print("  *** CHECK! You must get out of check. ***")

            print(f"  Move {move_number} | You are {color_name[player_color]}")
            print("  Enter move (e.g. e2e4 or Nf3): ", end='')
            user_input = input().strip()

            if user_input.lower() in ('q', 'quit', 'exit'):
                print("  Game aborted.")
                break

            move = parse_human_move(user_input, board, current, legal_moves)
            if move is None:
                print("  !! Invalid move. Try e2e4 or Nf3.\n")
                continue

            last_player_board = copy_board(board)
            last_player_legal_moves = list(legal_moves)
            last_player_move = move
            last_player_best_move = best_move_now if ranked else None
            last_player_best_score = best_score_now if ranked else None

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
            print("  Bot thinking...", end='', flush=True)
            t0 = time.time()
            ranked = get_ranked_moves_ab(board, current, depth=3)
            elapsed = time.time() - t0
            print(f"\r  Bot analyzed {len(ranked)} moves in {elapsed:.2f}s")

            if len(ranked) >= 2:
                move = ranked[1][1]
            elif ranked:
                move = ranked[0][1]
            else:
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
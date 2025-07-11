import random

def get_random_move(valid_moves):
    return random.choice(valid_moves) if valid_moves else None

def find_best_move(game_state, valid_moves, depth=3):
    global next_move
    next_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    # Find the move with the best evaluation
    minimax(game_state, valid_moves, depth, alpha, beta, False)
    return next_move if next_move else get_random_move(valid_moves)

def minimax(game_state, valid_moves, depth, alpha, beta, is_maximizing):

    global next_move
    
    if depth == 0 or len(valid_moves) == 0:
        return evaluate_board(game_state)
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            evaluation = minimax(game_state, next_moves, depth-1, alpha, beta, False)
            game_state.undo_move()
            
            if evaluation > max_eval:
                max_eval = evaluation
                if depth == DEPTH:  
                    next_move = move
            
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            evaluation = minimax(game_state, next_moves, depth-1, alpha, beta, True)
            game_state.undo_move()
            
            if evaluation < min_eval:
                min_eval = evaluation
                if depth == DEPTH:  
                    next_move = move
            
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval

def evaluate_board(game_state):
    piece_values = {
        'bp': -1, 'bn': -3, 'bb': -3, 'br': -5, 'bq': -9, 'bk': 0,
        'wp': 1, 'wn': 3, 'wb': 3, 'wr': 5, 'wq': 9, 'wk': 0
    }
    
    score = 0
    
    for row in game_state.board:
        for piece in row:
            if piece != '--':
                score += piece_values[piece]  
    
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for (r, c) in center_squares:
        piece = game_state.board[r][c]
        if piece != '--':
            score += 0.1 if piece[0] == 'w' else -0.1
    
    return score

next_move = None
DEPTH = 3  

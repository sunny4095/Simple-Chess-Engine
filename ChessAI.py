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

# import random
# import ChessEngine
# import threading


# def get_random_move(valid_moves):
#     return random.choice(valid_moves) if valid_moves else None

# class AIThread(threading.Thread):
#     def __init__(self, game_state, move, depth, alpha, beta, is_maximizing):
#         threading.Thread.__init__(self)
#         self.game_state = game_state
#         self.move = move
#         self.depth = depth
#         self.alpha = alpha
#         self.beta = beta
#         self.is_maximizing = is_maximizing
#         self.result = None
        
#     def run(self):
#         # Make a deep copy of the game state to avoid race conditions
#         local_state = self.copy_game_state(self.game_state)
#         local_state.make_move(self.move)
#         next_moves = local_state.get_valid_moves()
        
#         self.result = minimax(local_state, next_moves, self.depth-1, 
#                             self.alpha, self.beta, not self.is_maximizing)
        
#     def copy_game_state(self, game_state):
#         # Create a new GameState object with the same attributes
#         new_state = ChessEngine.GameState()
#         new_state.board = [row[:] for row in game_state.board]
#         new_state.whiteToMove = game_state.whiteToMove
#         new_state.move_log = list(game_state.move_log)
#         new_state.location_white_king = game_state.location_white_king
#         new_state.location_black_king = game_state.location_black_king
#         return new_state

# def find_best_move(game_state, valid_moves, depth=3):
#     global next_move
#     next_move = None
    
#     if not valid_moves:
#         return None
        
#     # If there are few moves or we're at shallow depth, don't bother with threads
#     if len(valid_moves) < 3 or depth <= 2:
#         return find_best_move_single_thread(game_state, valid_moves, depth)
    
#     # Multi-threaded approach
#     alpha = float('-inf')
#     beta = float('inf')
#     is_maximizing = not game_state.whiteToMove  # AI is always black in this implementation
    
#     # Create and start threads for each move
#     threads = []
#     results = []
    
#     for move in valid_moves:
#         thread = AIThread(game_state, move, depth, alpha, beta, is_maximizing)
#         threads.append(thread)
#         thread.start()
    
#     # Wait for all threads to complete
#     for thread in threads:
#         thread.join()
#         results.append((thread.move, thread.result))
    
#     # Find the best move based on results
#     if is_maximizing:
#         best_move = max(results, key=lambda x: x[1])[0]
#     else:
#         best_move = min(results, key=lambda x: x[1])[0]
    
#     return best_move

# def find_best_move_single_thread(game_state, valid_moves, depth):
#     global next_move
#     next_move = None
#     alpha = float('-inf')
#     beta = float('inf')
#     is_maximizing = not game_state.whiteToMove
    
#     minimax(game_state, valid_moves, depth, alpha, beta, is_maximizing)
#     return next_move if next_move else get_random_move(valid_moves)

# def minimax(game_state, valid_moves, depth, alpha, beta, is_maximizing):
#     global next_move
    
#     if depth == 0 or not valid_moves:
#         return evaluate_board(game_state)
    
#     if is_maximizing:
#         max_eval = float('-inf')
#         for move in valid_moves:
#             game_state.make_move(move)
#             next_moves = game_state.get_valid_moves()
#             evaluation = minimax(game_state, next_moves, depth-1, alpha, beta, False)
#             game_state.undo_move()
            
#             if evaluation > max_eval:
#                 max_eval = evaluation
#                 if depth == DEPTH:
#                     next_move = move
            
#             alpha = max(alpha, evaluation)
#             if beta <= alpha:
#                 break
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for move in valid_moves:
#             game_state.make_move(move)
#             next_moves = game_state.get_valid_moves()
#             evaluation = minimax(game_state, next_moves, depth-1, alpha, beta, True)
#             game_state.undo_move()
            
#             if evaluation < min_eval:
#                 min_eval = evaluation
#                 if depth == DEPTH:
#                     next_move = move
            
#             beta = min(beta, evaluation)
#             if beta <= alpha:
#                 break
#         return min_eval

# def evaluate_board(game_state):
#     piece_values = {
#         'bp': -1, 'bn': -3, 'bb': -3, 'br': -5, 'bq': -9, 'bk': 0,
#         'wp': 1, 'wn': 3, 'wb': 3, 'wr': 5, 'wq': 9, 'wk': 0
#     }
    
#     score = 0
    
#     # Material score
#     for row in game_state.board:
#         for piece in row:
#             if piece != '--':
#                 score += piece_values[piece]
    
#     # Center control bonus
#     center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
#     for (r, c) in center_squares:
#         piece = game_state.board[r][c]
#         if piece != '--':
#             score += 0.1 if piece[0] == 'w' else -0.1
    
#     # Mobility bonus
#     mobility = len(game_state.get_valid_moves())
#     if game_state.whiteToMove:
#         score += mobility * 0.05
#     else:
#         score -= mobility * 0.05
    
#     return score

# next_move = None
# DEPTH = 3
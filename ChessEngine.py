class GameState() :
    def __init__(self) :
        self.board = [
            ["br","bn","bb","bq","bk","bb","bn","br"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wr","wn","wb","wq","wk","wb","wn","wr"]
        ]

        self.whiteToMove = True
        self.move_log = []
        self.location_white_king = (7,4)
        self.location_black_king = (0,4)
        self.in_check = False
        self.pins = []
        self.checks = []

    def make_move(self, move) :
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.whiteToMove = not self.whiteToMove # swap players

        if move.piece_moved == "wk" :
            self.location_white_king = (move.end_row, move.end_col)
        elif move.piece_moved == "bk" :
            self.location_black_king = (move.end_row, move.end_col)

    def undo_move(self) :
        if len(self.move_log) != 0 :
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.whiteToMove = not self.whiteToMove

        if move.piece_moved == "wk" :
            self.location_white_king = (move.start_row, move.start_col)
        elif move.piece_moved == "bk" :
            self.location_black_king = (move.start_row, move.start_col)


    # def get_valid_moves(self) :
    #     return self.get_all_possible_moves()
    
    def get_valid_moves(self) :
        moves = []
        self.in_check, self.pins, self.checks = self.pins_and_checks()
        if self.whiteToMove :
            king_row = self.location_white_king[0]
            king_col = self.location_white_king[1]
        else :
            king_row = self.location_black_king[0]
            king_col = self.location_black_king[1]
        
        if self.in_check :
            if len(self.checks) == 1 : # only one piece is attacking the king
                moves = self.get_all_possible_moves()
                # Need to move a piece between attacking piece and the checked king
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []

                if piece_checking[1] == "n" : # If knight, must capture knight or move king
                    valid_squares = [(check_row,check_col)]
                else :
                    for i in range(1,8) :
                        valid_square = (king_row + check[2]*i, king_col + check[3]*i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col :
                            break

                # remove moves that dont respet the check
                for i in range(len(moves)-1,-1,-1) :
                    if moves[i].piece_moved[1] != "k" : # the king is not moving so the move must block the check
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares :
                            moves.remove(moves[i])

            else : # double check, the king has to move 
                self.get_king_moves(king_row, king_col, moves)

        else : # King not in check
            moves = self.get_all_possible_moves()
        
        return moves


    def get_all_possible_moves(self) :
        moves = []
        for row in range(8) :
            for col in range(8) :
                piece_col = self.board[row][col][0]
                if (piece_col == 'w' and self.whiteToMove) or (piece_col == 'b' and not self.whiteToMove) :
                    piece = self.board[row][col][1]
                    if piece == "p" :
                        self.get_pawn_moves(row,col,moves)
                    elif piece ==  "r" :
                        self.get_rook_moves(row,col,moves)
                    elif piece == "n" :
                        self.get_knight_moves(row,col,moves)
                    elif piece == "b" :
                        self.get_bishop_moves(row,col,moves)
                    elif piece == "q" :
                        self.get_queen_move(row,col,moves)
                    elif piece == "k" :
                        self.get_king_moves(row,col,moves)
        return moves

    def get_pawn_moves(self, r, c, moves) :
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1) :
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove :
            if self.board[r-1][c] == "--" :
                if not piece_pinned or pin_direction == (-1,0) :
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--" :
                        moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >= 0 :
                if self.board[r-1][c-1][0] == "b" :
                    if not piece_pinned or pin_direction == (-1,-1) :
                        moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <= 7 :
                if self.board[r-1][c+1][0] == "b" :
                    if not piece_pinned or pin_direction == (-1,1) :
                        moves.append(Move((r,c),(r-1,c+1),self.board))

        else :
            if self.board[r+1][c] == "--" :
                if not piece_pinned or pin_direction == (1,0) :
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "--" :
                        moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >= 0 :
                if self.board[r+1][c-1][0] == "w" :
                    if not piece_pinned or pin_direction == (1,-1) :
                        moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <= 7 :
                if self.board[r+1][c+1][0] == "w" :
                    if not piece_pinned or pin_direction == (1,1) :
                        moves.append(Move((r,c),(r+1,c+1),self.board))

    def get_knight_moves(self,r,c,moves) :
        piece_pinned = False
        for i in range(len(self.pins)-1,-1,-1) :
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-1,-2),(-1,2),(-2,-1),(-2,1),(1,-2),(1,2),(2,-1),(2,1))
        cur_color = "w" if self.whiteToMove else "b"
        for dr, dc in knight_moves :
            dest_row = r + dr
            dest_col = c + dc
            if 0 <= dest_row <= 7 and 0 <= dest_col <= 7 :
                if not piece_pinned :
                    dest_piece_color = self.board[dest_row][dest_col][0]
                    if dest_piece_color != cur_color :
                        moves.append(Move((r,c),(dest_row,dest_col),self.board))

    def get_bishop_moves(self,r,c,moves) :
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1) :
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "q" :
                    self.pins.remove(self.pins[i])
                break
        
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions :
            for i in range(1,8) :
                dest_row = r + d[0]*i
                dest_col = c + d[1]*i
                if 0 <= dest_col <= 7 and 0 <= dest_row <= 7 :
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]) :
                        dest_piece = self.board[dest_row][dest_col]
                        if dest_piece == "--" : 
                            moves.append(Move((r,c),(dest_row,dest_col),self.board))
                        elif dest_piece[0] == enemy_color : 
                            moves.append(Move((r,c),(dest_row,dest_col),self.board))
                            break
                        else :
                            break
                else :
                    break

    def get_rook_moves(self, r, c, moves) :
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins)-1,-1,-1) :
            if self.pins[i][0] == r and self.pins[i][1] == c :
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != "q" :
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions :
            for i in range(1,8) :
                dest_row = r + d[0]*i
                dest_col = c + d[1]*i
                if 0 <= dest_col <= 7 and 0 <= dest_row <= 7 :
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]) :
                        dest_piece = self.board[dest_row][dest_col]
                        if dest_piece == "--" : 
                            moves.append(Move((r,c),(dest_row,dest_col),self.board))
                        elif dest_piece[0] == enemy_color :
                            moves.append(Move((r,c),(dest_row,dest_col),self.board))
                            break
                        else :
                            break
                else :
                    break

    def get_queen_move(self,r,c,moves) :
        self.get_rook_moves(r,c,moves)
        self.get_bishop_moves(r,c,moves) 

    def get_king_moves(self,r,c,moves) :
        # directions = ((-1,0),(-1,-1),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        # cur_col = "w" if self.whiteToMove else "b"
        # for d in directions :
        #     dest_row = r + d[0]
        #     dest_col = c + d[1]
        #     if (0 <= dest_row <= 7 and 0 <= dest_col <= 7) :
        #         dest_piece = self.board[dest_row][dest_col]
        #         if dest_piece[0] != cur_col :
        #             moves.append(Move(r,c),(dest_row,dest_col),self.board)
        row_moves = (-1,-1,-1,0,0,1,1,1)
        col_moves = (-1,0,1,-1,1,-1,0,1)
        cur_col = "w" if self.whiteToMove else "b"
        for i in range(8) :
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7 :
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != cur_col :
                    if cur_col == "w" :
                        self.location_white_king = (end_row, end_col) 
                    else :
                        self.location_black_king = (end_row, end_col)
                    in_check, pins, checks = self.pins_and_checks()
                    if not in_check :
                        moves.append(Move((r,c),(end_row, end_col),self.board))
                    if cur_col == "w" :
                        self.location_white_king = (r,c) 
                    else :
                        self.location_black_king = (r,c)

    def pins_and_checks(self) :
        pins = []
        checks = []
        in_check = False

        if self.whiteToMove :
            enemy_color = "b"
            cur_color = "w"
            start_row = self.location_white_king[0]
            start_col = self.location_white_king[1]

        else :
            enemy_color = "w"
            cur_color = "b"
            start_row = self.location_black_king[0]
            start_col = self.location_black_king[1]

        # check outward from king for pins and checks
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)) :
            d = directions[j]
            possible_pins = ()
            for i in range(1,8) :
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7 :
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == cur_color and end_piece[1] != "k":
                        if possible_pins == () :
                            possible_pins = (end_row, end_col, d[0], d[1])
                        else :
                            break
                    elif end_piece[0] == enemy_color :
                        piece_type = end_piece[1]

                        if (0 <= j <= 3 and piece_type == "r") or (4 <= j <= 7 and piece_type == "b") or (i == 1 and piece_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4  <= j <= 5))) or (piece_type == "q") or (i == 1 and piece_type == "k") : 
                            if possible_pins == () : # no piece blocking so check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else : # piece is blacking, so it is pinned
                                pins.append(possible_pins)
                                break
                        else : # enemy piece is checking
                            break
                else : # out of board
                    break
        
        knight_moves = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        for m in knight_moves : # check for knight checks
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7 :
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "n" :
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks



class Move() :

    ranks_to_rows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    files_to_cols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    rows_to_ranks = {v:k for k, v in ranks_to_rows.items()}
    cols_to_files = {v:k for k, v in files_to_cols.items()}

    def __init__(self, start_square, end_square, board) :
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board [self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other) :
        if isinstance(other, Move) :
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self) :
        return self.cols_to_files[self.start_col] + self.rows_to_ranks[self.start_row] + self.cols_to_files[self.end_col] + self.rows_to_ranks[self.end_row]
    

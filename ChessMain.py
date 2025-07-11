import pygame
import ChessEngine, ChessAI

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

def LoadImages() :
    pieces = ['wp','wr','wk','wq','wb','wn','bp','br','bk','bq','bb','bn']
    for piece in pieces :
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("Images/" + piece + ".png"),(SQUARE_SIZE,SQUARE_SIZE))

def DrawGameState(screen, board) :
    # draw board
    colors = [pygame.Color("white"), pygame.Color("grey")]
    for row in range(DIMENSION) :
        for col in range(DIMENSION) :
            color = colors[(row+col)%2]
            pygame.draw.rect(screen,color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    #draw pieces 
    for row in range(DIMENSION) :
        for col in range(DIMENSION) :
            piece = board[row][col]
            if piece != "--" :
                screen.blit(IMAGES[piece], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
screen.fill(pygame.Color("white"))
LoadImages()

game_state = ChessEngine.GameState()
running = True
coords_selected = () # To keep track of the square selected
initial_final_coords = [] # To keep track of the  source and destination coordinates of a piece
valid_moves = game_state.get_valid_moves()
move_made = False
while running :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            running = False

        elif e.type == pygame.MOUSEBUTTONDOWN :
            if game_state.whiteToMove :

                coords = pygame.mouse.get_pos()
                col = coords[0] // SQUARE_SIZE
                row = coords[1] // SQUARE_SIZE 

                if coords_selected == (row,col) : # player clicked on the same square twice, unselect the piece
                    coords_selected = ()
                    initial_final_coords = []

                else :
                    coords_selected = (row,col)
                    initial_final_coords.append(coords_selected)
                    print(coords_selected)
                
                if len(initial_final_coords) == 2 :
                    move = ChessEngine.Move(initial_final_coords[0], initial_final_coords[1], game_state.board)
                    if move in valid_moves :
                        game_state.make_move(move)
                        move_made = True
                    coords_selected = ()
                    initial_final_coords = []

        elif e.type == pygame.KEYDOWN :
            if e.key == pygame.K_z :
                game_state.undo_move()
                move_made = True
            
    if move_made :
        valid_moves = game_state.get_valid_moves()
        move_made = False
        
    if not game_state.whiteToMove :
        computer_move = ChessAI.find_best_move(game_state, valid_moves)
        game_state.make_move(computer_move)
        move_made = True
    
    DrawGameState(screen, game_state.board)
    clock.tick(MAX_FPS)
    pygame.display.flip()




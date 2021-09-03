import pygame
import sys
from board import Board
from pygame.locals import *

pygame.init()

def draw_starting_page():
    title_font = pygame.font.SysFont('Calibri', 56, False, False)

    title = title_font.render('Sudoku', True, (0, 0, 0), (255, 255, 255))
    title_rect = title.get_rect()
    title_rect.center = (width // 2, height // 4)
    screen.blit(title, title_rect)

    easy_button = pygame.draw.rect(screen, (105, 105, 105), (225, height // 4 * 2, 200, 50), 0)
    medium_button = pygame.draw.rect(screen, (105, 105, 105), (225, (height // 4 * 2) + 75, 200, 50), 0)
    hard_button = pygame.draw.rect(screen, (105, 105, 105), (225, (height // 4 * 2) + 150, 200, 50), 0)

    button_font = pygame.font.SysFont('Calibri', 36, False, False)
    easy = button_font.render('Easy', True, (255, 255, 255), (105, 105, 105))
    easy_rect = easy.get_rect()
    easy_rect.center = (width // 2, (height // 4 * 2) + 25)
    screen.blit(easy, easy_rect)

    medium = button_font.render('Medium', True, (255, 255, 255), (105, 105, 105))
    medium_rect = medium.get_rect()
    medium_rect.center = (width // 2, (height // 4 * 2) + 100)
    screen.blit(medium, medium_rect)

    hard = button_font.render('Hard', True, (255, 255, 255), (105, 105, 105))
    hard_rect = hard.get_rect()
    hard_rect.center = (width // 2, (height // 4 * 2) + 175)
    screen.blit(hard, hard_rect)

    title_font = pygame.font.SysFont('Calibri', 24, True, False)
    hard = button_font.render('Controls', True, (0, 0, 0), (255, 255, 255))
    hard_rect = hard.get_rect()
    hard_rect.center = (width // 2, (height // 4 * 2) + 300)
    screen.blit(hard, hard_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if easy_button.collidepoint(pos[0], pos[1]):
                    return Board("easy")
                elif medium_button.collidepoint(pos[0], pos[1]):
                    return Board("medium")
                elif hard_button.collidepoint(pos[0], pos[1]):
                    return Board("hard")

        pygame.display.update()


        

    

def draw_board(solved):
    draw_grid()
    draw_solved_button()
    draw_captions()
    draw_cell_numbers(solved)

def draw_grid():
    # make background white
    screen.fill((255, 255, 255))

    # x and y pixels to update
    x = 0
    y = 0

    # make all the lines
    for i in range(9):
        x += width // 9
        y += height // 9

        # draw the thick lines
        pygame.draw.lines(screen, (0, 0, 0), False, [(0, 0), (0, height - 2)], 3)
        pygame.draw.lines(screen, (0, 0, 0), False, [(0, 0), (width, 0)], 3)
        if i % 3 == 2:
            pygame.draw.lines(screen, (0, 0, 0), False, [(x, 0), (x, height - 2)], 3)
            pygame.draw.lines(screen, (0, 0, 0), False, [(0, y), (width, y)], 3)
        # draw the thin lines
        else:
            pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height - 2))
            pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y))        

def draw_solved_button():
    # make the button different colors depending on if note_taking is enabled or not
    if game.is_solved:
        solved_button = pygame.draw.rect(screen, (192, 192, 192), (100, 490, 35, 35), 0)
    else:
        solved_button = pygame.draw.rect(screen, (105, 105, 105), (100, 490, 35, 35), 0)

    return solved_button



def draw_captions():
    # make directions telling user what the button is for
    caption_font = pygame.font.SysFont('Calibri', 28, False, False)
    text = caption_font.render('Press Button for Solved Board', True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (350, 510)
    screen.blit(text, textRect)

    caption_font = pygame.font.SysFont('Calibri', 24, False, False)
    text = caption_font.render('Press Space to Show Solved Puzzle', True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (318, 540)
    screen.blit(text, textRect)

def draw_cell_numbers(solved):
    # go through each cell to determine what to draw
    for i in range(9):
        for j in range(9):
            if board[i][j].is_fixed():
                x, y = get_position_of_cell(i, j)
                if i % 3 == 2 and j % 3 == 2:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 1, y + 1, (width // 9) - 2, (height //9) - 2), 0)
                elif i % 3 == 0 and j % 3 == 2:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 1, y + 2, (width // 9) - 2, (height //9) - 2), 0)
                elif i % 3 == 2 and j % 3 == 0:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 2, y + 1, (width // 9) - 2, (height //9) - 2), 0)
                elif i % 3 == 0 and j % 3 == 0:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 2, y + 2, (width // 9) - 2, (height //9) - 2), 0)
                elif i % 3 == 2:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 1, y + 1, (width // 9) - 1, (height //9) - 2), 0)
                elif j % 3 == 2:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 1, y + 1, (width // 9) - 2, (height //9) - 1), 0)
                elif i % 3 == 0:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 1, y + 2, (width // 9) - 1, (height //9) - 2), 0)
                elif j % 3 == 0:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 2, y + 1, (width // 9) - 2, (height //9) - 1), 0)
                else:
                    pygame.draw.rect(screen, (192, 192, 192), (x + 1, y + 1, (width // 9) - 1, (height //9) - 1), 0)
                draw_cell_num(i, j, board[i][j].get_correct_num(), (192, 192, 192))
            # if the cell is not empty
            elif solved:
                draw_cell_num(i, j, board[i][j].get_correct_num(), (255, 255, 255))
            elif board[i][j].get_cell_num() != 0:
                #if the cell number is given at the start of the game then make the cell background gray
                draw_cell_num(i, j, board[i][j].get_cell_num(), (255, 255, 255))
            # draw the note taking numbers if there is nothing in the cell and there are numbers to draw
            elif len(board[i][j].get_possible_nums()) > 0:
                for num in board[i][j].get_possible_nums():
                    draw_note_taking_num(i, j, num)

            # draw the selected box if the cell is selected
            if board[i][j].is_selected():
                draw_selected_cell_box(i, j)

# draw green box around selected cells
def draw_selected_cell_box(row, col):
    x, y = get_position_of_cell(row, col)
    pygame.draw.rect(screen, (0, 255, 0), (x, y, width // 9, height // 9), 3)

# draw numbers into the cells
def draw_cell_num(row, col, num, background_color):
    text = font.render(str(num), True, (0, 0, 0), background_color)
    textRect = text.get_rect()
    x, y = get_position_of_cell(row, col)
    textRect.center = (x + (width // 9 // 2), y + (height // 9 // 2))
    screen.blit(text, textRect)

# draw the note taking numbers into the cells
def draw_note_taking_num(row, col, num):
    note_taking_font = pygame.font.SysFont('Calibri', 12, False, False)
    text = note_taking_font.render(str(num), True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    x, y = get_position_of_cell(row, col)

    # gap between where the numbers are placed in the cells
    gap_x = width // 24
    gap_y = height // 30

    # position of the number rect based on what number it is
    x += 5 + (gap_x * ((num - 1) % 3))
    y += 3 + (gap_y * ((num - 1) // 3))

    textRect.x = x
    textRect.y = y
    screen.blit(text, textRect)

# get the row and column from the x y position inputed
def get_cell_row_and_col(pos):
    row = pos[1] // (height // 9)
    col = pos[0] // (width // 9)

    return row, col

# get the upper left hand corner xy position of the cell from the row and column
def get_position_of_cell(row, col):
    x = col * (width // 9)
    y = row * (height // 9)
    return x, y

# put user inputted number into cell and draw it
def insert_cell_num(row, col, num):
    board[row][col].set_cell_num(num)
    board[row][col].clear_possible_nums()
    
    draw_board(False)
    
def insert_note_taking_num(row, col, num):
    # if the notetaking number is already there delete it
    if board[row][col].is_num_in_possible_nums(num):
        board[row][col].delete_possible_num(num)
        draw_board(False)
    # draw note taking num
    else:
        board[row][col].insert_possible_num(num)
        draw_note_taking_num(row, col, num)

# variables for the game
width = 640     # width of grid
height = 480    # height of grid
screen = pygame.display.set_mode((640, 560))
screen.fill((255, 255, 255))
font = pygame.font.SysFont('Calibri', 48, False, False)
note_taking = False
note_taking_button = pygame.Rect(100, 500, 35, 35)
# make the game
row = -1
col = -1

game = draw_starting_page()
board = game.get_board()
draw_board(False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # toggle note taking button if clicked
            if note_taking_button.collidepoint(pos[0], pos[1]):
                game.set_solved(not game.is_solved())

                # deselect any cell
                if row != -1:
                    board[row][col].set_selected(False)

                draw_board(game.is_solved())

            # select a cell in the grid
            elif pos[1] < (height - 3):
                # deselect previous cell
                if row != -1:
                    board[row][col].set_selected(False)

                row, col = get_cell_row_and_col(pos)
                board[row][col].set_selected(True)
                draw_board(game.is_solved())
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                note_taking = not note_taking

            # write in the cell in non notetaking mode
            if (note_taking is False) and (board[row][col].is_fixed() is False) and (game.is_solved() is False):
                if event.key == pygame.K_1:
                    insert_cell_num(row, col, 1)
        
                elif event.key == pygame.K_2:
                    insert_cell_num(row, col, 2)

                elif event.key == pygame.K_3:
                    insert_cell_num(row, col, 3)

                elif event.key == pygame.K_4:
                    insert_cell_num(row, col, 4)

                elif event.key == pygame.K_5:
                    insert_cell_num(row, col, 5)

                elif event.key == pygame.K_6:
                    insert_cell_num(row, col, 6)

                elif event.key == pygame.K_7:
                    insert_cell_num(row, col, 7)

                elif event.key == pygame.K_8:
                    insert_cell_num(row, col, 8)

                elif event.key == pygame.K_9:
                    insert_cell_num(row, col, 9)

                elif event.key == pygame.K_BACKSPACE:
                    board[row][col].set_cell_num(0)
                    draw_board(False)

                if game.find_next_empty_cell(0,0,False) == (-1,-1):
                    if game.is_won():
                        screen.fill((173, 255, 47))
                        draw_board()
                    else:
                        caption_font = pygame.font.SysFont('Calibri', 28, True, False)
                        text = caption_font.render('Something is wrong, try again', True, (0, 0, 0), (255, 255, 255))
                        textRect = text.get_rect()
                        textRect.center = (300, 510)
                        screen.blit(text, textRect)

            # note taking mode
            elif (board[row][col].get_cell_num() == 0) and (game.is_solved() is False):

                if event.key == pygame.K_1:
                    insert_note_taking_num(row, col, 1)
        
                elif event.key == pygame.K_2:
                    insert_note_taking_num(row, col, 2)

                elif event.key == pygame.K_3:
                    insert_note_taking_num(row, col, 3)

                elif event.key == pygame.K_4:
                    insert_note_taking_num(row, col, 4)

                elif event.key == pygame.K_5:
                    insert_note_taking_num(row, col, 5)

                elif event.key == pygame.K_6:
                    insert_note_taking_num(row, col, 6)

                elif event.key == pygame.K_7:
                    insert_note_taking_num(row, col, 7)

                elif event.key == pygame.K_8:
                    insert_note_taking_num(row, col, 8)

                elif event.key == pygame.K_9:
                    insert_note_taking_num(row, col, 9)
            

    pygame.display.update()

pygame.quit()


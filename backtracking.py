#make functions to read in txt and excel files
#initializing 2d array (primitive)
rows, cols = (9, 9)
board = [[0]*cols]*rows

#needs to be fixed/double checked
#gets grid number by using row and column
def get_grid_number(row, col):
    return (row / 3) + (col / 3)

#recursive approach to finding next empty cell and returns a tuple that is the row and column
def find_next_empty_cell(row, col, board):
    #base case
    if board[row][col] == 0:
        return (row, col)
    
    #at end of board
    if row == 8 & col == 8:
        return find_next_empty_cell(0, 0, board)
    #at end of any row
    elif col == 8:
        return find_next_empty_cell(row + 1, 0, board)
    else:
        return find_next_empty_cell(row, col + 1, board)

#
def findValidNum(row_dict, col_dict, grid_dict, board, row, col):
    row_set = row_dict.get(row)
    col_set = col_dict.get(col)
    grid_set = grid_dict.get(get_grid_number(row, col))

    num_set = row_set.union(col_set)
    num_set = num_set.union(grid_set)

    for i in range(9):
        if not(num_set.issubset(i)):
            board[row][col] = i
            row, col = find_next_empty_cell(row, col, board)
            findValidNum(row_dict, col_dict, grid_dict, row, col + 1)
            

    

        

    


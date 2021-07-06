import csv

with open('expert.csv', newline='') as file: 
    reader = csv.reader(file)
    board = list(reader)
    
    #change from string to int
    for i in range(9):
        for j in range(9):
            board[i][j] = int(board[i][j])
    


#needs to be fixed/double checked
#gets grid number by using row and column
def get_grid_number(row, col):
    return ((col // 3) + (row // 3 * 3))

#recursive approach to finding next empty cell and returns a tuple that is the row and column
def find_next_empty_cell(row, col, board):
    #base case
    if board[row][col] == 0:
        return (row, col)
    
    #at end of board
    if row == 8 & col == 8:
        return (-1,-1)
    #at end of any row
    elif col == 8:
        return find_next_empty_cell(row + 1, 0, board)
    else:
        return find_next_empty_cell(row, col + 1, board)

#backtracking algorithm
def find_valid_num(row_list, col_list, grid_list, board, row, col):
    #find right sets using a dictionary
    universal_set = {0,1,2,3,4,5,6,7,8,9}
    row_set = row_list[row]
    col_set = col_list[col]
    grid_set = grid_list[get_grid_number(row, col)]

    #combine the sets to be used to get the available numbers
    num_set = row_set.union(col_set)
    num_set = num_set.union(grid_set)
    available_nums = universal_set.difference(num_set)
    print('row, col: ', row, ' ', col)
    print('available nums: ', available_nums)
    #puzzle is solved
    if row == -1:
        return True

    #a wrong number was put somewhere so need to go back
    if len(available_nums) == 0:
        return False
    
    #test the different numbers
    for num in available_nums:
        board[row][col] = num
        row_set.add(num)
        col_set.add(num)
        grid_set.add(num)
        next_row, next_col = find_next_empty_cell(row, col, board)
        success = find_valid_num(row_list, col_list, grid_list, board, next_row, next_col)

        if success is True:
            return True

        row_set.remove(num)
        col_set.remove(num)
        grid_set.remove(num)
        board[row][col] = 0

    return False
   
#make lists
row_list = [set() for i in range(9)]
col_list = [set() for i in range(9)]
grid_list = [set() for i in range(9)]

for row in range(9):
    for col in range(9):
        row_list[row].add(board[row][col])
        col_list[col].add(board[row][col])
        grid_list[get_grid_number(row, col)].add(board[row][col])


print(find_valid_num(row_list, col_list, grid_list, board, 0, 0))

for i in board:
    print(i)



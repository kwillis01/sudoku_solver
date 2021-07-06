import csv
import os

#open csv and make the board
def read_csv(file_name):
    with open(file_name, newline='') as file: 
        reader = csv.reader(file)
        board = list(reader)

        #change from string to int
        for i in range(9):
            for j in range(9):
                board[i][j] = int(board[i][j])

    return board

def read_txt(file):
    text = open('sudoku/' + file)
    rows = text.read().split('\n')
    board = [[0]*9]*9

    for i in range(9):
        board[i] = rows[i].split()
        
        for j in range(9):
            board[i][j] = int(board[i][j])

    return board

def read_solution(file):
    text = open('solutions/' + file)
    rows = text.read().split('\n')
    board = [[0]*9]*9
    for row in rows:
        if row.endswith('-'):
            rows.remove(row)

    for i in range(9):
        temp = rows[i].split()

        for elements in temp:
            if elements == '|':
                temp.remove(elements)
        
        board[i] = temp

        for j in range(9):
            board[i][j] = int(board[i][j])

        board[i].pop()
        board[i].pop()

    return board


#gets grid number by using row and column
def get_grid_number(row, col):
    return ((col // 3) + (row // 3 * 3))

#recursive approach to finding next empty cell and returns a tuple that is the row and column
def find_next_empty_cell(row, col, board):
    #base case
    if board[row][col] == 0:
        return (row, col)
    
    #at end of board which means there should be no more empty cells
    if row == 8 & col == 8:
        return (-1,-1)
    #at end of any row
    elif col == 8:
        return find_next_empty_cell(row + 1, 0, board)
    #go check next cell in row
    else:
        return find_next_empty_cell(row, col + 1, board)

#finds the set of valid numbers using the difference between the universal set and the row, column, and grid set
def find_valid_nums(row_set, col_set, grid_set):
    universal_set = {0,1,2,3,4,5,6,7,8,9}
    num_set = row_set.union(col_set)
    num_set = num_set.union(grid_set)
    available_nums = universal_set.difference(num_set)

    return available_nums

#backtracking algorithm to solve the board
def solve_board(row_list, col_list, grid_list, board, row, col):
    #get needed sets and valid number set
    row_set = row_list[row]
    col_set = col_list[col]
    grid_set = grid_list[get_grid_number(row, col)]

    available_nums = find_valid_nums(row_set, col_set, grid_set)

    #puzzle is solved
    if row == -1:
        return True

    #a wrong number was put somewhere so need to go back and try a different number
    if len(available_nums) == 0:
        return False
    
    #test the different valid numbers
    for num in available_nums:
        #set board to respective number and recursively go to next cell
        board[row][col] = num
        row_set.add(num)
        col_set.add(num)
        grid_set.add(num)
        next_row, next_col = find_next_empty_cell(row, col, board)
        success = solve_board(row_list, col_list, grid_list, board, next_row, next_col)

        #condition that the board is done and to not do the rest of the method
        if success is True:
            return True

        #the num did not work and this element needs to be reset to 0
        row_set.remove(num)
        col_set.remove(num)
        grid_set.remove(num)
        board[row][col] = 0

    #if all the different numbers have been tested and nothing worked
    return False
   
def main(board, solution):
    row_list = [set() for i in range(9)]
    col_list = [set() for i in range(9)]
    grid_list = [set() for i in range(9)]

    for row in range(9):
        for col in range(9):
            row_list[row].add(board[row][col])
            col_list[col].add(board[row][col])
            grid_list[get_grid_number(row, col)].add(board[row][col])

    #put the methods together
    row, col = find_next_empty_cell(0, 0, board)
    success = solve_board(row_list, col_list, grid_list, board, row, col)

    if (solution != board) | (not success):
        return False

    return True


    

#       MAIN        #
boards = os.listdir('sudoku/')
solutions = os.listdir('solutions/')

for i in range(len(boards)):
    board = read_txt(boards[i])
    solution = read_solution(solutions[i])

    if not main(board, solution):
        print('File names: ', boards[i], " ", solutions[i])
        print(board)
        print(solution)

print("Done!")


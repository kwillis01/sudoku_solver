import csv
import os

class Board:
    # constructor
    def __init__(self, file_name):
        # variables
        self.board = [[0]*9]*9 
        self.__row_list = [set() for i in range(9)]
        self.__col_list = [set() for i in range(9)]
        self.__grid_list = [set() for i in range(9)]

        # directs to right method depending on if the file is the puzzle in text form, csv, or the solution
        # solution direction
        if file_name.endswith('s.txt'):
            self.__read_solution(file_name)
        # csv direction
        elif file_name.endswith('.csv'):
            self.__read_csv(file_name)
        # text direction
        else:
            self.__read_txt(file_name)

        # makes the list of sets for the rows, columns, and grids
        for row in range(9):
            for col in range(9):
                self.__row_list[row].add(self.board[row][col])
                self.__col_list[col].add(self.board[row][col])
                self.__grid_list[self.__get_grid_number(row, col)].add(self.board[row][col])

    # read board from csv
    def __read_csv(self, file_name):
        with open(file_name, newline='') as file: 
            reader = csv.reader('C:/Users/kenda/OneDrive - University of Florida/Python Projects/sudoku_solver/sudoku solver/' + file_name)
            self.board = list(reader)

            # change from string to int
            for i in range(9):
                for j in range(9):
                    self.board[i][j] = int(self.board[i][j])


    # reads the solution from the solutions folder
    def __read_solution(self, file):
        # open and split into rows
        text = open('C:/Users/kenda/OneDrive - University of Florida/Python Projects/sudoku_solver/sudoku solver/solutions/' + file)
        rows = text.read().split('\n')

        # removes the rows that are only '-'
        for row in rows:
            if row.endswith('-'):
                rows.remove(row)

        # makes the board
        for i in range(9):
            # splits the text into its elements
            temp = rows[i].split()

            # removes the elements that are just '|'
            for elements in temp:
                if elements == '|':
                    temp.remove(elements)

            # makes the row
            self.board[i] = temp

            #makes the board
            for j in range(9):
                self.board[i][j] = int(self.board[i][j])

            # loses the extra info at the end
            self.board[i].pop()
            self.board[i].pop()


    #read text files from the sudoku folder and returns a board from them
    def __read_txt(self, file):
        text = open('C:/Users/kenda/OneDrive - University of Florida/Python Projects/sudoku_solver/sudoku solver/sudoku/' + file)
        rows = text.read().split('\n')

        for i in range(9):
            self.board[i] = rows[i].split()

            for j in range(9):
                self.board[i][j] = int(self.board[i][j])


    #gets grid number by using row and column
    def __get_grid_number(self, row, col):
        return ((col // 3) + (row // 3 * 3))

    #recursive approach to finding next empty cell and returns a tuple that is the row and column
    def __find_next_empty_cell(self, row, col):
        #base case
        if self.board[row][col] == 0:
            return (row, col)
        
        #at end of board which means there should be no more empty cells
        if row == 8 & col == 8:
            return (-1,-1)
        #at end of any row
        elif col == 8:
            return self.__find_next_empty_cell(row + 1, 0)
        #go check next cell in row
        else:
            return self.__find_next_empty_cell(row, col + 1)

    #finds the set of valid numbers using the difference between the universal set and the row, column, and grid set
    def __find_valid_nums(self, row_set, col_set, grid_set):
        universal_set = {0,1,2,3,4,5,6,7,8,9}
        num_set = row_set.union(col_set)
        num_set = num_set.union(grid_set)
        available_nums = universal_set.difference(num_set)

        return available_nums

    #backtracking algorithm to solve the board
    def __backtracking(self, row, col):
        #get needed sets and valid number set
        row_set = self.__row_list[row]
        col_set = self.__col_list[col]
        grid_set = self.__grid_list[self.__get_grid_number(row, col)]

        available_nums = self.__find_valid_nums(row_set, col_set, grid_set)

        #puzzle is solved
        if row == -1:
            return True

        #a wrong number was put somewhere so need to go back and try a different number
        if len(available_nums) == 0:
            return False
        
        #test the different valid numbers
        for num in available_nums:
            #set board to respective number and recursively go to next cell
            self.board[row][col] = num
            row_set.add(num)
            col_set.add(num)
            grid_set.add(num)
            next_row, next_col = self.__find_next_empty_cell(row, col)
            success = self.__backtracking(next_row, next_col)

            #condition that the board is done and to not do the rest of the method
            if success is True:
                return True

            #the num did not work and this element needs to be reset to 0
            row_set.remove(num)
            col_set.remove(num)
            grid_set.remove(num)
            self.board[row][col] = 0

        #if all the different numbers have been tested and nothing worked
        return False

    # solves the board
    def solve_board(self):
        row, col = self.__find_next_empty_cell(0, 0)
        if not(self.__backtracking(row, col)):
            print('Something went wrong!')

    # returns the board
    def get_board(self):
        return self.board

    # prints the board
    def print_board(self):
        row = 1
        col = 0
        for arr in self.board:
            for element in arr:
                if col % 3 == 0 and col != 0:
                    print('| ', end='')

                print(element, ' ', end='')
                col = col + 1

            print()

            if row % 3 == 0 and row < 9:
                print('------------------------------')

            row = row + 1
            col = 0


boards = os.listdir('C:/Users/kenda/OneDrive - University of Florida/Python Projects/sudoku_solver/sudoku solver/sudoku/')
solutions = os.listdir('C:/Users/kenda/OneDrive - University of Florida/Python Projects/sudoku_solver/sudoku solver/solutions/')

for i in range(len(boards)):
    puzzle = Board(boards[i])
    solution = Board(solutions[i])

    puzzle.solve_board()
    if puzzle.get_board() == solution.get_board():
        print(i, ": True")
    else:
        print(i, ": False")
        print("Puzzle Solved: ")
        puzzle.print_board()
        print()
        print("Given Solution: ")
        solution.print_board()
        print()
        print()





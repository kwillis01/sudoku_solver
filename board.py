import csv
import random

class Board:
    # constructor
    def __init__(self, file):
        # variables
        self.board = [[Cell() for i in range(9)] for i in range(9)]
        self.__row_list = [set() for i in range(9)]
        self.__col_list = [set() for i in range(9)]
        self.__grid_list = [set() for i in range(9)]
        self.__solved = False

        # directs to right method depending on if the file is the puzzle in text form, csv, or the solution
        # solution direction
        if file.endswith('s.txt'):
            self.__read_solution(file)
        # csv direction
        elif file.endswith('.csv'):
            self.__read_csv(file)
        # text direction
        elif file.endswith('.txt'):
            self.__read_txt(file)
        elif file == "easy":
            self.__create_rng_board(44)
        elif file == "medium":
            self.__create_rng_board(51)
        else:
            self.__create_rng_board(54)

        # makes the list of sets for the rows, columns, and grids
        for row in range(9):
            for col in range(9):
                self.__row_list[row].add(self.board[row][col].get_cell_num())
                self.__col_list[col].add(self.board[row][col].get_cell_num())
                self.__grid_list[self.__get_grid_number(row, col)].add(self.board[row][col].get_cell_num())


    # read board from csv
    def __read_csv(self, file):
        with open(file, newline='') as file: 
            reader = csv.reader(file)
            temp = list(reader)

            # change from string to int
            for i in range(9):
                for j in range(9):
                    self.board[i][j].set_cell_num(int(temp[i][j]))
                    self.board[i][j].set_correct_num(int(temp[i][j]))

                    # sets the given numbers as fixed
                    if self.board[i][j].get_cell_num() != 0:
                        self.board[i][j].set_fixed(True)

    # reads a solution board from a text file
    def __read_solution(self, file):
        # open and split into rows
        text = open(file)
        rows = text.read().split('\n')
        temp = [[0]*9]*9    # make temporary 2d list to hold data in

        # removes the rows that are only '-'
        for row in rows:
            if row.endswith('-'):
                rows.remove(row)

        # makes the board
        for i in range(9):
            # splits the text into its elements
            temp_row = rows[i].split()

            # removes the elements that are just '|'
            for elements in temp_row:
                if elements == '|':
                    temp_row.remove(elements)

            # makes the row
            temp[i] = temp_row

            #makes the board
            for j in range(9):
                self.board[i][j].set_cell_num(int(temp[i][j]))
                self.board[i][j].set_correct_num(int(temp[i][j]))

    # read board from text file
    def __read_txt(self, file):
        text = open(file)
        rows = text.read().split('\n')
        temp = [[0]*9]*9    # temp 2d array to store data in

        for i in range(9):
            temp[i] = rows[i].split()

            # make the board
            for j in range(9):
                self.board[i][j].set_cell_num(int(temp[i][j]))
                self.board[i][j].set_correct_num(int(temp[i][j]))

                # sets the given numbers as fixed
                if self.board[i][j].get_cell_num() != 0:
                    self.board[i][j].set_fixed(True)
    
    def __create_rng_board(self, blank_spaces):
        
        self.__fill_diag_grids_with_rand_nums()
        self.solve_board()
        self.__fill_board_rng()
        self.__clear_k_nums(blank_spaces)

    def __fill_diag_grids_with_rand_nums(self):
        col = 0
        grid = 0
        elements_used = set()

        for i in range(9):
            for j in range(3):
                rand_num = random.randint(1,9)

                while rand_num in elements_used:
                    rand_num = random.randint(1,9)
                
                elements_used.add(rand_num)
                self.board[i][col + j].set_correct_num(rand_num)
                self.__row_list[i].add(rand_num)
                self.__col_list[col + j].add(rand_num)
                self.__grid_list[grid].add(rand_num)

            if i % 3 == 2:
                col += 3
                grid += 4
                elements_used.clear()
    
    def __fill_board_rng(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j].set_cell_num(self.board[i][j].get_correct_num())
                self.board[i][j].set_fixed(True)

    def __clear_k_nums(self, blank_spaces):
        elements_cleared = set()

        rand_row = random.randint(0,8)
        rand_col = random.randint(0,8)

        for i in range(blank_spaces):

            while (rand_row, rand_col) in elements_cleared:
                rand_row = random.randint(0,8)
                rand_col = random.randint(0,8)

            self.board[rand_row][rand_col].set_cell_num(0)
            self.board[rand_row][rand_col].set_fixed(False)
            elements_cleared.add((rand_row, rand_col))

    # gets grid number by using row and column
    def __get_grid_number(self, row, col):
        return ((col // 3) + (row // 3 * 3))

    # recursive approach to finding next empty cell and returns a tuple that is the row and column
    def find_next_empty_cell(self, row, col, correct):
        #base case
        if correct and self.board[row][col].get_correct_num() == 0:
            return (row, col)
        elif (not correct) and (self.board[row][col].get_cell_num() == 0):
            return (row, col)
        
        #at end of board which means there should be no more empty cells
        if row == 8 & col == 8:
            return (-1,-1)
        #at end of any row
        elif col == 8:
            return self.find_next_empty_cell(row + 1, 0, correct)
        #go check next cell in row
        else:
            return self.find_next_empty_cell(row, col + 1, correct)

    # finds the set of valid numbers using the difference between the universal set and the row, column, and grid set
    def __find_valid_nums(self, row_set, col_set, grid_set):
        universal_set = {0,1,2,3,4,5,6,7,8,9}
        num_set = row_set.union(col_set)
        num_set = num_set.union(grid_set)
        available_nums = universal_set.difference(num_set)

        return available_nums

    # backtracking algorithm to solve the board
    def __backtracking(self, row, col):
        # get needed sets and valid number set
        row_set = self.__row_list[row]
        col_set = self.__col_list[col]
        grid_set = self.__grid_list[self.__get_grid_number(row, col)]

        # gets the numbers that can be used in this position
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
            self.board[row][col].set_correct_num(num)
            row_set.add(num)
            col_set.add(num)
            grid_set.add(num)
            next_row, next_col = self.find_next_empty_cell(row, col, True)

            # recursive step
            success = self.__backtracking(next_row, next_col)

            #condition that the board is done and to not do the rest of the method
            if success is True:
                return True

            #the num did not work and this element needs to be reset to 0
            row_set.remove(num)
            col_set.remove(num)
            grid_set.remove(num)
            self.board[row][col].set_correct_num(0)

        #if all the different numbers have been tested and nothing worked
        return False

    # solves the board
    def solve_board(self):
        row, col = self.find_next_empty_cell(0, 0, True)
        if not(self.__backtracking(row, col)):
            print('Something went wrong!')

    def is_solved(self):
        return self.__solved

    def set_solved(self, switch):
        self.__solved = switch

    # returns the board in the form of a 2D list
    def is_won(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].get_cell_num() != self.board[i][j].get_correct_num():
                    return False

        return True

    # returns the board
    def get_board(self):
        self.solve_board()
        return self.board

    # prints the board
    def print_board(self):
        row = 1
        col = 0

        for arr in self.board:
            for element in arr:
                # makes the grid column line
                if col % 3 == 0 and col != 0:
                    print('| ', end='')

                # prints the cell number
                print(element.get_cell_num(), ' ', end='')
                col = col + 1

            print()

            # makes the grid row line
            if row % 3 == 0 and row < 9:
                print('------------------------------')

            row = row + 1
            col = 0

    def test_solve_board(self):
        for arr in self.board:
            for element in arr:
                element.set_cell_num(element.get_correct_num())


class Cell:
    # default constructor
    def __init__(self):
        self.correct_num = 0        # correct number for cell found from solving board
        self.cell_num = 0           # number currently in the cell
        self.possible_nums = set()  # the numbers the user inputs using the note taking mode
        self.fixed = False          # if the number in the cell was given at the start of the game
        self.selected = False       # if the cell is currently selected       

    def set_correct_num(self, num):
        self.correct_num = num
    
    def get_correct_num(self):
        return self.correct_num

    def insert_possible_num(self, num):
        self.possible_nums.add(num)
    
    def is_num_in_possible_nums(self, num):
        return num in self.possible_nums

    def delete_possible_num(self, num):
        self.possible_nums.remove(num)

    def clear_possible_nums(self):
        self.possible_nums.clear()
    
    def get_possible_nums(self):
        return self.possible_nums

    def set_cell_num(self, num):
        self.cell_num = num
    
    def get_cell_num(self):
        return self.cell_num

    def set_fixed(self, switch):
        self.fixed = switch

    def is_fixed(self):
        return self.fixed

    def is_selected(self):
        return self.selected

    def set_selected(self, switch):
        self.selected = switch

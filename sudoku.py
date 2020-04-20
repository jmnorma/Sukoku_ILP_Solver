''' 
MATH 4400: Linear Program 
Course Project 3: Sudoku - Integer Programming Formulation 
Professor: Dr. Boshi Yang  
Names: Josh Norman and Delaney Higgins

Requirements: Python 2.7.1 and Pulp 
    pip install pulp

Resources: 
https://towardsdatascience.com/using-integer-linear-programming-to-solve-sudoku-puzzles-15e9d2a70baa
https://benalexkeen.com/linear-programming-with-python-and-pulp-part-4/

The set up calls for 729 parameters or 9^3. Where there are 9 values, 9 rows, 9 columns
Therefore the problem is taken into three dimension trucating the problem into 9 different board 
which only one "value" can exist within. Therefore will create a linear program using only Binary 
constraints. These values with represent a value hit(1) or miss(0). 

Linear Constraint of the Linear Program 
MAX 0 
S.T.  
    The sum from v =[1,9] of (Xvrc)= 1 for r,c exist within [1,9]
    The sum from r =[1,9] of (Xvrc)= 1 for v,c exist within [1,9]
    The sum from c =[1,9] of (Xvrc)= 1 for v,r exist within [1,9]
    
    The sum from r=[3p-2,3p] of the sum from c=[3q-2,3q] of (Xvrc)= 1 for v exist within [1,9] 
    and p,q exist within [1,3]
'''

import pulp


class SudokuSolver: 
    def __init__(self):
        super().__init__()   

        ## Create the Linear Programing object
        self.model = pulp.LpProblem( "Sudoku_Problem", pulp.LpMaximize)
        
        ## Inilized the 729 parameters
        self.rows = range(1,10)
        self.cols = range(1,10)
        self.values = range(1,10)

        ## Add the 792 parameters use Binary ie 1 or 0 
        self.parameter = pulp.LpVariable.dicts (name= "parameter", indexs=(self.values,self.rows,self.cols), cat=pulp.LpBinary)

        ## Add the objective function to the model 
        self.model += 0, "Objective Function"

        ## Add the Linear Constraint of the Linear Program 

        # sum from v =[1,9] of (Xvrc)= 1 for r,c exist within [1,9]
        for r in self.rows:
            for c in self.cols:
                self.model += pulp.lpSum( self.parameter[v][r][c] for v in self.values) == 1, ""

        # sum from r =[1,9] of (Xvrc)= 1 for v,c exist within [1,9]
        for v in self.values:
            for c in self.cols:
                self.model += pulp.lpSum( self.parameter[v][r][c] for r in self.rows) == 1, ""

        # sum from c =[1,9] of (Xvrc)= 1 for v,r exist within [1,9]
        for v in self.values:
            for r in self.rows:
                self.model += pulp.lpSum( self.parameter[v][r][c] for c in self.cols) == 1, ""

        # The sum from r=[3p-2,3p] of the sum from c=[3q-2,3q] of (Xvrc)= 1 for v exist within [1,9] and p,q exist within [1,3]
        for p in range(1,4):
            for q in range(1,4):
                subBox = []

                for r in range( 3*p-2, 3*p +1):
                    for c in range (3*q-2, 3*q +1):
                        subBox += [(r,c)]

                for v in self.values:
                    self.model += pulp.lpSum( self.parameter[v][r][c] for (r,c) in subBox) == 1, ""     


    def addBoard( self, board):
        for x in range(1,10):
            for y in range(1,10):
                if ( board[x-1][y-1] != 0 ):
                    self.model += self.parameter[board[x-1][y-1]][x][y] == 1,""
                    pass 

    def solve(self):
        self.model.solve()

    def dump(self):
        output = []

        for r in self.rows:
            row = []
            for c in self.cols:
                for v in self.values:
                    if pulp.value(self.parameter[v][r][c])== 1:
                         row += [v]
            output.append(row)
            print(row)
        
        return output

def textFileParse( fileName ):
    
    f = open( fileName, "r")
    lines = f.read()
    f.close() 

    lines = lines.split("\n")
    board = []
    for line in lines:
        line = line.split(" ")
        
        row = []
        for num in line: 
            row.append(int(num))

        board.append(row)
    
    return board 


## Main Functionality for Testing 
def main(): 
    ## Create a 2D List of integers 
    ## Blanks are filed with Zeros 
    board = textFileParse("puzzles/puzzle1.txt")

    SS = SudokuSolver()
    SS.addBoard(board)
    SS.solve()
    SS.dump()

if __name__ == "__main__":
    main()
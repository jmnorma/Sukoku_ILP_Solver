from sudoku import SudokuSolver, textFileParse

import kivy 
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.colorpicker import Color
from kivy.uix.textinput import TextInput

kivy.require('1.9.1')

class MainWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

        self.boardInput = []
        for x in range(9):
            row = []
            for y in range(9):
                    row +=  [TextInput( halign ="center",  hint_text = "0", input_filter ="int", write_tab =False)]

            self.boardInput.append(row)

        for row in self.boardInput:
            for textinput in row:
                self.ids["board"].add_widget(textinput)

    def solveButton(self):
        board = []
        for row in self.boardInput:
            rows=[]
            for textInput in row:
                if textInput.text != "":
                    rows += [int(textInput.text)]
                else:
                    rows += [0]

            board.append(rows)

        SS = SudokuSolver()            
        SS.addBoard(board)
        SS.solve()
        newBoard = SS.dump()

        for row in range(9):
            for textInput in range(9):
                if( self.boardInput[row][textInput].text != str(newBoard[row][textInput])):
                    self.boardInput[row][textInput].background_color = [0,1,0,.5]
                    self.boardInput[row][textInput].text += str(newBoard[row][textInput])
                else: 
                    self.boardInput[row][textInput].background_color = [1,1,1,1]

                
                
    def clearButton(self):
        for row in self.boardInput:
            for textInput in row:
                textInput.text = ""
                textInput.background_color = [1,1,1,1]

    def inputButton(self):
        self.clearButton()
        
        if(self.ids['input'].text != ''):
            self.ids['input'].background_color = [1,1,1,1]
            inputfile = self.ids['input'].text

            board = textFileParse(inputfile)

            for row in range(9):
                for col in range(9): 
                    if board[row][col] != 0:
                        self.boardInput[row][col].text += str(board[row][col])
                        self.boardInput[row][col].background_color = [0,1,0,.5]
                        

        else:
            self.ids['input'].background_color = [1,0,0,.75]
            self.ids['input'].hint_text = "Insert a Valid File Name"
        



class WindowManager(ScreenManager):
    pass

Builder.load_file('sudoku.kv')
sm = WindowManager()

screens = [MainWindow(name="main")]
for screen in screens:
  sm.add_widget(screen)

sm.current = "main"

class SudokuSolverApp(App):
    def build(self):
        return sm 


if __name__ == "__main__": 
    SudokuSolverApp().run() 

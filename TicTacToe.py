import customtkinter as ctk
from itertools import permutations


class TicTacToeBoard(ctk.CTk):
    def __init__(self, game_logic):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.title("Tic Tac Toe by weng")

        self.width, self.height = 400, 470
        screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y  = (screen_width/2) - (self.width/2), (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.count = 1
        self.logic = game_logic
        self.board_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2),
        }
        self.display_buttons = []
        
        self.display_box()
        self.draw_board()
        self.reset_button()
    
    def display_box(self):
            display_frame = ctk.CTkFrame(master=self,border_width=1,border_color="orange")
            display_frame.pack(padx=10,pady=20)
            self.display = ctk.CTkLabel(master = display_frame,text="Get Ready",corner_radius=20,font=ctk.CTkFont("INK FREE",30,"normal"))
            self.display.pack()

    def draw_board(self):
            grid_frame = ctk.CTkFrame(master=self)
            grid_frame.pack()

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure((0, 1), weight=1)
        
            for key,value in self.board_positions.items():
                button = ctk.CTkButton( master=grid_frame,text='',width = 100,height = 100,corner_radius=5,hover_color = "lightblue",
                                          font = ctk.CTkFont("Mv Boli",36,"bold"),command=lambda pos=key:self.update_board(pos))
                button.grid(row = value[0],column = value[1],padx = 5,pady = 5,ipadx = 2,ipady = 2,sticky = "nsew")
                self.display_buttons.append(button)

    def reset_button(self):
        button = ctk.CTkButton(master=self,text="RESET",corner_radius=5,hover_color="red",command=self.reset_board,
        font = ctk.CTkFont("Mv Boli",20,"bold"))
        button.pack(anchor=ctk.NE,pady=10,padx=10)
        
    def update_board(self,position):
        index = 1 if self.count%2!=0 else 2
        player = f'player_{index}'
        
        if position in self.logic.score_board:
            self.display.configure(text="MOVE HAS BEEN MADE",text_color="white")
            
        else:
            self.logic.score_board.append(position)
            self.display_buttons[position-1].configure(text=self.logic.marker[player],text_color=self.logic.color[player],hover_color='black')
            if self.game_still_on(player):
                self.display.configure(text=self.logic.player[player]+" played",text_color=self.logic.color[player])
            else:
                self.logic.score_board = [i for i in range(1,10)]
            self.count+=1
        
     # function -> to check if all the spaces on the board are full or if anyone has won
    def game_still_on(self, player):
        if self.logic.player_has_won(player):
            self.display.configure(text=self.logic.player[player]+" WINS",text_color="green")
            return False
        if sum(self.logic.score_board) >= sum([i for i in range(1, 10)]):
            self.display.configure(text="ENDS IN A TIE",text_color="red")
            return False
        return True

    def reset_board(self):
        self.logic.reset_logic()
        self.count = 1
        self.display.configure(text="Get Ready",text_color="green")
        for button in self.display_buttons:
            button.configure(hover_color="lightblue")
            button.configure(text="")
            
        
class TicTacToeLogic:
    def __init__(self, player_1 = 'player_1', player_2='weng'):
        self.player = {'player_1': player_1,'player_2': player_2}
        self.marker = {'player_1': 'X','player_2': 'O'}
        self.color = {'player_1':'yellow','player_2':'brown'}
        self.score_board = []
        self.move_list = []

    # function -> to split a list into two separate list depending on the pl
    def __split_list(self, general_list, player):
        for i, j in enumerate(general_list):
            if i % 2 == 0 and player == 'player_1':
                self.move_list.append(j)
            if i % 2 != 0 and player == 'player_2':
                self.move_list.append(j)
             
    # function -> to check if player has won
    def player_has_won(self, player):
        self.__split_list(self.score_board, player) #split
        self.move_list.sort() # sort 
        self.move_list = ''.join(map(str, self.move_list)) # convert to string
        self.move_list = [''.join(p) for p in permutations(self.move_list)] # permutation

        possible_win_sequence = ['123', '456', '789', '147', '258', '369', '159', '357']

        for i in possible_win_sequence: # for each possible win sequence
            for j in self.move_list: # for all the permutation of the players move
                if i in j: # if win_sequence matches any of the permutation player has won
                    self.move_list.clear()
                    return True     
        self.move_list.clear()
    
    def reset_logic(self):
        self.move_list.clear()
        self.score_board.clear()

def main():
    game_logic = TicTacToeLogic()
    board = TicTacToeBoard(game_logic)
    board.mainloop()

if __name__=="__main__":
    main()
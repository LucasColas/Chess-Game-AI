from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import *
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Rectangle, Color, Ellipse
from kivy.lang.builder import Builder


Width, Height = 800, 800
Window.size = (Width, Height)

#Config.set('graphics', 'resizable', False)
"""
class ChessPieceButton(ButtonBehavior, Image):

    grid_x = NumericProperty(0)
    grid_y = NumericProperty(0)

    position_hint = ReferenceListProperty(grid_x, grid_y)
    print("grid_x in class : ", grid_x)
"""
class ChessPiece(ButtonBehavior, Image):
    grid_x = NumericProperty()
    grid_y = NumericProperty()
    id = StringProperty()

class Pawn(ChessPiece):
    """
        Class for Pawn Piece.
    """
    First_use = BooleanProperty()
    def callback(instance, value):
        print("Value of First_use changed", value)

    def available_moves(self, pieces):
        """
            parameters : pieces -> a container with every available pieces in the game.
            Check if it's a white or black pawn.
            Then find if there are available moves.
            Look for pieces to capture (on the left or on the right)
            available moves are stored in a dictionary (available_moves).
            available_moves has 2 keys. The first one contains a tuple with every possible moves.
            A move is a tuple that contains x and y coordinates.
            The second key contains the position of the pieces that can be captured.

            return : available_moves (dictionary)
        """
        if self.id[:5] == "White": #if it's the first time a pawn moves
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use:
                #self.First_use = False
                #origins of the x and y axis are in the bottom left corner.
                #so a white pawn moves forward by incrementing its y coordinate.
                available_moves["available_moves"] = ((self.grid_x, self.grid_y+1), (self.grid_x, self.grid_y+2))
            else:
                available_moves["available_moves"] = ((self.grid_x, self.grid_y+1))

            for piece in pieces:
                #if there is a piece in front of it then it can move forward.
                if piece.grid_y == self.grid_y + 1:
                    available_moves["available_moves"] = ()

                #Look for pieces to capture. They must be white pieces.
                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))

                if piece.id[:5] == "Black" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y + 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))

            return available_moves

        if self.id[:5] == "Black":
            print("Black")
            available_moves = {"available_moves":(), "pieces_to_capture":[]}
            if self.First_use: #if it's the first time a pawn moves
                #self.First_use = False
                print("First Use")
                #a white pawn moves forward by decrementing its y coordinate.
                available_moves["available_moves"] = ((self.grid_x, self.grid_y-1), (self.grid_x,self.grid_y-2))
            else:
                available_moves["available_moves"] = (self.grid_y+1)
            for piece in pieces:
                if piece.grid_y == self.grid_y - 1:
                    available_moves["available_moves"] = ()

                #Look for pieces to capture. They must be white pieces.
                if piece.id[:5] == "White" and piece.grid_x == self.grid_x + 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x + 1,self.grid_y + 1))

                if piece.id[:5] == "White" and piece.grid_x == self.grid_x - 1 and piece.grid_y == self.grid_y - 1:
                    available_moves["pieces_to_capture"].append((self.grid_x - 1,self.grid_y + 1))

            return available_moves

class Rook(ChessPiece):
    pass

class Knight(ChessPiece):
    pass

class Bishop(ChessPiece):
    pass

class Queen(ChessPiece):
    pass

class King(ChessPiece):
    pass

class ChessBoard(RelativeLayout):
    """
        Relative Layout for the whole chess board.
    """
    piece_pressed = False
    available_moves = {"available_moves":(), "pieces_to_capture":[]}
    def on_touch_down(self, touch):
        print("mouse ")
        grid_x = int(touch.pos[0] / self.width * 8)
        grid_y = int(touch.pos[1] / self.height * 8)

        for child in self.children:
            #Find if a player clicked on a piece
            #TODO : check the turn
            #print(child.id)
            if grid_x == child.grid_x and grid_y == child.grid_y:
                ChessBoard.piece_pressed = True
                if child.id[5:9] == "Pawn": # TODO: set First_use to False
                    ChessBoard.available_moves = child.available_moves(self.children)
                    print("available_moves : ", ChessBoard.available_moves)
                    self.draw_moves()


        anim = Animation(grid_x=grid_x, grid_y=grid_y, t='in_quad', duration=0.5)
        #anim.start(self.children[0])
    def draw_moves(self):

        """
        Draw available moves.
        Moves are circles. They are added in a group.
        We can delete this group and so delete the ellipses.
        """
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        Color_ = (0,0,1)
        #self.canvas.clear()

        with self.canvas:
            #self.canvas.remove_group()
            print("draw")
            self.canvas.remove_group("moves") #remove previous moves drawn
            size = (0.2*grid_size_x, 0.2*grid_size_y) #size of a circle that represents a move
            moves = InstructionGroup() #Group where we store every circles

            for move in ChessBoard.available_moves["available_moves"]:
                Color(rgb=Color_)
                Ellipse(pos=(grid_size_x * move[0]+grid_size_x/2 - size[0]/2, grid_size_y * move[1] + grid_size_x/2 - size[1]/2), size=size, group="moves")

        #print("moves : ",self.canvas.get_group('moves'))

    def on_size(self, *_):
        #update the board
        self.draw_board()
        self.draw_moves()

    def update(self):
        pass

    def on_pos(self, *_):
        #update the board
        self.draw_board()
        self.draw_moves()

    def draw_board(self):
        black = 0.5, 0.2, 0.2
        white = 1, 1, 1
        is_white = False
        grid_size_x = self.width / 8
        grid_size_y = self.height / 8
        #self.canvas.clear()
        with self.canvas.before:
            #draw the board.
            for y in range(8):
                for x in range(8):
                    if is_white:
                        Color(rgb=white)
                    else:
                        Color(rgb=black)
                    Rectangle(pos=(grid_size_x * x, grid_size_y * y), size=(grid_size_x, grid_size_y))
                    is_white = not is_white
                is_white = not is_white



class ChessBoardScreen(Screen):
    def __init__(self, **kwargs):
        super(ChessBoardScreen, self).__init__(**kwargs)
        #self.board = ChessBoard()
        #self.add_widget(self.board)
        self.game = ChessGame()
        self.add_widget(self.game)



class ChessApp(App):
    def build(self):
        #sm = ScreenManager()
        #sm.add_widget(ChessBoardScreen(name='board'))
        board = ChessBoard()
        #Add every piece.
        for row in range(8):
            for col in range(8):
                if row == 1:
                    board.add_widget(Pawn(id="WhitePawn_"+str(col),source="Assets\PNG\WhitePawn.png",grid_x=col, grid_y=row))
                elif row == 6:
                    board.add_widget(Pawn(id="BlackPawn_"+str(col),source="Assets\PNG\BlackPawn.png",grid_x=col, grid_y=row))

                elif row == 0:

                    if col == 0:
                        board.add_widget(ChessPiece(id="WhiteRook_"+str(0),source="Assets\PNG\WhiteRook.png",grid_x=col, grid_y=row))
                    elif col == 7:
                        board.add_widget(ChessPiece(id="WhiteRook_"+str(1),source="Assets\PNG\WhiteRook.png",grid_x=col, grid_y=row))

                    elif col == 1:
                        board.add_widget(ChessPiece(id="WhiteKnight_"+str(0),source="Assets\PNG\WhiteKnight.png",grid_x=col, grid_y=row))
                    elif col == 6:
                        board.add_widget(ChessPiece(id="WhiteKnight_"+str(1),source="Assets\PNG\WhiteKnight.png",grid_x=col, grid_y=row))

                    elif col == 2:
                        board.add_widget(ChessPiece(id="WhiteBishop_"+str(0),source="Assets\PNG\WhiteBishop.png",grid_x=col, grid_y=row))
                    elif col == 5:
                        board.add_widget(ChessPiece(id="WhiteBishop_"+str(1),source="Assets\PNG\WhiteBishop.png",grid_x=col, grid_y=row))

                    elif col == 3:
                        board.add_widget(ChessPiece(id="WhiteKing",source="Assets\PNG\WhiteKing.png",grid_x=col, grid_y=row))

                    else:
                        board.add_widget(ChessPiece(id="WhiteQueen",source="Assets\PNG\WhiteQueen.png",grid_x=col, grid_y=row))

                elif row == 7:
                    if col == 0:
                        board.add_widget(ChessPiece(id="BlackRook_"+str(0),source="Assets\PNG\BlackRook.png",grid_x=col, grid_y=row))
                    elif col == 7:
                        board.add_widget(ChessPiece(id="BlackRook_"+str(1),source="Assets\PNG\BlackRook.png",grid_x=col, grid_y=row))

                    elif col == 1:
                        board.add_widget(ChessPiece(id="BlackKnight_"+str(0),source="Assets\PNG\BlackKnight.png",grid_x=col, grid_y=row))
                    elif col == 6:
                        board.add_widget(ChessPiece(id="BlackKnight_"+str(1),source="Assets\PNG\BlackKnight.png",grid_x=col, grid_y=row))

                    elif col == 2:
                        board.add_widget(ChessPiece(id="BlackBishop_"+str(0),source="Assets\PNG\BlackBishop.png",grid_x=col, grid_y=row))
                    elif col == 5:
                        board.add_widget(ChessPiece(id="BlackBishop_"+str(1),source="Assets\PNG\BlackBishop.png",grid_x=col, grid_y=row))

                    elif col == 3:
                        board.add_widget(ChessPiece(id="BlackKing",source="Assets\PNG\BlackKing.png",grid_x=col, grid_y=row))

                    else:
                        board.add_widget(ChessPiece(id="BlackQueen",source="Assets\PNG\BlackQueen.png",grid_x=col, grid_y=row))



        return board

if __name__ == '__main__':
    ChessApp().run()

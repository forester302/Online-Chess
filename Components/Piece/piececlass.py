import pygame


# class representing a piece in a chess game
class Piece:
    def __init__(self, pos, direction):
        # store the position of the piece
        self.pos_moves = []
        self.just_moved = None
        self.just_moved_lock = None
        self.has_moved = None
        self.x = pos[0]
        self.y = pos[1]
        # store the direction of the piece (1=player 1/-1=player 2)
        self.d = direction
        # boolean indicating whether the piece is currently selected
        self.selected = False

        # set the color of the piece based on the direction
        if self.d > 0:
            self.colour = (255, 0, 0)  # red
        else:
            self.colour = (0, 0, 255)  # blue

    def __repr__(self):
        return f"<{self.__class__.__name__} At ({self.x},{self.y})>"

    def place_piece(self, board):
        # get the name of the class that this piece is an instance of
        t = self.__class__.__name__
        # get the side of the board (1=red/-1=blue) that this piece is on
        if self.d > 0:
            image = f"images/red_{t}.png"
        else:
            image = f"images/blue_{t}.png"
        # draw the piece on the board
        board.board.set_image((self.x, self.y), image)

    def click(self, board):
        # reset the selected flag
        self.selected = False
        # check if the piece was clicked
        if self.x == board.board.lastclick[0] and self.y == board.board.lastclick[1]:
            # set the selected flag to True
            self.selected = True
            # draw circles to show the possible moves
            for pos in self.possible_moves(board):
                pygame.draw.circle(board.board.screen, (0, 255, 0), (pos[0] * 75 + 37.5, pos[1] * 75 + 37.5), 25)

    def move(self, board):
        if self.selected:
            self.selected = False
            lastclick = board.board.lastclick
            for move in self.pos_moves:
                if move[0] == lastclick[0] and move[1] == lastclick[1]:
                    oldpos = (self.x, self.y)
                    self.x = move[0]
                    self.y = move[1]
                    board.board[oldpos[0]][oldpos[1]].image = None
                    self.place_piece(board)
                    board.board.draw()
                    self.has_moved = True

                    for i in range(0, len(board.otherpieces)):
                        piece = board.otherpieces[i]
                        if piece.x == self.x and piece.y == self.y:
                            board.otherpieces.pop(i)
                            break

                    self.just_moved = True
                    self.just_moved_lock = True
                    self.pos_moves = []
                    return True
        return False

    def possible_moves(self, board):
        # return an empty list by default
        return []

    def check_move(self, currentmove, moves, board):
        # Check if there is a piece in the way
        for piece in board.pieces:
            if piece.x == currentmove[0] and piece.y == currentmove[1]:
                # If there is a piece in the way, set the cantmove flag to True
                break
        else:
            if 8 >= currentmove[0] >= 0 and 8 >= currentmove[1] >= 0:
                moves.append(currentmove)

    def get_moves_straight(self, board):
        def loop(range: range, x: bool = None):
            def filter():
                return (x and (piece.x == i and piece.y == self.y and piece != self)) \
                       or ((not x) and (piece.x == self.x and piece.y == i and piece != self))

            for i in range:
                # add the current position to the list of moves
                if x:
                    moves.append([i, self.y])
                else:
                    moves.append([self.x, i])
                # check if there is a piece in the way
                for piece in board.pieces + board.otherpieces:
                    if filter():
                        break
                else:
                    continue
                break
        # list of possible moves
        moves = []
        # check all positions to the left of the piece
        loop(range(self.x, -1, -1), True)

        # check all positions to the right of the piece
        loop(range(self.x, 8), True)

        # check all positions above the piece
        loop(range(self.y, -1, -1), False)

        # check all positions below the piece
        loop(range(self.y, 8))

        # return the list of possible moves
        return moves

    def get_moves_diagonal(self, board):
        # list of possible moves
        moves = []
        # check all positions to the top-left of the piece
        for i in range(1, self.x + 1):
            moves.append([self.x - i, self.y - i])
            # check if there is a piece in the way
            for piece in board.pieces + board.otherpieces:
                if piece.x == self.x - i and piece.y == self.y - i and piece != self:
                    break
            else:
                continue
            break
        # check all positions to the top-right of the piece
        for i in range(1, 8-self.x):
            moves.append([self.x + i, self.y - i])
            for piece in board.pieces + board.otherpieces:
                if piece.x == self.x + i and piece.y == self.y - i and piece != self:
                    break
            else:
                continue
            break
        # check all positions to the bottom-left of the piece
        for i in range(1, self.x + 1):
            moves.append([self.x - i, self.y + i])
            for piece in board.pieces + board.otherpieces:
                if piece.x == self.x - i and piece.y == self.y + i and piece != self:
                    break
            else:
                continue
            break
        # check all positions to the bottom-right of the piece
        for i in range(1, 8-self.x):
            moves.append([self.x + i, self.y + i])
            for piece in board.pieces + board.otherpieces:
                if piece.x == self.x + i and piece.y == self.y + i and piece != self:
                    break
            else:
                continue
            break
            # return the list of possible moves
        return moves

    def adjust_moves(self, moves, board):

        # List to hold the actual moves that the piece can make
        actualmoves = []
        for move in moves:
            self.check_move(move, actualmoves, board)
            moves = actualmoves
        actualmoves = []
        # Iterate over the possible moves
        for move in moves:
            # Create a list containing the current position and the move being considered
            move1 = [[self.x, self.y], move]
            # Update the position of the piece to the new position specified by the move
            self.x = move1[1][0]
            self.y = move1[1][1]
            # Check if the king is in check after the move is made
            if not board.king.is_in_check(board, move):
                # If the king is not in check, add the move to the list of actual moves
                actualmoves.append(move)
            # Restore the original position of the piece
            self.x = move1[0][0]
            self.y = move1[0][1]
        # Set the pos_moves attribute of the piece to the list of actual moves
        self.pos_moves = actualmoves
        # If the list of actual moves is empty, set the selected attribute of the piece to False
        if len(actualmoves) == 0:
            self.selected = False
        # Return the list of actual moves
        return actualmoves

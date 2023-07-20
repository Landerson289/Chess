import pygame
import time
import copy
import random

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Chess')

#FOR CASTLING AND EN PASSANT ETC ADD THE POSSIBLE MOVE IN THE piece.getMove() function. Then in the grid.move() function, calculate if the move needs extra stuff like moving a piece or taking one or promoting etc and carry out that action. Code for castling has been started.



#A1 is [0,0]
#A2 is [0,1]
#C1 is [2,0]
#A1 is top left corner
#moves are represented by [prevSquare, newSquare, pieceMoved]


###No castling while in/through check
###Can't move king in front of enemy pawn because it views moving the pawn forward as a viable move and thus thinks the king would be in check.
###Bug with getBestMove returning squares with None
###Draw by repitition
###Clocks
###UI
###Resigning and draw by agreement


###BOT
###Rewrite bot code to use grid.move instead of place and take to account for en passant
###Sometimes the bot gets stuck
###The bot is biased to end pieces

pieceValue = {
  "pawn" : 1,
  "knight" : 3,
  "bishop" : 3.1,
  "rook" : 5,
  "queen" : 9,
  "king" : 1000000
}
pieceHeatMaps = {
  "pawn" : [
    [0  , 0, 0, 0, 0, 0  , 0, 0],
    [4  , 0, 4, -5, 0, 4  , 0, 4],
    [2.5, 4, 2, 2, 2, 2  , 3, 2.5],
    [3  , 3, 3, 5, 5, 3.1, 3, 3],
    [4  , 4, 4, 6, 6, 4  , 4, 4],
    [6  , 6, 6, 7, 7, 6  , 6, 6],
    [8  , 8, 8, 8, 8, 8  , 8, 8],
    [9  , 9, 9, 9, 9, 9  , 9, 9],
  ],

  "knight" : [
    [-5, -3, -3, -3, -3, -3, -3, -5],
    [-3, -1, -1, 3, 3, -1, -1, -3],
    [-3, 0, 4, 4, 4, 4, 0, -3],
    [-3, 0, 4, 5, 5, 4, 0, -3],
    [-3, 0, 4, 5, 5, 4, 0, -3],
    [-3, 0, 5, 4, 4, 5, 0, -3],
    [-3, 0, 0, 0, 0, 0 ,0, -3],
    [-5, -3, -3, -3, -3, -3, -3, -5],
    
  ],

  "bishop" : [
    [-4, -2, -2, -2, -2, -2, -2, -4],
    [-2, 0, 0, 0, 0, 0, 0, -2],
    [-2, 0, 4, 4, 4, 4, 0, -2],
    [-2, 0, 4, 2, 2, 4, 0, -2],
    [-2, 3, 4, 2, 2, 4, 3, -2],
    [-2, 0, 0, 0, 0, 0, 0, -2],
    [-2, 0, 0, 0, 0, 0, 0, -2],
    [-4, -2, -2, -2, -2, -2, -2, -4],
  ],

  "rook" : [
    [3, 0, 5, 4, 5, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0 ,2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 2],
    [2, 2, 2, 5, 5, 3, 3, 3],
  ],

  "queen" : [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ],

  "king" : [
    [2, 5, 2, 3, 2, 4, 3, 2],
    [0, 2, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ],
}


def testMove(position, move):
  '''
  newPosition = []
  for i in range(len(position.grid)):
    newPosition.append([])
    for j in position[i]:
      newPosition[i].append(copy.copy(i))
  '''
  
  prevSquare = move[0]
  newSquare = move[1]
  piece = move[2]
  
  pieceIndex = position.pieces.index(piece)
  #if position.grid[newSquare[1]][newSquare[0]] != 0:
  takenPiece = position.grid[newSquare[1]][newSquare[0]]
    #takenPiece.square = None
    
  #newPosition[newSquare[1]][newSquare[0]] = piece
  #newPosition[prevSquare[1]][prevSquare[0]] = 0

  newPieces = []
  for i in position.pieces:
    newPieces.append(copy.copy(i))
    if i == takenPiece:
      newPieces[-1].square = None
  newPieces[pieceIndex].square = newSquare
  return Grid(newPieces)

class Bot:
  def __init__(self, colour, maxDepth):
    self.colour = colour
    self.timePerMove = 0.5
    self.depth = 0
    self.maxDepth = maxDepth
    self.moveTree = []
    self.bestMoveTree = []
    self.bestScore = -9223372036854775807
  
  def getBestMove(self, position, colour):
    global bestMoveCount
    bestMoveCount += 1
    bestMove = None
    bestScore = -9223372036854775807
    moveList = position.getPossibleMovesWithCheck(colour)
    #print(position.pieces[31].square)
    
    for move in moveList:
      #print(move)
      copyMove = []
      for i in move:
        copyMove.append(copy.copy(i))
      #print(copyMove[0], copyMove[1], copyMove[2].type, copyMove[2].square)
      newPosition = []
      for i in position.pieces:
        newPosition.append(copy.copy(i))
      newPosition = Grid(newPosition)
      for piece in newPosition.pieces:
        if piece.square == copyMove[2].square:
          copyMove[2] = piece
          #print(newPosition.pieces.index(piece))
          

      #print(copyMove[2].square)
      #print(copyMove[2])
      #print(newPosition.grid[copyMove[1][1]][copyMove[1][0]])
      if newPosition.grid[copyMove[1][1]][copyMove[1][0]] != 0:
        #print("CHECK")
        take(newPosition, newPosition.grid[copyMove[1][1]][copyMove[1][0]])
      #print(copyMove[2].square)
      place(newPosition, copyMove)
      #print(copyMove)
      #print(newPosition.grid[copyMove[1][1]][copyMove[1][0]])
      
      score = self.evaluate(newPosition)
      
      #print(move[0], move[1], move[2].type, score)
      if score > bestScore:
        #print("b",bestScore)
        bestScore = score
        bestMove = move
        for i in board.pieces:
          if i.square == bestMove[2].square:
            bestMove[2] = i
      elif score == bestScore:
        rand = random.randint(0,5)
        if rand == 0:
          bestScore = score
          bestMove = move
          for i in board.pieces:
            if i.square == bestMove[2].square:
              bestMove[2] = i
              
    return bestScore, bestMove
    
  def evaluate(self, position):
    score = 0
    for piece in position.pieces:
      if piece.square != None:
        if piece.colour == self.colour:
          score += piece.value
        else:
          score -= piece.value
    #print("\t", score)
    for piece in position.pieces:
      if piece.square != None:
        if piece.type in pieceHeatMaps:
          if self.colour == piece.colour:
            if piece.colour == "white":
              heat = pieceHeatMaps[piece.type][piece.square[1]][piece.square[0]]
            else:
              
              heat = pieceHeatMaps[piece.type][7-piece.square[1]][piece.square[0]]
            score += heat * 0.19
          #print("\t\t",piece.type, piece.square, heat, score)
    moveList = position.getPossibleMovesWithCheck(self.colour)
    if len(moveList) == 0:
      if position.checkBoolInPosition(self.colour):
        score = 0
      else:
        score = 9223372036854775807
    return score  
    
  def oldSearch(self, position, colour):
    localPosition = position.copy()
    bestScore, bestMove = self.getBestMove(localPosition, colour)

    '''
    for move in moveList:
      newPosition = MOVE(position, move)
      moveList2 = newPosition.get_moves
      for move in moveList2:
        newPosition = 
    '''
    return bestScore, bestMove
  
  def newSearch(self,position, colour):
    global searchCount # For testing
    searchCount +=1
    global lastTime
    ###DEPTH FIRST
    self.depth += 1
    if self.depth <= self.maxDepth:
      moveList = position.getPossibleMovesWithCheck(colour)
      for move in moveList:
        lastTime = time.time()
        if move[0] != None:
          newPosition = position.copy()
          for i in newPosition.pieces:
            if i.square == move[2].square:
              move[2] = i
          if newPosition.grid[move[1][1]][move[1][0]] != 0:
            
            take(newPosition, newPosition.grid[move[1][1]][move[1][0]])  
          place(newPosition, move)
          
          self.moveTree.append(move)
          if colour == "white":
            newColour = "black"
          else:
            newColour = "white"
          eval, enemyMove = self.getBestMove(newPosition, newColour)
          if enemyMove != None:
            nextPosition = newPosition.copy()
            for i in nextPosition.pieces:
              
              if i.square == enemyMove[2].square:
               enemyMove[2] = i
            nextPosition.move(enemyMove)
            nextPosition.show()
          else:
            ### There are no moves available so its stalemate or checkmate
            self.deth = self.maxDepth + 1
              
          #for i in nextPosition.pieces:
          #  #print(i.type, i.square)
          pygame.display.update()
          self.newSearch(nextPosition, colour)
          self.moveTree.remove(move)
          self.depth -= 1
        
        
        
    else:
      score = self.evaluate(position)
      #print(score, self.bestScore)
      if score > self.bestScore:
        #print(self.getBestMove(position, "white"))
        #print(self.moveTree)
        self.bestScore = score
        self.bestMoveTree = copy.copy(self.moveTree)
        
        self.bestMove = self.bestMoveTree[0]
        for piece in board.pieces:
          if piece.square == self.bestMove[0]:
            self.bestMove[2] = piece
      elif score == self.bestScore:
        #print(self.moveTree)
        self.bestScore = score
        self.bestMoveTree = copy.copy(self.moveTree)
        
        self.bestMove = self.bestMoveTree[0]
        for piece in board.pieces:
          if piece.square == self.bestMove[0]:
            self.bestMove[2] = piece
            
  def move(self):
    #print("1",board.pieces[14].square)
    #print(board.pieces[31].square)
    if self.colour == "white":
      move = self.oldSearch(board,self.colour)[1]
    else:
      
      self.newSearch(board, self.colour)
      move = self.bestMoveTree[0]
    
    prevSquare = move[0]
    newSquare = move[1]
    piece = move[2]
    self.bestMoveTree = []
    self.bestMove = []
    self.bestScore = -9223372036854775807
    self.depth = 0
    piece.move(move)
class Grid:
  def __init__(self, pieces):
    self.pieces = pieces
    self.grid = []
    for i in range(8):
      self.grid.append([])
      for j in range(8):
        self.grid[-1].append(0)
    self.moves = []  
    self.turn = 0
    self.repeatedMoves = 0
    self.colour = "white"
    self.darkSprite = pygame.image.load("square.png")
    self.darkSprite = pygame.transform.scale(self.darkSprite,(50,50))

    var = pygame.PixelArray(self.darkSprite)
    var.replace((0,0,0),(67,38,22))
    del var
    
    self.lightSprite = pygame.image.load("square.png")
    self.lightSprite = pygame.transform.scale(self.lightSprite,(50,50))
    var = pygame.PixelArray(self.lightSprite)
    var.replace((0,0,0),(128,71,28))
    del var

    self.dotSprite = pygame.image.load("circle.png")
    self.dotSprite = pygame.transform.scale(self.dotSprite, (20,20))
    var = pygame.PixelArray(self.dotSprite)
    var.replace((0,0,0),(0,0,255))
    del var
    
    self.pieces = pieces

    for i in self.pieces:
      if i.square != None:
        self.grid[i.square[1]][i.square[0]] = i 
  def show(self):
    for i in range(8):
      for j in range(8):
        parity = (j%2 + i%2)%2
        #print(parity)
        if parity == 0:
          screen.blit(self.lightSprite,(i*50,j*50))
        else:
          screen.blit(self.darkSprite,(i*50,j*50))
    
    for i in self.pieces:
      if i.square != None:
        i.show()
    self.showDots()
    font = pygame.font.SysFont(None, 24)
    img = font.render(str(round(bot.evaluate(self),1)), True, (0,0,0))
    img2 = font.render(str(round(wbot.evaluate(self), 1)), True, (0,0,0))
    screen.blit(img, (0, 350))
    screen.blit(img2, (0, 0))
  def showDots(self):
    for piece in self.pieces:
      if piece.square != None:
        piece.moveDotsShow()
  def update(self):
    #if self.turn%2 == 0:
    #  self.colour = "white"
    #else:
    #  self.colour = "black"
    #print(self.pieces[19].moveCount)
    #print(bot.evaluate(board))
    if self.colour == "white":
      
      self.playerMove()
      
      #wbot.move()
    else:
      #bot.move()
      self.playerMove()
  def copy(self):
    global copyCount # For testing
    copyCount += 1
    newPieces = []
    for i in self.pieces:
      newPieces.append(copy.copy(i))
    return Grid(newPieces)
  def move(self, move):
    if self.grid[move[1][1]][move[1][0]] != 0:
      take(self, self.grid[move[1][1]][move[1][0]])
    else:  
      if move[2].type == "pawn":
        if move[1][0] != move[0][0]: # If its moving diagonally
          if self.grid[move[1][1]][move[1][0]] == 0: # And its moving to an empty square
            take(self,self.grid[move[0][1]][move[1][0]])
            
    if move[2].type == "pawn":
      if move[1][1] == 0 or move[1][1] == 7:
        promote(self, move[2], move[1])
        
    place(self, move)
    if move[2].type == "king":
      if move[1][0]-move[0][0] == -2:
        for piece in self.pieces:
          if piece.square != None:
            if piece.type == "rook" and piece.moveCount == 0 and piece.colour == move[2].colour and piece.square[0] < move[0][0]:
              place(self, [piece.square, [move[1][0]+1,piece.square[1]], piece])
            
      elif move[1][0] - move[0][0] == 2:
        for piece in self.pieces:
          if piece.square != None:
            if piece.type == "rook" and piece.moveCount == 0 and piece.colour == move[2].colour and piece.square[0] > move[0][0]:
              place(self, [piece.square, [move[1][0]-1, piece.square[1]], piece])  
  def playerMove(self):
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: #Left click
          global holding
          mousePos = pygame.mouse.get_pos()
          mousePos = [mousePos[0]//50,mousePos[1]//50]
          for piece in self.pieces:
            if piece.hold == False:
              if mousePos == piece.square and piece.colour == self.colour:
                if piece.movable and (not holding):
                  piece.hold = True
                  holding = True
            else:
              if piece.colour == self.colour:
                move = [piece.square, mousePos, piece]
                piece.move(move)
        else:
          holding = False
          for piece in self.pieces:
            piece.hold = False
  def new_get_possible_moves_without_check(self, colour):
    possibleMoves = []
    for piece in self.pieces:
      if piece.square != None and piece.colour == colour:
        possibleMoves += piece.getMoves(self)
    #if possibleMoves[0][2].type == "knight":  
      #print(possibleMoves[0][2].square)
    return possibleMoves  
  def getPossibleMovesWithCheck(self, colour):
    moveList = self.new_get_possible_moves_without_check(colour)
    newList = []
    for move in moveList:
      if self.checkBoolFromMove(move) == False and (None not in move):
        newList.append(move)
    
    return newList
  def checkBoolFromMove(self, move): # If they do this move will they be in check?
    global holding
    #print(move[0], move[1], move[2].type)
    copyOfMove = []
    for i in move:
      copyOfMove.append(copy.copy(i))
    pieceMoved = copyOfMove[2]
    ### MOVE PIECE ###
    
    for i in self.pieces:
      if i.square == pieceMoved.square:
        pieceIndex = self.pieces.index(i)
    newBoard = self.copy()
    pieceMoved = newBoard.pieces[pieceIndex]
    
    copyOfMove[2] = pieceMoved # Might not be necessary as it might automatically overwrite
    
    takenPiece = None
    newBoard.move(copyOfMove)

    ### CHECK ###
    check = newBoard.checkBoolInPosition(move[2].colour)
    return check
  def checkBoolInPosition(self, colour): # Is colour in check
    if colour == "white":
      enemyColour = "black"
    else:
      enemyColour = "white"
    
    ### GET POSSIBLE MOVES ###
    enemyPossibleMoves = self.new_get_possible_moves_without_check(enemyColour)
    possibleMove = True
    
    for piece in self.pieces:
      if piece.colour == colour and piece.type == "king":
        yourKing = piece
        
    ### CHECK IF KING IS ATTACKED
    check = False
    for move in enemyPossibleMoves:
      if yourKing.square == move[1]:
        check = True
    return check
  def statemate_bool_from_move(self, move):
    global holding
    #print(move[0], move[1], move[2].type)
    copyOfMove = []
    for i in move:
      copyOfMove.append(copy.copy(i))
    pieceMoved = copyOfMove[2]
    ### MOVE PIECE ###
    
    for i in self.pieces:
      if i.square == pieceMoved.square:
        pieceIndex = self.pieces.index(i)
    newBoard = self.copy()
    pieceMoved = newBoard.pieces[pieceIndex]
    
    copyOfMove[2] = pieceMoved # Might not be necessary as it might automatically overwrite
    
    takenPiece = None
    newBoard.move(copyOfMove)

    stalemate = newBoard.stalemate_bool_in_position(move[2].colour)
    return stalemate
  def stalemate_bool_in_position(self, colour):
    draw = False
    if len(self.getPossibleMovesWithCheck(colour)) == 0 and self.checkBoolInPosition(colour) == False:
      draw = True
      
    #if self.repeatedMoves == 3:
    #  draw = True
    return draw
  def checkmate_bool_from_move(self, move):
    global holding
    #print(move[0], move[1], move[2].type)
    copyOfMove = []
    for i in move:
      copyOfMove.append(copy.copy(i))
    pieceMoved = copyOfMove[2]
    ### MOVE PIECE ###
    
    for i in self.pieces:
      if i.square == pieceMoved.square:
        pieceIndex = self.pieces.index(i)
    newBoard = self.copy()
    pieceMoved = newBoard.pieces[pieceIndex]
    
    copyOfMove[2] = pieceMoved # Might not be necessary as it might automatically overwrite
    
    takenPiece = None
    newBoard.move(copyOfMove)

    checkmate = newBoard.checkmate_bool_in_position(move[2].colour)
    return checkmate
  def checkmate_bool_in_position(self, colour):
    moves = self.getPossibleMovesWithCheck(colour)
    if len(moves) == 0 and self.checkBoolInPosition(colour) == True:
      checkmate = True
    else:
      checkmate = False
    return checkmate
class Piece:
  def __init__(self,type, square, colour, verifyMove):
    self.square = square
    self.type = type
    self.sprite = pygame.image.load("images/"+type+".png")
    self.sprite = pygame.transform.scale(self.sprite,(50,50))
    if colour == "white":
      var = pygame.PixelArray(self.sprite)
      var.replace((0,0,0),(255,255,255))
      del var
    self.value = pieceValue[type]
    self.colour = colour
    self.hold = False
    self.movable = True
    self.verifyMove = verifyMove
    self.moveCount = 0 
    self.lastMove = 0# Turn it was last moved on
  def move(self, move):
    #otherPiece = board.grid[move[1][1]][move[1][0]]
    #if self.verifyMove(board, self.square, move[1], self, True):
    if move in self.getMoves(board):
      if board.checkBoolFromMove(move) == False:
        if board.stalemate_bool_from_move(move) == False:
          if board.checkmate_bool_from_move(move) == False:
            board.move(move)
            self.moveCount += 1
            self.lastMove = board.turn
            board.turn += 1
            if board.colour == "white":
              board.colour = "black"
            else:
              board.colour = "white"
            board.moves.append(move)
          else:
            CHECKMATE()
        else:
          STALEMATE()        
  def show(self):
    screen.blit(self.sprite,(self.square[0]*50, self.square[1]*50))
  def moveDotsShow(self):
    if self.hold == True:
      moves = self.getMoves(board)
      for move in moves:
        if board.checkBoolFromMove(move):
          rank = move[1][0]
          file = move[1][1]
      
          screen.blit(board.dotSprite, (rank*50+10,file*50+10))       
  def getMoves(self, position):
    moves = []
    if self.type == "pawn":
      if self.colour == "white":
        
        if self.square[1] + 1 < 8:
          if position.grid[self.square[1] + 1][self.square[0]] == 0:
            moves.append([self.square, [self.square[0], self.square[1] + 1], self])
          if self.square[0] + 1 < 8:
            if position.grid[self.square[1] + 1][self.square[0] + 1] != 0:
              if position.grid[self.square[1] + 1][self.square[0] + 1].colour != self.colour:
                moves.append([self.square, [self.square[0] + 1, self.square[1] + 1], self])
          if 0 <= self.square[0] - 1:
            if position.grid[self.square[1] + 1][self.square[0] - 1] != 0:
              if position.grid[self.square[1] + 1][self.square[0] - 1].colour != self.colour:
                moves.append([self.square, [self.square[0] - 1, self.square[1] + 1], self])
        if self.square[1] + 2 < 8:
          if position.grid[self.square[1] + 2][self.square[0]] == 0 and self.moveCount == 0 and position.grid[self.square[1] + 1][self.square[0]] == 0:
            moves.append([self.square, [self.square[0], self.square[1] + 2], self])
        if self.square[1] == 4:
          if self.square[0] + 1 < 8:
            otherPiece = position.grid[self.square[1]][self.square[0] + 1]
            if otherPiece != 0:
              if otherPiece.type == "pawn" and otherPiece.lastMove == position.turn - 1:
                moves.append([self.square, [self.square[0]+1, self.square[1]+1], self])
          if self.square[0] - 1 < 8:
            otherPiece = position.grid[self.square[1]][self.square[0] - 1]
            if otherPiece != 0:
              if otherPiece.type == "pawn" and otherPiece.lastMove == position.turn - 1:
                moves.append([self.square, [self.square[0]-1, self.square[1]+1], self])
      if self.colour == "black":
        
        if 0 <= self.square[1] - 1 :
          if position.grid[self.square[1] - 1][self.square[0]] == 0:
            moves.append([self.square, [self.square[0], self.square[1] - 1], self])
          if  self.square[0] + 1 < 8:
            if position.grid[self.square[1] - 1][self.square[0] + 1] != 0:
              if position.grid[self.square[1] - 1][self.square[0] + 1].colour != self.colour:
                moves.append([self.square, [self.square[0] + 1, self.square[1] - 1], self])
          if 0 <= self.square[0] - 1:
            if position.grid[self.square[1] - 1][self.square[0] - 1] != 0:
              if position.grid[self.square[1] - 1][self.square[0] - 1].colour != self.colour:
                moves.append([self.square, [self.square[0] - 1, self.square[1] - 1], self])
        if 0 <= self.square[1] - 2:
          if position.grid[self.square[1] - 2][self.square[0]] == 0 and self.moveCount == 0 and position.grid[self.square[1] - 1][self.square[0]] == 0:
            moves.append([self.square, [self.square[0], self.square[1] - 2], self])
        if self.square[1] == 3:
          if self.square[0] + 1 < 8:
            otherPiece = position.grid[self.square[1]][self.square[0] + 1]
            if otherPiece != 0:
              if otherPiece.type == "pawn" and otherPiece.lastMove == position.turn - 1:
                moves.append([self.square, [self.square[0]+1, self.square[1]-1], self])
          if 0 <= self.square[0] - 1:
            otherPiece = position.grid[self.square[1]][self.square[0] - 1]
            if otherPiece != 0:
              if otherPiece.type == "pawn" and otherPiece.lastMove == position.turn - 1:
                moves.append([self.square, [self.square[0]-1, self.square[1]-1], self])
    elif self.type == "rook":
      for y in range(1, 8):
        newSquare = [self.square[0], self.square[1] + y]
        if newSquare[1] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for y in range(1, 8):
        newSquare = [self.square[0], self.square[1] - y]
        if 0 <= newSquare[1]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for x in range(1, 8):
        newSquare = [self.square[0] + x, self.square[1]]
        if newSquare[0] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for x in range(1, 8):
        newSquare = [self.square[0] - x, self.square[1]]
        if 0 <= newSquare[0]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
    elif self.type == "knight":
      newSquares = [
        [self.square[0] - 2, self.square[1] - 1],
        [self.square[0] - 2, self.square[1] + 1],
        [self.square[0] + 2, self.square[1] - 1],
        [self.square[0] + 2, self.square[1] + 1],
        [self.square[0] - 1, self.square[1] - 2],
        [self.square[0] - 1, self.square[1] + 2],
        [self.square[0] + 1, self.square[1] - 2],
        [self.square[0] + 1, self.square[1] + 2],
      ]
      for newSquare in newSquares:
        if 0 <= newSquare[1] < 8:
          if 0 <= newSquare[0] < 8:
            if position.grid[newSquare[1]][newSquare[0]] == 0:
              moves.append([self.square, newSquare, self])
            else:
              if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
                moves.append([self.square, newSquare, self])
    elif self.type == "bishop":
      for i in range(1, 8):
        newSquare = [self.square[0] + i, self.square[1] + i]
        if newSquare[1] < 8 and newSquare[0] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] - i, self.square[1] - i]
        if 0 <= newSquare[1]  and 0 <= newSquare[0]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] + i, self.square[1] - i]
        if newSquare[0] < 8 and 0 <= newSquare[1]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] - i, self.square[1] + i]
        if 0 <= newSquare[0] and newSquare[1] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
    elif self.type == "queen":
      for y in range(1, 8):
        newSquare = [self.square[0], self.square[1] + y]
        if newSquare[1] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for y in range(1, 8):
        newSquare = [self.square[0], self.square[1] - y]
        if 0 <= newSquare[1]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for x in range(1, 8):
        newSquare = [self.square[0] + x, self.square[1]]
        if newSquare[0] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for x in range(1, 8):
        newSquare = [self.square[0] - x, self.square[1]]
        #if newSquare == [3,7]:
          #print(position.grid[newSquare[1]][newSquare[0]])
        if 0 <= newSquare[0]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] + i, self.square[1] + i]
        if newSquare[1] < 8 and newSquare[0] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] - i, self.square[1] - i]
        if 0 <= newSquare[1]  and 0 <= newSquare[0]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] + i, self.square[1] - i]
        if newSquare[0] < 8 and 0 <= newSquare[1]:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
      for i in range(1, 8):
        newSquare = [self.square[0] - i, self.square[1] + i]
        if 0 <= newSquare[0] and newSquare[1] < 8:
          if position.grid[newSquare[1]][newSquare[0]] == 0:
            moves.append([self.square, newSquare, self])
          else:
            if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
              moves.append([self.square, newSquare, self])
            break
        else:
          break
    elif self.type == "king":
      for x in range(-1, 2):
        for y in range(-1, 2):
          if (x,y) != (0,0):
            newSquare = [self.square[0] + x, self.square[1] + y]
            if 0 <= newSquare[1] < 8 and 0 <= newSquare[0] < 8:
              if position.grid[newSquare[1]][newSquare[0]] == 0:
                moves.append([self.square, newSquare, self])
              else:
                if position.grid[newSquare[1]][newSquare[0]].colour != self.colour:
                  moves.append([self.square, newSquare, self])  
      if self.moveCount == 0:
        for piece in position.pieces:
          if piece.type == "rook" and piece.moveCount == 0 and piece.square != None:
            if piece.square[0] < self.square[0]:
              possibleMove = True
              for i in range(piece.square[0] + 1, self.square[0]):
                
                if position.grid[self.square[1]][i] != 0:
                  possibleMove = False
              if possibleMove:
                moves.append([self.square, [self.square[0] - 2, self.square[1]], self])
            else:
              possibleMove = True
              for i in range(self.square[0] + 1, piece.square[0]):
                if position.grid[self.square[1]][i] != 0:
                  possibleMove = False
              if possibleMove:
                moves.append([self.square, [self.square[0] + 2, self.square[1]], self])
    return moves
def pawnMove(position, prevSquare,newSquare, piece, moving):
  legalMove = False
  if newSquare[0]-prevSquare[0] == 0:
    if position.grid[newSquare[1]][newSquare[0]] == 0:
      if piece.colour == "white":
        if newSquare[1]-prevSquare[1] == 1:
          legalMove = True
    
        if piece.moveCount == 0:
          if newSquare[1]-prevSquare[1] == 2:
            if position.grid[prevSquare[1]+1][newSquare[0]] == 0:
              legalMove = True
            else:
              legalMove = False
            
        if legalMove == True:
          if newSquare[1] == 7:
            promote(position, piece, newSquare)
      else:
        if newSquare[1]-prevSquare[1] == -1:
          legalMove = True
    
        if piece.moveCount == 0:
          if newSquare[1]-prevSquare[1] == -2:
            if position.grid[prevSquare[1]-1][newSquare[0]] == 0:
              legalMove = True
            
        if legalMove == True:
          if newSquare[1] == 0:
            promote(position, piece, newSquare)
            
  elif abs(newSquare[0]-prevSquare[0]) == 1:
    if position.grid[newSquare[1]][newSquare[0]] != 0:
      if piece.colour == "white":
        if newSquare[1]-prevSquare[1] == 1:
          legalMove = True
    
        #if piece.moveCount == 0:
        #  if newSquare[1]-prevSquare[1] == 2:
        #    legalMove = True
            
        if legalMove == True:
          if newSquare[1] == 7:
            if moving == True:
              promote(position, piece, newSquare)
      else:
        if newSquare[1]-prevSquare[1] == -1:
          legalMove = True
    
        #if piece.moveCount == 0:
        #  if newSquare[1]-prevSquare[1] == -2:
        #   legalMove = True
            
        if legalMove == True:
          if newSquare[1] == 0:
            if moving == True:
              promote(piece, newSquare)
    
    if piece.colour == "white":
      otherPiece = position.grid[newSquare[1]-1][newSquare[0]]
      if otherPiece != 0:
        if otherPiece.moveCount == 1 and newSquare[1] == 5 and otherPiece.lastMove == position.turn-1:
          if abs(newSquare[1]-prevSquare[1]) == 1:
            legalMove = True
            if moving == True:
              take(position, otherPiece)
    else:
      otherPiece = position.grid[newSquare[1]-1][newSquare[0]]
      if otherPiece != 0:
        if otherPiece.moveCount == 1 and newSquare[1] == 2 and otherPiece.lastMove == position.turn-1:
          if newSquare[1]-prevSquare[1] == -1:
            legalMove = True
            if moving == True:
              take(otherPiece)
  if position.grid[newSquare[1]][newSquare[0]] != 0:
    if position.grid[newSquare[1]][newSquare[0]].colour == position.grid[prevSquare[1]][prevSquare[0]].colour:
      legalMove = False    
  return legalMove   
def rookMove(position, prevSquare, newSquare, piece, moving):
  legalMove = False
  path = []
  if prevSquare[0] == newSquare[0]:
    legalMove = True
    if prevSquare[1]>newSquare[1]:
      for i in range(newSquare[1]+1,prevSquare[1]):
        otherPiece = position.grid[i][newSquare[0]]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[1]+1,newSquare[1]):
        otherPiece = position.grid[i][newSquare[0]]
        path.append(otherPiece)
  elif prevSquare[1] == newSquare[1]:
    legalMove = True
    if prevSquare[0]>newSquare[0]:
      for i in range(newSquare[0]+1,prevSquare[0]):
        otherPiece = position.grid[newSquare[1]][i]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[0]+1,newSquare[0]):
        otherPiece = position.grid[newSquare[1]][i]
        path.append(otherPiece)

  
  jumping = False
  for square in path:
    if square != 0:
      jumping = True
      #print(jumping)  
  if jumping == True:
    legalMove = False
  if position.grid[newSquare[1]][newSquare[0]] != 0:
      if position.grid[newSquare[1]][newSquare[0]].colour == position.grid[prevSquare[1]][prevSquare[0]].colour:
        legalMove = False
  return legalMove 
def knightMove(position, prevSquare, newSquare, piece, moving):
  #if moving == True:
    #print("f",position.grid[prevSquare[1]][prevSquare[0]]) 
  legalMove = False
  deltaUp = newSquare[1] - prevSquare[1]
  deltaRight = newSquare[0] - prevSquare[0]

  if abs(deltaUp) == 2:
    if abs(deltaRight) == 1:
      legalMove = True
  elif abs(deltaUp) == 1:
    if abs(deltaRight) == 2:
      legalMove = True
  if position.grid[newSquare[1]][newSquare[0]] != 0:
    if position.grid[newSquare[1]][newSquare[0]].colour == position.grid[prevSquare[1]][prevSquare[0]].colour:
      legalMove = False
      
  
      
  return legalMove
def bishopMove(position, prevSquare, newSquare, piece, moving):
  legalMove = False
  deltaUp = newSquare[1] - prevSquare[1]
  deltaRight = newSquare[0] - prevSquare[0]
  path = []
  
  if abs(deltaUp) == abs(deltaRight):
    legalMove = True
    
    if prevSquare[0] < newSquare[0]:
      for i in range(1, newSquare[0]-prevSquare[0]):
        if prevSquare[1] < newSquare[1]:
          pos = [prevSquare[0]+i , prevSquare[1]+i]
        else:
          pos = [prevSquare[0]+i, prevSquare[1]-i]
        square = position.grid[pos[1]][pos[0]]
        path.append(square)
        
    else:
      for i in range(1,prevSquare[0]-newSquare[0]):
        if prevSquare[1] < newSquare[1]:
          pos = [prevSquare[0]-i, prevSquare[1]+i]
        else:
          pos = [prevSquare[0]-i, prevSquare[1]-i]
        square = position.grid[pos[1]][pos[0]]
        path.append(square)

  jumping = False
  for square in path:
    if square != 0:
      jumping = True

  if jumping == True:
    legalMove = False

  if position.grid[newSquare[1]][newSquare[0]] != 0:
    if position.grid[newSquare[1]][newSquare[0]].colour == position.grid[prevSquare[1]][prevSquare[0]].colour:
      legalMove = False
        
  return legalMove
def queenMove(position, prevSquare, newSquare, piece, moving):
  legalMove = False
  path = []
  
  if prevSquare[0] == newSquare[0]:
    legalMove = True
    
    if prevSquare[1]>newSquare[1]:
      for i in range(newSquare[1]+1,prevSquare[1]):
        otherPiece = position.grid[i][newSquare[0]]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[1]+1,newSquare[1]):
        otherPiece = position.grid[i][newSquare[0]]
        path.append(otherPiece)
        
  elif prevSquare[1] == newSquare[1]:
    legalMove = True
    
    if prevSquare[0]>newSquare[0]:
      for i in range(newSquare[0]+1,prevSquare[0]):
        otherPiece = position.grid[newSquare[1]][i]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[0]+1,newSquare[0]):
        otherPiece = position.grid[newSquare[1]][i]
        path.append(otherPiece)

  
  deltaUp = newSquare[1] - prevSquare[1]
  deltaRight = newSquare[0] - prevSquare[0]

  if abs(deltaUp) == abs(deltaRight):
    legalMove = True
    
    if prevSquare[0] < newSquare[0]:
      for i in range(1, newSquare[0]-prevSquare[0]):
        if prevSquare[1] < newSquare[1]:
          pos = [prevSquare[0]+i , prevSquare[1]+i]
        else:
          pos = [prevSquare[0]+i, prevSquare[1]-i]
        square = position.grid[pos[1]][pos[0]]
        path.append(square)
        
    else:
      for i in range(1,prevSquare[0]-newSquare[0]):
        if prevSquare[1] < newSquare[1]:
          pos = [prevSquare[0]-i, prevSquare[1]+i]
        else:
          pos = [prevSquare[0]-i, prevSquare[1]-i]
        square = position.grid[pos[1]][pos[0]]
        path.append(square)

  jumping = False
  for square in path:
    if square != 0:
      jumping = True

  if jumping == True:
    legalMove = False

  if position.grid[newSquare[1]][newSquare[0]] != 0:
    
    if position.grid[newSquare[1]][newSquare[0]].colour == position.grid[prevSquare[1]][prevSquare[0]].colour:
      legalMove = False

  
  
  return legalMove
def kingMove(position, prevSquare, newSquare, piece, moving):
  
  legalMove = False
  path = []
  
  deltaUp = newSquare[1] - prevSquare[1]
  deltaRight = newSquare[0] - prevSquare[0]

  if deltaUp == 0 or abs(deltaUp) == 1:
    if deltaRight == 0 or abs(deltaRight) == 1:
      legalMove = True

  if piece.moveCount == 0:
    #print("TEST 0")
    if abs(deltaRight) == 2 and deltaUp == 0:
      #print("TEST 1")
      if deltaRight == 2:
        if piece.colour == "white":
          i = position.grid[0][7]
        else:
          i = position.grid[7][7]
      elif deltaRight == -2:
        #print("TEST 2")
        if piece.colour == "white":
          #print("TEST 3")
          i = position.grid[0][0]
        else:
          i = position.grid[7][0]
          
      if i != 0:
        #print("TEST 4")
        
        if i.type == "rook" and i.moveCount == 0 and i.colour == piece.colour:
          #print("TEST 5")
          
          legalMove = True

          if deltaRight == 2:
            for j in range(prevSquare[0]+1, 7):
              path.append(position.grid[prevSquare[1]][j])
          elif deltaRight == -2:
            #print("TEST 6")
            for j in range(1,prevSquare[0]):
              path.append(position.grid[prevSquare[1]][j])
            

          for square in path:
            if square != 0:
              #print("taken")
              legalMove = False
              
          if legalMove == True and moving == True:
            if deltaRight == 2:
              place(board, [i.square, [newSquare[0]-1,newSquare[1]], i])
            else:
              place(board, [i.square, [newSquare[0]+1,newSquare[1]], i])
          
  if position.grid[newSquare[1]][newSquare[0]] != 0:
    if position.grid[newSquare[1]][newSquare[0]].colour == position.grid[prevSquare[1]][prevSquare[0]].colour:
      legalMove = False
      
  return legalMove
def take(position, piece):
  #print(piece)
  position.grid[piece.square[1]][piece.square[0]] = 0
  piece.square = None
def place(position, move):
  global holding
  if move[0] != move[2].square:
    print("ERROR: THE FIRST SQUARE IS NOT EQUAL TO THE SQUARE THE PIECE IS ON")
    print(move[0], move[1], move[2].type,  move[2].square)
    throwError
  piece = move[2]
  location = move[1]
  #try:
  position.grid[piece.square[1]][piece.square[0]] = 0
  #except:
    #print(position.pieces.index(piece))
    #print(piece.square)
    #print(piece.type)
    #print(location)
    #quit()
  piece.hold = False
  holding = False
  piece.square = location
  position.grid[location[1]][location[0]] = piece  
def promote(position, piece,location):
  newType = False
  while not newType:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
          newType = "queen"
          newFunc = queenMove
        elif event.key == pygame.K_2:
          newType = "rook"
          newFunc = rookMove
        elif event.key == pygame.K_3:
          newType = "knight"
          newFunc = knightMove
        elif event.key == pygame.K_4:
          newType = "bishop"
          newFunc = bishopMove

  #position.pieces.append(Piece(newType, location, piece.colour, newFunc))
  index = position.pieces.index(piece)
  #position.pieces.pop(index)
  position.pieces[index] = Piece(newType, location, piece.colour, newFunc)

def CHECKMATE(colour):
  print(colour.upper() + " WINS")
  if colour == "white":
    print("1 - 0")
  else:
    print("0 - 1")
  quit()
def STALEMATE():
  print("DRAW")
  print("1/2 - 1/2")


board = Grid([
  Piece("king",[3,0], "white", kingMove),
  Piece("king",[3,7], "black", kingMove),
  
  Piece("queen",[4,0], "white", queenMove),
  Piece("queen",[4,7], "black", queenMove),
  
  Piece("rook",[0,0], "white", rookMove),
  Piece("rook",[7,0], "white", rookMove),
  Piece("rook",[0,7], "black", rookMove),
  Piece("rook",[7,7], "black", rookMove),
  
  Piece("bishop",[2,0], "white", bishopMove),
  Piece("bishop",[5,0], "white", bishopMove),
  Piece("bishop",[2,7], "black", bishopMove),
  Piece("bishop",[5,7], "black", bishopMove),
  
  Piece("knight",[1,0], "white", knightMove),
  Piece("knight",[6,0], "white", knightMove),
  Piece("knight",[1,7], "black", knightMove),
  Piece("knight",[6,7], "black", knightMove),

  Piece("pawn", [0,1], "white", pawnMove),
  Piece("pawn", [1,1], "white", pawnMove),
  Piece("pawn", [2,1], "white", pawnMove),
  Piece("pawn", [3,1], "white", pawnMove),
  Piece("pawn", [4,1], "white", pawnMove),
  Piece("pawn", [5,1], "white", pawnMove),
  Piece("pawn", [6,1], "white", pawnMove),
  Piece("pawn", [7,1], "white", pawnMove),
  
  Piece("pawn", [0,6], "black", pawnMove),
  Piece("pawn", [1,6], "black", pawnMove),
  Piece("pawn", [2,6], "black", pawnMove),
  Piece("pawn", [3,6], "black", pawnMove),
  Piece("pawn", [4,6], "black", pawnMove),
  Piece("pawn", [5,6], "black", pawnMove),
  Piece("pawn", [6,6], "black", pawnMove),
  Piece("pawn", [7,6], "black", pawnMove),
])


wbot = Bot("white", 1)
bot = Bot("black", 2)

holding = False #Bool to check nothing is being held so that two pieces aren't being picked up

print("""
######################### CHESS ########################
LEFT CLICK TO PICK UP/PLACE A PIECE
RIGHT CLICK TO PUT A PIECE DOWN WHERE IT WAS
########################################################
  """)
searchCount = 0
getMovesCount = 0
copyCount = 0
bestMoveCount = 0
startTime1 = time.time()
lastTime = startTime1
while True:
  board.update()
  board.show()
  pygame.display.update()


print(startTime1)
bot.newSearch(board, "black")
endTime1 = time.time()
print()
print("new copyCount", copyCount)
print("new bestMoveCount", bestMoveCount)
print("new getMovesCount", getMovesCount)
print("searchCount", searchCount)

getMovesCount = 0
bestMoveCount = 0
copyCount = 0
startTime2 = time.time()
for i in range(100):
  bot.oldSearch(board, "black")
endTime2 = time.time()
print("old CopyCount", copyCount/100)
print("old bestMoveCount", bestMoveCount/100)
print("old get moves count", getMovesCount/100)

print()

print("new", endTime1 - startTime1)
print("old", (endTime2 - startTime2)/100)

startTime3 = time.time()
for i in range(1000):
  board.copy()
endTime3 = time.time()
print("copy", (endTime3 - startTime3)/1000)

startTime4 = time.time()
for i in range(10):
  bot.getBestMove(board, "white")
endTime4 = time.time()
print("bestMove", (endTime4 - startTime4)/10)


startTime5 = time.time()
for i in range(1000):
  board.get_possible_moves_without_check("white")
endTime5 = time.time()
print("getMoves", (endTime5 - startTime5)/1000)

startTime5 = time.time()
for i in range(1000):
  board.new_get_possible_moves_without_check("white")
endTime5 = time.time()
print("new_getMoves", (endTime5 - startTime5)/1000)

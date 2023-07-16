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

###Castling, en passant and promotion broken
###Check script completely broken
###Fix bugs with possible move dots (checks)
###No castling while in/through check
###Can't move king in front of enemy pawn because it views moving the pawn forward as a viable move and thus thinks the king would be in check.
###Bug with getBestMove returning squares with None
###Redo pawnMove scripts etc to remove place and stuff for castling etc. 
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
    [0, 0, 0, 1, 0, 0, 0, 0],
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
    #position.show()
    #pygame.display.update()
    #print(bestScore)
    #print(colour)
    #if bestScore != 0:
      #print(bestMove)
      #time.sleep(30)
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
      #print("2",position.pieces[14].square)
      #print("3",moveList[0][2].square)
      for move in moveList:
        #print("move: ", time.time() - lastTime)
        lastTime = time.time()
        if move[0] != None:
          #print("move:", move[0], move[1], move[2].type)
          newPosition = position.copy()
          for i in newPosition.pieces:
            if i.square == move[2].square:
              move[2] = i
          #print("4",move[2].square)  
          if newPosition.grid[move[1][1]][move[1][0]] != 0:
            
            take(newPosition, newPosition.grid[move[1][1]][move[1][0]])  
          place(newPosition, move)
          #print("g",newPosition.pieces[24].square)
          
          self.moveTree.append(move)
          if colour == "white":
            newColour = "black"
          else:
            newColour = "white"
          #print(move)
          #print(newPosition.pieces[31].square)
          eval, enemyMove = self.getBestMove(newPosition, newColour)
          #print("Emove: ", enemyMove[0], enemyMove[1], enemyMove[2].type)
          nextPosition = newPosition.copy()
          for i in nextPosition.pieces:
            #print(i.square, enemyMove[2].square)
            if i.square == enemyMove[2].square:
             enemyMove[2] = i
          #nextPosition.move(enemyMove)
          #nextPosition.show()
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
      #print("bestMove: ", self.bestMove[0], self.bestMove[1], self.bestMove[2].type) 
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
      #'''
      self.playerMove()
      #'''
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
    place(self, move)
    if move[2].type == "king":
      if move[1][0]-move[0][0] == -2:
        for piece in self.pieces:
          if piece.type == "rook" and piece.moveCount == 0 and piece.colour == move[2].colour and piece.square[0] < move[0][0]:
            place(self, [piece.square, [move[1][0]+1,piece.square[1]], piece])
            
      elif move[1][0] - move[0][0] == 2:
        for piece in self.pieces:
          if piece.type == "rook" and piece.moveCount == 0 and piece.colour == move[2].colour and piece.square[0] > move[0][0]:
            place(self, [piece.square, [move[1][0]-1, piece.square[1]], piece])

    if move[2].type == "pawn":
      if move[1][0] - move[0][0] != 0: # If its moving diagonally
        if self.grid[move[1][1]][move[1][0]] == 0: # And its moving to an empty square
          take(self,self.grid[move[0][1]][move[1][0]])

      if move[1][1] == 0 or move[1][1] == 7:
        promote(self, move[2], move[1])
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
        
  def get_possible_moves_without_check(self, colour):
    global getMovesCount # for testing
    getMovesCount += 1
    possibleMoves = []
    test = []
    
    for piece in self.pieces:
      if piece.square != None and piece.colour == colour:
        for rank in range(len(self.grid)):
          for file in range(len(self.grid[rank])):
            if piece.verifyMove(self, piece.square, [rank, file], piece, False):
              possibleMoves.append([piece.square,[rank, file],piece])
    
    return possibleMoves
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
    
    #print("1.1",moveList[0][2].square)
    for move in moveList:
      #print("f",move[2].square)
      if self.checkVerify(move, True) == True and (None not in move):
        newList.append(move)
      #print("g",move[2].square)
    #print("1.2",newList[0][2].square)
    
    return newList
  def checkVerify(self, move, mateCheck):
    global holding
    copyOfMove = []
    for i in move:
      copyOfMove.append(copy.copy(i))
    prevSquare = copyOfMove[0]
    newSquare = copyOfMove[1]
    pieceMoved = copyOfMove[2]
    
    for piece in self.pieces:
      if piece.colour == pieceMoved.colour and piece.type == "king":
        yourKing = piece
      if piece.colour != pieceMoved.colour and piece.type == "king":
        enemyKing = piece
    if pieceMoved.colour == "white":
      enemyColour = "black"
    else:
      enemyColour = "white"
    
    
    
    ### MOVE PIECE ###
    #pieceIndex = self.pieces.index(pieceMoved)
    
    for i in self.pieces:
      if i.square == pieceMoved.square:
        pieceIndex = self.pieces.index(i)
    
    '''
    newPieces = copy.copy(self.pieces)
    board = copy.copy(self.grid)
    takenPiece = None
    prevHoldBool = self.pieces[pieceIndex].hold
    prevHoldingBool = holding
  
    for piece in newPieces:
      if piece.square == newSquare:
        take(self,piece)
        takenPiece = piece

    lastMove = copy.copy(newPieces[pieceIndex].lastMove)
    place(self, newPieces[pieceIndex], newSquare)
    '''
    newBoard = self.copy()
    pieceMoved = newBoard.pieces[pieceIndex]
    #print("FFF", pieceMoved.square)
    
    copyOfMove[2] = pieceMoved # Might not be necessary as it might automatically overwrite
    
    #print(pieceIndex, move[2].type, move[2].square, move[0], move[1])
    takenPiece = None
    #print("f",move[2].square)
    newBoard.move(copyOfMove)
    #print("g",move[2].square)
    
    
    ### GET POSSIBLE MOVES ###
    possibleMoves = newBoard.new_get_possible_moves_without_check(pieceMoved.colour)
    enemyPossibleMoves = newBoard.new_get_possible_moves_without_check(enemyColour)
  
    possibleMove = True
    
    
              
    ### CHECK IF KING ATTACKED
    for move2 in enemyPossibleMoves:
      if yourKing.square == move2[1]:
        check = True
        possibleMove = False

    
    
    ### CHECK IF ATTACKING KING
    if mateCheck == False:
      for move2 in possibleMoves:
        if enemyKing.square == move2[1]:
          check = True
        
          ## For every move check if it removes the check
          ## which means checking if their king's square is no longer in the moves list
    
          ## generate move list () 
          ## for move in move list:
          ##   board after move = ???
          ##   if king.square not in get_possible_moves(boardAfterMove...)
        
          movelist = newBoard.new_get_possible_moves_without_check(enemyColour) ## Figure out how to get all moves         
                    
          checkMate = True
          for move3 in movelist:
            #print(move[0], move[1], move[2].type)
            
            if self.checkVerify(move3, True) == True:
              #print()
              checkMate = False
        
          if checkMate == True:
            CHECKMATE(copyOfMove[2].colour)
     
      
    ### MOVE PIECE BACK ###
    
    #piece = new[pieceIndex]
    #piece.lastMove = lastMove
    #piece.moveCount -= 1
    #board[prevSquare[1]][prevSquare[0]] = piece
    
    #piece.square = prevSquare
    #piece.hold = prevHoldBool
    #holding = prevHoldingBool
    #board[newSquare[1]][newSquare[0]] = 0
    #if takenPiece != None:
    #  takenPiece.square = newSquare
    #  board[newSquare[1]][newSquare[0]] = takenPiece
    
    
    return possibleMove
  def stalemateVerify(self,move):
    draw = False
    if len(self.getPossibleMovesWithCheck(move[2].colour)) == 0 and self.checkVerify(move, False) == True:
      draw = True 
    if self.repeatedMoves == 3:
      draw = True
    return draw
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
      if board.checkVerify(move, False):
        if board.stalemateVerify(move) == False:
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
          STALEMATE()        
  def show(self):
    screen.blit(self.sprite,(self.square[0]*50, self.square[1]*50))
  def moveDotsShow(self):
    if self.hold == True:
      moves = self.getMoves(board)
      for move in moves:
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
          if 0 < self.square[0] - 1:
            if position.grid[self.square[1] + 1][self.square[0] - 1] != 0:
              if position.grid[self.square[1] + 1][self.square[0] - 1].colour != self.colour:
                moves.append([self.square, [self.square[0] - 1, self.square[1] + 1], self])
        if self.square[1] + 2 < 8:
          if position.grid[self.square[1] + 2][self.square[0]] == 0 and self.moveCount == 0:
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
          if position.grid[self.square[1] - 2][self.square[0]] == 0 and self.moveCount == 0:
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
    
                      
      ###ADD
      ### 2. En passant (half done)
      ### 3. Black pieces
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
              if position.grid[self.square[1]][self.square[0] - 2] == 0:
                moves.append([self.square, [self.square[0] - 2, self.square[1]], self])
            else:
              if position.grid[self.square[1]][self.square[0] + 2] == 0:
                moves.append([self.square, [self.square[0] + 2, self.square[1]], self])
    return moves


def take(position, piece):
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
bot = Bot("black", 1)

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

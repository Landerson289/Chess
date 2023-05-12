import pygame
import time

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Chess')

#A1 is [0,0]
#A2 is [0,1]
#C1 is [2,0]
#A1 is top left corner



###Fix bugs with possible move dots (Goes one to far in every direction)
###refactor pawn move code
###Check for checks
###Checkmate
###Stalemate
###Clocks
###Promoted pieces have value of 0
###Putting down pieces
###UI
###Fix pawn double move take bug

class Grid:
  def __init__(self, pieces):
    self.grid = []
    for i in range(8):
      self.grid.append([])
      for j in range(8):
        self.grid[-1].append(0)
        
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
      i.show()
  def update(self):
    if turn%2 == 0:
      colour = "white"
    else:
      colour = "black"
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONDOWN:
        for i in self.pieces:
          if i.colour == colour:
            i.move()

class Piece:
  def __init__(self,type, square, value, colour, verifyMove):
    self.square = square
    self.type = type
    self.sprite = pygame.image.load("images/"+type+".png")
    self.sprite = pygame.transform.scale(self.sprite,(50,50))
    if colour == "white":
      var = pygame.PixelArray(self.sprite)
      var.replace((0,0,0),(255,255,255))
      del var
    self.value = value
    self.colour = colour
    self.hold = False
    self.movable = True
    self.verifyMove = verifyMove
    self.moveCount = 0 
    self.lastMove = 0# Turn it was last moved on
  def move(self):
    
    global holding
    mousePos = pygame.mouse.get_pos()
    mousePos = [mousePos[0]//50,mousePos[1]//50]
    if self.hold == False:
      if self.movable and (not holding):
        if mousePos == self.square:
          self.hold = True
          holding = True
    else:
      if board.grid[mousePos[1]][mousePos[0]] == 0:
        if self.verifyMove(self.square, mousePos, self, True):
          place(self,mousePos)
      else:
        otherPiece = board.grid[mousePos[1]][mousePos[0]]
        if otherPiece.colour != self.colour:
          if self.verifyMove(self.square, mousePos, self, True):
            take(otherPiece)
            place(self,mousePos)
  def show(self):
    
    screen.blit(self.sprite,(self.square[0]*50, self.square[1]*50))
    if self.hold == True:
      for rank in range(len(board.grid)):
        for file in range(len(board.grid[rank])):
          moveable = False
          
          if self.verifyMove(self.square,[rank,file],self,False):
            moveable = True
    
          if moveable == True:
            #print(rank,file)
            screen.blit(board.dotSprite, (rank*50+10,file*50+10))

def pawnMove(prevSquare,newSquare, piece, moving):
  legalMove = False
  if newSquare[0]-prevSquare[0] == 0:
    if board.grid[newSquare[1]][newSquare[0]] == 0:
      if piece.colour == "white":
        if newSquare[1]-prevSquare[1] == 1:
          legalMove = True
    
        if piece.moveCount == 0:
          if newSquare[1]-prevSquare[1] == 2:
            if board.grid[prevSquare[1]+1][newSquare[0]] == 0:
              legalMove = True
            else:
              legalMove = False
            
        if legalMove == True:
          if newSquare[1] == 7:
            promote(piece, newSquare)
      else:
        if newSquare[1]-prevSquare[1] == -1:
          legalMove = True
    
        if piece.moveCount == 0:
          if newSquare[1]-prevSquare[1] == -2:
            if board.grid[prevSquare[1]-1][newSquare[0]] == 0:
              legalMove = True
            
        if legalMove == True:
          if newSquare[1] == 0:
            promote(piece, newSquare)
            
  elif abs(newSquare[0]-prevSquare[0]) == 1:
    if board.grid[newSquare[1]][newSquare[0]] != 0:
      if piece.colour == "white":
        if newSquare[1]-prevSquare[1] == 1:
          legalMove = True
    
        #if piece.moveCount == 0:
        #  if newSquare[1]-prevSquare[1] == 2:
        #    legalMove = True
            
        if legalMove == True:
          if newSquare[1] == 7:
            if moving == True:
              promote(piece, newSquare)
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
      otherPiece = board.grid[newSquare[1]-1][newSquare[0]]
      if otherPiece != 0:
        if otherPiece.moveCount == 1 and newSquare[1] == 5 and otherPiece.lastMove == turn-1:
          if abs(newSquare[1]-prevSquare[1]) == 1:
            legalMove = True
            if moving == True:
              take(otherPiece)
    else:
      otherPiece = board.grid[newSquare[1]-1][newSquare[0]]
      if otherPiece != 0:
        if otherPiece.moveCount == 1 and newSquare[1] == 2 and otherPiece.lastMove == turn-1:
          if newSquare[1]-prevSquare[1] == -1:
            legalMove = True
            if moving == True:
              take(otherPiece)
      
  return legalMove     
def rookMove(prevSquare,newSquare, piece, moving):
  legalMove = False
  path = []
  if prevSquare[0] == newSquare[0]:
    legalMove = True
    if prevSquare[1]>newSquare[1]:
      for i in range(newSquare[1]+1,prevSquare[1]):
        otherPiece = board.grid[i][newSquare[0]]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[1]+1,newSquare[1]):
        otherPiece = board.grid[i][newSquare[0]]
        path.append(otherPiece)
  elif prevSquare[1] == newSquare[1]:
    legalMove = True
    if prevSquare[0]>newSquare[0]:
      for i in range(newSquare[0]+1,prevSquare[0]):
        otherPiece = board.grid[newSquare[1]][i]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[0]+1,newSquare[0]):
        otherPiece = board.grid[newSquare[1]][i]
        path.append(otherPiece)

  
  jumping = False
  for square in path:
    if square != 0:
      jumping = True
      #print(jumping)
      
  if jumping == True:
    legalMove = False
  return legalMove
def knightMove(prevSquare,newSquare, piece, moving):
  legalMove = False
  deltaUp = newSquare[1] - prevSquare[1]
  deltaRight = newSquare[0] - prevSquare[0]

  if abs(deltaUp) == 2:
    if abs(deltaRight) == 1:
      legalMove = True
  elif abs(deltaUp) == 1:
    if abs(deltaRight) == 2:
      legalMove = True
  return legalMove
def bishopMove(prevSquare,newSquare, piece, moving):
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
        square = board.grid[pos[1]][pos[0]]
        path.append(square)
        
    else:
      for i in range(1,prevSquare[0]-newSquare[0]):
        if prevSquare[1] < newSquare[1]:
          pos = [prevSquare[0]-i, prevSquare[1]+i]
        else:
          pos = [prevSquare[0]-i, prevSquare[1]-i]
        square = board.grid[pos[1]][pos[0]]
        path.append(square)

  jumping = False
  for square in path:
    if square != 0:
      jumping = True

  if jumping == True:
    legalMove = False
  return legalMove
def queenMove(prevSquare,newSquare, piece, moving):
  legalMove = False
  path = []
  
  if prevSquare[0] == newSquare[0]:
    legalMove = True
    
    if prevSquare[1]>newSquare[1]:
      for i in range(newSquare[1]+1,prevSquare[1]):
        otherPiece = board.grid[i][newSquare[0]]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[1]+1,newSquare[1]):
        otherPiece = board.grid[i][newSquare[0]]
        path.append(otherPiece)
        
  elif prevSquare[1] == newSquare[1]:
    legalMove = True
    
    if prevSquare[0]>newSquare[0]:
      for i in range(newSquare[0]+1,prevSquare[0]):
        otherPiece = board.grid[newSquare[1]][i]
        path.append(otherPiece)
        
    else:
      for i in range(prevSquare[0]+1,newSquare[0]):
        otherPiece = board.grid[newSquare[1]][i]
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
        square = board.grid[pos[1]][pos[0]]
        path.append(square)
        
    else:
      for i in range(1,prevSquare[0]-newSquare[0]):
        if prevSquare[1] < newSquare[1]:
          pos = [prevSquare[0]-i, prevSquare[1]+i]
        else:
          pos = [prevSquare[0]-i, prevSquare[1]-i]
        square = board.grid[pos[1]][pos[0]]
        path.append(square)

  jumping = False
  for square in path:
    if square != 0:
      jumping = True

  if jumping == True:
    legalMove = False
  
  return legalMove
def kingMove(prevSquare,newSquare, piece, moving):
  global turn
  
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
          i = board.grid[0][7]
        else:
          i = board.grid[7][7]
      elif deltaRight == -2:
        #print("TEST 2")
        if piece.colour == "white":
          #print("TEST 3")
          i = board.grid[0][0]
        else:
          i = board.grid[7][0]
          
      if i != 0:
        #print("TEST 4")
        
        if i.type == "rook" and i.moveCount == 0 and i.colour == piece.colour:
          #print("TEST 5")
          
          legalMove = True

          if deltaRight == 2:
            for j in range(prevSquare[0]+1, 7):
              path.append(board.grid[prevSquare[1]][j])
          elif deltaRight == -2:
            #print("TEST 6")
            for j in range(1,prevSquare[0]):
              path.append(board.grid[prevSquare[1]][j])
            

          for square in path:
            if square != 0:
              #print("taken")
              legalMove = False
              
          if legalMove == True and moving == True:
            if deltaRight == 2:
              place(i,[newSquare[0]-1,newSquare[1]])
            else:
              place(i,[newSquare[0]+1,newSquare[1]])
            turn -= 1
        #else:
          #print("not right conditions")
          #print(i.type)
          #print(i.moveCount)
          #print(i.colour)
          #quit()
      #else:
        #print("corner open")
  return legalMove
  

def take(piece):
  board.grid[piece.square[1]][piece.square[0]] = 0
  piece.square = [-1,-1]
def place(piece,location):
  global holding
  global turn
  board.grid[piece.square[1]][piece.square[0]] = 0
  piece.hold = False
  holding = False
  piece.square = location
  board.grid[location[1]][location[0]] = piece
  piece.moveCount += 1
  piece.lastMove = turn
  turn += 1
def promote(piece,location):
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

  board.pieces.append(Piece(newType, location, 0, piece.colour, newFunc))
  index = board.pieces.index(piece)
  board.pieces.pop(index)

turn = 0
board = Grid([
  Piece("king",[3,0], 100, "white", kingMove),
  Piece("king",[3,7], 100, "black", kingMove),
  
  Piece("queen",[4,0], 9, "white", queenMove),
  Piece("queen",[4,7], 9, "black", queenMove),
  
  Piece("rook",[0,0], 5, "white", rookMove),
  Piece("rook",[7,0], 5, "white", rookMove),
  Piece("rook",[0,7], 5, "black", rookMove),
  Piece("rook",[7,7], 5, "black", rookMove),
  
  Piece("bishop",[2,0], 3, "white", bishopMove),
  Piece("bishop",[5,0], 3, "white", bishopMove),
  Piece("bishop",[2,7], 3, "black", bishopMove),
  Piece("bishop",[5,7], 3, "black", bishopMove),
  
  Piece("knight",[1,0], 3, "white", knightMove),
  Piece("knight",[6,0], 3, "white", knightMove),
  Piece("knight",[1,7], 3, "black", knightMove),
  Piece("knight",[6,7], 3, "black", knightMove),

  Piece("pawn", [0,1], 1, "white", pawnMove),
  Piece("pawn", [1,1], 1, "white", pawnMove),
  Piece("pawn", [2,1], 1, "white", pawnMove),
  Piece("pawn", [3,1], 1, "white", pawnMove),
  Piece("pawn", [4,1], 1, "white", pawnMove),
  Piece("pawn", [5,1], 1, "white", pawnMove),
  Piece("pawn", [6,1], 1, "white", pawnMove),
  Piece("pawn", [7,1], 1, "white", pawnMove),
  
  Piece("pawn", [0,6], 1, "black", pawnMove),
  Piece("pawn", [1,6], 1, "black", pawnMove),
  Piece("pawn", [2,6], 1, "black", pawnMove),
  Piece("pawn", [3,6], 1, "black", pawnMove),
  Piece("pawn", [4,6], 1, "black", pawnMove),
  Piece("pawn", [5,6], 1, "black", pawnMove),
  Piece("pawn", [6,6], 1, "black", pawnMove),
  Piece("pawn", [7,6], 1, "black", pawnMove),
])

holding = False #Bool to check nothing is being held so that two pieces aren't being picked up 

while True:
  board.show()
  board.update()
  pygame.display.update()

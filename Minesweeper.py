import random as Rand


def ClearConsole():
  print(100 * "\n")


VisualGrid = []

BombGrid = []

convertSymbol = ["○", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⦿", "⊛"]

#unicode symbols i will use ○ ● ① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ◙ ⦿ ⊛

x_size = int(input("size of x:"))
y_size = int(input("size of y:"))
neighborhoods = [
  -x_size - 1, -x_size, -x_size + 1, -1, 1, x_size - 1, x_size, x_size + 1
]
pCentBomb = int(input("bomb percentage (20 recommended):"))

TotalTiles = (x_size * y_size) - int(x_size * y_size * pCentBomb / 100)
TilesFound = 0
Cx = int(x_size / 2)
Cy = int(y_size / 2)

if pCentBomb > 99:
  raise Exception("too high of a percentage")

#print(pCentBomb / 100)


def ConvertXYToList(x, y):
  return x + y * x_size


def MakeGrid(x, y):
  #Make a long list of the grid
  for i in range(x):
    for j in range(y):
      VisualGrid.append("●")
      BombGrid.append(0)


def PrintGrid(list, Hx=x_size + 1, Hy=y_size + 1):
  ClearConsole()
  i = 0
  Hlight = ConvertXYToList(Hx, Hy)
  for i in range(len(list)):
    #print(i, end=" ")
    if i % x_size == 0:
      print("")
    if i == Hlight:
      print("◙", end=" ")
    else:
      print(list[i], end=" ")
  print("")
  if Hlight <= x_size * y_size:
    print("Highlighted tile is " + list[Hlight])


def SafeGet(index, list):  #safely get the specified index of a list, returning 0 if it is out of range

  if index < 0 or index >= len(list):
    return 0
  else:
    return list[index]


def PlaceBombs():
  #print("here")
  BombAmt = int(x_size * y_size * pCentBomb / 100)
  BombsPlaced = 0
  index = 0
  while BombsPlaced < BombAmt:
    index %= x_size * y_size
    if BombGrid[index] == 0:
      if Rand.random() < (pCentBomb / 100.0):
        BombGrid[index] = "X"
        BombsPlaced += 1
    index += 1
    #print(BombGrid)


def CountBombs(index):
  #print(index)
  #print(BombGrid[index])

  if BombGrid[index] != "X":
    for neighbor in neighborhoods:
      #catch overflows between rows
      #print(neighbor)
      #print(neighbor % x_size)
      #print(index)
      if neighbor % x_size == 1:
        if index % x_size == x_size - 1:
          continue
      elif neighbor % x_size == x_size - 1:
        if index % x_size == 0:
          continue

      check = SafeGet(index + neighbor, BombGrid)

      if check == "X":
        BombGrid[index] += 1


def click(index, Flag=False):
  global TilesFound
  symbol = BombGrid[index]
  if (VisualGrid[index] != "⊛") and (not Flag):
    if (symbol == "X") and (Flag == False):
      print("Lost")
      #stop program
      exit()
    else:
      if VisualGrid[index] == "●":
        TilesFound += 1
      VisualGrid[index] = convertSymbol[int(BombGrid[index])]
      
      if symbol == 0:
        #recursive 0 spreading
        for neighbor in neighborhoods:
          if neighbor % x_size == 1:
            if index % x_size == x_size - 1:
              continue
          elif neighbor % x_size == x_size - 1:
            if index % x_size == 0:
              continue

          if (index + neighbor) < 0 or (index + neighbor) >= len(BombGrid):
            continue

          if VisualGrid[index + neighbor] == "●":
            click(index + neighbor, False)
  else:
    if VisualGrid[index] == "⊛":
      VisualGrid[index] = "●"
    else:
      VisualGrid[index] = "⊛"
  PrintGrid(VisualGrid, Cx, Cy)
  #print("")


def MoveCursor(Dir):
  global Cx, Cy
  if Dir == "W":
    if Cy > 0:
      Cy -= 1
  elif Dir == "S":
    if Cy < y_size:
      Cy += 1
  elif Dir == "A":
    if Cx > 0:
      Cx -= 1
  elif Dir == "D":
    if Cx < x_size:
      Cx += 1
  PrintGrid(VisualGrid, Cx, Cy)


MakeGrid(x_size, y_size)
PlaceBombs()
#PrintGrid(BombGrid, 0, 0)
print("")
for i in range(len(BombGrid)):
  CountBombs(i)
  #PrintGrid(BombGrid,0,0)
  #print("")
#PrintGrid(BombGrid)
#print("")
#PrintGrid(VisualGrid)
#print("")


def GameLoop():
  while TilesFound != TotalTiles:
    action = input("Use WASD to move, nothing to clear area, and F to flag:")
    print(action)
    if action == '':
      click(ConvertXYToList(Cx, Cy))

    else:
      action = action.upper()
      if action == "F":
        click(ConvertXYToList(Cx, Cy), True)
      elif action in "WASD":
        MoveCursor(action)
  print("You Win")

GameLoop()

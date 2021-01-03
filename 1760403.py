
try:
    import pygame
    import math
    import heapq
    #******INSTANCE*******
    #FILE
    f = open('map.txt', 'r')
    #SCREEN
    SCREEN_SIZE = (600, 600)
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    FPS = 60
    #MAP
    MAP_SIZE_X = 0
    MAP_SIZE_Y = 0
    LISTOFBLOCK = []
    LISTOFFUEL = []

    MAP_SIZE_X = int(f.readline())
    MAP_SIZE_Y = int(f.readline())
    NUMOFBLOCK = int(f.readline())

    for i in range(NUMOFBLOCK):
        tempX = int(f.read(1))
        tempY = int(f.read(1))
        LISTOFBLOCK.append((tempX, tempY))

    f.readline()
    NUMOFFUEL = int(f.readline().strip())
    for i in range(NUMOFFUEL):
        tempX = int(f.read(1))
        tempY = int(f.read(1))
        LISTOFFUEL.append((tempX, tempY))
    f.readline()
    END_POINT_X = int(f.readline())
    END_POINT_Y = int(f.readline())
    #PLAYER
    PLAYER_SIZE = 20
    CURR_POS_X = 0
    CURR_POS_Y = 0
    NEXT_POS = (0, 0)
    SPEED = 1
    #COLORS
    GREY = (120, 120, 120)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    CYAN = (255, 0, 255)
    ORANGE = (0, 255, 255)
    BROWN = (255, 128, 0)
    PASSOVERCOLOr = (29, 29, 29)
    CELL_SIZE = 50
    #LOGIC GAME
    START_POINT_X = 0
    START_POINT_Y = 0
    #AI MOVEMENT
    LISTOFDIRECTION = []
    LISTOFROAD = []
    TARGET_X = 0
    TARGET_Y = 0
    #PLAYER INTERACTION
    MOUSE_CURRENT_POS_X = 0
    MOUSE_CURRENT_POS_Y = 0
    #*******CLASSES*******
    class Cells:
        #TYPE 1 ==> ROAD
        #TYPE 2 ==> ROCK(CANT MOVE)
        #TYPE 3 ==> FUEL STATION
        def __init__(self, _isVisited, _color, _x, _y, _type):
            self.Type = _type
            self.IsVisited = _isVisited
            self.Color = _color
            self.PosX = _x
            self.PosY = _y
        def ChangeColor(self, _color):
            self.Color = _color
        def ChangeType(self, _type):
            self.Type = _type

    class Player:
        def __init__(self, _fuel, _score):
            self.Fuel = _fuel
            self.Score = _score
            self.CurPosX = START_POINT_X
            self.CurPosY = START_POINT_Y
            self.IsRun = False
        def LookAround(self, _listOfCells):
            pass
        def Move(self, _targetX, _targetY):
            #Move Base on Direction
            pass
    class Map:
        def __init__(self, _listOfCells):
            self.ListOfCells = _listOfCells
            self.ListOfRoadDFS = []
            self.ListOfRoadBFS = []
            self.ListOfRoadAStar = []
            self.ListOfRoadUCS = []
            pass
        def UpdateMap(self, _listOfCells):
            self.ListOfCells = _listOfCells
            pass
        def SeekNeighbour(self, _x, _y):
            _x = int(_x)
            _y = int(_y)
            tempList = []
            if _x - 1 >= 0:
                tempList.append(self.ListOfCells[_x - 1][_y])
            if _x + 1 <= len(self.ListOfCells[0]) - 1:
                tempList.append(self.ListOfCells[_x + 1][_y])
            if _y + 1 <= len(self.ListOfCells) - 1:
                tempList.append(self.ListOfCells[_x][_y + 1])
            if _y - 1 >= 0:
                tempList.append(self.ListOfCells[_x][_y - 1])
            return tempList

        def BFS(self):
            ProgressList = [(START_POINT_X, START_POINT_Y)]
            #
            VisitedList = []
            VisitedList.append((START_POINT_X, START_POINT_Y))
            #
            ResultList = {(START_POINT_X, START_POINT_Y) : (START_POINT_X, START_POINT_Y)}
            #
            while len(ProgressList) > 0:
                (tempX, tempY) = ProgressList[0]
                del ProgressList[0]
                #RIGHT
                if tempX + 1 <= len(self.ListOfCells[0]) - 1 and not((tempX + 1, tempY) in VisitedList) and self.ListOfCells[tempX + 1][tempY].Type != 2:
                    ProgressList.append((tempX + 1, tempY))
                    ResultList[(tempX + 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX + 1, tempY))
                    #print("RIGHT")
                #DOWN
                if tempY + 1 <= len(self.ListOfCells) - 1 and not((tempX, tempY + 1) in VisitedList) and self.ListOfCells[tempX][tempY + 1].Type != 2:
                    ProgressList.append((tempX, tempY + 1))
                    ResultList[(tempX, tempY + 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY + 1))
                    #print("DOWN")
                #UP
                if tempY - 1 >= 0 and not((tempX, tempY - 1) in VisitedList) and self.ListOfCells[tempX][tempY - 1].Type != 2:
                    ProgressList.append((tempX, tempY - 1))
                    ResultList[(tempX, tempY - 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY - 1))
                    #print("UP")
                #LEFT
                if tempX - 1 >= 0 and not((tempX - 1, tempY) in VisitedList) and self.ListOfCells[tempX - 1][tempY].Type != 2:
                    ProgressList.append((tempX - 1, tempY))
                    ResultList[(tempX - 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX - 1, tempY))
                    #print("LEFT")

            return ResultList
        def DFS(self):
            #Add player for input to make AI better
            #
            ProgressList = [(START_POINT_X, START_POINT_Y)]
            #
            VisitedList = []
            VisitedList.append((START_POINT_X, START_POINT_Y))
            #
            ResultList = {(START_POINT_X, START_POINT_Y) : (START_POINT_X, START_POINT_Y)}
            #
            while len(ProgressList) > 0:
                (tempX, tempY) = ProgressList[len(ProgressList) - 1]
                del ProgressList[len(ProgressList) - 1]
                #LEFT
                if tempX - 1 >= 0 and not((tempX - 1, tempY) in VisitedList) and self.ListOfCells[tempX - 1][tempY].Type != 2:
                    ProgressList.append((tempX - 1, tempY))
                    ResultList[(tempX - 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX - 1, tempY))
                #UP
                if tempY - 1 >= 0 and not((tempX, tempY - 1) in VisitedList) and self.ListOfCells[tempX][tempY - 1].Type != 2:
                    ProgressList.append((tempX, tempY - 1))
                    ResultList[(tempX, tempY - 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY - 1))
                #RIGHT
                if tempX + 1 <= len(self.ListOfCells[0]) - 1 and not((tempX + 1, tempY) in VisitedList) and self.ListOfCells[tempX + 1][tempY].Type != 2:
                    ProgressList.append((tempX + 1, tempY))
                    ResultList[(tempX + 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX + 1, tempY))
                #DOWN
                if tempY + 1 <= len(self.ListOfCells) - 1 and not((tempX, tempY + 1) in VisitedList) and self.ListOfCells[tempX][tempY + 1].Type != 2:
                    ProgressList.append((tempX, tempY + 1))
                    ResultList[(tempX, tempY + 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY + 1))

            return ResultList
        def AStart(self):
            tempDis = CalculateMagnitude(END_POINT_X, END_POINT_Y, START_POINT_X, START_POINT_Y)
            #init
            VisitedList = [(START_POINT_X, START_POINT_Y)]
            ProgressList = {tempDis : (START_POINT_X, START_POINT_Y)}
            ResultList = {(START_POINT_X, START_POINT_Y) : (START_POINT_X, START_POINT_Y)}
            #MAIN
            while len(ProgressList) > 0:
                tempList = list(ProgressList.keys())
                heapq.heapify(tempList)
                temp = heapq.heappop(tempList)
                tempX, tempY = ProgressList[temp]
                del ProgressList[temp]
                #LEFT
                if tempX - 1 >= 0 and not((tempX - 1, tempY) in VisitedList) and self.ListOfCells[tempX - 1][tempY].Type != 2:
                    tempDis = CalculateMagnitude(tempX - 1, tempY, END_POINT_X, END_POINT_Y)
                    if self.ListOfCells[tempX - 1][tempY].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX - 1, tempY)})
                    ResultList[(tempX - 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX - 1, tempY))
                #UP
                if tempY - 1 >= 0 and not((tempX, tempY - 1) in VisitedList) and self.ListOfCells[tempX][tempY - 1].Type != 2:
                    tempDis = CalculateMagnitude(tempX, tempY - 1, END_POINT_X, END_POINT_Y)
                    if self.ListOfCells[tempX][tempY - 1].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX, tempY - 1)})
                    ResultList[(tempX, tempY - 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY - 1))
                #DOWN
                if tempY + 1 <= len(self.ListOfCells) - 1 and not((tempX, tempY + 1) in VisitedList) and self.ListOfCells[tempX][tempY + 1].Type != 2:
                    tempDis = CalculateMagnitude(tempX, tempY + 1, END_POINT_X, END_POINT_Y)
                    if self.ListOfCells[tempX][tempY + 1].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX, tempY + 1)})
                    ResultList[(tempX, tempY + 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY + 1))
                #RIGHT
                if tempX + 1 <= len(self.ListOfCells[0]) - 1 and not((tempX + 1, tempY) in VisitedList) and self.ListOfCells[tempX + 1][tempY].Type != 2:
                    tempDis = CalculateMagnitude(tempX + 1, tempY, END_POINT_X, END_POINT_Y)
                    if self.ListOfCells[tempX + 1][tempY].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX + 1, tempY)})
                    ResultList[(tempX + 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX + 1, tempY))
            
            return ResultList
        def UCS(self):
            i = 0
            tempDis = 1 + i
            #init
            VisitedList = [(START_POINT_X, START_POINT_Y)]
            ProgressList = {tempDis : (START_POINT_X, START_POINT_Y)}
            ResultList = {(START_POINT_X, START_POINT_Y) : (START_POINT_X, START_POINT_Y)}
            #MAIN
            while len(ProgressList) > 0:
                tempList = list(ProgressList.keys())
                heapq.heapify(tempList)
                temp = heapq.heappop(tempList)
                tempX, tempY = ProgressList[temp]
                del ProgressList[temp]
                #LEFT
                if tempX - 1 >= 0 and not((tempX - 1, tempY) in VisitedList) and self.ListOfCells[tempX - 1][tempY].Type != 2:
                    i += 1
                    tempDis = 1 + i
                    if self.ListOfCells[tempX - 1][tempY].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX - 1, tempY)})
                    ResultList[(tempX - 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX - 1, tempY))
                #UP
                if tempY - 1 >= 0 and not((tempX, tempY - 1) in VisitedList) and self.ListOfCells[tempX][tempY - 1].Type != 2:
                    i += 1
                    tempDis = 1 + i
                    if self.ListOfCells[tempX][tempY - 1].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX, tempY - 1)})
                    ResultList[(tempX, tempY - 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY - 1))
                #DOWN
                if tempY + 1 <= len(self.ListOfCells) - 1 and not((tempX, tempY + 1) in VisitedList) and self.ListOfCells[tempX][tempY + 1].Type != 2:
                    i += 1
                    tempDis = 1 + i
                    if self.ListOfCells[tempX][tempY + 1].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX, tempY + 1)})
                    ResultList[(tempX, tempY + 1)] = (tempX, tempY)
                    VisitedList.append((tempX, tempY + 1))
                #RIGHT
                if tempX + 1 <= len(self.ListOfCells[0]) - 1 and not((tempX + 1, tempY) in VisitedList) and self.ListOfCells[tempX + 1][tempY].Type != 2:
                    i += 1
                    tempDis = 1 + i
                    if self.ListOfCells[tempX + 1][tempY].Type == 3:
                        tempDis = -1
                    ProgressList.update({tempDis : (tempX + 1, tempY)})
                    ResultList[(tempX + 1, tempY)] = (tempX, tempY)
                    VisitedList.append((tempX + 1, tempY))
            
            return ResultList
    LISTOFCELLS = []
    #******FUNCTION********
    def DrawMap(n, m):
        xEnd, yEnd = END_POINT_X, END_POINT_Y
        xStart, yStart = START_POINT_X, START_POINT_Y
        for i in range(n):
            tempList = []
            for j in range(m):
                tempCell = Cells(False, WHITE, i, j, 1)
                pygame.draw.rect(SCREEN, BLACK, (CELL_SIZE * i, CELL_SIZE * j, CELL_SIZE, CELL_SIZE))
                if (i, j) in LISTOFROAD:
                    pygame.draw.rect(SCREEN, PASSOVERCOLOr, (CELL_SIZE * i + 2, CELL_SIZE * j + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                    tempCell.Type = 1
                elif (i, j) in LISTOFFUEL:
                    pygame.draw.rect(SCREEN, ORANGE, (CELL_SIZE * i + 2, CELL_SIZE * j + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                    tempCell.Type = 3
                elif (i, j) in LISTOFBLOCK:
                    pygame.draw.rect(SCREEN, BROWN, (CELL_SIZE * i + 2, CELL_SIZE * j + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                    tempCell.Type = 2
                elif i == xStart and j == yStart:
                    pygame.draw.rect(SCREEN, GREEN, (CELL_SIZE * i + 2, CELL_SIZE * j + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                    tempCell.Color = GREEN
                elif i == xEnd and j == yEnd:
                    pygame.draw.rect(SCREEN, RED, (CELL_SIZE * i + 2, CELL_SIZE * j + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                    tempCell.Color = RED
                else:
                    pygame.draw.rect(SCREEN, WHITE, (CELL_SIZE * i + 2, CELL_SIZE * j + 2, CELL_SIZE - 4, CELL_SIZE - 4))
                tempList.append(tempCell)
            LISTOFCELLS.append(tempList)

    def DrawPlayer(posX, posY):
        #5/8 is 50/40 * 1/2
        pygame.draw.circle(SCREEN, GREY, (CELL_SIZE * posX + PLAYER_SIZE * 2 * 5 / 8, CELL_SIZE * posY + PLAYER_SIZE * 2 * 5 / 8), PLAYER_SIZE)
        pass

    def GetNextTarget(_x, _y, _dir):
        if(_dir == 2):
            return (_x, _y + 1)
        elif(_dir == 4):
            return (_x - 1, _y)
        elif(_dir == 6):
            return (_x + 1, _y)
        elif(_dir == 8):
            return (_x, _y - 1)
        else:
            return (_x, _y) 
        
    def DisplayText(_text, _x, _y):
        text = _text
        font = pygame.font.SysFont(None, 30)
        img = font.render(text, True, RED)

        SCREEN.blit(img, (_x, _y))
        pass
    
    def CalculateMagnitude(_x1, _y1, _x2, _y2):
        return math.sqrt(math.pow(abs(_x2 - _x1), 2) + math.pow(abs(_y2 - _y1), 2))
    #MAIN
    if __name__ == "__main__":
        LISTOFROAD = LISTOFDIRECTION.copy()
        #Display Screen and Logic Solution
        pygame.init()
        isRunning = True
        MyPlayer = Player(10000, 0)
        DrawPlayer(MyPlayer.CurPosX, MyPlayer.CurPosY)
        #V0.1
        direction = 0
        DrawMap(MAP_SIZE_X, MAP_SIZE_Y)
        MyMap = Map(LISTOFCELLS)
        tempStr = ""
        #BFS
        dictOfRoad = MyMap.BFS()
        tempPoint = (END_POINT_X, END_POINT_Y)
        while(tempPoint != (START_POINT_X, START_POINT_Y)):
            MyMap.ListOfRoadBFS.append(tempPoint)
            tempPoint = dictOfRoad[tempPoint]
            pass
        MyMap.ListOfRoadBFS.append((START_POINT_X, START_POINT_Y))
        #DFS
        dictOfRoad = MyMap.DFS()
        tempPoint = (END_POINT_X, END_POINT_Y)
        while(tempPoint != (START_POINT_X, START_POINT_Y)):
            MyMap.ListOfRoadDFS.append(tempPoint)
            tempPoint = dictOfRoad[tempPoint]
            pass
        MyMap.ListOfRoadDFS.append((START_POINT_X, START_POINT_Y))
        #A*
        dictOfRoad = MyMap.AStart()
        tempPoint = (END_POINT_X, END_POINT_Y)
        while(tempPoint != (START_POINT_X, START_POINT_Y)):
            MyMap.ListOfRoadAStar.append(tempPoint)
            tempPoint = dictOfRoad[tempPoint]
        MyMap.ListOfRoadAStar.append((START_POINT_X, START_POINT_Y))
        #UCS
        dictOfRoad = MyMap.UCS()
        tempPoint = (END_POINT_X, END_POINT_Y)
        while(tempPoint != (START_POINT_X, START_POINT_Y)):
            MyMap.ListOfRoadUCS.append(tempPoint)
            tempPoint = dictOfRoad[tempPoint]
        MyMap.ListOfRoadUCS.append((START_POINT_X, START_POINT_Y))


        LISTOFDIRECTION = MyMap.ListOfRoadDFS.copy()
        while isRunning:
            #DRAW BACKGROUND
            SCREEN.fill(GREY)
            #Display map 60 times per sec
            DrawMap(MAP_SIZE_X, MAP_SIZE_Y) 
            MyMap.UpdateMap(LISTOFCELLS)
            tempFuel = 1000
            #DRAW PLAYER AT CURRENT POS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    (MOUSE_CURRENT_POS_X, MOUSE_CURRENT_POS_Y) = pygame.mouse.get_pos()
                    #INVOKE RESET
                    if MOUSE_CURRENT_POS_X >= len(MyMap.ListOfCells) * CELL_SIZE and MOUSE_CURRENT_POS_X <= len(MyMap.ListOfCells) * CELL_SIZE + 100 and MOUSE_CURRENT_POS_Y >= 0 and MOUSE_CURRENT_POS_Y <= 50:
                        MyPlayer.CurPosX = 0
                        MyPlayer.CurPosY = 0
                        direction = 0
                        LISTOFDIRECTION.clear()
                        LISTOFROAD.clear()
                    #INVOKE DFS
                    if MOUSE_CURRENT_POS_X >= len(MyMap.ListOfCells) * CELL_SIZE and MOUSE_CURRENT_POS_X <= len(MyMap.ListOfCells) * CELL_SIZE + 100 and MOUSE_CURRENT_POS_Y >= 51 and MOUSE_CURRENT_POS_Y <= 100:
                        tempStr = ""
                        LISTOFDIRECTION.clear()
                        LISTOFDIRECTION = MyMap.ListOfRoadDFS.copy()
                        MyPlayer.CurPosX = 0
                        MyPlayer.CurPosY = 0
                        TARGET_X = 0
                        TARGET_Y = 0
                        MyPlayer.IsRun = False
                        MyPlayer.Fuel = 10000
                        LISTOFROAD.clear()
                        LISTOFROAD = MyMap.ListOfRoadDFS.copy()
                    #INVOKE BFS
                    if MOUSE_CURRENT_POS_X >= len(MyMap.ListOfCells) * CELL_SIZE and MOUSE_CURRENT_POS_X <= len(MyMap.ListOfCells) * CELL_SIZE + 100 and MOUSE_CURRENT_POS_Y >= 102 and MOUSE_CURRENT_POS_Y <= 153:
                        tempStr = ""
                        LISTOFDIRECTION.clear()
                        LISTOFDIRECTION = MyMap.ListOfRoadBFS.copy()
                        MyPlayer.CurPosX = 0
                        MyPlayer.CurPosY = 0
                        TARGET_X = 0
                        TARGET_Y = 0
                        MyPlayer.IsRun = False
                        MyPlayer.Fuel = 10000
                        LISTOFROAD.clear()
                        LISTOFROAD = MyMap.ListOfRoadBFS.copy()
                    #INVOKE A*
                    if MOUSE_CURRENT_POS_X >= len(MyMap.ListOfCells) * CELL_SIZE and MOUSE_CURRENT_POS_X <= len(MyMap.ListOfCells) * CELL_SIZE + 100 and MOUSE_CURRENT_POS_Y >= 153 and MOUSE_CURRENT_POS_Y <= 204:
                        tempStr = ""
                        LISTOFDIRECTION.clear()
                        LISTOFDIRECTION = MyMap.ListOfRoadAStar.copy()
                        MyPlayer.CurPosX = 0
                        MyPlayer.CurPosY = 0
                        TARGET_X = 0
                        TARGET_Y = 0
                        MyPlayer.IsRun = False
                        MyPlayer.Fuel = 10000
                        LISTOFROAD.clear()
                        LISTOFROAD = MyMap.ListOfRoadAStar.copy()
                    #INVOKE UCS
                    if MOUSE_CURRENT_POS_X >= len(MyMap.ListOfCells) * CELL_SIZE and MOUSE_CURRENT_POS_X <= len(MyMap.ListOfCells) * CELL_SIZE + 100 and MOUSE_CURRENT_POS_Y >= 204 and MOUSE_CURRENT_POS_Y <= 255:
                        tempStr = ""
                        LISTOFDIRECTION.clear()
                        LISTOFDIRECTION = MyMap.ListOfRoadUCS.copy()
                        MyPlayer.CurPosX = 0
                        MyPlayer.CurPosY = 0
                        TARGET_X = 0
                        TARGET_Y = 0
                        MyPlayer.IsRun = False
                        MyPlayer.Fuel = 10000
                        LISTOFROAD.clear()
                        LISTOFROAD = MyMap.ListOfRoadUCS.copy()
            #CHANGE TARGET POSITION
            if len(LISTOFDIRECTION) > 0 and not MyPlayer.IsRun:
                TARGET_X, TARGET_Y = LISTOFDIRECTION.pop()
                if TARGET_X > round(MyPlayer.CurPosX):
                    direction = 6
                elif TARGET_X < round(MyPlayer.CurPosX):
                    direction = 4
                elif TARGET_Y > round(MyPlayer.CurPosY):
                    direction = 2
                elif TARGET_Y < round(MyPlayer.CurPosY):
                    direction = 8
                MyPlayer.IsRun = True

            else:
                pass
            if MyPlayer.CurPosX <= TARGET_X and direction == 6 and MyPlayer.Fuel > 0:
                MyPlayer.CurPosX += SPEED * 1 / FPS
            elif MyPlayer.CurPosY <= TARGET_Y and direction == 2 and MyPlayer.Fuel > 0:
                MyPlayer.CurPosY += SPEED * 1 / FPS
            elif MyPlayer.CurPosX >= TARGET_X and direction == 4 and MyPlayer.Fuel > 0:
                MyPlayer.CurPosX -= SPEED * 1 / FPS
            elif MyPlayer.CurPosY >= TARGET_Y and direction == 8 and MyPlayer.Fuel > 0:
                MyPlayer.CurPosY -= SPEED * 1 / FPS
            else:
                direction = 0
                MyPlayer.IsRun = False
                MyPlayer.Fuel -= 1000
                if (round(MyPlayer.CurPosX), round(MyPlayer.CurPosY)) in LISTOFFUEL:
                    MyPlayer.Fuel = 10000
                else:
                    pass
                    
                if int(MyPlayer.CurPosX) == END_POINT_X and int(MyPlayer.CurPosY) == END_POINT_Y:
                    MyPlayer.Fuel = 0
                    tempStr = "SUCCESSFULLY"
                elif MyPlayer.Fuel <= 0:
                    MyPlayer.Fuel = 0
                    print("CAN'T MOVE TO END POINT")
            #DRAW PLAYER
            pygame.draw.rect(SCREEN, WHITE, (len(MyMap.ListOfCells) * CELL_SIZE + 1, 1, 98, 48))
            DisplayText("RESET", len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE / 3, 20)
            pygame.draw.rect(SCREEN, WHITE, (len(MyMap.ListOfCells) * CELL_SIZE + 1, 51, 98, 48))
            DisplayText("DFS", len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE * 3 / 5, 70)

            pygame.draw.rect(SCREEN, WHITE, (len(MyMap.ListOfCells) * CELL_SIZE + 1, 102, 98, 48))
            DisplayText("BFS", len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE * 3 / 5, 120)
            pygame.draw.rect(SCREEN, WHITE, (len(MyMap.ListOfCells) * CELL_SIZE + 1, 153, 98, 48))
            DisplayText("A*", len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE * 6 / 7, 170)
            pygame.draw.rect(SCREEN, WHITE, (len(MyMap.ListOfCells) * CELL_SIZE + 1, 204, 98, 48))
            DisplayText("UCS", len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE * 5 / 7, 220)

            
            DisplayText("STATUS: ", 100, len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE / 2)
            DisplayText(tempStr, 200, len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE / 2)

            DisplayText("YOUR FUEL: ", 100, len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE)
            DisplayText(str(MyPlayer.Fuel) + "ml", 250, len(MyMap.ListOfCells) * CELL_SIZE + CELL_SIZE)
            MyMap.ListOfCells.clear()
            DrawPlayer(MyPlayer.CurPosX, MyPlayer.CurPosY)
            pygame.display.flip()

        pygame.quit()

except Exception as bug:
    print(bug)
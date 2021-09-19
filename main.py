import random

n = 5
m = 5
bombs = []

def readN():
    global n
    print("Enter height: integer from 1 to 20")
    try:
        n = int(input())
        if not (1 <= n and n <= 20):
            raise ValueError
    except ValueError:
        return 1
    return 0

def readM():
    global m
    print("Enter width: integer from 1 to 20")
    try:
        m = int(input())
        if not (1 <= m and m <= 20):
            raise ValueError
    except ValueError:
        return 1
    return 0

def readB():
    global n
    global m
    global bombs
    print("Enter bombs amount: integer from 0 to", n * m)
    try:
        kolvo = int(input())
        if not (0 <= kolvo and kolvo <= n * m):
            raise ValueError
    except ValueError:
        return -1
    return kolvo

def fillBombs(kolvo):
    global n
    global m
    global bombs
    curs = []
    bombs.clear()
    for i in range(n):
        bombs.append([])
        for j in range(m):
            bombs[i].append(0)
            curs.append([i, j])
    random.shuffle(curs)
    for i in range(kolvo):
        bombs[curs[i][0]][curs[i][1]] = 9

def readInput():
    global n
    global m
    status = readN()
    if status != 0:
        return 1
    status = readM()
    if status != 0:
        return 2
    kolvo = readB()
    if kolvo == -1:
        return 3
    fillBombs(kolvo)
    return 0

def setup_first():
    global bombs
    status = readInput()
    if status != 0:
        return 1
    curs = []
    for i in range(n):
        for j in range(m):
            curs.append([i, j])
    return 0

def desifr(shifr):
    global bombs
    if len(shifr) == 0:
        return 1
    if shifr[-1] == '\n':
         shifr = shifr[:-1]
    if len(shifr) != n * m:
        return 1
    for pos in range(n * m):
        if not(shifr[pos] == '0' or shifr[pos] == '1' or shifr[pos] == '8' or shifr[pos] == '9'):
            return 2
    for i in range(n):
        bombs.append([])
    for i in range(n):
        for j in range(m):
            bombs[i].append(0)
    for pos in range(n * m):
        x = pos // m
        y = pos % m
        bombs[x][y] = int(shifr[pos])
    return 0

def setup():
    global n
    global m
    try:
        f = open("cash.txt", "r")
        time = 0
        for line in f:
            if time == 0:
                tmp = line.split(' ')
                if len(tmp) != 2:
                    raise FileNotFoundError
                n = int(tmp[0])
                m = int(tmp[1])
            elif  time == 1:
                status = desifr(line)
                if status != 0:
                    raise FileNotFoundError
            time = time + 1
        if time != 2:
             raise FileNotFoundError
    except FileNotFoundError or ValueError:
        status = setup_first()
        if status != 0:
            return 1
    return 0

def closing(status):
    if status == 0:
        f = open("cash.txt", "w")
        f.close()
        exit(0)
    f = open("cash.txt", "w")
    global n
    global m
    global bombs
    Line1 = str(n) + ' ' + str(m) + '\n'
    f.write(Line1)
    Line2 = ""
    for i in range(n):
        for j in range(m):
            Line2 = Line2 + str(bombs[i][j])
    f.write(Line2)
    f.close()
    exit(0)

def readCommand(gameGoes):
    if gameGoes == 0:
        print("To exit write 0")
        print("To start next game write 1")
        val = input()
        if val == "0":
            return 0
        if val == "1":
            return 1
    print("To exit write 0")
    print("To start next game write 1")
    print("To make an action write 2")
    val = input()
    if val == "0":
        return 0
    if val == "1":
        return 1
    if val == "2":
        return 2
    return -1

def winCheck():
    global bombs
    global n
    global m
    for i in range(n):
        for j in range(m):
            if bombs[i][j] == 0:
                return 0
    return 1

def parseX(cash):
    global n
    try:
        x = int(cash)
        if not(1 <= x and x <= n):
            print("WRONG COMMAND! X SHOULD BE FROM 1 to", n, ", BUT ", x, "FOUND!")
            return 0
    except ValueError:
        print("WRONG COMMAND! X MUST BE A NUMBER!")
        return 0
    return x

def parseY(cash):
    global m
    try:
        y = int(cash)
        if not(1 <= y and y <= m):
            print("WRONG COMMAND! Y SHOULD BE FROM 1 to ", m, ", BUT ", m, "FOUND!")
            return 0
    except ValueError:
        print("WRONG COMMAND! Y MUST BE A NUMBER!")
        return 0
    return y

def putFlag(x, y):
    global bombs
    if bombs[x][y] == 9:
        bombs[x][y] = 8
        return 0
    return -1

def exist(x, y):
    global n
    global m
    if (0 <= x and x < n):
        if (0 <= y and y < m):
            return 1
    return 0

def getBombsNear(x, y):
    ans = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not(i == 0 and j == 0):
                ans = ans + hasBomb(x + i, y + j)
    return ans

def doOpenStep(x, y):
    global bombs
    if bombs[x][y] == 8:
        return -2
    if bombs[x][y] == 9:
        return -1
    bombs[x][y] = 1
    cash = [[x, y]]
    while len(cash) != 0:
        xnow = cash[-1][0]
        ynow = cash[-1][1]
        cash.pop(-1)
        if getBombsNear(xnow, ynow) == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    print(xnow + i, ynow + j, "STEP")
                    if exist(xnow + i, ynow + j):
                        if bombs[xnow + i][ynow + j] == 0:
                            cash.append([xnow + i, ynow + j])
                            bombs[xnow + i][ynow + j] = 1
    return 0

def doStep():
    global n
    global m
    print("Enter X, Y, Action: X should be from 1 to", n, ", Y should be from 1 to", m, ", Action = Open or Flag")
    tmp = input().split(' ')
    if len(tmp) != 3:
        print("WRONG COMMAND! SHOULD BE 3 Parametrs!")
        return 0

    x = parseX(tmp[0])
    if x == 0:
        return 0
    y = parseY(tmp[1])
    if y == 0:
        return 0
    global bombs
    if tmp[2] == 'Open':
        StepStatus = doOpenStep(x - 1, y - 1)
        if StepStatus == -1:
            print("THERE IS A BOMB AT THIS FIELD, SO")
            return -1
        if StepStatus == -2:
            print("INVALID STEP BECAUSE THERE IS A FLAG!")
            return 0
    elif tmp[2] == 'Flag':
        FlagStatus = putFlag(x - 1, y - 1)
        if (FlagStatus == -1):
            print("THERE ISN`T ANY BOMBS AT THIS FIELD, SO")
            return -1
    else:
        print("ACTION MUST BE Open or Flag, BUT", tmp[2], "FOUND")
        return 0
    return 0

def hasBomb(x, y):
    global bombs
    if exist(x, y) == 0:
        return 0
    if (bombs[x][y] == 8 or bombs[x][y] == 9):
        return 1
    return 0

def showField():
    global n
    global m
    global bombs
    for i in range(n):
        for j in range(m):
            if bombs[i][j] == 0:
                print("X", end = '')
            elif bombs[i][j] == 1:
                count = getBombsNear(i, j)
                if count == 0:
                    print(".", end = '')
                else:
                    print(count, end = '')
            elif bombs[i][j] == 8:
                print("F", end = '')
            else:
                print("X", end = '')
        print()

random.seed()
status = setup()
if status != 0:
    print("setupFailed!")
    exit(0)
gameGoes = 1
while True:
    status = readCommand(gameGoes)
    if status == -1:
        print("WRONG COMMAND!")
        continue
    if status == 0:
        closing(gameGoes)
    elif status == 1:
        tmpStatus = setup_first()
        if tmpStatus == 0:
            gameGoes = 1
        else:
            print("New game setup failed!")
    elif status == 2:
        showField()
        stepStatus = doStep()
        if stepStatus == -1:
            print("GAME OVER!")
            gameGoes = 0
        else:
            showField()
    gameStatus = winCheck()
    if (gameStatus == 1):
        print("YOU WIN!")
        gameGoes = 0

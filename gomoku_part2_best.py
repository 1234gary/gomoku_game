def get_move(board, col):
    n1 = 9
    n2 = 7
    
    if is_empty(board):
        move_y = board_height // 2
        move_x = board_width // 2
        return move_y, move_x
        
    if col == "b":
        c = "w"
    else:
        c = "b"
    
    maxy = 0
    miny = len(board)
    maxx = 0
    minx = len(board)
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != " ":
                if i > maxy:
                    maxy = i
                if i < miny:
                    miny = i
                if j > maxx:
                    maxx = j
                if j < minx:
                    minx = j
                    
    if maxx < len(board) - 1:
        maxx += 2
    else:
        maxx += 1
        
    if maxy < len(board) - 1:
        maxy += 2
    else:
        maxy += 1
    
    if minx != 0:
        minx -= 1
    if miny != 0:
        miny -= 1
    
    
    if maxx - minx >= 10 or maxy - miny >= 10:
        print("phase1")
        n1 = 3
        n2 = 3
    if maxx - minx >= 13 or maxy - miny >= 13:
        print("yolololololololo")
        
        print(maxx,minx,maxy,miny)
        
        move1 = find_top(board, col, maxx,minx,maxy,miny, 5)
        #print(move1)
        move = move1[max(move1)][0]
        move_y, move_x = move[0], move[1]
        return move_y, move_x
    
   
    
    
    #print(maxy, miny, maxx, minx)
    move1 = find_top(board,col, maxx,minx,maxy,miny,n1)
    
    #move1 = find_top(board,col, 8,0,8,0)
    
    if max(move1) == 10000000:
        move = move1[max(move1)][0]
        #print(move)
        move_y, move_x = move[0], move[1]
    
        return move_y, move_x
        
    #print(move1)
    move2 = {}
    move3 = {}
    move_viability = {}
    for i in move1.keys():
        for j in move1[i]:
            #print(j)
            board[j[0]][j[1]] = col
            temp_minx, temp_miny, temp_maxx, temp_maxy = minx, miny, maxx, maxy
            if j[1] != 0 and j[1] < minx + 1:
                temp_minx = j[1] - 1
            if j[0] != 0 and j[0] < miny + 1:
                temp_miny = j[0] - 1
            if j[1] < len(board) - 1 and j[1] > maxx - 2:
                temp_maxx = j[1] + 2
            if j[0] < len(board) - 1 and j[0] > maxx - 2:
                temp_maxy = j[0] + 2
            move2[j] = find_top(board, c, maxx,minx,maxy,miny, n2)
            #print(move2)
            '''for k in move2[j].keys():
                for l in move2[j][k]:
                    board[l[0]][l[1]] = c
                    if l[1] != 0 and l[1] < temp_minx + 1:
                        temp_minx = l[1] - 1
                    if l[0] != 0 and l[0] < temp_miny + 1:
                        temp_miny = l[0] - 1
                    if l[1] < len(board) - 1 and l[1] > temp_maxx - 2:
                        temp_maxx = l[1] + 2
                    if l[0] < len(board) - 1 and l[0] > temp_maxx - 2:
                        temp_maxy = l[0] + 2
                    move3[l] = find_top(board, col, maxx,minx,maxy,miny, 3)
                    #print(move_viability)
                    move_viability[max(move3[l])] = j
                    board[l[0]][l[1]] = " "'''
            move_viability[max(move2[j])] =j
            board[j[0]][j[1]] = " "
    
    
    #print(move1)
    #print(move_viability, maxx, minx, maxy, miny)
    #for i in move2:
        #print(move2[i])
    #print(move_viability)
    
    move = move_viability[min(move_viability)]
    move_y, move_x = move[0], move[1]
    
    return move_y, move_x

def find_top(board, col, maxx, minx, maxy, miny, foresight):
    if col == "b":
        c = "w"
    else:
        c = "b"            

    score = score_better(board, col)
    score_list1 = {}
    for i in range(miny, maxy):
        for j in range(minx, maxx):
            #print(i,j)
            if board[i][j] == " ":
    
                board[i][j] = col
    
                #print_board(board)
                cur_score = score_better(board, col)
                if cur_score > score:
                    if cur_score not in score_list1:
                        score_list1[cur_score] = [(i,j)]
                    else:
                        score_list1[cur_score].append((i,j))
                board[i][j] = " "
    

    score_list2 = {}
    count = 0
    #print(score_list1)
    while count < foresight:
        if score_list1 == {}:
            a = len(board) // 2
            if board[a][a] == " ":
                score_list2[0] = [(a,a)]
            elif board[a - 1][a - 1] == " ":
                score_list2[0] = [(a - 1,a - 1)]
            else:
                score_list2[0] = [(0,0)]
            return score_list2
        score_list2[max(score_list1)] = score_list1[max(score_list1)]
        count += len(score_list1[max(score_list1)])
        if len(score_list1[max(score_list1)]) < foresight:
            score_list1.pop(max(score_list1), None)
            #print(score_list1, "yo")
            #print(score_list2, count)

        #print(count > 5)
        #if score_list1 == {} or count > 4:
        #    break
    
    return score_list2
    
def score_better(board, col):
    if col == "b":
        c = "w"
    else:
        c = "b"
    
    MAX_SCORE = 10000000
    
    our_combos = detect_tiles(board, col)
    their_combos = detect_tiles(board, c)
    
    our_state = {}
    their_state = {}
    
    for i in range(8):
        our_state["OPEN" + str(i + 1)] = 0
        our_state["CLOSED" + str(i + 1)] = 0
        our_state["SEMIOPEN" + str(i + 1)] = 0
        our_state["GAP" + str(i + 1)] = 0
        their_state["OPEN" + str(i + 1)] = 0
        their_state["CLOSED" + str(i + 1)] = 0
        their_state["SEMIOPEN" + str(i + 1)] = 0
        their_state["GAP" + str(i + 1)] = 0
        
    for i in our_combos:
            our_state[i] += 1
    
    for i in their_combos:
            their_state[i] += 1
    
    if our_state["OPEN5"] >= 1 or our_state["SEMIOPEN5"] >= 1 or our_state["CLOSED5"] >= 1:
        return MAX_SCORE
    
    elif their_state["OPEN5"] >= 1 or their_state["SEMIOPEN5"] >= 1 or their_state["CLOSED5"] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (their_state["OPEN4"] + their_state["SEMIOPEN4"] + their_state["GAP5"])  + 
            1000  * our_state["OPEN4"]                    + 
            30   * our_state["SEMIOPEN4"]                + 
            -100  * (their_state["OPEN3"] + their_state["GAP4"])                   + 
            -30   * their_state["SEMIOPEN3"]               + 
            50   * our_state["OPEN3"]                   + 
            30 * our_state["GAP4"]                     +
            10   * our_state["SEMIOPEN3"]              +  
            10 * our_state["GAP3"] - 10* their_state["GAP3"] + 
            (20 * our_state["OPEN2"] + our_state["SEMIOPEN2"]) - (20* their_state["OPEN2"] -  their_state["SEMIOPEN2"] - their_state["OPEN1"]))

def is_bounded(board, y_end, x_end, d_y, d_x, col):
    if col == "b":
        c = "w"
    else:
        c = "b"
    y = y_end
    x = x_end
    spaces = 0
    length = 0
    cont = True
    while cont:
        if board[y][x] == " " and board[y - d_y][x - d_x] == col and spaces == 0:
            spaces += 1
        elif board[y][x] == c or board[y][x] == " ":
            break 
        length += 1
        y -= d_y
        x -= d_x
    if spaces == 1:
        return "GAP"+str(length)
    
    start_coor = (y_end + d_y, x_end + d_x)
    end_coor = (y_end - d_y*(length), x_end - d_x*(length))
    #print(y_end, x_end, d_y, d_x, length, start_coor, end_coor, len(board))
    #print((0 <= start_coor[0] < len(board)) and (0 <= start_coor[1] < len(board)))
    
    start_open = True
    end_open = True
    
    if not ((0 <= start_coor[0] < len(board)) and (0 <= start_coor[1] < len(board))):
        start_open = False
    if not ((0 <= end_coor[0] < len(board)) and (0 <= end_coor[1] < len(board))):
        end_open = False
    
    if start_open:
        if board[start_coor[0]][start_coor[1]] != " ":
            start_open = False
    if end_open:
        if board[end_coor[0]][end_coor[1]] != " ":
            end_open = False
    
    if start_open and end_open:
         return "OPEN" + str(length)
    elif  start_open or end_open:
         return "SEMIOPEN" + str(length)
    else:
         return "CLOSED" + str(length)

def detect_tile(board, col, y, x):
    answer = []
    
    if col == "b":
        c = "w"
    else:
        c = "b"

    #print_board(board)
    if (board[y + 1][x] == " " or board[y + 1][x] == c) and (board[y - 1][x] == col or board[y - 1][x] == " "):
        answer.append(is_bounded(board, y, x, 1,0, col))
    if (board[y + 1][x + 1] == " " or board[y + 1][x + 1] == c) and (board[y - 1][x - 1] == col or board[y - 1][x - 1] == " "):
        answer.append(is_bounded(board, y, x, 1,1, col))    
    if (board[y + 1][x - 1] == " " or board[y + 1][x - 1] == c) and (board[y - 1][x + 1] == col or board[y - 1][x + 1] == " "):
        answer.append(is_bounded(board, y, x, 1,-1, col)) 
    if (board[y][x + 1] == " " or board[y][x + 1] == c) and (board[y][x - 1] == col or board[y][x - 1] == " "):
        answer.append(is_bounded(board, y, x, 0,1, col))    
    
    return answer
    

def detect_tiles(board, col):
    if col == "b":
        c = "w"
    else:
        c = "b"
        
    temp_board = board[:]
    for i in range(len(board)):
        temp_board[i] = board[i][:]
        temp_board[i].insert(0, c)
        temp_board[i].append(c)
        
    temp_board.insert(0, [c]* (len(board) + 2))
    temp_board.append([c] * (len(board) + 2))   
    
    total_combinations = []
    for y in range(1, len(temp_board)):
        for x in range(1, len(temp_board)):
            if temp_board[y][x] == col:
                #print(y,x)
                total_combinations.extend(detect_tile(temp_board, col,y,x))
    
    return total_combinations
    
########################################################################################

def play_gomoku_test(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    import time
    
    #board[7][7] = "w"
    #board[6][6] = "b"
    #board[6][8] = "w"
    while True:
        a = time.time()
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = get_move(board, "b")
        b = time.time()
        print("The time is", (b-a))
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        #analysis(board, "w")
        
        '''game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res'''
    
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board, "b")
        
        '''game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res'''

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    import time
    '''import random
    
    count = 0
    while count < 2:
        x = random.randint(0, len(board) - 1)
        y = random.randint(0, len(board) - 1)
        if board[y][x] == " ":
            board[y][x] = "b"
            count += 1
    count = 0
    while count < 1:
        x = random.randint(0, len(board) - 1)
        y = random.randint(0, len(board) - 1)
        if board[y][x] == " ":
            board[y][x] = "w"
            count += 1'''
    
    board[8][8] = "b"
    
    while True:
        a = time.time()
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = get_move(board, "w")
        b = time.time()
        print("The time is", (b-a))
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board, "w")
        
        '''game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res'''
    
        print("Your move:")
        '''
        move1 = find_top(board,"b", len(board),0,len(board),0)
        move = move1[max(move1)][0]
        move_y, move_x = move[0], move[1]
        '''
        move_y, move_x = search_max2(board, "b")
        board[move_y][move_x] = "b"
        print_board(board)
        #analysis(board, "b")
        
        '''game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res'''
            
def testing():
    
    board =[[' ', ' ', 'w', ' ', 'w', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' '], 
            [' ', ' ', ' ', 'w', 'w', 'b', ' ', ' '], 
            [' ', ' ', 'w', 'b', ' ', 'b', 'w', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'w', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    #print(is_bounded(board, 7,7,1,1, "w"))
    #print(is_bounded(board,5,4,1,0,"b"))
    #print(detect_tile(board, "b", 3, 4))
    #print(detect_tiles(board,"b"))
    board =[[' ', ' ', ' ', ' ', ' ', ' ', 'w', 'w'], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'b', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b'], 
            [' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b'], 
            [' ', ' ', ' ', ' ', ' ', 'b', 'b', 'b'],
            [' ', ' ', ' ', ' ', ' ', 'b', ' ', 'b'], 
            [' ', 'w', ' ', ' ', ' ', 'b', 'w', 'b'], 
            ['w', 'w', 'w', 'w', ' ', 'b', 'w', 'b']]

    print(detect_tiles(board,"w"))
    #print(get_move(board,"w"))
    
    board =[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' '], 
            [' ', 'w', ' ', 'b', ' ', 'b', ' ', ' '], 
            [' ', ' ', 'w', ' ', 'w', ' ', ' ', ' '],
            [' ', ' ', ' ', 'w', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    print(score_better(board, "w"))
    
    board =[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', 'w', ' ', ' ', ' ', ' ', ' ', 'w'], 
            [' ', ' ', 'b', 'w', 'w', 'w', 'b', ' '], 
            [' ', ' ', 'b', 'b', 'w', 'b', ' ', ' '], 
            [' ', ' ', 'w', 'b', 'b', 'b', ' ', ' '],
            [' ', ' ', 'w', 'b', 'b', 'b', ' ', ' '], 
            [' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    print(score_better(board, "b"))
    print(get_move(board, "b"))


###########################################################################################



def is_empty(board):
    board_empty = True
    for i in board:
        if "w" in i or "b" in i:
            board_empty = False
    return board_empty
    
    

   
def is_win(board):
    '''
    
    black_board_list = board[:]
    white_board_list = board[:]
    for i in range(len(board)):
        black_board_list[i] = board[i][:]
        white_board_list[i] = board[i][:]
    
    for i in range(len(board)):
        for j in range(len(board)):
            if black_board_list[i][j] == "w":
                black_board_list[i][j] = " "
            if white_board_list[i][j] == "b":
                white_board_list[i][j] = " "
        
    if (detect_rows(white_board_list, "w", 5)[0] > 0 or 
        detect_rows(white_board_list, "w", 5)[1] > 0):
            return "White won"
    if (detect_rows(black_board_list, "b", 5)[0] > 0 or 
        detect_rows(black_board_list, "b", 5)[1] > 0):
            return "Black won"
    
    board_filled = True 
    for i in board:
        if " " in i:
            board_filled = False
    if board_filled:
        return "Draw"
    '''
    return "Continue playing"
    
    


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                

#####################################################################################################

if __name__ == '__main__':
    testing()
    #play_gomoku(16)
    play_gomoku_test(16)
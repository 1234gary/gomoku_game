def is_empty(board):
    board_empty = True
    for i in board:
        if "w" in i or "b" in i:
            board_empty = False
    return board_empty
    

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
    
    

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    import random
    
    count = 0
    while count < 2:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if board[y][x] == " ":
            board[y][x] = "b"
            count += 1
    count = 0
    while count < 1:
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        if board[y][x] == " ":
            board[y][x] = "w"
            count += 1
    
    print_board(board)
    
    while True:
        
        move_y, move_x = get_move(board, "w")
        
        print("Our AI move: (%d, %d)" % (move_y, move_x))
        
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        
        board[move_y][move_x] = "b"
        print_board(board)
        #analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
        
       
        




########################################################################################

'''def play_gomoku_test(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max_better(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res'''
            
'''def testing():
    
    board =[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', 'b', 'b', 'b', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'b', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', 'w', 'w', ' '], 
            [' ', ' ', ' ', 'b', 'w', 'w', 'w', 'w'], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
    print(score_better(board))
    print(search_max_better(board))'''




    



###########################################################################################



'''def is_empty(board):
    board_empty = True
    for i in board:
        if "w" in i or "b" in i:
            board_empty = False
    return board_empty'''
    
    
def is_bounded3(board, y_end, x_end, length, d_y, d_x):
    upper_open, lower_open = True, True
    if (d_x == -1 and (y_end == len(board) - 1 or x_end == 0)):
        lower_open = False
    elif ((y_end == len(board) - 1 and d_y != 0) or 
         (x_end == len(board) - 1 and d_x != 0)):
        lower_open = False
    if (d_x == -1 and (y_end - d_y * (length - 1) == 0 or
        x_end - d_x * (length - 1) == len(board) - 1)):
        upper_open = False
    elif ((y_end - d_y * (length - 1) == 0 and d_y != 0) or 
         (x_end - d_x * (length - 1) == 0 and d_x != 0)):
        upper_open = False
    if lower_open:
        if board[y_end + d_y][x_end + d_x] != " ":
            lower_open = False
    if upper_open:
        if board[y_end - d_y * length][x_end - d_x * length] != " ":
            upper_open = False
    
    if upper_open and lower_open:
         return "OPEN"
    elif  upper_open or lower_open:
         return "SEMIOPEN"
    else:
         return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count, length_count = 0, 0, 0
    y, x = y_start, x_start
    correct_length = True
    while (0 <= x <= len(board) - 1 and 0 <= y <= len(board) - 1):
        if board[y][x] == col:
            length_count += 1
        else:
            if length_count == length:
                if is_bounded3(board, y - d_y, x - d_x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded3(board, y - d_y, x - d_x, length, d_y, d_x) == "SEMIOPEN":

                    semi_open_seq_count += 1
            length_count = 0
        y += d_y
        x += d_x
    
    if length_count == length:
        if is_bounded3(board, y - d_y, x - d_x, length, d_y, d_x) == "OPEN":
            open_seq_count += 1
        elif is_bounded3(board, y - d_y, x - d_x, length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1
                
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(len(board)):
        open_seq_count += (detect_row(board, col, i, 0, length, 0, 1)[0] + 
                           detect_row(board, col, i, 0, length, 1, 1)[0] +
                           detect_row(board, col, i, len(board) - 1, length, 1, -1)[0])
        semi_open_seq_count += (detect_row(board, col, i, 0, length, 0, 1)[1] + 
                                detect_row(board, col, i, 0, length, 1, 1)[1] +
                                detect_row(board, col, i, len(board) - 1, length, 1, -1)[1])
        
    for k in range(len(board)):
        open_seq_count += detect_row(board, col, 0, k, length, 1, 0)[0] 
        semi_open_seq_count += detect_row(board, col, 0, k, length, 1, 0)[1]
        if k != 0:
            open_seq_count += detect_row(board, col, 0, k, length, 1, 1)[0]
            semi_open_seq_count += detect_row(board, col, 0, k, length, 1, 1)[1]
        if k != 7:
            open_seq_count += detect_row(board, col, 0, k, length, 1, -1)[0]
            semi_open_seq_count += detect_row(board, col, 0, k, length, 1, -1)[1]
            
    return (open_seq_count, semi_open_seq_count)
    
      
def search_max(board):
    max_score = -10000000
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":    
                board[i][j] = "b"
                if score(board) >= max_score:
                    max_score = score(board)
                    move_y, move_x = i, j
                board[i][j] = " "
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 7):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    
    
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
                


def analysis(board):
    for c, full_name in [["w", "White"], ["b", "Black"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x
            
if __name__ == '__main__':
   # testing()
    play_gomoku(8)
    #play_gomoku_test(8)
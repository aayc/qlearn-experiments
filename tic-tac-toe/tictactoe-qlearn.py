from aiplayer import AI_Player;

def getReward (board, playNum):
    for i in range(0, len(board)):
        if max(board[i]) == min(board[i]) and max(board[i]) != 0:
            return REWARD_TERM if board[i][0] == playNum else -REWARD_TERM;
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != 0:
            return REWARD_TERM if board[0][i] == playNum else -REWARD_TERM;
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != 0:
        return REWARD_TERM if board[0][0] == playNum else -REWARD_TERM;
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != 0:
        return REWARD_TERM if board[0][2] == playNum else -REWARD_TERM;
    return 0;

def isTie (board):
    for i in board:
        for j in i:
            if j == 0:
                return False;
    return True;

def inBounds (p, a, b, w, h):
    return p[0] > a and p[0] < a + w and p[1] > b and p[1] < b + h;
def aiMakeMove (ai):
    res = ai.act(board);
    return (res, getReward(res, ai.playNum) != 0);
        
GRAPHICAL_DISPLAY = True;
USER_INPUT = False;
USER_CAN_PLAY = False;
TILE_SIZE = 100;
REWARD_TERM = 50;

board = [[0 for i in range(0, 3)] for j in range(0, 3)];
ais = [AI_Player(1), AI_Player(2)];
numWins = [0 for i in range(0, len(ais))];
numTies = 0;
cnt = 0;

if not GRAPHICAL_DISPLAY:
    for i in range(0, 400000):
        res = aiMakeMove(ais[cnt]);
        board = res[0];
        if res[1]:
            numWins[cnt] += 1;
            board = [[0 for i in range(0, 3)] for j in range(0, 3)];
            ais[cnt].learn(100);
            for i in range(0, len(ais)):
                if i != cnt:
                    ais[i].learn(-100);
        if isTie(board):
            board = [[0 for i in range(0, 3)] for j in range(0, 3)];
            numTies += 1;
        cnt = (cnt + 1) % len(ais);
    GRAPHICAL_DISPLAY = True;
if GRAPHICAL_DISPLAY:
    import sys, pygame;
    pygame.init();
    screen = pygame.display.set_mode((800, 600));
    done = False;
    reset = False;
    
    counter = 0;
    
    textFont = pygame.font.SysFont("Arial", 14);
    renderText = lambda x: textFont.render(x, 1, (10, 10, 10));
    tileColors = [(255, 255, 255), (200, 0, 0), (0, 0, 200), (200, 200, 0)];
    menuColor = (0, 200, 200);
    humanColor = (200, 200, 0);
    while not done:
        screen.fill((255, 255, 255));
        
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True;
            elif USER_INPUT and not USER_CAN_PLAY and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if reset:
                    board = [[0 for i in range(0, 3)] for j in range(0, 3)];
                    reset = False;
                
                res = aiMakeMove(ais[cnt]);
                board = res[0];
                if res[1]:
                    reset = True;
                    numWins[cnt] += 1;
                    ais[cnt].learn(100);
                    for i in range(0, len(ais)):
                        if i != cnt:
                            ais[i].learn(-100);
                elif isTie(board):
                    reset = True;
                    numTies += 1;
                cnt = (cnt + 1) % len(ais);
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                p = event.pos;
                if inBounds(p, 400, 200, 150, 50):
                    USER_INPUT = not USER_INPUT;
                elif inBounds(p, 600, 200, 150, 50):
                    board = [[0 for i in range(0, 3)] for j in range(0, 3)];
                    USER_CAN_PLAY = not USER_CAN_PLAY;

                if USER_CAN_PLAY:
                    if reset:
                        board = [[0 for i in range(0, 3)] for j in range(0, 3)];
                        reset = False;
                        continue;
                    c = event.pos[0]/TILE_SIZE;
                    r = event.pos[1]/TILE_SIZE;
                    if r < 3 and c < 3 and board[r][c] == 0:
                        board[r][c] = 2;

                        if getReward(board, 2) > 0:
                            ais[0].learn(-100);
                            reset = True;
                            print "YAY YOU WIN";
                            continue;

                        if isTie(board):
                            reset = True;
                            numTies += 1;
                        
                        
                        res = aiMakeMove(ais[0]);
                        board = res[0];
                        if res[1]:
                            reset = True;
                            numWins[cnt] += 1;
                            ais[0].learn(100);
                            for i in range(0, len(ais)):
                                if i != cnt:
                                    ais[i].learn(-100);
                                    
                        if isTie(board):
                            reset = True;
                            numTies += 1;
                        
        
                    
        if not USER_INPUT and not USER_CAN_PLAY:
            if reset:
                board = [[0 for i in range(0, 3)] for j in range(0, 3)];
                reset = False;
            
            res = aiMakeMove(ais[cnt]);
            board = res[0];
            if res[1]:
                reset = True;
                numWins[cnt] += 1;
                ais[cnt].learn(100);
                for i in range(0, len(ais)):
                    if i != cnt:
                        ais[i].learn(-100);
            elif isTie(board):
                reset = True;
                numTies += 1;
            cnt = (cnt + 1) % len(ais);
    

        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, tileColors[board[i][j]], rect);
        if USER_CAN_PLAY:
            pos = pygame.mouse.get_pos()
            c = pos[0]/TILE_SIZE;
            r = pos[1]/TILE_SIZE;
            if r < 3 and c < 3 and board[r][c] == 0:
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE);
                pygame.draw.rect(screen, (0, 255, 0), rect);
        pygame.draw.rect(screen, menuColor, pygame.Rect(400, 200, 150, 50));
        pygame.draw.rect(screen, menuColor, pygame.Rect(600, 200, 150, 50));
        screen.blit(renderText("Toggle Speed"), (410, 200));
        screen.blit(renderText("Face AI 1"), (610, 200));
        screen.blit(renderText("AI 1 wins: " + str(numWins[0])), (500, 50));
        screen.blit(renderText("AI 2 wins: " + str(numWins[1])), (500, 100));
        screen.blit(renderText("Ties: " + str(numTies)), (500, 150));
        pygame.display.flip();
    pygame.quit();
    sys.exit();
                
        

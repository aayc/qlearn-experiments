from agent import Agent;

board = [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]];

rewards = [[0 for i in range(0, len(board[0]))] for j in range(0, len(board))];
print rewards;
rewards[2][5] = -50;
rewards[5][5] = 100;

GRAPHICAL_DISPLAY = True;
USER_INPUT = False;
ITER_SPEED = 2;
posFreq = {};

agentStart = [3, 1];
dude = Agent(agentStart[0], agentStart[1], board, rewards);
dudeColor = (0, 128, 255);
wallColor = (255, 128, 0);
rewardColor = (0, 255, 0);
reset = False;

if GRAPHICAL_DISPLAY:
    import sys, pygame
    pygame.init();
    screen = pygame.display.set_mode((800, 600));
    done = False;
    runCount = 0;
    while not done:
        screen.fill((0, 0, 0));
        if reset:
            dude.pos = (agentStart[0], agentStart[1])
            reset = False;
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True;
            elif USER_INPUT and event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                dude.act();                   
                posFreq[dude.pos] = 0 if dude.pos not in posFreq else posFreq[dude.pos] + 1;
                if (rewards[dude.pos[0]][dude.pos[1]] != 0):
                    reset = True;
            elif not USER_INPUT:
                runCount += 1;
                if runCount == ITER_SPEED:
                    runCount = 0;
                    dude.act();
                    posFreq[dude.pos] = 0 if dude.pos not in posFreq else posFreq[dude.pos] + 1;
                    if (rewards[dude.pos[0]][dude.pos[1]] != 0):
                       reset = True;
        
        dudeRect = pygame.Rect(dude.pos[1]*50, dude.pos[0]*50, 50, 50);
        
        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                if board[r][c] == 1:
                    pygame.draw.rect(screen, wallColor, pygame.Rect(c*50, r*50, 50, 50));
                elif rewards[r][c] > 0:
                    pygame.draw.rect(screen, (0, min(rewards[r][c], 255), 0), pygame.Rect(c*50, r*50, 50, 50));
                elif rewards[r][c] < 0:
                    pygame.draw.rect(screen, (min(abs(rewards[r][c]), 255), 0, 0), pygame.Rect(c*50, r*50, 50, 50));
        pygame.draw.rect(screen, dudeColor, dudeRect)
        pygame.display.flip();
    pygame.quit();
    sys.exit();
else:
    print "yo";
    for i in range(0, 30000):
        dude.act();
        posFreq[dude.pos] = 0 if dude.pos not in posFreq else posFreq[dude.pos] + 1;
    freqList = [(i, posFreq[i]) for i in posFreq.keys()];
    for f in freqList:
        print f;


from agent import Agent;

board = [[1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]];

rewards =[[0, 0, 0, 0, 0, 0, 0, 0],
          [0, 50, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 10, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0]];

GRAPHICAL_DISPLAY = True;
posFreq = {};

agentStart = [3, 4];
dude = Agent(agentStart[0], agentStart[1], board, rewards);
dudeColor = (0, 128, 255);
wallColor = (255, 128, 0);
rewardColor = (0, 255, 0);

if GRAPHICAL_DISPLAY:
    import sys, pygame
    pygame.init();
    screen = pygame.display.set_mode((800, 600));
    done = False;
    while not done:
        screen.fill((0, 0, 0));
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True;
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                dude.act();
                posFreq[dude.pos] = 0 if dude.pos not in posFreq else posFreq[dude.pos] + 1;
                
        
        dudeRect = pygame.Rect(dude.pos[0]*50, dude.pos[1]*50, 50, 50);
        
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] == 1:
                    pygame.draw.rect(screen, wallColor, pygame.Rect(i*50, j*50, 50, 50));
                elif rewards[i][j] > 0:
                    pygame.draw.rect(screen, rewardColor, pygame.Rect(i*50, j*50, 50, 50));
        pygame.draw.rect(screen, dudeColor, dudeRect)
        pygame.display.flip();
    pygame.quit();
    sys.exit();
else:
    for i in range(0, 30000):
        dude.act();
    freqList = [(i, posFreq[i]) for i in posFreq.keys()];
    for f in freqList:
        print f;


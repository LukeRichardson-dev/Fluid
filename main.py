from fluid import *
import pygame
from time import sleep

SIZE = 400
CELLS = 40

def handle_events():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
    return True

def run_v_test(vf, df):
    vf = curl(vf)
    vf = curl(vf)
    win = pygame.display.set_mode((SIZE, SIZE))
    cell_size = SIZE / CELLS

    while handle_events():

        win.fill((0, 0, 0))
        
        for x, c in enumerate(df):
            for y, d in enumerate(c):
                colour = max(0, min(100 * d, 255))
                pygame.draw.rect(win, (colour, colour, colour), (x * cell_size, y * cell_size, cell_size, cell_size))
        
        pygame.display.update()
        # sleep(1)
        df = diffuse(df, 0.011)
        df = advectate(vf, df, 1)

if __name__ == '__main__':
    pygame.init()

    print(create_vector_field(CELLS, CELLS))
    print(create_density_field(CELLS, CELLS))

    v, d = create_basic_fluid(CELLS, CELLS)
    v = np.ones(v.shape)

    # d = np.zeros((400, 400))
    
    run_v_test(v, d)

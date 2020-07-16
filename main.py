import pygame
from time import time
from vector_class import Vector2D as Vec, randint, sin

#region pygame init
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
screen.fill([255, 255, 255])
pygame.display.set_icon(screen)
clock, fps = pygame.time.Clock(), 0

delta_time = 0 ; frame_start_time = 0
#endregion

max_size = 30
min_size = 10
samples_per_try = 25
sampling_fail_counter = 0 ; min_failed_samples = 50
disks = []

class Disk():
    def __init__(self, x, y, rad):
        self.pos = Vec(x, y)
        self.rad = rad

        self.max_dist_from_others = -1
        self.viable = True

        self.colour = [randint(80, 200) for _ in range(3)]
        self.show_rad = 1
        self.flash_index = randint(0, 2) ; self.flash_counter = 0
    
    def update(self, delta_time):
        if self.show_rad < self.rad:
            self.show_rad += 1
        
        self.colour[self.flash_index] += sin(self.flash_counter) * 50
        if self.colour[self.flash_index] > 255 : self.colour[self.flash_index] = 255
        if self.colour[self.flash_index] < 0 : self.colour[self.flash_index] = 0
        self.flash_counter += 1 * delta_time

def get_new_disk():
    rad = randint(min_size, max_size)
    x, y = Vec.random_pos(size[0] - rad, size[1] - rad, min_x=rad, min_y=rad).get()
    return Disk(x, y, rad)

def generate_candidates():
    return [get_new_disk() for _ in range(samples_per_try)]

def select_best_candidate(candidates):
    for candidate in candidates:
        for disk in disks:
            dist = candidate.pos.dist(disk.pos)

            if dist < disk.rad + candidate.rad:
                candidate.viable = False
                break

            if dist > candidate.max_dist_from_others or candidate.max_dist_from_others == -1:
                candidate.max_dist_from_others = dist
    
    max_dist = -1
    selected = None
    for candidate in candidates:
        if (candidate.max_dist_from_others > max_dist or max_dist == -1) and candidate.viable:
            max_dist = candidate.max_dist_from_others
            selected = candidate
    
    return selected

disks.append(get_new_disk())
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    frame_start_time = time()
    screen.fill(0)

    if max_size > min_size:
        candidates = generate_candidates()
        candidate = select_best_candidate(candidates)

        if candidate is not None:
            disks.append(candidate)
            sampling_fail_counter = 0
        else:
            sampling_fail_counter += 1
        
        if sampling_fail_counter >= min_failed_samples:
            max_size -= 1
            sampling_fail_counter = 0

    for disk in disks:
        pygame.draw.circle(screen, disk.colour, disk.pos.get(), disk.show_rad)
        disk.update(delta_time)

    pygame.display.update()
    clock.tick(fps)
    delta_time = time() - frame_start_time
    pygame.display.set_caption(f'Framerate: {int(clock.get_fps())}')







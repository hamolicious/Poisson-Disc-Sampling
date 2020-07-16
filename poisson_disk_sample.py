"""
This file can be used to generate Poisson Disk Sampled Planes

"""

from vector_class import Vector2D as Vec, randint

class Disk():
    def __init__(self, x, y, rad):
        self.pos = Vec(x, y)
        self.rad = rad

        self.max_dist_from_others = -1
        self.viable = True

def get_new_disk(size, min_size, max_size):
    rad = randint(min_size, max_size)
    x, y = Vec.random_pos(size[0] - rad, size[1] - rad, min_x=rad, min_y=rad).get()
    return Disk(x, y, rad)

def generate_candidates(samples_per_try, size, min_size, max_size):
    return [get_new_disk(size, min_size, max_size) for _ in range(samples_per_try)]

def select_best_candidate(candidates, disks):
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

def get_disk_plane(plane_size, min_disk_size, max_disk_size, samples_per_try, min_failed_samples):
    """
    returns a set of Disks that are contained inside the plane size

    param plane_size : tuple -> size of plane to add disks to (will not overflow that boundary)
    param min_disk_size : int -> smallest possible disk size
    param max_disk_size : int -> largest possible disk size
    param samples_per_try : int -> number of candidates to try per sample
    param min_failed_samples : int -> minimum amount of failed additions before lowering the max size
    """
    disks = [get_new_disk(plane_size, min_disk_size, max_disk_size)]
    sampling_fail_counter = 0

    while max_disk_size > min_disk_size:
        candidates = generate_candidates(samples_per_try, plane_size, min_disk_size, max_disk_size)
        candidate = select_best_candidate(candidates, disks)

        if candidate is not None:
            disks.append(candidate)
            sampling_fail_counter = 0
        else:
            sampling_fail_counter += 1
        
        if sampling_fail_counter >= min_failed_samples:
            max_disk_size -= 1
            sampling_fail_counter = 0
    
    return disks







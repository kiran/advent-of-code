import math

with open("./input.txt") as f:
    slope_map = f.read().splitlines()

width = len(slope_map[0])
height = len(slope_map)


def next_coords(coords, slope):
    return (coords[0] + slope[0], coords[1] + slope[1])


def has_tree(coords):
    x_axis = coords[0] % width
    point = slope_map[coords[1]][x_axis]
    if point == ".":
        return False
    elif point == "#":
        return True
    else:
        raise ValueError(point)


def count_trees(slope):
    current_coords = (0, 0)
    num_trees = 0

    while current_coords[1] < height:
        # print(current_coords, has_tree(current_coords))
        if has_tree(current_coords):
            num_trees += 1

        current_coords = next_coords(current_coords, slope)

    return num_trees


slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
trees = [count_trees(slope) for slope in slopes]

print(trees)
print(math.prod(trees))

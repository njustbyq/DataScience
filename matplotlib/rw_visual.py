import matplotlib.pyplot as plt
import random

from random_walk import RandomWalk

while True:

    rw = RandomWalk(50000)
    rw.fill_walk()

    plt.figure(figsize=(10, 6))

    point_numbers = list(range(rw.num_points))
    plt.scatter(rw.x_values, rw.y_values, edgecolors='none', s=1, c=point_numbers, cmap=plt.cm.Blues)

    plt.scatter(0, 0, c='green', edgecolors='none', s=5)
    plt.scatter(rw.x_values[-1], rw.y_values[-1], c='red', edgecolors='none', s=5)

    plt.xlabel('Axis X', fontsize=14)
    plt.ylabel('Axis Y', fontsize=14)
    plt.title('Random Walk', fontsize=24)    

    plt.axes().get_xaxis().set_visible(False)
    plt.axes().get_yaxis().set_visible(False)

    flag = input('Make another walk? (y/n):')
    if flag.lower() not in ['y', 'yes']:
        break
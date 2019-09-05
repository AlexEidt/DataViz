"""Creates a Scatter Plot with Randomly filled values"""

import os
import random
from matplotlib import pyplot as plt

current_dir = os.path.normpath(f'{os.getcwd()}/Scatter Plots')

if __name__ == "__main__":
    x_axis = [random.randint(0, 1000) for _ in range(1000)]
    y_axis = [random.randint(0, 1000) for _ in range(1000)]
    colors = [random.randint(0, 9) for _ in range(1000)]

    plt.scatter(x_axis, y_axis, c=colors, cmap='Greens',
                edgecolor='black', linewidth=1, alpha=0.61)

    cbar = plt.colorbar()
    cbar.set_label('Randomness')

    plt.title('Random Number Generation is Actually Random!')
    plt.savefig(os.path.normpath(f'{current_dir}/Random.png'))
    plt.show()
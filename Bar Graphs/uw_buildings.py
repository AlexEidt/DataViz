"""Creates Horizontal Bar Graphs for Building Use for each Campus
of the University of Washington
Find data at: https://github.com/AlexEidt/UW-Course-Tool/tree/master/static/UW_Time_Schedules
"""

import json
import os
from collections import Counter
from matplotlib import pyplot as plt

current_dir = os.path.normpath(f'{os.getcwd()}/Bar Graphs')

if __name__ == '__main__':

    plt.style.use('seaborn')

    fig, plots = plt.subplots(nrows=1, ncols=3)

    for i, campus in enumerate(['Bothell', 'Seattle', 'Tacoma']):

        # Read Time Schedule Data for each UW Campus
        with open(os.path.normpath(f'{current_dir}/Data/UW_{campus}_AUT2019.json'), mode='r') as file:
            sections = json.loads(file.read())['Total']

        section_counter = Counter()
        # Keep a running total of the number of sections in each building
        for section in sections:
            section_counter.update(section['Building'])

        # Get the top 20 buildings with the number of sections in them
        building, num_sections = map(list, zip(*section_counter.most_common(10)))
        # Reverse both lists
        building = building[::-1]
        num_sections = num_sections[::-1]

        # Plot Data as a Bar Graph
        plots[i].barh(building, num_sections)

        plots[i].set_xlabel('Number of Sections')
        plots[i].set_ylabel(f'{campus} - Autumn 2019')

    fig.suptitle('Most Commonly used Buildings at UW')
    plt.tight_layout()
    plt.savefig(os.path.normpath(f'{current_dir}/UW_Building_Data.png'))
    plt.show()




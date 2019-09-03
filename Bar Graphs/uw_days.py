"""Creates a Histogram of Courses offered at different time intervals
at the University of Washington"""

import os
import re
import json
from itertools import chain
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt

current_dir = os.path.normpath(f'{os.getcwd()}/Bar Graphs')

def get_days(offered):
    """Gets the days a course is offered
    @params
        'offered': String representing the days a course is offered
        Example: 'MWF' -> Monday, Wednesday, Friday
    Returns
        Set of abbreviated days the course is offered
    """
    days = ['Th', 'M', 'T', 'W', 'F', 'S']
    result = set()
    for day in days:
        if day in offered:
            result.add(day)
            offered = offered.replace(day, '', 1)
    return result


if __name__ == '__main__':
    total_uw = []
    for campus in ['Seattle', 'Bothell', 'Tacoma']:
        with open(f'{current_dir}/Data/UW_{campus}_AUT2019.json', mode='r') as file:
            total_uw.append(json.loads(file.read())['Total'])
    total_uw = chain(*total_uw)
    # Count number of sections per day
    counter = Counter()
    for section in total_uw:
        for day in section['Days']:
            counter.update(get_days(day))

    days = ['M', 'T', 'W', 'Th', 'F', 'S'] 

    # Create Bar Graph
    plt.style.use('ggplot')

    plt.bar(days, counter.values())

    plt.title('Course Sections per day at UW')
    plt.ylabel('Number of Sections')

    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{current_dir}/UW_Days_Offered.png')
    plt.show()

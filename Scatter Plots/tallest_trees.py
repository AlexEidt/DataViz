"""Creates 3 Scatter Plots showing relational data
of the Height of Trees to their trunk volume, diameter and circumference
Find data at: https://en.wikipedia.org/wiki/List_of_largest_giant_sequoias
"""

import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as Soup
from matplotlib import pyplot
from matplotlib import pyplot as plt
from matplotlib import ticker as pltticker

current_dir = os.path.normpath(f'{os.getcwd()}/Scatter Plots')

trees_page = Soup(requests.get('https://en.wikipedia.org/wiki/List_of_largest_giant_sequoias').text, 
                  features='lxml')
table = trees_page.find('table', class_='wikitable sortable')
data = list(table.find_all('tr'))
header = []
th = Soup(str(data[0]), features='lxml').find_all('th')
for i, h in enumerate(th):
    if i not in [2, len(th) - 1]:
        header.append(re.sub(r'\n|\[.+\]', '', h.text))

total = []
for i in range(1, len(data)):
    row = []
    cells = Soup(str(data[i]), features='lxml')
    for td in cells.find_all('td'):
        cell_data = re.sub(r'[(\n)((cubic)? feet)]*', '', td.text.split('(', 1)[0].strip())
        row.append(re.sub(r'\[.+\]', '', cell_data).replace(',', '').replace(' ', ''))
    total.append([x for i, x in enumerate(row) if i not in [2, len(row) - 1]])

df = pd.DataFrame(total, columns=header)
df.to_csv(os.path.normpath(f'{current_dir}/Data/Largest_Trees.csv'))
df.set_index('Rank', inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(thresh=3, inplace=True)

# Plot Data

for attribute in [('Circumference', 'ft'), ('Diameter', 'ft'), ('BoleVolume', 'cubic ft')]:

    fig, ax = plt.subplots(1, 1)
    plt.scatter(df['Height'], df[attribute[0]], cmap='plasma', edgecolor='green',
                linewidth=1, alpha=0.5)
    ax.set_title('Tree Height vs. Circumference')
    ax.set_xlabel(f'{attribute[0]} ({attribute[1]})')
    ax.set_ylabel('Height (ft)')
    pyplot.locator_params(axis='y', nbins=10)
    pyplot.locator_params(axis='x', nbins=10)

    plt.tight_layout()
    plt.savefig(os.path.normpath(f'{current_dir}/Graphs/Tree_Data_{attribute[0]}.png'))
    plt.show()



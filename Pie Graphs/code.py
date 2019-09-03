"""Creates a pie graph with all programming languages
used in a given directory
Find data at: https://en.wikipedia.org/wiki/List_of_programming_languages
"""

import os
import re
import json
import requests
import pandas as pd
from itertools import cycle
from collections import Counter
from bs4 import BeautifulSoup
from tqdm import tqdm
from matplotlib import pyplot as plt

current_dir = os.path.normpath(f'{os.getcwd()}/Pie Graphs')
popular = ['Python', 'Java', 'JavaScript', 'C#', 'PHP', 'C', 'C++', 'R', 'Objective-C', 'Swift', 'MATLAB', 'TypeScript',
           'Ruby', 'Kotlin', 'Go', 'Scala', 'Visual Basic', 'Rust', 'Perl', 'Lua', 'Haskell', 'Delphi', 'Julia', 'PowerShell']

def parse_data():
    """Gets all Programming Languages and their extensions from a Wikipedia Page
    and prints them into a json file"""
    languages = str(requests.get('https://en.wikipedia.org/wiki/List_of_programming_languages').text)
    languages = languages.split('class="div-col columns column-width"', 2)[-1]
    languages = languages.rsplit('class="mw-headline" id="See_also"', 1)[0]

    languages = BeautifulSoup(languages, features='lxml')
    code_dict = {}
    for li in tqdm(languages.find_all('li')):
        link = li.find('a')
        l = link.get('href')
        name = str(link.get('title')).replace('(programming language)', '')
        language = str(requests.get('https://en.wikipedia.org{}'.format(l)).text)
        if 'Filename extension' in language:
            # Get extensions from Progamming Language Wikipedia page
            extensions = []
            language = BeautifulSoup(language, features='lxml')
            table = language.find('table', class_='infobox')
            for row in table.find_all('tr'):
                if row.find('a', {'title': 'Filename extension'}):
                    for extension in row.find_all('td'):
                        for x in extension.text.strip().strip(',').replace('\n', ' ').split(' '):
                            if re.search(r'\.[a-zA-Z0-9_]+', x) and x.startswith('.'):
                                for ext in re.findall(r'\.[a-zA-Z0-9_]+', x):
                                    extensions.append(ext.split('[')[0].strip())
            if extensions:
                code_dict[name.split('(')[0].strip()] = list(map(lambda x: x.strip(','), extensions))

    # Eliminate less-popular languages that have the same extensions as other popular languages
    remove = set()
    for lang, count in code_dict.items():
        for l, c in code_dict.items():
            if l != lang:
                if set(c).intersection(count):
                    if l in popular and lang not in popular:
                        remove.add(lang)
                    elif l not in popular and lang in popular:
                        remove.add(l)
    for lang in remove:
        del code_dict[lang]
    
    # Add common markup languages not found in the Wikipedia article
    code_dict['HTML'] = ['.html']
    code_dict['CSS'] = ['.css']

    with open(os.path.normpath(f'{current_dir}/Data/progamming_languages.json'), mode='w') as file:
        json.dump(code_dict, file, indent=4, sort_keys=True)


def find_languages(dirname, code_dict, counter):
    """Recursively Analyzes all files/directories for the given dirname
    @params
        'dirname': Directory to search
        'code_dict': Dictionary with Programming Language Names to extensions mappings
        'counter': Count of characters for each programming language found in the directory
    """
    if not os.path.isdir(dirname):
        if '.md' not in dirname: # Filter out MarkDown files
            ext = '.{}'.format(dirname.rsplit('.', 1)[-1])
            for lang, extns in code_dict.items():
                if ext in extns:
                    with open(dirname, mode='r', encoding='ISO-8859-1') as file:
                        if lang not in counter:
                            counter[lang] = 0
                        counter[lang] += len(file.read().replace(' ', ''))
    else:
        for f in os.listdir(dirname):
            file_name, ext = os.path.splitext(f)
            find_languages(os.path.normpath(f'{dirname}/{file_name}{ext}'), code_dict, counter)
                    

if __name__ == '__main__':
    if 'progamming_languages.json' not in os.listdir(os.path.normpath(f'{current_dir}/Data')):
        parse_data()

    dir_name = input('Enter Directory to Scan (Must be in current directory): ')
    directory = os.path.normpath(f'{current_dir}/{dir_name}')
    with open(os.path.normpath(f'{current_dir}/Data/progamming_languages.json'), mode='r') as file:
        code_dict = json.loads(file.read())
    counter = {}
    find_languages(directory, code_dict, counter)
    lang_freq = {'Language': list(counter.keys()), 'Frequency': list(counter.values())}
    df = pd.DataFrame(lang_freq)
    df.insert(2, 'Explode', df['Frequency'][df['Frequency'] == df['Frequency'].max()])
    df = df.fillna(0)
    index = df.loc[df['Explode'] != 0].index # Index of Highest Frequency Language in Explode column
    df['Explode'][index] = 0.1

    # Create Pie Graph
    plt.style.use('fivethirtyeight')

    plt.pie(df['Frequency'], labels=df['Language'], explode=df['Explode'],
            wedgeprops={'edgecolor': 'black', 'linewidth': 2},
            startangle=90, shadow=True, autopct='%1.0f%%',
            rotatelabels=False)

    plt.title(f'Code used in {dir_name}')
    plt.figtext(0.90, 0.05, 
                '*Comments included\n*Markup Languages not Included\n(except HTML, CSS)', 
                horizontalalignment='right', verticalalignment='bottom', fontsize='xx-small')

    plt.tight_layout()
    plt.savefig(os.path.normpath(f'{current_dir}/Code used in {dir_name}'))
    plt.show()
    



    
                


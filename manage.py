#!/usr/bin/env python2
from __future__ import print_function
import argparse
import json
import re

class DistInfo(object):
    def __init__(self, d):
        self.name = ''
        self.recipes = []
        for key, value in d.items():
            setattr(self, key, value)

def get_data():
    try:
        with open('dists.json', 'r') as fileh:
            data = json.load(fileh)
    except IOError:
        data = []
    data = [DistInfo(v) for v in data]  # data is a list of dicts
    return data

def write_data(l):
    data = [{'name': item.name, 'recipes': item.recipes} for item in l]
    with open('dists.json', 'w') as fileh:
        json.dump(data, fileh)

def list_current_dists():
    data = get_data()

    print('Dists are:')
    if not data:
        print('    --- there are no dists yet ---')
    for d in data:
        print('    {}: recipes are ({})'.format(
            d.name, ', '.join(d.recipes)))


def main():
    parser = argparse.ArgumentParser(
        description='Tool for managing python-for-android binary dists',
        )
    parser.add_argument('command', help='The thing to do')
    parser.add_argument('--name', default='')
    parser.add_argument('--recipes', default='')

    args = parser.parse_args()

    command = args.command
    if command == 'list':
        list_current_dists()

    elif command == 'add_dist':
        data = get_data()
        if not args.name or not args.recipes:
            raise ValueError('Command requires both name and recipes')
        name = args.name
        recipes = re.split(r'[ ,]*', args.recipes)
    
        if name in [d.name for d in data]:
            raise ValueError('Dist with this name already stored')

        data.append(DistInfo({'name': name, 'recipes': recipes}))

        write_data(data)


if __name__ == "__main__":
    main()

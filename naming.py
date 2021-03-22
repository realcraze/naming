#!/usr/bin/env python3

import os
import json
import random
import re

FOLDER_NAMES = ['shijing', 'json', 'wudai', 'ci', 'caocao']


def load_poetry_file(folder_path):
    res = []
    if os.path.exists(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = folder_path + os.path.sep + file_name
            if os.path.isdir(file_path):
                res.extend(load_poetry_file(file_path))
            elif file_name.endswith('.json'):
                file = open(file_path, 'r')
                res.extend(json.loads(file.read()))
                file.close()
    return res


def select_from_poetry(poetry):
    content = []
    if 'paragraphs' in poetry:
        content = poetry['paragraphs']
    elif 'content' in poetry:
        content = poetry['content']

    paragraph = content[random.randint(0, len(content) - 1)]
    sentences = re.split('。|！|？|；', paragraph)
    end = len(sentences) - 1
    if len(sentences[-1]) == 0:
        end -= 1
    sentence = sentences[random.randint(0, end)]

    groups = re.split('，', sentence)
    if len(groups) > 1:
        first_index = random.randint(0, len(groups) - 2)
        second_index = first_index + 1
        first_pos = random.randint(0, len(groups[first_index]) - 1)
        second_pos = first_pos
        if len(groups[first_index]) != len(groups[second_index]):
            second_pos = random.randint(0, len(groups[second_index]) - 1)
        return (groups[first_index], groups[second_index], groups[first_index][first_pos], groups[second_index][second_pos])
    else:
        return None


if __name__ == '__main__':
    all = []
    for folder_name in FOLDER_NAMES:
        all.extend(load_poetry_file('database' + os.path.sep + folder_name))
    for i in range(100):
        poetry = all[random.randint(0, len(all) - 1)]
        select = select_from_poetry(poetry)
        if select:
            print(poetry)
            print('[%s,%s] - %s%s' % select)
            print()

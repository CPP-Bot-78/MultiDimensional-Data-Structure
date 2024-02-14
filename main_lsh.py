import os
import string
from random import randint, uniform, sample

from lsh.lsh import lsh
from range_tree import Range_tree as rt
from octree.octree import build_octree, query_octree
from main import create_new_demo, save_results


def experiment(tests: list, tree):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    FOLDERNAME = 'results'
    if not os.path.exists(FOLDERNAME):
        folder_path = os.path.join(script_directory, FOLDERNAME)
        os.makedirs(folder_path)
    os.chdir(FOLDERNAME)
    if os.path.exists('results.txt'):
        demo_name = create_new_demo('results.txt', 1)
    else:
        demo_name = 'results.txt'
    with open(demo_name, 'w') as f:
        f.write("")
    for test in tests:
        surname_range = test[0].split('-')
        min_awards = int(test[1])
        dblp_range = list(map(int, test[2].split('-')))
        education_similarity = float(test[3])


def get_test_set():
    characters = string.ascii_lowercase[:25]
    random_characters = sample(characters, randint(1, len(characters)))
    num_samples = randint(1, len(characters))
    random_characters = sample(characters, num_samples)
    random_characters.sort()
    num_indices = min(2, len(random_characters))
    chars = sample(range(len(random_characters)), num_indices)
    selected_characters = [random_characters[i] for i in chars]
    chars = sorted(selected_characters)
    #chars = sorted(chars)
    char_range = f"{chars[0]}-{chars[1]}"

    test_set = [
        char_range,
        randint(1, 20),
        f'{randint(1, 20)}-{randint(1, 10)*(randint(100, 1000))}',
        uniform(0.01, 1.0)
    ]
    return test_set


for i in range(10):
    print(get_test_set())


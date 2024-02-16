import time
import os
import string
from random import randint, uniform, sample
from demo_old import create_new_demo
from range_tree.Range_tree import build_range_tree, query_range_tree_by_ranges
from octree.octree import build_octree, query_octree
from kdtree.kdtree import build_kdtree, query_kdtree
from r_tree.r_tree import create_rtree, query_rtree_by_range
from lsh.lsh import lsh
import numpy
import matplotlib.pyplot as plt


global TREES
TREES = []
global RESULTS
RESULTS = []
global TEST_SETS
TEST_SETS = []
BUILD_FUNCS = [create_rtree, build_octree, build_kdtree, build_range_tree]
QUERY_FUNCS = [query_rtree_by_range, query_octree, query_kdtree, query_range_tree_by_ranges]

TREE_TIMES = [[], [], [], []]
#  TREE_TIMES[0] = [[build_time1, query_time1], [build_time2, query_time2], ... [build_time10, query_time10]] gia to rtree
#  TREE_TIMES[1] = [[build_time1, query_time1], [build_time2, query_time2]] gia to octree
build_time = []
query_time = []


def save_experiment(trees: list, results: list, test: list):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    FOLDERNAME = 'results'
    FOLDERNAME = os.path.join(script_directory, FOLDERNAME)
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

    for tree in trees:
        tree_results = results[trees.index(tree)]
        with open(demo_name, 'a', encoding='utf-8') as file:
            file.write(f" Found {len(tree_results)} results for {tree.__str__()}:\n")
            file.write(
                f"Given values were: Surname: {test[0]}, "
                f"min Awards: {test[1]}, "
                f"DBLP: {test[2]}, "
                f"Similarity: {test[3]:.2f}\n")
            file.write("Surname: , #Awards: , #DBLP: , Education:\n")
            for item in tree_results:
                if len(tree_results) != 0:
                    file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")
            end_str = '\n' + ('-' * 10) + ('\n' * 2)
            file.write(end_str)


def get_test_set():
    characters = string.ascii_lowercase[:24]
    num_samples = randint(1, len(characters))
    random_characters = sample(characters, num_samples)
    random_characters.sort()
    num_indices = min(2, len(random_characters))
    chars = sample(range(len(random_characters)), num_indices)
    selected_characters = [random_characters[i] for i in chars]
    char_range = sorted(selected_characters)
    if len(char_range) < 2:
        char_range = ['a', 'w']
    test_set = [
        char_range,  # characters list
        randint(1, 20),  # Min Awards
        # f'{randint(1, 20)}-{randint(1, 10)*(randint(100, 1000))}',
        [randint(1, 20), randint(1, 10) * (randint(100, 1000))],  # DBLP Range
        # uniform(0.01, 1.0)  # Similarity Threshold
        uniform(0.4, 0.9)  # Below 0.4 it's no use
    ]
    return test_set


def experiment(build_function, query_function, test_set):
    try:
        start = time.time()
        tree = build_function()
        build_time = time.time() - start
    except Exception:
        start = time.time()
        tree = build_function(test_set[1])
        build_time = time.time() - start
    TREES.append(tree)
    start = time.time()
    query_results = query_function(tree, test_set[0], test_set[1], test_set[2])
    query_time = time.time() - start
    return tree, build_time, query_time, query_results


def main():
    for i in range(10):
        test_set = get_test_set()
        trees = []
        total_results = []
        for j in range(len(BUILD_FUNCS)):
            tree, tree_build_time, tree_query_time, results = experiment(BUILD_FUNCS[j], QUERY_FUNCS[j], test_set)
            TREE_TIMES[j].append([tree_build_time, tree_query_time])
            RESULTS.append(results)
            total_results.append(results)
            trees.append(tree)
        TEST_SETS.append(test_set)
        save_experiment(trees, total_results, test_set)

    for i in range(len(TREE_TIMES)):  # το δεντρο TREE_TIMES[[]]
        for j in range(len(TREE_TIMES[i])):  # η λιστα [build_time1, query_time1]
            build_time.append(TREE_TIMES[i][j][0])  # build_time1
            query_time.append(TREE_TIMES[i][j][1])  # query_time1

    build_avg = numpy.average(build_time)
    query_avg = numpy.average(query_time)


if __name__ == '__main__':
    main()

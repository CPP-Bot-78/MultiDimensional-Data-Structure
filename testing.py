import os
import string
from random import randint, uniform, sample
from lsh.lsh import lsh
from range_tree.Range_tree import build_range_tree, query_range_tree_by_ranges
from octree.octree import build_octree, query_octree
from kdtree.kdtree import build_kdtree, query_kdtree
from r_tree.r_tree import create_rtree, query_rtree_by_range
from main import create_new_demo

TREES = []
BUILD_FUNCS = [create_rtree, build_octree, build_kdtree, build_range_tree]
QUERY_FUNCS = [query_rtree_by_range, query_octree, query_kdtree, query_range_tree_by_ranges]
RESULTS = []


def save_experiment(trees: list, results: list, test: list):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    FOLDERNAME = 'results_lsh'
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
            file.write(f"Results for {tree.__str__()}:\n")
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


def auto_measure_lsh(trees, test):
    for i in range(len(trees)):
        try:
            tree = BUILD_FUNCS[i](test[1])
        except Exception:
            tree = BUILD_FUNCS[i]()
        TREES.append(tree)
        results = QUERY_FUNCS[i](tree, test[0], test[1], test[2])
        RESULTS.append(results)
        print(tree.__str__())
        print(f'Found {len(results)} results with Surname starting from {test[0][0]} to {test[0][1]}, Awards: {test[1]}'
              f' and DBLP from {test[2][0]} to {test[2][1]}')
        threshold = test[3]
        similar_science = lsh(results, test[3])
        while len(similar_science) == 0 and (threshold - 0.1) > 0:
            print(f'No similar for {threshold * 100:.2f} %')
            threshold = threshold / 2
            similar_science = lsh(results, threshold)
        print(similar_science)
        print(f'For similarity above: {threshold * 100:.2f} % the results are: {len(similar_science)}')
        if threshold <= 0:
            print(f'No similar for {test[3] * 100:.2f} %')
        print()
        print(results)
        print((lambda: "-" * 50)())
    save_experiment(TREES, RESULTS, test)


if __name__ == '__main__':
    for i in range(100):
        auto_measure_lsh(BUILD_FUNCS, get_test_set())

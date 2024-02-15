import time
import os
import string
from random import randint, uniform, sample
from main import create_new_demo
from range_tree.Range_tree import build_range_tree, query_range_tree_by_ranges
from octree.octree import build_octree, query_octree
from kdtree.kdtree import build_kdtree, query_kdtree
from r_tree.r_tree import RTree, create_rtree, query_rtree
from lsh.lsh import lsh

global TREES
TREES = []
global RESULTS
RESULTS = []
global TEST_SETS
TEST_SETS = []
BUILD_FUNCS = [create_rtree, build_octree, build_kdtree, build_range_tree]
QUERY_FUNCS = [query_rtree, query_octree, query_kdtree, query_range_tree_by_ranges]


def main():
    for i in range(10):
        test_set = get_test_set()
        for j in range(len(BUILD_FUNCS)):
            built_time, query_time, results = experiment(BUILD_FUNCS[j], QUERY_FUNCS[j], test_set)
        TEST_SETS.append(test_set)
    save_experiment(TREES, RESULTS, TEST_SETS)


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
    query_results = query_function(tree, test_set[0][0], test_set[0][1], test_set[1], test_set[2][0], test_set[2][1])
    query_time = time.time() - start
    RESULTS.append(query_results)

    return build_time, query_time, query_results


if __name__ == '__main__':
    main()


# test = [['g', 'k'], 3, [4, 6309], 0.5]  # fixed test set for now
test = get_test_set()
rangetree = build_range_tree()
octree = build_octree()
r_tree = create_rtree()
kdtree = build_kdtree(test[1])
results = query_rtree(r_tree, test[0][0], test[0][1], test[1], test[2][0], test[2][1])
trees = [rangetree, octree, kdtree, r_tree]

# RangeTree
results = query_range_tree_by_ranges(rangetree, test[0], test[1], test[2])
# print(f'Surname: {test[0]}, Awards: {test[1]}, DBLP: {test[2]}')
print(rangetree.__str__())
print(results)
print()
print(f'Found {len(results)} results with Surname starting from {test[0][0]} to {test[0][1]}, Awards: {test[1]} '
      f'and DBLP from {test[2][0]} to {test[2][1]}')
print((lambda: "-" * 50)())
similar_science = lsh(results, test[3])
if len(similar_science) == 0:
    print('No similar')
    new_threshold = test[3]/2
    similar_science = lsh(results, new_threshold)
    print(similar_science)
    print(f'For new similarity above:{new_threshold * 100:.2f}% found: {len(similar_science)} results')
else:
    print(similar_science)
    print(f'For similarity above:{test[3] * 100:.2f}% the results are: {len(similar_science)}')
print((lambda: "*" * 150)())
print()

# Octree
results = query_octree(octree, test[0], test[1], test[2])
# print(f'Surname: {test[0]}, Awards: {test[1]}, DBLP: {test[2]}')
print(octree.__str__())
print(results)
print()
print(f'Found {len(results)} results with Surname starting from {test[0][0]} to {test[0][1]}, Awards: {test[1]} '
      f'and DBLP from {test[2][0]} to {test[2][1]}')
print((lambda: "-" * 50)())
similar_science = lsh(results, test[3])
if len(similar_science) == 0:
    print('No similar')
    new_threshold = test[3]/2
    similar_science = lsh(results, new_threshold)
    print(similar_science)
    print(f'For new similarity above:{new_threshold * 100:.2f}% found: {len(similar_science)} results')
else:
    print(similar_science)
    print(f'For similarity above:{test[3] * 100:.2f}% the results are: {len(similar_science)}')

save_experiment(TREES, RESULTS, test)


def save_experiment(trees:list, results: list, test: list):
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
        with open(demo_name, 'a', encoding='utf-8') as file:
            file.write(f"Results for {tree.__str__()}:\n")
            file.write(
                f"Given values were: Surname: {test[0]}, "
                f"min Awards: {test[1]}, "
                f"DBLP: {test[2]}, "
                f"Similarity:{test[3]:.2f}\n")
            file.write("Surname: , #Awards: , #DBLP: , Education:\n")
            for item in results:
                if len(results) != 0:
                    file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")
            end_str = '\n' + ('-' * 10) + ('\n' * 2)
            file.write(end_str)


def get_test_set():
    characters = string.ascii_lowercase[:25]
    # random_characters = sample(characters, randint(1, len(characters)))
    num_samples = randint(1, len(characters))
    random_characters = sample(characters, num_samples)
    random_characters.sort()
    num_indices = min(2, len(random_characters))
    chars = sample(range(len(random_characters)), num_indices)
    selected_characters = [random_characters[i] for i in chars]
    char_range = sorted(selected_characters)
    # char_range = f"{chars[0]}-{chars[1]}"

    test_set = [
        char_range,  # characters list
        randint(1, 20),  # Min Awards
        # f'{randint(1, 20)}-{randint(1, 10)*(randint(100, 1000))}',
        [randint(1, 20), randint(1, 10) * (randint(100, 1000))],  # DBLP Range
        uniform(0.01, 1.0)  # Similarity Threshold
    ]
    return test_set

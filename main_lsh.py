import os
import string
from random import randint, uniform, sample

from lsh.lsh import lsh
from range_tree import Range_tree as rt
from octree.octree import build_octree, query_octree
from main import create_new_demo, save_results


def save_experiment(tree, results: list, test: list):
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
    random_characters = sample(characters, randint(1, len(characters)))
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


# Tree
tree = rt.build_range_tree()
test = get_test_set()
results = rt.query_range_tree_by_ranges(tree, test[0], test[1], test[2])
# print(f'Surname: {test[0]}, Awards: {test[1]}, DBLP: {test[2]}')
print(results)
print()
print(f'Found {len(results)} results with Surname starting from {test[0][0]} to {test[0][1]}, Awards: {test[1]} '
      f'and DBLP from {test[2][0]} to {test[2][1]}')
print((lambda: "=" * 100)())
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
save_experiment(tree, results, test)

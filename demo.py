# proxeirh main poy kalei to kdtree.py kai kanei write ta apotelesmata se pinaka sto results.txt
# mazi me ton xrono poy xreiastike to kdtree.py
import os
import pandas as pd
import time
from kdtree.kdtree import KdTree, convert_to_list, load_scientist_data
from range_tree import Range_tree as rangetree
from octree.octree import build_octree, query_octree
from r_tree.r_tree import create_rtree, query_rtree
from lsh.lsh import lsh


def create_new_demo(filename, count):
    filename, extension = os.path.splitext(filename)
    count += 1
    while filename[-1].isdigit():
        filename = filename[:-1]
    new_filename = f"{filename}{count}{extension}"
    if count == 50:
        return f"{filename}_50{extension}"
    if os.path.exists(new_filename):

        return create_new_demo(new_filename, count)
    else:
        return new_filename


def main():
    # Get user input for the range criteria
    try:
        surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
        min_awards = int(input("Enter the minimum #Awards: "))
        dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))
        lsh_threshold = float(input("Enter the similarity threshold as float (e.g., 0.5): "))
        data = [surname_range, min_awards, dblp_range, lsh_threshold]
    except Exception:
        print("Please enter an acceptable value")
        surname_range = dblp_range = ['a', 'w']
        min_awards = 0
        lsh_threshold = 0.5
        data = []  # just to stop the weak warning signs
        main()
    # create txt file or clean it
    script_directory = os.path.dirname(os.path.abspath(__file__))
    FOLDERNAME = 'results'
    if not os.path.exists(FOLDERNAME):
        folder_path = os.path.join(script_directory, FOLDERNAME)
        try:
            os.makedirs(folder_path)
        except Exception:
            if os.path.isdir(folder_path):
                pass
    os.chdir(FOLDERNAME)
    if os.path.exists('results.txt'):
        demo_name = create_new_demo('results.txt', 1)
    else:
        demo_name = 'results.txt'
    with open(demo_name, 'w') as f:
        f.write("")

    scientist_data = load_scientist_data()
    kdstart_time = time.time()
    kdtree = KdTree(scientist_data, min_awards=min_awards)  # Pass min_awards to KdTree constructor
    kdtree_build_time = time.time() - kdstart_time
    kdstart_time_range_query = time.time()
    results_kdtree = kdtree.range_query2(kdtree.root, [], surname_range, dblp_range)
    kdrange_query_time = time.time() - kdstart_time_range_query
    kdtree_lsh = lsh(results_kdtree, lsh_threshold)
    save_results(kdtree, kdtree_build_time, kdrange_query_time, results_kdtree, demo_name, data, len(kdtree_lsh))

    range_start_time = time.time()
    range_tree = rangetree.build_range_tree()
    range_build_time = time.time() - range_start_time
    range_time_range_query = time.time()
    results_range_tree = rangetree.query_range_tree_by_ranges(range_tree, surname_range, min_awards, dblp_range)
    range_query_time = time.time() - range_time_range_query
    rangetree_lsh = lsh(results_range_tree, lsh_threshold)
    save_results(range_tree, range_build_time, range_query_time, results_range_tree, demo_name, data, len(rangetree_lsh))

    octree_start_time = time.time()
    octree = build_octree()
    octree_build_time = time.time() - octree_start_time
    octree_time_range_query = time.time()
    results_octree = query_octree(octree, surname_range, min_awards, dblp_range)
    octree_query_time = time.time() - octree_time_range_query
    octree_lsh = lsh(results_octree, lsh_threshold)
    save_results(octree, octree_build_time, octree_query_time, results_octree, demo_name, data, len(octree_lsh))

    rtree_start_time = time.time()
    r_tree = create_rtree()
    rtree_build_time = time.time() - rtree_start_time
    rtree_time_range_query = time.time()
    results_rtree = query_rtree(r_tree, surname_range[0], surname_range[1], min_awards, dblp_range[0], dblp_range[1])
    rtree_query_time = time.time() - rtree_time_range_query
    rtree_lsh = lsh(results_rtree, lsh_threshold)
    save_results(r_tree, rtree_build_time, rtree_query_time, results_rtree, demo_name, data, len(rtree_lsh))

    print(f"Results written in {demo_name}")


def save_results(tree, tree_build_time, query_time, results, demo_name, given_data, lsh_count):
    with open(demo_name, 'a', encoding='utf-8') as file:
        file.write(f"Found {len(results)} results for {tree.__str__()}:\n")
        file.write(
                f"Given values were: Surname: {given_data[0]}, "
                f"min Awards: {given_data[1]}, "
                f"DBLP: {given_data[2]}, "
                f"Similarity:{given_data[3]:.2f}\n")
        file.write(f"Construction Time: {tree_build_time} seconds\n")
        file.write(f"Range Query Time: {query_time} seconds\n")
        file.write(f'Found {lsh_count} of similar education above {given_data[3]:.2f}\n')
        file.write("Surname: , #Awards: , #DBLP: , Education:\n")
        for item in results:
            file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")
        end_str = '\n' + ('-' * 10) + ('\n' * 2)
        file.write(end_str)


if __name__ == "__main__":
    main()

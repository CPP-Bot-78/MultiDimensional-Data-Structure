# proxeirh main poy kalei to kdtree.py kai kanei write ta apotelesmata se pinaka sto results.txt
# mazi me ton xrono poy xreiastike to kdtree.py
import os
import pandas as pd
import time
from kdtree.kdtree import KdTree, convert_to_list, load_scientist_data
from range_tree import Range_tree as rt
from octree.octree import build_octree, query_octree


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
    # create txt file or clean it
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

    # Get user input for the range criteria
    surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
    # Ask for the minimum awards instead of a range
    min_awards = int(input("Enter the minimum #Awards: "))
    dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))

    
    # Load scientist data
    scientist_data = load_scientist_data()

    # Load k-d tree from kdtree.py
    kdstart_time = time.time()
    kdtree = KdTree(scientist_data, min_awards=min_awards)  # Pass min_awards to KdTree constructor
    kdtree_time = time.time() - kdstart_time
    # Generate result list once
    result_list = []
    kdtree.range_query(kdtree.root, result_list, surname_range, dblp_range)
    # Start timer for range query
    kdstart_time_range_query = time.time()
    kdtree.range_query(kdtree.root, result_list, surname_range, dblp_range)  # Adjust the call to range_query
    kdrange_query_time = time.time() - kdstart_time_range_query
    # Perform range query and save results for KD-Tree
    result_kdtree = result_list
    kdtree.range_query(kdtree.root, result_list, surname_range, dblp_range)
    save_results('KDTree', kdtree_time, kdrange_query_time, result_kdtree, demo_name)

    range_start_time = time.time()
    range_tree = rt.build_range_tree()
    range_build_time = time.time() - range_start_time
    range_time_range_query = time.time()
    results = rt.query_range_tree_by_ranges(range_tree, surname_range, min_awards, dblp_range)
    range_query_time = time.time() - range_time_range_query
    save_results('Range Tree', range_build_time, range_query_time, results, demo_name)

    octree_start_time = time.time()
    octree = build_octree()
    octree_build_time = time.time() - octree_start_time
    octree_time_range_query = time.time()
    results = query_octree(octree, surname_range, min_awards, dblp_range)
    octree_query_time = time.time() - octree_time_range_query
    save_results('Oct Tree', octree_build_time, octree_query_time, results, demo_name)

    print(f"Results written in {demo_name}")


def save_results(tree, tree_build_time, query_time, results, demo_name):
    with open(demo_name, 'a', encoding='utf-8') as file:
        file.write(f"Results for {tree}:\n")
        file.write(f"Construction Time: {tree_build_time} seconds\n")
        file.write(f"Range Query Time: {query_time} seconds\n")
        file.write("Surname: , #Awards: , #DBLP: , Education:\n")
        for item in results:
            file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")
        end_str = '\n' + ('-' * 10) + ('\n' * 2)
        file.write(end_str)
    # print(f"Results written in {demo_name}")


if __name__ == "__main__":
    main()

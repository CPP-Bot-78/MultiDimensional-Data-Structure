import pandas as pd
import time
from r_tree import R_tree as r_t


def main():
    # Get user input for the range criteria
    surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
    
    # Ask for the minimum awards instead of a range
    min_awards = int(input("Enter the minimum #Awards: "))
    
    dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))
    print("Results written in results_rtree.txt")

    rtree_start_time = time.time()
    rtree_tree = r_t.create_rtree()
    rtree_build_time = time.time() - rtree_start_time

    rtree_time_range_query = time.time()
    results = r_t.query_rtree(rtree_tree, surname_range[0], surname_range[1], min_awards, dblp_range[0], dblp_range[1])
    rtree_query_time = time.time() - rtree_time_range_query
    save_results('R-Tree', rtree_build_time, rtree_query_time, results)


def save_results(tree, tree_build_time, query_time, results):
    with open('results_rtree.txt', 'a', encoding='utf-8') as file:
        file.write(f"Results for {tree}:\n")
        file.write(f"Construction Time: {tree_build_time} seconds\n")
        file.write(f"Range Query Time: {query_time} seconds\n")
        file.write("Surname: , #Awards: , #DBLP: , Education:\n")
        for item in results:
            file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")
        end_str = '\n' + ('-' * 10) + '\n'
        file.write(end_str)


if __name__ == "__main__":
    main()


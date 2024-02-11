#proxeirh main poy kalei to kdtree.py kai kanei write ta apotelesmata se pinaka sto results.txt
#mazi me ton xrono poy xreiastike to kdtree.py
import pandas as pd
import time
from kdtree import KdTree, convert_to_list, load_scientist_data

def main():
    # Get user input for the range criteria
    surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
    
    # Ask for the minimum awards instead of a range
    min_awards = int(input("Enter the minimum #Awards: "))
    
    dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))
    print("Results written in results.txt")
    
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

    # Save results to file
    with open('results.txt', 'w') as file:
        file.write("Results for KD-Tree:\n")
        file.write(f"Construction Time: {kdtree_time} seconds\n")
        file.write(f"Range Query Time: {kdrange_query_time} seconds\n")
        file.write("Surname: , #Awards: , #DBLP: , Education:\n")
        for item in result_kdtree:
            file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")

if __name__ == "__main__":
    main()

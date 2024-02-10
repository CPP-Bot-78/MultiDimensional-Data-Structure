#proxeirh main poy kalei to rtree.py kai kanei write ta apotelesmata se pinaka sto results.txt
#mazi me ton xrono poy xreiastike to rtree.py
import pandas as pd
import time
from r_tree import rtree, create_rtree

def main():
    # Get user input for the range criteria
    surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
    awards_range = list(map(int, input("Enter the range for #Awards (e.g., 0-5): ").split('-')))
    dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))
    print("Results written in results.txt")

    # Load k-d tree from rtree.py
    start_time = time.time()
    created_rtree = create_rtree("./computer_scientists_data1.csv")
    rtree_time = time.time() - start_time

    result_rtree = rtree.query_rtree(created_rtree, surname_range[0], awards_range[0], dblp_range[0], dblp_range[1], awards_range[1], surname_range[1])

    # Start timer for range query
    start_time_range_query = time.time()
    rtree.query_rtree(created_rtree, surname_range[0], awards_range[0], dblp_range[0], dblp_range[1], awards_range[1], surname_range[1])
    range_query_time = time.time() - start_time_range_query

    # Save results to file
    with open('results.txt', 'w') as file:
        file.write("Results for R-Tree:\n")
        file.write(f"Construction Time: {rtree_time} seconds\n")
        file.write(f"Range Query Time: {range_query_time} seconds\n")
        file.write("Surname: , #Awards: , #DBLP: , Education:\n")
        for item in result_rtree:
            file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")

if __name__ == "__main__":
    main()


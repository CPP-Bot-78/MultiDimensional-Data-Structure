#proxeirh main poy kalei to kdtree.py k kanei write ta apotelesmata se pinaka sto results.txt
#mazi me ton xrono poy xreiastike to kdtree.py
import pandas as pd
import time
from kdtree import KdTree, convert_to_list

def load_scientist_data():
    data = pd.read_csv('computer_scientists_data.csv')
    scientist_data = [
        (row['Surname'], (row['#Awards'],), convert_to_list(row['DBLP']), [val.strip(" '") for val in str(row['Education'])[1:-1].split(', ')]
         if pd.notna(row['Education']) and str(row['Education']).startswith('[')
         else [row['Education']])
        for _, row in data.iterrows()
    ]
    return scientist_data

def main():
    # Get user input for the range criteria
    surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
    awards_range = list(map(int, input("Enter the range for #Awards (e.g., 0-5): ").split('-')))
    dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))
    print("Results written in results.txt")
    # Load scientist data
    scientist_data = load_scientist_data()

    # Load k-d tree from kdtree.py
    start_time = time.time()
    kdtree = KdTree(scientist_data)
    kdtree_time = time.time() - start_time

    # Generate result list once
    result_list = []
    kdtree.range_query(kdtree.root, result_list, surname_range, awards_range, dblp_range)

    # Perform range query and save results for KD-Tree
    result_kdtree = result_list

    # Save results to file
    with open('results.txt', 'w') as file:
        file.write("Results for KD-Tree:\n")
        file.write(f"Construction Time: {kdtree_time} seconds\n")
        file.write("Surname: , #Awards: , #DBLP: , Education:\n")
        for item in result_kdtree:
            file.write(f"{item[0]}, {item[1]}, {item[2]}, {item[3]}\n")

if __name__ == "__main__":
    main()

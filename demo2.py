from testing import auto_testing, test_trees, get_test_set
import os
from demo import create_new_demo


def user_input():
    try:
        surname_range = input("Enter the range for Surname (e.g., A-E): ").upper().split('-')
        min_awards = int(input("Enter the minimum #Awards: "))
        dblp_range = list(map(int, input("Enter the range for #DBLP (e.g., 0-100): ").split('-')))
        lsh_threshold = float(input("Enter the similarity threshold as float (e.g., 0.5): "))
        data = [surname_range, min_awards, dblp_range, lsh_threshold]
        return data  # surname_range, min_awards, lsh_threshold, data
    except Exception:
        print("Please enter an acceptable value")
        user_input()


def main():
    choice = int(input('Αν θέλετε να τρέξουν πολλά τέστ εισάγετε 0. Αλλιώς οποιοδήποτε άλλο αριθμό\n'))
    if choice == 0:
        iterations = int(input('Εισάγετε τον αριθμό των test που θέλετε ως ακέραιο\n'))
        test_trees(iterations)
    else:
        data = user_input()
        test_trees(1, data)


if __name__ == '__main__':
    main()
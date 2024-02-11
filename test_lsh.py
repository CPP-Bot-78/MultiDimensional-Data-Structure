from range_tree import *
from range_tree import Range_tree as rt
from lsh import lsh as lshm

# Tree
tree = rt.build_range_tree()
results = rt.query_range_tree(tree, "a", "w", 5, 0, 10)
print(results)
# Lsh
similarity_percentage = input("Give the similarity percentage as a float between 0 and 1: ")
similarity_float = float(similarity_percentage)
# Create a list of names and education data to pass to lsh
similar_science = lshm.lsh(results, similarity_float)
print(similar_science)
# remove duplicates #TODO
# unique_pairs = set()
unique_list = []
for sc in similar_science:
    # If the item is not already in the unique_list, add it
    if sc not in unique_list:
        unique_list.append(sc)

print(unique_list)

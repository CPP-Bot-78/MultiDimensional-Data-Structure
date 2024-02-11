from range_tree import Range_tree as rt
import pprint as pp

tree = rt.build_range_tree()
results = rt.query_range_tree(tree, "a", "w", 1, 2, 4)
pp.pprint(results)
# print(results)
print((lambda: "=" * 50)())
results = rt.query_range_tree(tree, "a", "w", 2, 0, 10)
pp.pprint(results, width=-1)
print((lambda: "=" * 50)())
results = rt.query_range_tree(tree, "a", "w", 1, 0, 4)
pp.pprint(results)
'''
pp.pprint(results)
print((lambda: "=" * 50)())
query_results = []
tree.query(tree.root,  , 'w', 0, 2, 0, 5, query_results)
print(query_results)
query_results = []
tree.query(tree.root, 'a', 'w', 0, 2, 0, 10, query_results)
print(query_results)
query_results = []
tree.query(tree.root, 'a', 'w', 10, 15, 30, 180, query_results)
print(query_results)'''

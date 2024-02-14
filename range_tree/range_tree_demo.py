from range_tree import Range_tree as rt

tree = rt.build_range_tree()
print(tree.__str__())
results = rt.query_range_tree(tree, "a", "w", 1, 2, 4)
print(results)
print((lambda: "=" * 50)())
results = rt.query_range_tree(tree, "a", "w", 2, 0, 10)
print(results)
print((lambda: "=" * 50)())
results = rt.query_range_tree(tree, "p", "w", 1, 0, 4)
print(results)

'''
pp.pprint(results)
print((lambda: "=" * 50)())
query_results = []
tree.query(tree.root, 15, 16, 0, 2, 0, 5, query_results)
print(query_results)
query_results = []
tree.query(tree.root, 'a', 'w', 0, 2, 0, 10, query_results)
print(query_results)
query_results = []
tree.query(tree.root, 'a', 'w', 10, 15, 30, 180, query_results)
print(query_results)
'''
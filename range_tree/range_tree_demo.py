from range_tree import Range_tree as rt

tree = rt.build_range_tree()
print(tree.__str__())
results = rt.query_range_tree(tree, "a", "w", 1, 2, 4)
print(f'Found {len(results)} results:\n{results}')
print((lambda: "=" * 50)())
results = rt.query_range_tree(tree, "a", "w", 5, 0, 100)
print(f'Found {len(results)} results:\n{results}')
print((lambda: "=" * 50)())
results = rt.query_range_tree(tree, "k", "w", 1, 100, 400)
print(f'Found {len(results)} results:\n{results}')

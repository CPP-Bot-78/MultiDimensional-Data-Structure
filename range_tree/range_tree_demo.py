from range_tree import Range_tree as rt
import pprint as pp

tree = rt.build_range_tree()
results = rt.query_range_tree(tree, "C", "y", 1)
pp.pprint(results)
print((lambda: "=" * 50)())
print((lambda: "=" * 50)())
tree = rt.build_range_tree()
results = rt.query_range_tree(tree, "m", "T", 5)
pp.pprint(results)

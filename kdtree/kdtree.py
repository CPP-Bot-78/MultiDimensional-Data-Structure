import pandas as pd

class KDNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class KdTree:
    def __init__(self, points, depth=0):
        if not points:
            self.root = None
        else:
            k = len(points[0][1]) if isinstance(points[0][1], (list, tuple)) else 1
            axis = depth % k
            points.sort(key=lambda x: x[1][axis] if isinstance(x[1], (list, tuple)) else x[1])
            median = len(points) // 2
            self.root = KDNode(points[median])
            self.root.left = KdTree(points[:median], depth + 1).root
            self.root.right = KdTree(points[median + 1:], depth + 1).root

    def range_query(self, node, results, surname_range, awards_range, dblp_range):
        if node is not None:
            if surname_range[0] <= node.data[0][0].upper() <= surname_range[1] and awards_range[0] <= node.data[1][0] <= awards_range[1] and dblp_range[0] <= int(node.data[2][0]) <= dblp_range[1]:
                results.append(node.data)

            self.range_query(node.left, results, surname_range, awards_range, dblp_range)
            self.range_query(node.right, results, surname_range, awards_range, dblp_range)

def convert_to_list(value):
    return [int(val) for val in str(value)[1:-1].split(', ')] if pd.notna(value) and str(value).startswith('[') else [int(value)]

import pandas as pd
import os

class KDNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

class KdTree:
    def __init__(self, points, depth=0, min_awards=0):
        if not points:
            self.root = None
        else:
            k = len(points[0][1]) if isinstance(points[0][1], (list, tuple)) else 1
            axis = depth % k
            points.sort(key=lambda x: x[1][axis] if isinstance(x[1], (list, tuple)) else x[1])
            median = len(points) // 2
            self.root = KDNode(points[median])
            self.root.left = KdTree(points[:median], depth + 1, min_awards).root
            self.root.right = KdTree(points[median + 1:], depth + 1, min_awards).root
            self.min_awards = min_awards

    def __str__(self):
        return "KDTree"

    def range_query(self, node, results, surname_range, dblp_range):
        if node is not None:
          duplicate = any(
            node.data[0].upper() == result[0].upper()
            and node.data[1] == result[1]
            and node.data[2] == result[2]
            for result in results
          )

          if not duplicate:
            if (
                surname_range[0] <= node.data[0][0].upper() <= surname_range[1]
                and self.min_awards <= node.data[1]
                and dblp_range[0] <= node.data[2] <= dblp_range[1]
            ):
              	results.append(node.data)
          if node.left is not None:
              self.range_query(node.left, results, surname_range, dblp_range)
          if node.right is not None:
              self.range_query(node.right, results, surname_range, dblp_range)

    def range_query2(self, node, results, surname_range, dblp_range):
        results = results
        if node is not None:
            if (
                surname_range[0].upper() <= node.data[0][0].upper() <= surname_range[1].upper()
                and self.min_awards <= node.data[1]
                and dblp_range[0] <= node.data[2] <= dblp_range[1]
            ):
                results.append(node.data)
            if node.left is not None:
                self.range_query2(node.left, results, surname_range, dblp_range)
            if node.right is not None:
                self.range_query2(node.right, results, surname_range, dblp_range)
        if len(results) == 0:
            return results
        unique_sc = []
        seen = []
        for item in results:
            name = item[0]
            if name not in seen:
                seen.append(name)
                unique_sc.append(item)
        return sorted(unique_sc, key=lambda x: x[0], reverse=False)


def build_kdtree(min_awards: int):
    scientist_data = load_scientist_data()
    kdtree = KdTree(scientist_data, min_awards=min_awards)
    return kdtree


def query_kdtree(kdtree, surname_range, awards, dblp_range):  # , surname_1, surname_2, awards, min_dblp, max_dblp):
    results = []
    # surname_range = [surname_1, surname_2]
    # dblp_range = [min_dblp, max_dblp]
    query_results = kdtree.range_query2(
        kdtree.root,
        results,
        surname_range,
        dblp_range
    )
    return query_results


def load_scientist_data():
    try:
        data = pd.read_csv('computer_scientists_data2.csv')
    except Exception as e:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        home_dir = os.path.dirname(script_directory)
        CSV_PATH = os.path.join(home_dir, 'computer_scientists_data2.csv')
        data = pd.read_csv(CSV_PATH)
    # data = pd.read_csv('computer_scientists_data2.csv')
    scientist_data = [
        #(row['Surname'], int(row['#Awards'],), int(row['DBLP']), [val.strip(" '") for val in str(row['Education'])[1:-1].split(', ')]
        (row['Surname'], int(row['#Awards'], ), int(row['DBLP']), str(row['Education'])
         if pd.notna(row['Education']) and str(row['Education']).startswith('[')
         else [row['Education']])
        for _, row in data.iterrows()
    ]
    return scientist_data

def convert_to_list(value):
    return [int(val) for val in str(value)[1:-1].split(', ')] if pd.notna(value) and str(value).startswith('[') else [int(value)]


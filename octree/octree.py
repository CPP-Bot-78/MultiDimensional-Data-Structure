import pandas as pd
from memory_profiler import profile

# An octree works just like a quadtree, just for 3 dimensions.
# It splits a 3D space (cube) into 8 octants (smaller cubes) and inserts data based on the datapoints coordinates 
# Using median to evenly distribute data to each octant

# Initialise the leaf threshold for when to split a child octant
LEAF_TRESHOLD = 50

# The class Octant describes each node of the octree
class Octant:
    def __init__(self, x_bounds, y_bounds, z_bounds, leaf_node):
        # x, y and z bounds are the ranges of each octant to show which values belong in them
        # When leaf_node is True you can store data inside(Child), when it's false it has 8 octants inside(Parent)
        # Medians of each octant for determining the bounds of each child
        # Data stores the values of each octant
        # Each parent node has 8 children
        self.x_bounds = x_bounds
        self.y_bounds = y_bounds
        self.z_bounds = z_bounds
        self.leaf_node = leaf_node
        self.medians = []
        self.data = []
        self.children = [None] * 8

# The class Octree contains all the needed functions and uses the octant class
class Octree:
    def __init__(self, x_bounds, y_bounds, z_bounds, leaf_node):
        self.root = Octant(x_bounds, y_bounds, z_bounds, leaf_node)     


    def split_octant(self, octant):
        # Calculate and store median for each variable to determine in which octant the data goes in
        x_list, y_list, z_list = split_list(octant.data)
        x_median = find_median(x_list)
        y_median = find_median(y_list)
        z_median = find_median(z_list)
        octant.medians = [x_median, y_median, z_median]

        # Split the Parent octant into 8 children
        # The split works with a 3-bit binary logic where 0=min,median and 1=median,max [000,001,010,011,100,101,110,111]
        octant.children[0] = Octant((octant.x_bounds[0], x_median), (octant.y_bounds[0], y_median),(octant.z_bounds[0], z_median), True)
        octant.children[1] = Octant((octant.x_bounds[0], x_median), (octant.y_bounds[0], y_median),(z_median, octant.z_bounds[1]), True)
        octant.children[2] = Octant((octant.x_bounds[0], x_median), (y_median, octant.y_bounds[1]),(octant.z_bounds[0], z_median), True)
        octant.children[3] = Octant((octant.x_bounds[0], x_median), (y_median, octant.y_bounds[1]),(z_median, octant.z_bounds[1]), True)
        octant.children[4] = Octant((x_median, octant.x_bounds[1]), (octant.y_bounds[0], y_median),(octant.z_bounds[0], z_median), True)
        octant.children[5] = Octant((x_median, octant.x_bounds[1]), (octant.y_bounds[0], y_median),(z_median, octant.z_bounds[1]), True)
        octant.children[6] = Octant((x_median, octant.x_bounds[1]), (y_median, octant.y_bounds[1]),(octant.z_bounds[0], z_median), True)
        octant.children[7] = Octant((x_median, octant.x_bounds[1]), (y_median, octant.y_bounds[1]),(z_median, octant.z_bounds[1]), True)


    def find_child_index(self, datapoint, octant):
        # Finds which of the 8 children contains the datapoint
        # Same logic as the split_octant function, it adds to the variable child the corresponding number to determine where it belongs
        # For example: If x is smaller than the median it belongs in the first 4 children
        # If y is smaller than the median it belongs to childrens 0,1,4,5
        # If z is bigger that the median it belongs to the odd numbered children
        index, x, y, z = datapoint
        x_median, y_median, z_median = octant.medians
        child = 0
        
        if x > x_median:
                child += 4
        if y > y_median:
                child += 2
        if z > z_median:
                child += 1

        return child


    def insert(self, datapoint, octant=None):
        # The insert function places the datapoint to the right octant
        # If we are at a leaf_node it appends the data.
        # If we reached the LEAF_TRESHOLD we split the octant and insert the data into the created children
        # If we are at a Parent node we find the right child and call the insert function again to enter the value
        if octant is None:
            octant = self.root

        if octant.leaf_node:
            octant.data.append(datapoint)

            # If we reached the leaf threshold
            if len(octant.data) == LEAF_TRESHOLD:
                octant.leaf_node = False
                self.split_octant(octant)

                # Recursively insert into the child
                for data in octant.data:
                    child = self.find_child_index(data, octant)
                    self.insert(data, octant.children[child])
                octant.data = []

            return

        # Find the correct child index
        child = self.find_child_index(datapoint, octant)
        # Try to insert in that child
        self.insert(datapoint, octant.children[child])
    
    
    def search(self, search_bounds, octant=None):
        # The search funtion first checks if our search_bounds intersect with the octant's bounds
        # This lowers repetition by not checking outside the search_bounds box
        # If it is inside the box and the octant is a leaf_node find the datapoints
        # If not a leaf_node recursively search in its children
        x_min, x_max, y_min, y_max, z_min, z_max = search_bounds
        found = []

        if octant is None:
            octant = self.root

        # Check if the search box intersects with the octant's bounds
        if (
            x_max < octant.x_bounds[0] or x_min > octant.x_bounds[1] or
            y_max < octant.y_bounds[0] or y_min > octant.y_bounds[1] or
            z_max < octant.z_bounds[0] or z_min > octant.z_bounds[1]
        ):
            # No intersection, return
            return found

        # Check if the octant is a leaf node and search for data points
        if octant.leaf_node:
            for data_point in octant.data:
                x, y, z = data_point[1:]
                if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
                    found.append(data_point[0])
        else:
            # Recursively search in child octants
            for child in octant.children:
                found.extend(self.search(search_bounds, child))

        return found

    

def find_median(my_list):
    #Finds the median of a list
    sort = sorted(my_list)
    length = len(my_list)
    
    #If the length is even, find the average of the middle values
    if length % 2 ==0:
        median1 = sort[(length // 2) - 1]
        median2 = sort[length // 2]
        median = (median1 + median2) // 2
    #If the length is odd, the median is the middle value
    else:
        median= sort[length // 2]
    
    return median


def split_list(my_list):
    #Splits a list into 3 lists, one for each coordinate(x,y,z) 
    x = [point[1] for point in my_list]
    y = [point[2] for point in my_list]
    z = [point[3] for point in my_list]

    return x, y, z


def extract_data(file_csv):
    # Extract the data from our csv and return 4 lists
    df = pd.read_csv(file_csv)
    
    # Convert alphabetical letters into integers[A=0,B=1,C=2...]
    df['Surname'] = df['Surname'].apply(lambda x: ord(x[0].lower()) - 97)

    index_list = df['Index'].tolist()
    surname_list = df['Surname'].tolist()
    awards_list = df['#Awards'].tolist()
    dblp_list = df['DBLP'].tolist()
    
    return index_list, surname_list, awards_list, dblp_list

#@profile
def build_octree():
    #Construct the Octree and insert the data
    csv_file = 'scripts/computer_scientists_data1.csv'
    index, surname, awards, dblp = extract_data(csv_file)
    cs_data = list(zip(index, surname, awards, dblp))

    ot = Octree([min(surname),max(surname)], [min(awards),max(awards)], [min(dblp),max(dblp)], False)
    #Initialize root
    ot.root.data = cs_data
    ot.split_octant(ot.root)
    #Insert datapoints
    for datapoint in cs_data:
        ot.insert(datapoint)

    return ot

#@profile
def query_octree(octree, x_range, y_min, z_range):
    df = pd.read_csv('scripts/computer_scientists_data1.csv')
    y_max = df['#Awards'].max()
    y_range = [y_min, y_max]
    x_range = [ord(letter.lower()) - 97 for letter in x_range]
    # Search the octree for the given ranges using a bounding box
    search_bounds = (x_range[0], x_range[1], y_range[0], y_range[1], z_range[0], z_range[1])
    found = octree.search(search_bounds)

    # Create one list with the indexes found
    index_list = pd.Series(found).explode().tolist()

    # Find values based on the index
    filter_by_index = df.loc[index_list]
    result = filter_by_index[['Surname', '#Awards', 'Education', 'DBLP']].values.tolist()

    return result


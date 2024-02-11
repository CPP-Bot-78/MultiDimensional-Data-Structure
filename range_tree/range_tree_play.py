from range_tree import Range_tree as rt
import pprint as pp

tree = rt.build_range_tree()
print('0-> Έξοδος')
print('1-> Αναζήτηση')
choice = input('->Παρακαλώ επιλέξτε λειτουργία.')
while choice != '0':
    surname_first = input('Το εύρος ονομάτων θα ξεκινάει από το γράμμα:').lower()
    surname_last = input('Το εύρος ονομάτων θα τελειώνει από το γράμμα:').lower()
    awards_threshold = int(input('Ο ελάχιστος αριθμός των βραβείων που θα έχει:'))
    dblp_min = int(input('Το εύρος των DBLP θα είναι τουλάχιστον:'))
    dblp_max = int(input('Το εύρος των DBLP θα είναι το πολύ:'))
    results = rt.query_range_tree(tree, surname_first, surname_last, awards_threshold, dblp_min, dblp_max)
    pp.pprint(results)


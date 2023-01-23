import random

def random_subsets(lst, num_item):
    random.shuffle(lst)
    subsets_container = []
    while bool(len(lst)):
        if len(lst) >= num_item:
            subset = [lst.pop() for i in range(num_item)]
            subsets_container.append(subset)
        elif len(lst) > 1:
            subsets_container.append(lst)
            break
    return subsets_container
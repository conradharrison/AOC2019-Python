import math

object_map = (None, []) # list of nodes: [node]; Each node is a tuple: (name, [node])

def search_map(map, object):
    (map_c, map_o) = map
    if map_o == []:
        return map
    else:
        for (c, o) in map_o:
            if c==object:
                return map
        for submap in map_o:
            (center, orbiters) = search_map(submap, object)
            if orbiters == []:
                continue
            else:
                return (center, orbiters)
        return (None, [])

def search_map_and_insert(center, orbiter):
    global object_map
    new_orbiter = (orbiter, [])
    (_, result_center_list) = search_map(object_map, center)
    (_, result_orbiter_list) = search_map(object_map, orbiter)
    if result_orbiter_list == []:
        insert_orbiter = new_orbiter
    else:
        insert_orbiter = [(c, o) for (c, o) in result_orbiter_list if c==orbiter][0]
        result_orbiter_list.remove(insert_orbiter)
    if result_center_list == []:
        new_center = (center, [insert_orbiter])
        object_map[1].append(new_center)
    else:
        insert_center = [(c, o) for (c, o) in result_center_list if c==center][0]
        result_center_list.remove(insert_center)
        insert_center[1].append(insert_orbiter)
        result_center_list.append((insert_center[0], insert_center[1]))

def orbit_count(map, my_orbits):
    (map_c, map_o) = map
    if map_o == []:
        return my_orbits
    else:
        sum = 0
        for (c, o) in map_o:
            sub_count = orbit_count((c, o), my_orbits+1)
            sum = sum + sub_count
        sum = sum + (0 if my_orbits == -1 else my_orbits)
        return sum

f = open("6.txt", "r")
lines = f.readlines()
for line in lines:
    (center, orbiter) = line.strip().split(')')
    search_map_and_insert(center, orbiter)

print(orbit_count(object_map, -1))

def depth_count(map, x, depth):

    (c, o) = map
    for (c_, o_) in o:
        if c_ == x:
            return depth + 1
    for submap in o: 
        r = depth_count(submap, x, depth+1)
        if r >= 0:
            return r

    return -1

def traverse(us, them, our_jumps):

    global object_map

    (our_parent, our_siblings) = search_map(object_map, us)
    if our_parent == None:
        raise ValueError(us + " not found.")

    their_jumps = depth_count((our_parent, our_siblings), them, -1)
    if their_jumps >= 0:
        return our_jumps + their_jumps
    else:
        (our_parent, our_siblings) = search_map(object_map, us)
        if our_parent == None:
            raise ValueError(us + " not found.")
        return traverse(our_parent, them, our_jumps+1)

print(traverse("YOU", "SAN", 0))

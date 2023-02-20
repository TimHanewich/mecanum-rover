
def percent_difference(n1:float, n2:float) -> float:
    diff = n2 - n1
    ap = diff / n1
    return abs(ap)

def select_first_cycle(data:list):

    # SETTINGS
    tolerance = 0.001 #percent tolerance
    repeat_confirmation = 5 #5 units following suit will confirm

    if len(data) < repeat_confirmation:
        return None

    # create the confiration set
    confirmation_set = []
    for x in range(0, repeat_confirmation):
        confirmation_set.append(data[x])

    # try to find a pattern here that starts with first    
    for x in range(1, len(data) - repeat_confirmation):
        this_item = data[x]

        # measure percent difference between this one and the first one
        fpd = percent_difference(confirmation_set[0], this_item)
        if fpd <= tolerance:

            # create this set
            this_set = []
            for s in range(0, repeat_confirmation):
                this_set.append(data[x + s])

            # run through each, see if they match up within tolerance
            is_match = True
            for bv in range(0, len(confirmation_set)):
                confirmation_value = confirmation_set[bv]
                set_value = this_set[bv]
                vpd = percent_difference(confirmation_value, set_value)
                if vpd > tolerance:
                    is_match = False
            
            # if the match held up, return it
            if is_match:
                first_cycle = [] # to return
                for v in range(0, x):
                    first_cycle.append(data[v])
                return first_cycle

    # if we got to this point, a match wasn't found. So a cycle was probbaly not made, at least with the tolerance val. So return None
    return None



#data = [75, 3, 53, 20, 60, 65, 31, 57, 71, 41, 22, 22, 69, 13, 31, 88, 83, 23, 93, 56, 75, 3, 53, 20, 60, 65, 31, 57, 71, 41, 22, 22, 69, 13, 31, 88, 83, 23, 93, 56]
#data = [75, 3, 53, 20, 60, 65, 31, 57, 71, 41, 22, 22, 69, 13, 31, 88, 83]
#data = [1,4,6,4,2,6,2,4]
#data = [75, 74, 73, 72, 71, 75, 74, 73, 72, 71]

# REAL data
#data = [71.32685, 71.344, 72.97325, 107.9593, 85.1326, 84.18935, 86.35025, 230.4789, 250.5958, 80.3992, 82.52579, 85.1669, 109.3141, 1202.609, 1202.798, 1202.781, 146.8555, 146.3238, 146.2038, 156.631, 72.87035, 68.1884, 65.42725, 64.87845, 65.04995, 67.38235, 102.4198, 85.83575, 82.09705, 82.61155, 86.1959, 1202.798, 88.44255, 86.1959, 87.0877, 113.756, 1202.832, 1202.781, 68.85725, 69.6976, 146.9412, 147.3699, 150.4227, 66.73065, 63.5922, 60.00785, 58.7216, 59.0303, 61.5342, 95.13105, 97.6521, 81.634, 80.7422, 83.2461, 147.8844, 92.90155, 80.48495, 91.70105, 119.2783, 1202.764, 1202.712, 73.62495, 150.7142, 148.7076, 148.8792, 152.5664, 194.8411, 60.9854, 55.41165, 54.24545, 54.51985, 56.74935, 91.18655, 91.97545, 95.61125, 82.97169, 232.7598, 233.1543, 96.02285, 94.8738]

#cycle = select_first_cycle(data)
#print(cycle)
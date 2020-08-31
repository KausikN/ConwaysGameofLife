'''
State Generation Methods
'''

# Imports
import cv2
import numpy as np

# Main Functions
def RandomState(size, values):
    State = np.random.choice(values, size)
    return State

def StateFromImage(I, size, values):
    State = []

    I = cv2.resize(I, (size[0], size[1]))
    if len(I.shape) == 2:
        I = np.reshape(I, (I.shape[0], I.shape[1], 1))

    MapCache = [[], []]
    for i in range(I.shape[0]):
        values_i = []
        for j in range(I.shape[1]):
            # Check in Cache
            CacheHit = True
            cache_index = None
            mappedVal = None
            try:
                cache_index = MapCache[0].index(','.join(list(I[i, j, :].astype(str))))
            except IndexError:
                CacheHit = False

            if CacheHit:
                mappedVal = MapCache[1][cache_index]
            else:
                mappedVal = ClosestMap(I[i, j, :], values)
                MapCache[0].append(','.join(list(I[i, j, :].astype(str))))
                MapCache[1].append(mappedVal)
                
            values_i.append(mappedVal)
        State.append(values_i)

    return State

def ClosestMap(val, values):
    val = np.array(val)

    minDist = -1
    minDistIndex = -1
    for i in range(len(values)):
        values[i] = np.array(values[i])

        dist = np.sum(np.subtract(val, values[i])) ** (0.5)

        if minDistIndex == -1 or dist < minDist:
            minDist = dist
            minDistIndex = i

    return values[minDistIndex]



# Driver Code
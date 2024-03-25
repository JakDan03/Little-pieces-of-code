# the travelling salesman problem is simplified to a 2D map with X'es (empty places) and P's (measuring points) 
# this program finds the exact solution, going through all possibilities

map = "XPXXP,PXPXP,XXXXP,XPXXX,XPXPX".split(",") # an example of the map

#     X  P  X  X  P
#     P  X  P  X  P
#     X  X  X  X  P
#     X  P  X  X  X
#     X  P  X  P  X

# map presentation
for l in map: print(l)
print("")

# empty space for length and P coordinates
length = 0
cords = []

# finding all of P coordinates
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == "P": cords.append([i, j])

# printing all P's available
for x in range(len(cords)): print("Point %d: %s" %(x+1, str(cords[x])))
print("")

# simple cases (up to 3 points)
if len(cords) == 0: print("There is no P's on the map!")
elif len(cords) == 1: print("Distance between points: 0")
elif len(cords) <= 3:
    for p in range(len(cords)):
        length += ((cords[p%len(cords)][0] - cords[(p+1)%len(cords)][0]) ** 2 + (cords[p%len(cords)][1] - cords[(p+1)%len(cords)][1]) ** 2) ** (1/2)
    print("Distance between points: %f" %length)

# other cases (more than 3 points)
else:
    
    # a list of distances between points
    odl = [[((cords[i][0] - cords[j][0]) ** 2 + (cords[i][1] - cords[j][1]) ** 2) ** (1/2) for i in range(len(cords))] for j in range(len(cords))]

    # candidates for the shortest route (we always start from the first point)
    cand = [[[i+1], i+1, odl[0][i]] for i in range(1, len(cords))]

    # finding every possibilities to connect a point with a point
    ilp = 0
    while len(cand[-1][0]) < len(cords) - 1:
        ilp = len(cand)
        for i in range(ilp):
            for j in range(1, len(cords)):
                if j+1 not in cand[i][0]:
                    cand.append([[j+1]+cand[i][0], j+1, cand[i][2]+odl[j][cand[i][1]-1]])
        cand = cand[ilp:]

    # add a distance to the first point
    for i in range(len(cand)): cand[i][2] += odl[cand[i][1]-1][0]

    # sort routes in the appropriate order
    cand = sorted(cand, key=lambda x: x[2])

    # find the answer
    ans_p, ans_l = [1] + cand[0][0] + [1], cand[0][2]
    ans_p = [str(x) for x in ans_p]

    # show the answer
    print("The shortest possible distance between all given points is: %f" %ans_l)
    print("To achieve it, you have to take a following route (starting from the 1st point): %s" %"-".join(ans_p))

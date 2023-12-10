
map = input().split(",") # mapa w formie linii po przecinku, gdzie P są punktami a X wypełniają puste przestrzenie, np. XXXXX,XPXXX,XXPXP,XXXPX,PXPXX (mapa 5x5)print("")
for l in map: print(l) # prezentacja mapy
print("")
length = 0
cords = []
for i in range(len(map)):
    for j in range(len(map[0])):
        if map[i][j] == "P": cords.append([i, j])
for x in range(len(cords)): print("Punkt %d: %s" %(x+1, str(cords[x])))
print("")
if len(cords) == 0: print("Brak punktów P na mapie!")
elif len(cords) == 1: print("Odległość: 0")
elif len(cords) <= 3:
    for p in range(len(cords)):
        length += ((cords[p%len(cords)][0] - cords[(p+1)%len(cords)][0]) ** 2 + (cords[p%len(cords)][1] - cords[(p+1)%len(cords)][1]) ** 2) ** (1/2)
    print("Odległość: %f" %length)
else:
    odl = [[((cords[i][0] - cords[j][0]) ** 2 + (cords[i][1] - cords[j][1]) ** 2) ** (1/2) for i in range(len(cords))] for j in range(len(cords))]
    cand = [[[i+1], i+1, odl[0][i]] for i in range(1, len(cords))]
    ilp = 0
    while len(cand[-1][0]) < len(cords) - 1:
        ilp = len(cand)
        for i in range(ilp):
            for j in range(1, len(cords)):
                if j+1 not in cand[i][0]:
                    cand.append([[j+1]+cand[i][0], j+1, cand[i][2]+odl[j][cand[i][1]-1]])
        cand = cand[ilp:]
    for i in range(len(cand)): cand[i][2] += odl[cand[i][1]-1][0]
    cand = sorted(cand, key=lambda x: x[2])
    ans_p, ans_l = [1] + cand[0][0] + [1], cand[0][2]
    ans_p = [str(x) for x in ans_p]
    print("Najkrótsza odległość jaką należy pokonać aby przemieścić się między wszystkimi punktami to: %f" %ans_l)
    print("Można tego dokonać poruszając się w następującej kolejności (zaczynając od 1): %s" %"-".join(ans_p))

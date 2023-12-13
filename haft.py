def szlaczek(num, sign):
    line = sign
    for i in range(num-1): line += " " + sign
    return line

# czy_break - True: przerywamy funkcję wg parametru dlugosc, False: dokańczamy rozpoczętą część wzoru (do "rogu")
# czy_prawy - True: wzór może skończyć się w prawym rogu, False: nie może skończyć się w prawym rogu
def haft(dlugosc, szerokosc=3, wciecie=2, znak="#", czy_break=True, break_prawy=True):
    linia = szlaczek(szerokosc, znak)
    if wciecie == 0:
        for i in range(dlugosc): print(linia)
    else:
        r, spacje = 1, 0
        dlugosc_r = dlugosc + ((1 + wciecie - dlugosc % wciecie) % wciecie * (not czy_break)) # rzeczywista długość wzoru
        czy_prawy = wciecie * (not break_prawy) * (not czy_break) * ((dlugosc_r % (2 * wciecie)) != 1) # kończy wzór zawsze po lewej stronie jeśli break_prawy=False
        for i in range(dlugosc_r + czy_prawy):
            print(" " * spacje + linia)
            if spacje == 0: r = abs(r)
            elif spacje == wciecie: r = r * (-1)
            spacje += r

# przykładowe wzory
haft(7)
print()
print("*" * 10)
print()
haft(8, 4)
print()
print("*" * 10)
print()
haft(10, 2, 0, "*")
print()
print("*" * 10)
print()
haft(8, 4, 5, "$", False)
print()
print("*" * 10)
print()
haft(8, 6, 3, "@", False, False)
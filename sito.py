# sito Erastotenesa
zakres = 0
while zakres < 2:
    zakres = int(input("Podaj górny zakres znajdowania liczb: "))
starter = 0
list = [True for i in range(zakres - 1)]
while starter < int(zakres ** (1/2)):
    while not list[starter]:
        starter += 1
    for j in range(starter, len(list), starter+2):
        list[j] = False
    list[starter] = True
    starter += 1
primary = [i+2 for i in range(len(list)) if list[i]]
print(primary)
print("Ilość liczb pierwszych między 2 a " + str(zakres) + ": " + str(len(primary)))

# Gra w wojnę - każdy dostaje taką samą ilość
# kart po czym porównuje się wyciągając za każdym razem zupełnie
# losową kartę z tych, które ma w talii (brak taktyki po obu
# stronach). W razie braku kart dobiera on karty ze zdobytych
# kart, a przegrywa wówczas, gdy nie będzie miał kart ani
# w talii ani w wygranych kartach. Wyjątkiem jest sytuacja, gdy
# gracz nie ma żadnych kart ale jest w stanie wojny - wówczas
# może dobrać losową kartę/karty od przeciwnika

import random

# karty w grze
figury = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
kolory = ["♣", "♦", "♥", "♠"]
talia = [f+k for f in figury for k in kolory] + ["Joker", "Joker", "Joker"]

# moc kart
karta = dict(zip(talia, [int(i/4) for i in range(len(talia))]))

# rozdajemy karty
gracz = []
bot = []
for i in range(int((len(talia)-1)/2)):
    los = talia[random.randint(0, len(talia)-1)]
    gracz.append(los)
    talia.remove(los)
    los = talia[random.randint(0, len(talia)-1)]
    bot.append(los)
    talia.remove(los)

# prezentujemy karty
gracz = sorted(gracz, key=lambda x: karta[x])
bot = sorted(bot, key=lambda x: karta[x])
print("\n")
print("Talia gracza: " + str(gracz))
print("Talia bota: " + str(bot))
print("\n")

# miejsca na zdobyte karty
gain_gracz = []
gain_bot = []

# statystyki
win_gracz = 0
win_bot = 0
tie = 0
streak_gracz = 0
streak_bot = 0
str_temp_gracz = 0
str_temp_bot = 0

#rozgrywka
for i in range(1000):
    choice_gracz = gracz[random.randint(0, len(gracz)-1)]
    choice_bot = bot[random.randint(0, len(bot)-1)]
    print("%s vs %s" %(choice_gracz, choice_bot))
    if karta[choice_gracz] > karta[choice_bot]:
        win_gracz += 1
        str_temp_gracz += 1
        if str_temp_gracz > streak_gracz: streak_gracz += 1
        str_temp_bot = 0
        gain_gracz.extend([choice_gracz, choice_bot])
        gracz.remove(choice_gracz)
        bot.remove(choice_bot)
    elif karta[choice_gracz] < karta[choice_bot]:
        win_bot += 1
        str_temp_bot += 1
        if str_temp_bot > streak_bot: streak_bot += 1
        str_temp_gracz = 0
        gain_bot.extend([choice_gracz, choice_bot])
        gracz.remove(choice_gracz)
        bot.remove(choice_bot)
    else:
        stack = [choice_gracz, choice_bot]
        gracz.remove(choice_gracz)
        bot.remove(choice_bot)
        while True:
            tie += 1
            for j in range(2):
                if len(gracz) == 0:
                    if len(gain_gracz) != 0:
                        gracz.extend(gain_gracz)
                        gain_gracz = []
                    else:
                        if len(bot) != 0:
                            gracz.append(bot[random.randint(0, len(bot)-1)])
                        else:
                            gracz.append(gain_bot[random.randint(0, len(gain_bot) - 1)])
                if len(bot) == 0:
                    if len(gain_bot) != 0:
                        bot.extend(gain_bot)
                        gain_bot = []
                    else:
                        if len(gracz) != 0:
                            bot.append(gracz[random.randint(0, len(gracz)-1)])
                        else:
                            bot.append(gain_gracz[random.randint(0, len(gain_gracz) - 1)])
                war_gracz = gracz[random.randint(0, len(gracz)-1)]
                war_bot = bot[random.randint(0, len(bot)-1)]
                print("%s vs %s" % (war_gracz, war_bot) + " (zakryte)" * (1-j))
                stack.extend([war_gracz, war_bot])
                gracz.remove(war_gracz)
                bot.remove(war_bot)
            if karta[war_gracz] != karta[war_bot]:
                if karta[war_gracz] > karta[war_bot]:
                    win_gracz += 1
                    str_temp_gracz += 1
                    if str_temp_gracz > streak_gracz: streak_gracz += 1
                    str_temp_bot = 0
                    gain_gracz.extend(stack)
                else:
                    win_bot += 1
                    str_temp_bot += 1
                    if str_temp_bot > streak_bot: streak_bot += 1
                    str_temp_gracz = 0
                    gain_bot.extend(stack)
                break
    if len(gracz) == 0:
        if len(gain_gracz) == 0:
            ruchy = i + 1
            break
        else:
            gracz.extend(gain_gracz)
            #print("Gracz: %s" %str(gain_gracz))
            gain_gracz = []
    if len(bot) == 0:
        if len(gain_bot) == 0:
            ruchy = i + 1
            break
        else:
            bot.extend(gain_bot)
            #print("Bot: %s" %str(gain_bot))
            gain_bot = []

# wybór zwycięzcy
print("\n")
if len(gracz) == 0 and len(gain_gracz) == 0:
    print("Wygrywa bot!")
elif len(bot) == 0 and len(gain_bot) == 0:
    print("Wygrywa gracz!")
else:
    print("Panom nie udało się dograć po tysiącu ruchów")
    ruchy = 1000
    print("Karty gracza: " + str(sorted(gracz + gain_gracz, key=lambda x: karta[x])))
    print("Karty bota: " + str(sorted(bot + gain_bot, key=lambda x: karta[x])))
print("Statystyki:")
print("Ilość kolejek: %d" %ruchy)
print("Wygrane przez gracza: %d (%d" %(win_gracz, round(win_gracz/ruchy*100, 0)) + "%)")
print("Wygrane przez bota: %d (%d" %(win_bot, round(win_bot/ruchy*100, 0)) + "%)")
print("Ilość dogrywek (wojen): %d" %tie)
print("Najdłuższy streak gracza: %d" %streak_gracz)
print("Najdłuższy streak bota: %d" %streak_bot)

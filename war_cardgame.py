# War card game - everyone gets the same number of cards and then compares each time by choosing a completely random card from those in the deck (no tactics on both sides).  The player with the higher card takes both of the cards played and moves them to their stack. If the two cards played are of equal value, then there is a "war". Both players place the next card from their deck face down and then another card face-up. The owner of the higher face-up card wins the war and adds all the cards on the table to their stack. If no cards left in deck, players draw cards from his stack, and loses when he has no cards in either the deck or the stack. The exception is when the player has no cards but the war is on - then he can draw a random card / cards from the opponent.
import random

# cards in game
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["♣", "♦", "♥", "♠"]
deck = [r+s for r in ranks for s in suits] + ["Joker", "Joker", "Joker"]

# cards rank
card = dict(zip(deck, [int(i/4) for i in range(len(deck))]))

# dealing cards
player = []
bot = []
for i in range(int((len(deck)-1)/2)):
    los = deck[random.randint(0, len(deck)-1)]
    player.append(los)
    deck.remove(los)
    los = deck[random.randint(0, len(deck)-1)]
    bot.append(los)
    deck.remove(los)

# presenting cards
player = sorted(player, key=lambda x: card[x])
bot = sorted(bot, key=lambda x: card[x])
print("\n")
print("Player deck: " + str(player))
print("Bot deck: " + str(bot))
print("\n")

# stacks
gain_player = []
gain_bot = []

# statistics
win_player = 0
win_bot = 0
tie = 0
streak_player = 0
streak_bot = 0
str_temp_player = 0
str_temp_bot = 0

# gameplay
for i in range(1000):
    choice_player = player[random.randint(0, len(player)-1)]
    choice_bot = bot[random.randint(0, len(bot)-1)]
    print("%s vs %s" % (choice_player, choice_bot))
    if card[choice_player] > card[choice_bot]:
        win_player += 1
        str_temp_player += 1
        if str_temp_player > streak_player: streak_player += 1
        str_temp_bot = 0
        gain_player.extend([choice_player, choice_bot])
        player.remove(choice_player)
        bot.remove(choice_bot)
    elif card[choice_player] < card[choice_bot]:
        win_bot += 1
        str_temp_bot += 1
        if str_temp_bot > streak_bot: streak_bot += 1
        str_temp_player = 0
        gain_bot.extend([choice_player, choice_bot])
        player.remove(choice_player)
        bot.remove(choice_bot)
    else:
        war_cards = [choice_player, choice_bot]
        player.remove(choice_player)
        bot.remove(choice_bot)
        while True:
            tie += 1
            for j in range(2):
                if len(player) == 0:
                    if len(gain_player) != 0:
                        player.extend(gain_player)
                        gain_player = []
                    else:
                        if len(bot) != 0:
                            player.append(bot[random.randint(0, len(bot)-1)])
                        else:
                            player.append(gain_bot[random.randint(0, len(gain_bot) - 1)])
                if len(bot) == 0:
                    if len(gain_bot) != 0:
                        bot.extend(gain_bot)
                        gain_bot = []
                    else:
                        if len(player) != 0:
                            bot.append(player[random.randint(0, len(player)-1)])
                        else:
                            bot.append(gain_player[random.randint(0, len(gain_player) - 1)])
                war_player = player[random.randint(0, len(player)-1)]
                war_bot = bot[random.randint(0, len(bot)-1)]
                print("%s vs %s" % (war_player, war_bot) + " (hidden)" * (1-j))
                war_cards.extend([war_player, war_bot])
                player.remove(war_player)
                bot.remove(war_bot)
            if card[war_player] != card[war_bot]:
                if card[war_player] > card[war_bot]:
                    win_player += 1
                    str_temp_player += 1
                    if str_temp_player > streak_player: streak_player += 1
                    str_temp_bot = 0
                    gain_player.extend(war_cards)
                else:
                    win_bot += 1
                    str_temp_bot += 1
                    if str_temp_bot > streak_bot: streak_bot += 1
                    str_temp_player = 0
                    gain_bot.extend(war_cards)
                break
    if len(player) == 0:
        if len(gain_player) == 0:
            battles = i + 1
            break
        else:
            player.extend(gain_player)
            gain_player = []
    if len(bot) == 0:
        if len(gain_bot) == 0:
            battles = i + 1
            break
        else:
            bot.extend(gain_bot)
            gain_bot = []

# choosing a winner
print("\n")
if len(player) == 0 and len(gain_player) == 0:
    print("Bot won!")
elif len(bot) == 0 and len(gain_bot) == 0:
    print("Player won")
else:
    print("The game not finished after 1000 battles!")
    battles = 1000
    print("Player cards: " + str(sorted(player + gain_player, key=lambda x: card[x])))
    print("Bot cards: " + str(sorted(bot + gain_bot, key=lambda x: card[x])))
print("Statistics:")
print("Total battles: %d" % battles)
print("Won by the player: %d (%d" %(win_player, round(win_player/battles*100, 0)) + "%)")
print("Won by the bot: %d (%d" %(win_bot, round(win_bot/battles*100, 0)) + "%)")
print("Wars (ties): %d" % tie)
print("The longest streak of the player: %d" % streak_player)
print("The longest streak of the bot: %d" % streak_bot)
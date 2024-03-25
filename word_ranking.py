# giving a rank of the word comparing to other words which can be made from the word given (even if they do not make sense)
# try not to give words longer than 10 letters (it may end up badly)

# permutations defined
def permutations(x):
    if x == 1: perms.append(list(letters))
    else:
        for j in range(x):
            letters[j], letters[x-1] = letters[x-1], letters[j]
            permutations(x-1)
            letters[j], letters[x-1] = letters[x-1], letters[j]

# a word is given and divided into letters
word = str(input())
letters = [word[i] for i in range(len(word))]

# permutations are found
perms = []
permutations(len(word))

# letters are matched into words again
words = []
for i in range(len(perms)):
    w = ""
    for j in range(len(perms[i])):
        w += perms[i][j]
    words.append(w)

# identical words are deleted
words = set(words)
words = list(words)

# words are sorted
words.sort()
if len(words) < 100: print(words)

# rank is printed
rank = words.index(word) + 1
print(str(rank) + "/" + str(len(words)))

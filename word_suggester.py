# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# word_suggester.py
# Carrie West
# A program that suggests words to follow an input word based on a given
# piece of raw text data.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
from nltk import word_tokenize, ngrams, FreqDist
from re import sub
from nltk.corpus import stopwords

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# word_search(key, bigram)
# Searches through the top 70 most common word pairs for any pair containing
#   the key. It sorts the pair and checks to make sure if that if there are
#   duplicates that they are added to the previous occurrence total and not
#   their own value.
# Returns a list object with the values found, and the total amount of
#   occurrences for the key
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def word_search(key, bigram):
    sug_results = []
    total = 0
    for words, frequency in bigram.most_common(70):
        no_dupe = True
        sortable = sorted(words)

        if key in sortable:
            total += frequency
            for pair in sug_results:

                if list(pair[0]) == sortable:
                    pair[1] += frequency

                    no_dupe = False
            if no_dupe:
                sug_results.append([sorted(words), frequency])
    return sug_results, total


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# choose_suggestion(key,sug_results,total)
# Finds the most common suggestion pair based on a predetermined tolerance
#   level of commonality. If there are less than three valid results, it fills
#   the remaining spots with common filler words.
# Returns a list of the viable (>65% connection and/or filler words)
#   suggestions
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def choose_suggestion(key, sug_results, total):
    common_fillers = ['the', 'this', 'of']
    viable_sugs = []

    for sug in sug_results:
        if (sug[1] / total) >= 0.65:  # tolerance level could (probably should) be a variable value in an actual build
            if sug[0][0] == key:
                viable_sugs.append(sug[0][1])
            else:
                viable_sugs.append(sug[0][0])
    if len(viable_sugs) < 3:
        for x in range(len(viable_sugs), 3):
            viable_sugs.append(common_fillers[x])
    return viable_sugs


STOP = stopwords.words('english')

with open('messages.txt') as f:
    word_bag = [sub("'s|[^A-Za-z0-9\-]+", "", token.lower()) for token in word_tokenize(f.read())
                if len(token) > 2 and token not in STOP]

my_bigrams = FreqDist(ngrams(word_bag, 2))

key = input('input a word ').lower()
total = 0
sug_results, total = word_search(key, my_bigrams)
viable_sugs = choose_suggestion(key, sug_results, total)

for viable_sug in viable_sugs:
    print(f"You next word might be '{viable_sug}'.")

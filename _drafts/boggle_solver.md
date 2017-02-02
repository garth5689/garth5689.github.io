---
layout:     post
title:      "Boggle Solver"
date:       2017-1-19 1:00:00
author:     Andrew
header-img: img/posts/boggle_solver/the-maze.jpg
tags:       puzzles programming
---

If you haven't read my [last post]({{ page.previous.url | prepend: site.baseurl | replace: '//', '/' }}), go ahead and read that before diving in here.  It's not strictly necessary, but it will give you some context.

In my last post discussing the genetic algorithm approach to generating Boggle boards, I skipped over an important detail.  Because I wanted to keep my focus on the genetics aspect of the solution, I didn't go into details about actually scoring the boards.  A few people have asked me about the details, so I thought it'd be best to share.  If your recreational reading is solely focused on boggle board solving, there are
<!--break-->
many resources out there for you as well beyond this post[^blog1] [^blog2] [^blog3].  I won't be blazing any trails here, but it's still fun to explain.

I'll re-iterate the rules of Boggle for everyone who may have forgotten them since we last talked.

> Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.

# Solution Approach
Let's start by listing off criteria that our algorithm must meet:
* Words can start on any square.
* The next letter in a word can be orthogonal or diagonal to the current letters.
* A single letter cannot be used more than once in a word.
* Words must be three or more letters.

#### Dictionary
Let's start by talking about the dictionary.  In order to know if we have words, we need a dictionary to pull from.  In this case, I'll be using a public domain word list titled [enable1.txt](http://norvig.com/ngrams/enable1.txt).  It contains approximately 170,000 of the most commonly used words.  There's nothing particularly special about this list, it just happens to be very popular and public domain.

## Searching The Grid
Now we know what we're looking for, so let's start to search.

### Naive
The most basic solution would be to traverse all possible paths through the grid, only stopping when there are no more available squares to move to.  Along the way, each string of letters would be checked to see if it's a word.  This approach would certainly be the the most thorough, but would also lead to countless unnecessary calculations.

For example, say the search is four letters in, and the first four squares spell out "XKCD".  Using this naive strategy, the search would continue, looking for words starting with "XKCD".  Clearly, this is going to be fruitless, and the search could have been stopped earlier.  The naive search will spend a significant amount of time searching dead ends looking for words.

Additionally, this algorithm would also have to construct every possible traversal of the grid, which would take quite a long time.  Moving along a grid such as this, while not allowing for repeated stops at the same point is called a [self-avoiding walk](https://en.wikipedia.org/wiki/Self-avoiding_walk).  For smaller grids such as this, it's possible to enumerate all the paths, but a general formula doesn't exist for an arbitrary grid size.

### Be More Selective
It may make sense for us to trim our search down to not pursue dead ends, but how can we do that?  In the example above, it makes sense to stop searching once we know no words begin with the squares we have traversed so far.

While searching now, for each string that we have found, we'll check to see if there is a word that starts with that string.  If we have found a full word, we can add it to our list and keep going.  If there doesn't exist a word that starts with that string, stop searching that path and pick a new direction to search.

### Search Smarter
Now that we know we're going to be checking the dictionary frequently for prefixes, let's explore ways to make that lookup faster.  As an aside, think about how you might check a paper dictionary for the word `isopod`.  You would start at `i`, then move to `is`, etc.  If your dictionary didn't have any words that started with `isop`, you can conclude that your word is not in the dictionary.

Our algorithm (so far) is searching for prefixes by starting at the top of the list and searching the entire thing.  Let's search like a human (because we already know how anyway).


## Data structures
In order to make the most efficient search possible, we'll be transforming our dictionary into a an ordered tree called a [trie](https://en.wikipedia.org/wiki/Trie).  A trie is great for this application because as you travel down the nodes of the tree, you're constructing a word.  As you search, if the next letter in your word doesn't appear in the tree, you know that your word is not contained in the dictionary.

An example may help here:

#### Trie
One of the data structures best suited for this task is the [trie](https://en.wikipedia.org/wiki/Trie) .  A trie is an ordered tree structure that, as it is traversed, can efficiently know when a word is not contained in a potential list.  The trie is created by first creating a set of nodes that correspond to the first letters of all the words in the list.  Then, for each of those letters, a node is added for each second letter in the words starting with that original letter.  

This allows the search for a word to proceed letter by letter, similar to how you would look up a word in the dictionary if someone was spelling the word to you.  As soon as you can't find the next letter, you know the word is not contained!






# The Nitty Gritty

#### Traversing the Grid
For consistency, let's refer to the board on a coordinate system, with each square having an x and a y coordinate.  The origin will be in the top left, with x going horizontal and y being vertical.

Functionality will be needed to determine the neighbors of a particular square, to find the next squares in the grid to travel to.

~~~ python
def neighbors(x, y):
    if not 0 <= x < BOARD_SIZE or not 0 <= y < BOARD_SIZE:
        raise ValueError("square not within board")

    """
    x is the x index of the supplied square.  To cover squares to
    the left and right, we should go from x-1 to x+1.  Because
    the range() function is not inclusive on the upper bound,
    we'll need to go to x+2.

    To prevent returning squares that are outside the board, the
    range should be capped at 0 and BOARD_SIZE.
    """

    lower_x = max(0, x - 1)    
    upper_x = min(x + 2, BOARD_SIZE)

    lower_y = max(0, y - 1)
    upper_y = min(y + 2, BOARD_SIZE)

    for nx in range(lower_x, upper_x):
        for ny in range(lower_y, upper_y):
            yield (nx, ny)
~~~


#### Constructing the trie
The trie is constructed as a dict [^trie_python].  At the top level, the keys are the first letters of all the words.  Inside each of those is another dict containing all the seconds letters of words that started with the first letter.  Additionally, because we want to find words that are contained within other words, there is a special key that signals that the string ending on that node is a word itself.  This makes sure that we both count that word, but also continue searching if it's also a prefix to further words.

~~~ python
def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            # as the letters get counted, traverse further into the dict
            # if the key does not exist, it will be created.  Otherwise
            # current_dict will just move deeper into the dictionary.
            current_dict = current_dict.setdefault(letter, {})
        # add the END key at the deepest node for this word
        # to signal that this string is a word.
        current_dict[END] = END
    return root
~~~


#### Searching the trie
~~~ python
class TrieMembership(IntEnum):
    invalid = 1
    prefix = 2
    word = 3

# This is a cache of all the lookups so far, to speed up repeated queries to the trie.
TRIE_MEMBERS = dict()


def trie_member(trie, word):
    # try to fetch the membership from the list in memory first.
    try:
        return TRIE_MEMBERS[word]

    # if the word has not been tested already, calculate whether the string
    # is not a valid word/prefix, whether it is a prefix to possible words
    # or a word itself.
    except KeyError:
        current_dict = trie
        for letter in word:
            try:
                # attempt to follow the letters through the trie dict
                current_dict = current_dict[letter]
            except KeyError:
                # once a key is not found, this means this word is not in the trie
                TRIE_MEMBERS[word] = TrieMembership.invalid
                return TRIE_MEMBERS[word]
        if END in current_dict:
            # If END is found, this string is a full word in our original dictionary
            TRIE_MEMBERS[word] = TrieMembership.word
            return TRIE_MEMBERS[word]
        else:
            # If all letters are still in the trie, but this is not a full word,
            # it means there are words that start with this string.
            TRIE_MEMBERS[word] = TrieMembership.prefix
            return TRIE_MEMBERS[word]
~~~

#### Traversing the grid
~~~ python
def recurse_grid_internal(grid, path, current_word, words_trie, found_words):
    # path should be empty on the initial call
    if not path:
        # This is the initial call to ensure that a search
        # starts from each square in the grid.
        for y, row in enumerate(grid):
            for x, letter in enumerate(row):
                for (next_path, next_word) in recurse_grid_internal(grid,
                                                                    [(x, y)],
                                                                    letter,
                                                                    words_trie,
                                                                    found_words):
                    yield (next_path, next_word)

        return
    # path is a list of coordinates, so the last one
    # in the list is our current position in the grid
    current_position = path[-1]

    # test to see how our word is contained in the word list
    membership = trie_member(words_trie, current_word)

    # We have found a new word from our list and
    # should yield the current path and the word
    if membership == TrieMembership.word and current_word not in found_words:
        found_words.add(current_word)
        yield (path, current_word)

    # If it's not a full word, but a prefix to one or more words in the
    # list, continue searching by moving to a neighbor
    # and adding that letter to the current word.
    if membership >= TrieMembership.prefix:
        for nx, ny in neighbors(*current_position):
            # the same square can only be used in each word once
            if (nx, ny) not in path:
                new_letter = grid[ny][nx]

                # the Q cube in boggle has QU on it.
                new_letter = new_letter if new_letter != 'q' else 'qu'

                # add the letter on the newest cube to the current word.
                new_word = current_word + new_letter

                # if the new word is either a word or prefix,
                # continue recursively searching from that new square.
                if trie_member(words_trie, new_word) != TrieMembership.invalid:
                    for (next_path, next_word) in recurse_grid_internal(grid,
                                                                        path + [(nx, ny)],
                                                                        new_word,
                                                                        words_trie,
                                                                        found_words):
                        yield (next_path, next_word)
~~~

~~~ python
LEN_TO_SCORE = {3: 1,
                4: 1,
                5: 2,
                6: 3,
                7: 5,
                8: 11,
                9: 11,
                10: 11,
                11: 11,
                12: 11,
                13: 11,
                14: 11,
                15: 11,
                16: 11}

total_score = 0
for word in recurse_grid_internal(grid, list(), "", trie, set())):
    total_score += LEN_TO_SCORE[len(word)]
~~~

[^trie_python]: [How to create a TRIE in Python](http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python)
[^blog1]:[How to find list of possible words from a letter matrix [Boggle Solver]](http://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver)
[^blog2]: [Solving the Boggle Game - Recursion, Prefix Tree, and Dynamic Programming](http://exceptional-code.blogspot.com/2012/02/solving-boggle-game-recursion-prefix.html)
[^blog3]: [Solving Boggle boards at scale](https://blog.niallconnaughton.com/2015/12/10/solving-boggle-boards-at-scale/)

0	:(6,	8),
1	:(5,	3),
2	:(5	,11),
3	:(4,	1),
4	:(4,	4),
5	:(4,	7),
6	:(4	,10),
7	:(4	,13),
8	:(4	,15),
9	:(3,	0),
10:(	3,	1),
11:(	3,	3),
12:(	3,	4),
13:(	3,	5),
14:(	3,	6),
15:(	3,	7),
16:(	3,	8),
17:(	3,	9),
18:(	3	,10),
19:(	3	,11),
20:(	3	,12),
21:(	3	,13),
22:(	3	,13),
23:(	3	,14),
24:(	2,	2),
25:(	2,	3),
26:(	2,	4),
27:(	2,	7),
28:(	2	,10),
29:(	2	,13),
30:(	2	,14),
31:(	2	,15),
32:(	1,	7),
33:(	0,	7),

---
layout:     post
title:      "Boggle Revisited: Solver"
date:       2017-1-19 1:00:00
author:     Andrew
header-img: img/boggle_solver/the-maze.jpg
tags:       puzzles programming
---

## Background
If you haven't read my [last post]({{ page.previous.url | prepend: site.baseurl | replace: '//', '/' }}), go ahead and read that before diving in here.  It's not strictly necessary, but it will give you some context.

In my last post discussing Boggle board generation, I skipped over an important detail.  Because I wanted to keep my focus on the genetics aspect of the solution, I didn't go into details about actually scoring the boards.  A few people have asked me about the details, so I thought it'd be best to share.  If your recreational reading is solely focused on boggle board solving, there are many resources out there for you as well beyond this post[^blog1] [^blog2] [^blog3].  I won't be blazing any trails here, but it's still fun to explain.

I'll re-iterate the rules of Boggle for everyone who may have forgotten them since we last talked.

> Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.

# Solution Approach
First, it's important to note what we don't know.  We can't know the potential orientation of any word, or it's length.  We also can't know if and when words will be contained in other words.  With these in mind, I'll try to come up with a generic solution that should scale to any size board.

#### Dictionary
Let's start by talking about the dictionary.  In order to know if we have words, we have to define what a word is.  In this case, I'll be using a public domain word list titled [enable1.txt](http://norvig.com/ngrams/enable1.txt).  It contains approximately 170,000 of the most commonly used words.  There's nothing particularly special about this list, it just happens to be very popular and public domain.


## Searching The Grid
### Naive
The most basic solution would be to traverse all possible paths through the grid, only stopping when there are no more available squares to move to.  Along the way, each string of letters would be checked to see if it's a word.  This approach would certainly be the the most thorough, but would also lead to countless unnecessary calculations.  

For example, if the algorithm has started to construct a string to check for possible words, and the string starts with "FFF", a lot of time will be spent checking all the possible combinations of squares to find longer words.  It may make sense to check words as the grid is being searched and stop when there are no words that start with the letters checked so far.  Additionally, this algorithm would also have to construct every possible traversal of the grid, which would take quite a long time.

This type of problem is known as a [self-avoiding walk](https://en.wikipedia.org/wiki/Self-avoiding_walk), which is most definitely beyond the scope of this algorithm.  


### Do Less
So we've ruled out searching the entire tree, but how can we effectively trim off searches that we know won't be fruitful?  Let's start by stopping a search once we know that there are no words that start with the letters we have found so far.

Think about how you might check if a word is in the dictionary.  If I asked you to look up the word


## The Grid
First, let's tackle traveling around the grid.  What do we know?
* Words can start on any square
* The next letter in a word can be orthogonal or diagonal to the current letters
* A single letter cannot be used more than once in a word.

For consistency, let's refer to the board on a coordinate system, with each square having an x and a y coordinate.  The origin will be in the top left, with x going horizontal and y being vertical.

The most basic functionality needed will be a function to determine the neighbors of a particular square.  This is a good first step to take.

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





### Path Truncating
The first optimization we should take is to only continue following paths if we know it could result in a word.  When the first four letter of the string are "XKCD" for example, it's fine to stop and move to the next path, because no words in our list start with "XKCD", which should save considerable computation time.

To summarize, our solution is now to search all the paths, but stop once we know a string can't result in a word.  Now we're doing far fewer lookups in the dictionary, but still performing a "dumb" lookup.  Conveniently, there's a data structure that can help us more efficiently test if a word is in our list.

#### Trie
One of the data structures best suited for this task is the [trie](https://en.wikipedia.org/wiki/Trie) [^trie_python].  A trie is an ordered tree structure that, as it is traversed, can efficiently know when a word is not contained in a potential list.  The trie is created by first creating a set of nodes that correspond to the first letters of all the words in the list.  Then, for each of those letters, a node is added for each second letter in the words starting with that original letter.  

This allows the search for a word to proceed letter by letter, similar to how you would look up a word in the dictionary if someone was spelling the word to you.  As soon as you can't find the next letter, you know the word is not contained!

In python, the trie is constructed as a dict.  At the top level, the keys are the first letters of all the words.  At the next level, the keys are the second letters of words and so on.  Additionally, because we want to find words that are contained within other words, there is a special key that signals that this prefix is a word itself.  This makes sure that we both count that word, but also continue searching.

~~~ python
~~~

[^trie_python]: [How to create a TRIE in Python](http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python)
[^blog1]:[How to find list of possible words from a letter matrix [Boggle Solver]](http://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver)
[^blog2]: [Solving the Boggle Game - Recursion, Prefix Tree, and Dynamic Programming](http://exceptional-code.blogspot.com/2012/02/solving-boggle-game-recursion-prefix.html)
[^blog3]: [Solving Boggle boards at scale](https://blog.niallconnaughton.com/2015/12/10/solving-boggle-boards-at-scale/)

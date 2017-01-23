---
layout:     post
title:      "Boggle Revisited: Solver"
date:       2017-1-19 1:00:00
author:     Andrew
header-img: img/boggle_solver/the-maze.jpg
tags:       puzzles programming
---

For starters, if you haven't read my [last post]({{ page.previous.url | prepend: site.baseurl | replace: '//', '/' }}), go ahead and read that before diving in here.  It's not strictly necessary, but it will give you some context.

In my last post discussing Boggle board generation using a genetic algorithm, I skipped over an important part.  Because I wanted to keep my focus on the genetics part of it, I didn't go into details about how I actually scored the boards.  A few people have asked me about the details, so I thought I'd write it down.  If your recreational reading is solely focused on boggle board solving, there are many resources out there for you as well beyond this post[^blog1] [^blog2] [^blog3]

I'll rephrase the rules of Boggle for everyone who may have forgotten them since we last talked.

> Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.

Let's start by talking about the dictionary.  In order to know if we have words, we have to define what a word is.  In this case, I'll be using a public domain word list titled [enable1.txt](http://norvig.com/ngrams/enable1.txt).  It contains approximately 170,000 of the most commonly used words.  There's nothing particularly special about this list, it just happens to be very popular and public domain.

First, it's important to note what we don't know.  We can't know the potential orientation of any word, or it's length.  We also can't know if and when words will be contained in other words.

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

Next, let's think about how we want to efficiently detect words.  Let's brainstorm some approaches.

### Naive
As we traverse through the grid, check if our currently built word is a word in our list.  Keep going until all possible traversals are done.
2. We could check words as we go along and stop when we find a word.
3. We could check words as we go along and stop when our currently string doesn't start any words in our list.

The structure I ended up using for

http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

[^blog1]:[How to find list of possible words from a letter matrix [Boggle Solver]](http://stackoverflow.com/questions/746082/how-to-find-list-of-possible-words-from-a-letter-matrix-boggle-solver)
[^blog2]: [Solving the Boggle Game - Recursion, Prefix Tree, and Dynamic Programming](http://exceptional-code.blogspot.com/2012/02/solving-boggle-game-recursion-prefix.html)
[^blog3]: [Solving Boggle boards at scale](https://blog.niallconnaughton.com/2015/12/10/solving-boggle-boards-at-scale/)

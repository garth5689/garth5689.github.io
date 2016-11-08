---
layout:     post
title:      "Generate Boggle Boards with Genetics"
date:       2016-10-31 17:00:00
author:     "Andrew"
header-img: "img/The_family_of_Laocoon_entwined_in_coils_of_DNA.jpg"
tags:       "puzzles,programming"
---

I recently had a bit of fun working on a puzzle, and learned some interesting things along the way about generic algorithms as well, so I thought I'd share.

Each week, [FiveThirtyEight](http://fivethirtyeight.com) posts a Riddler puzzle for intrepid puzzlers to solve.  On Oct, 14th, this was the [Riddler:](http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/)  
<blockquote>What arrangement of any letters on a Boggle board has the most points attainable?  Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.</blockquote>

There are myriad ways that this type of problem can be tackled, and some of the successful solutions can be seen in the [following week's Ridder](http://fivethirtyeight.com/features/rig-the-election-with-math/).  Personally, I decided to try using a genetic algorithm.  It's something I have heard about quite a bit, but had yet to find a suitable puzzle.

## Genetic Algorithm Background
Per wikipedia:[^wikiga]
<blockquote>A genetic algorithm is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on bio-inspired operators such as mutation, crossover and selection.</blockquote>
<!--break-->

Right...

I'll start by giving a quick background into the actual mechanisms of natural selection and how they relate to the algorithmic kind of selection.

### Population
Both in the natural and computer version, for the fittest to survive, there must be a population to choose from.  In the classic example of Darwin's finches, an initial population of very similar finches was present on the galapagos.  In my more modern puzzle, the population will consist of a group of boggle boards, each of which can be scored individually.

### Selection


#### Fitness[^fitness]
In natural selection, individuals that are most "fit" are more likely to survive and reproduce.  This gives their genes the highest likelihood of being passed on.  In the natural world, this would likely be difficult to measure and depends on many factors.  However, in the algorithmic sense, we can define our own fitness function.  This is how individuals in our population will be evaluated against one another.  I'll define the fitness function to be the total score of the board (given the dictionary at: ...)

### Mating
Just like in real life, in order to pass down

#### Crossover

#### Mutation

![finches]({{ site.baseurl }}/img/Finchadaptiveradiation.png)[^birdimg]

![beaks]({{ site.baseurl }}/img/Darwin's_finches.jpeg)[^beaks]

#### References

Header Image By <a rel="nofollow" class="external free" href="http://wellcomeimages.org/indexplus/obf_images/6c/d2/f0a4468f0181ae48d0e410beeb51.jpg">http://wellcomeimages.org/indexplus/obf_images/6c/d2/f0a4468f0181ae48d0e410beeb51.jpg</a> Gallery: <a rel="nofollow" class="external free" href="http://wellcomeimages.org/indexplus/image/L0020440.html">http://wellcomeimages.org/indexplus/image/L0020440.html</a>, <a href="http://creativecommons.org/licenses/by/4.0" title="Creative Commons Attribution 4.0">CC BY 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=35994175">Link</a>

[^birdimg]: By <a href="//commons.wikimedia.org/w/index.php?title=User:Jmalvin17&amp;action=edit&amp;redlink=1" class="new" title="User:Jmalvin17 (page does not exist)">Jackie malvin</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=40655181">Link</a>

[^wikiga]:[https://en.wikipedia.org/wiki/Genetic_algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm)

[^fitness]:[https://en.wikipedia.org/wiki/Natural_selection#Fitness](https://en.wikipedia.org/wiki/Natural_selection#Fitness)


[^beaks]:<a title="By John Gould (14.Sep.1804 - 3.Feb.1881) [Public domain], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File%3ADarwin's_finches.jpeg"></a>

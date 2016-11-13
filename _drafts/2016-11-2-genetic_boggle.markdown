---
layout:     post
title:      "Generate Boggle Boards with Genetics"
date:       2016-10-31 17:00:00
author:     "Andrew"
header-img: "img/The_family_of_Laocoon_entwined_in_coils_of_DNA.jpg"
tags:       "puzzles,programming"
---

I recently had a bit of fun working on a puzzle, and learned some interesting things along the way about generic algorithms as well, so I thought I'd share.

Each week, [FiveThirtyEight](http://fivethirtyeight.com) posts a Riddler puzzle for intrepid puzzlers to solve.  On Oct. 14th, this was the [Riddler:](http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/)  
<blockquote>What arrangement of any letters on a Boggle board has the most points attainable?  Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.</blockquote>

There are many ways to tackle this problem, and some of the successful solutions can be seen in the [following week's Ridder](http://fivethirtyeight.com/features/rig-the-election-with-math/).  I decided that it would be interesting to use a genetic algorithm.  It's something I have heard about quite a bit, but had yet to find a suitable application for.

<!--break-->

## Genetic Algorithm Background
Per wikipedia:[^wikiga]
<blockquote>A genetic algorithm is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA). Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on bio-inspired operators such as mutation, crossover and selection.</blockquote>

I'll translate.  For problems where it is difficult to test every permutation, emulating natural selection can help find a good enough solution.  The basic process is:

1. Generate many possible individuals (Population)
2. Score them (Fitness)
3. Select the most "fit" individuals (Selection)
4. Intermixing those (Mating)
5. Introduce random mutations (Mutation)
6. Repeat 2-4.

Performing this process creates many successive generations of the population.  By continuously pruning the poor solutions and introducing random mutations, the population will become more "fit" overall.

Because I can't possibly search all possible combinations of boards, a genetic algorithm may be appropriate.  I can a population of random boggle boards and see how they score.  The highest scoring ones will be mixed and mutated, hopefully uncovering even higher scoring boards.  The goal is that over enough generations, the low scoring boards will be reduced in the gene pool, and only the highest scoring ones will survive.

### Population

The population is the group of individuals that's evolving.  In nature, this could be a species of birds on an isolated island,

Natural selection can only work when there is a population of individuals to evolve.  For example, when a similar group of birds migrate over many generations to a new climate, this is the base population.  Genetic variation may already exist among this population, and I simulate that by introducing some randomization into my initial population.

For solving this puzzle, the population will consist of individual Boggle boards, each of which can be scored.  The size and initial diversity of our population can play a large role in the final solution as well.  In this case, each board will start as a completely random string of 16 letters:  
`SERSPATGLINESERS`  
The board has been 'flattened' for easier processing.  For example, an individual board may look like this:
![boggle board]({{ site.baseurl }}/img/boggle_individual.jpg)
and the population may look something like this:
![boggle board population]({{ site.baseurl }}/img/boggle_population.jpg)

{% highlight python %}
def generate_random_boggle_letters():
    return random.choice(string.ascii_lowercase)

toolbox.register("rand_letter",generate_random_boggle_letters)
toolbox.register("individual",
                 tools.initRepeat,
                 creator.Individual,
                 toolbox.rand_letter,
                 n=SIZE**2)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)
{% endhighlight %}


#### Fitness[^fitness]
In natural selection, individuals that are most "fit" are more likely to survive and reproduce.  This gives their genes the highest likelihood of being passed on.  In the natural world, this would likely be difficult to measure and depends on many factors.  However, in the algorithmic sense, we can define our own fitness function.  This is how individuals in our population will be evaluated against one another.  I'll define the fitness function to be the total score of the board (given the dictionary at: ...)

### Selection
Once the most fit individuals have been determined, some of them must reproduce to produce the next generation.  In my solution, I used [tournament selection](https://en.wikipedia.org/wiki/Tournament_selection).  This solutions pits several individuals against each other, where the probably of the most fit individual being selected from each tournament is one of the inputs to the algorithm.  


### Mating
Just like in real life, in order to pass down traits to the next generation, individuals must reproduce.  For our puzzle, I'll be using [two-point crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_crossover).  This involves selecting two points on the "gene sequence" and then switching the middle sections between the selected individuals.  In the puzzle, it may look something like this:
`SERS``PATGLIN``ESERS`  
`ERTS``RGUJOSA``CELPS`  

`SERS``RGUJOSA``ESERS`  
`ERTS``PATGLIN``CELPS`  
![crossover_picture](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/TwoPointCrossover.svg/226px-TwoPointCrossover.svg.png)[^crossoverpic]

#### Mutation
Random mutations of the genome are the mechanism for natural selection to

![finches]({{ site.baseurl }}/img/Finchadaptiveradiation.png)[^birdimg]

![beaks]({{ site.baseurl }}/img/Darwin's_finches.jpeg)[^beaks]

## Solution

## References

Header Image By <a rel="nofollow" class="external free" href="http://wellcomeimages.org/indexplus/obf_images/6c/d2/f0a4468f0181ae48d0e410beeb51.jpg">http://wellcomeimages.org/indexplus/obf_images/6c/d2/f0a4468f0181ae48d0e410beeb51.jpg</a> Gallery: <a rel="nofollow" class="external free" href="http://wellcomeimages.org/indexplus/image/L0020440.html">http://wellcomeimages.org/indexplus/image/L0020440.html</a>, <a href="http://creativecommons.org/licenses/by/4.0" title="Creative Commons Attribution 4.0">CC BY 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=35994175">Link</a>

[^birdimg]: By <a href="//commons.wikimedia.org/w/index.php?title=User:Jmalvin17&amp;action=edit&amp;redlink=1" class="new" title="User:Jmalvin17 (page does not exist)">Jackie malvin</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=40655181">Link</a>

[^wikiga]:[https://en.wikipedia.org/wiki/Genetic_algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm)

[^fitness]:[https://en.wikipedia.org/wiki/Natural_selection#Fitness](https://en.wikipedia.org/wiki/Natural_selection#Fitness)

[^beaks]:<a title="By John Gould (14.Sep.1804 - 3.Feb.1881) [Public domain], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File%3ADarwin's_finches.jpeg"></a>

[^crossoverpic]:By <a href="//commons.wikimedia.org/w/index.php?title=User:R0oland&amp;action=edit&amp;redlink=1" class="new" title="User:R0oland (page does not exist)">R0oland</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=29950354">Link</a>

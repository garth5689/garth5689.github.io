---
layout:     post
title:      "Generate Boggle Boards with Genetics"
date:       2016-10-31 17:00:00
author:     "Andrew"
header-img: "img/The_family_of_Laocoon_entwined_in_coils_of_DNA.jpg"
tags:       "puzzles programming"
---

I recently had a bit of fun working on a puzzle, and learned some interesting things along the way about generic algorithms as well, so I thought I'd share.

Each week, [FiveThirtyEight](http://fivethirtyeight.com) posts a Riddler puzzle for intrepid puzzlers to solve.  On Oct. 14th, this was the [Riddler:](http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/)  
<blockquote>What arrangement of any letters on a Boggle board has the most points attainable?  Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.</blockquote>

There are many ways to tackle this problem, and some of the successful solutions can be seen in the [following week's Ridder](http://fivethirtyeight.com/features/rig-the-election-with-math/).  I decided that it would be interesting to use a genetic algorithm.  It's something I have heard about quite a bit, but had yet to find a suitable application for.

<!--break-->

#### Code
I will be including code snippets throughout this post, and the full code can be found here:.  I used Python 3.5, and the [deap toolbox](https://github.com/DEAP/deap) for the genetic algorithm part.

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

A population is generally a group of organisms of the same species, in a particular area, that have a chance to breed.  For example, this could be a species of birds in the Caribbean islands, or a species of tree in the pacific northwest.  In order for natural selection to apply, the individuals in the population must be capable of reproducing amongst themselves.

The population for this puzzle might not be as intuitive as a flock of birds.  It will consist of individual Boggle boards, each of which can be scored.  An individual board looks like this:
![boggle board]({{ site.baseurl }}/img/boggle_individual.jpg)
and the population may look something like this:
![boggle board population]({{ site.baseurl }}/img/boggle_population.jpg)

### Fitness[^fitness]
In the natural world, each individual does not have an equal chance to pass their genes onto the next generation.  Fitness is a way to quantify the probability that an individual will contribute to the genes of subsequent generations.  Individuals that have the best chance of reproducing are the most "fit" (hence, "survival of the fittest").  The most fit individuals are not necessarily the strongest, fastest or biggest.  A particular gene that controls coloring could have a sizable impact on reproduction if it provides great camouflage.

In the natural world, fitness can be tough to measure for an individual.  The great thing is that Boggle boards canm be scored to have a definitive best one.  My fitness function will be the total score of all words that can be found in a board.  After all, this is the goal of the puzzle, so this should be maximized.

The actual function to perform the maximum is probably worthy of a post in itself.  However, to not distract from the interesting genetic stuff, you can check it out here:

### Selection
Once the population has been evaluated for fitness, some of the individuals will reproduce to create the next generation.  Because we have control algorithmically, this can be done in any number of ways.  We could select via any of these methods:  

* highest scoring individuals
* randomly
* tournament selection[^tourn_select] [^deap_tourn]
* roulette selection

Because I'm not experienced with these type of algorithms, I picked tournament selection to use.  This

### Mating
In order to pass on the genes that lead to their success, individuals must mate.  In nature, this takes on many different forms, but ultimately results in a new chromosome which is a combination of the parents' chromosomes.  For our algorithm, this is done via two point crossover[^two_pc].  Two point crossover basically selects two points along the chromosome and then swaps the intermediate sections to create two new chromosomes.

{::options parse_block_html="true" /}
<p align="center">
<img style="display:inline-block;vertical-align:top;"  src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/TwoPointCrossover.svg/226px-TwoPointCrossover.svg.png" />
[^crossoverpic]
</p>
{::options parse_block_html="false" /}

In our algorithm, this may look like this:  

<p><div style="color:crimson;background-color:lightpink;display: inline-block;">ERTSRGUJOSACELPS</div></p>
<p><div style="color:blue;background-color:powderblue;display: inline-block;">SERSPATGLINESERS</div></p>

<p><div style="color:crimson;background-color:lightpink;display: inline-block;">ERTS</div>  
<div style="color:blue;background-color:powderblue;display: inline-block;">PATGLIN</div>
<div style="color:crimson;background-color:lightpink;display: inline-block;">CELPS</div></p>

<p><div style="color:blue;background-color:powderblue;display: inline-block;">SERS</div>  
<div style="color:crimson;background-color:lightpink;display: inline-block;">RGUJOSA</div>
<div style="color:blue;background-color:powderblue;display: inline-block;">ESERS</div></p>

#### Mutation
Random mutations are the second mechanism for introducing changes into the population.  After the offspring has been produced, small mutations are introduced into the population.  Naturally this occurs through errors in DNA reproduction and damage to the DNA sequence.  One natural example of this is Darwin's finches.  Darwin observed that many seemingly similar birds had different beaks that allowed them an advantage for eating a particular food source.  These beak differences may have emerged through random mutations that allowed birds access to those food sources, thus a better chance to survive and reproduce.

{::options parse_block_html="true" /}
<p align="center">
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/Darwin's_finches.jpeg" />
[^beaks]
</p>
{::options parse_block_html="false" /}

Algorithmically, there are many ways to approach this, but the mutation must be explicitly defined.  I've chosen to mutate the grid by swapping letters for another random letter with a supplied probability.  This functionally means that each letter has a small change to change to a completely random new letter.  The aggressiveness of the mutations depend on the supplied probability.  If a small probability is used, large changes in the offspring are unlikely.

## Solution

In the code, each board will be represented as a flattened string of 16 letters for easier processing:
`SERSPATGLINESERS`  

Below is the code to set up the algorithm and create the initial population.  

{% highlight python %}
import random
from deap import base, creator, tools, algorithms

SIZE = 4

def generate_random_boggle_letters():
    return random.choice(string.ascii_lowercase)

# First the overall simulation needs to be set up.
# The creator is used to set up the weights for our algorithm.
# Because board score is the only fitness,
# and we want that to be maximized, the weight will be 1.
# A weight of -1 would indicate that we want to minimize fitness
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list ,fitness = creator.FitnessMax)


toolbox = base.Toolbox()

# Seed the initial population with random Boggle boards
toolbox.register("rand_letter",generate_random_boggle_letters)
toolbox.register("individual",
                 tools.initRepeat,
                 creator.Individual,
                 toolbox.rand_letter,
                 n=SIZE**2)
toolbox.register("population",tools.initRepeat,list,toolbox.individual)
{% endhighlight %}

## References

Header Image By <a rel="nofollow" class="external free" href="http://wellcomeimages.org/indexplus/obf_images/6c/d2/f0a4468f0181ae48d0e410beeb51.jpg">http://wellcomeimages.org/indexplus/obf_images/6c/d2/f0a4468f0181ae48d0e410beeb51.jpg</a> Gallery: <a rel="nofollow" class="external free" href="http://wellcomeimages.org/indexplus/image/L0020440.html">http://wellcomeimages.org/indexplus/image/L0020440.html</a>, <a href="http://creativecommons.org/licenses/by/4.0" title="Creative Commons Attribution 4.0">CC BY 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=35994175">Link</a>

[^birdimg]: By <a href="//commons.wikimedia.org/w/index.php?title=User:Jmalvin17&amp;action=edit&amp;redlink=1" class="new" title="User:Jmalvin17 (page does not exist)">Jackie malvin</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=40655181">Link</a>

[^wikiga]:[https://en.wikipedia.org/wiki/Genetic_algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm)

[^fitness]:[https://en.wikipedia.org/wiki/Natural_selection#Fitness](https://en.wikipedia.org/wiki/Natural_selection#Fitness)

[^beaks]:<a title="By John Gould (14.Sep.1804 - 3.Feb.1881) [Public domain], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File%3ADarwin's_finches.jpeg"></a>

[^crossoverpic]:By <a href="//commons.wikimedia.org/w/index.php?title=User:R0oland&amp;action=edit&amp;redlink=1" class="new" title="User:R0oland (page does not exist)">R0oland</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=29950354">Link</a>

[^tourn_select]:[https://en.wikipedia.org/wiki/Tournament_selection](https://en.wikipedia.org/wiki/Tournament_selection)
[^deap_tourn]:[http://deap.readthedocs.io/en/master/api/tools.html#deap.tools.selTournament](http://deap.readthedocs.io/en/master/api/tools.html#deap.tools.selTournament)
[^two_pc]:[https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_crossover)

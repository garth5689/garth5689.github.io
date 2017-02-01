---
layout:     post
title:      Generating Boggle Boards with Genetics
date:       2016-12-16 1:00:00
author:     Andrew
header-img: img/posts/genetic_boggle/The_family_of_Laocoon_entwined_in_coils_of_DNA.jpg
tags:       puzzles programming
header-credit: "Wellcome Images CC BY 4.0, via Wikimedia Commons"
---

Each week, [FiveThirtyEight](http://fivethirtyeight.com) posts a puzzle call the Riddler.  On Oct. 21st, this was the [Riddler](http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/):

> What arrangement of any letters on a Boggle board has the most points attainable?  Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.

I had a lot of fun solving this puzzle, and I learned a lot as well, so I decided to share.  The approach I took was to use a genetic algorithm, which mimics the mechanics of natural selection.  In the past, I hadn't found a good application, but wanted to give it a shot.  You shouldn't need in-depth knowledge of programming, genetics, or Boggle to learn something!
<!--break-->

## Genetic Algorithm Background
> Natural selection is the process where organisms with favourable traits are more likely to reproduce. In doing so, they pass on these traits to the next generation. Over time this process allows organisms to adapt to their environment. This is because the frequency of genes for favourable traits increases in the population. [^wikins]

> A genetic algorithm is a metaheuristic inspired by the process of natural selection. Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on bio-inspired operators such as mutation, crossover and selection. [^wikiga]

It may not seem obvious at first how this could be used to generate high scoring Boggle boards, but sit tight!  Generally, natural selection works via the following process:

1. Start with a population of possible solutions ([population](#population))
2. Evaluate them to determine which ones are the best (most fit) ([fitness](#fitness))
3. The most fit individuals survive ([selection](#selection))
4. The surviving individuals reproduce ([mating](#mating))
5. Random mutations are introduced into the gene pool ([mutation](#mutation))
6. Repeat 2-5 for many generations.

Ok, now for the fun stuff!  Generating all the possible boggle boards would be practically impossible, so let's pick a smaller number, say a million.  If we scored those boards, we should see a wide range of scores.  Now let's take the high scoring boards, and create some new boards by swapping sections of letters amongst them.  This leaves us with some new boards that have potentially high scoring sections in them.  Lastly, let's change a few letters randomly to keep things fresh.  Additionally, this may open some new avenues for higher scores.  As this process continues, low scoring boards should be eliminated and only high scoring ones will remain (hopefully).

P.S.: If you would like a semi-modern example of natural selection, check out the [peppered moth](https://en.wikipedia.org/wiki/Peppered_moth_evolution).

#### Code
The code for this simulation can be found [here](https://github.com/andrewzwicky/puzzles/tree/master/FiveThirtyEightRiddler/2016-10-21).  Python 3.5, the [deap toolbox](https://github.com/DEAP/deap) and [matplotlib](http://matplotlib.org/) were the tools used.

### Population {#population}

A population is a group of organisms of the same species, in a particular area, that are capable of reproducing.  For example, this could be a species of birds on an island, or a species of tree in a forest.  Within the population, an individual's physical traits are controlled by their genome.  Genomes are broken down into genes, which combine to control the physical traits of the individual.  You may be familiar with some traits that are controlled by genes, such as eye color, hair color and blood type.

For our population it makes sense to just have a whole bunch of boards.  Unlike nature, we have complete control over the number of individuals and the initial population.  We are seeking the highest scoring individual board, so it makes sense for the population to be a large group of boards.  The larger the population, the more potential areas that could be explored, with the limiting factor being computation time.


<p align="center">
Here is an example individual:<br>
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/boggle_individual.jpg" />
</p>

<p align="center">
And here's an example population:<br>
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/boggle_population.jpg" />
</p>


Each board can be represented by a 16 character string, e.g. `SERSPATGLINESERS`.  This string can be thought of as our individual's genome, and each individual letter can be thought of as a gene.  We will be manipulating the genes to get new individuals.

Because we don't know what kind of solution we might get, the initial population will be created randomly.  Once the population is created, we need to determine which solutions should survive and reproduce.

### Fitness {#fitness}
In the natural world, each individual does not have an equal chance to pass their genes onto the next generation.  Fitness is the term to describe the probability that an individual will contribute to the genes of subsequent generations.  Individuals that have the best chance of reproducing are the most "fit" (hence, "survival of the fittest").  The most fit individuals are not necessarily the strongest, fastest or biggest.  For example, a particular gene that controls coloring could have a sizable impact on reproduction if it provides great camouflage.

In the natural world, fitness is not as obvious as a single number.  One great thing about our problem is that Boggle boards can be scored easily, which gives each board a very clear fitness value.  Our fitness function will be the total score of all possible words in the board.  After all, this is the goal of the puzzle, so it makes sense to try to maximize this value.

The actual function to perform the scoring is probably worthy of a post in itself, however I think it would be too big of an aside.  It can be found in the code [here](https://github.com/andrewzwicky/puzzles/blob/master/FiveThirtyEightRiddler/2016-10-21/recurse_grid.pyx).

<p align="center">
Here's an animation showing a particular board being solved:<br>
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/path_animation.gif" height="300" width="300"/>
</p>

### Selection {#selection}
Once the population has been evaluated for fitness, some of the individuals will reproduce to create the next generation.  In nature, the individuals that would breed would be based on their fitness, mainly the ones that survive and attract a mate.  For this problem, we'll be using tournament selection[^tourn_select][^deap_tourn].  In tournament selection, several individuals are pulled randomly from the population, where they participate in a "tournament".  One individual is picked from the tournament, and individuals with higher fitness are more likely to be picked.  

### Mating {#mating}
In order to pass on the genes that lead to their success, individuals must mate.  In nature, this takes on many different forms, but ultimately results in a new genome which is a combination of the parents' genome.  For our algorithm, this is done via two point crossover[^two_pc].  Two point crossover selects two points along the genome and then swaps the intermediate sections to create two new chromosomes.

{::options parse_block_html="true" /}
<p align="center">
<img style="display:inline-block;vertical-align:top;"  src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/TwoPointCrossover.svg/226px-TwoPointCrossover.svg.png" />
[^crossoverpic]
</p>
<p align="center">
In our algorithm, this may look like this:<br>  
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/crossover.png" />
</p>
{::options parse_block_html="false" /}

### Mutation {#mutation}
Random mutations are the second mechanism for introducing changes into the population.  After the offspring has been produced, small mutations are introduced into the population.  Naturally this occurs through errors in DNA reproduction and damage to the DNA sequence.  An example of this is Charles Darwin's finches.  In the Galapagos Islands, Darwin discovered that many seemingly similar finches were actually different species.  These different species had developed many different beak shapes that allowed them access to new food sources.  Some beaks are sharp and pointed to catch insects, while others are broad to better eat seeds from cacti.  As these beaks developed, it gave each species access to the new food source, and a better chance of survival.

{::options parse_block_html="true" /}
<p align="center">
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/Darwin's_finches.jpeg" />
[^beaks]
</p>
{::options parse_block_html="false" /}


Algorithmically, there are many ways to approach this, but the mutation must be explicitly defined.  I've chosen to give each letter a small probability to mutate into another random letter.  The aggressiveness of the mutation depend on the probability.  It's likely there are other mutations that would work as well, including swapping letters, or additionally shifting letters.  Because there is no meaningful link between letters, I chose to mutate the letter randomly.

## Solution
Gathering this all together, 1 million boards were generated and evolved over 100 generations.  Without specific knowledge about what makes a high scoring Boggle board, we've been able to find some very high scoring boards!  Likely next steps would be to continue to refine the parameters and probabilities used to further optimize the result.  For now though, I'm pretty happy with the result.  The final board has a score of 3001:
<p align="center">
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/final_board.png" height="300" width="300"/>
</p>

<p align="center">
Here is how the boards evolved over the generations:<br>
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/scores_over_generation.png" />
</p>

<p align="center">
And here are all of the generations:<br>
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/posts/genetic_boggle/evolve_animation.gif" height="300" width="300"/>
</p>  

More solutions can be seen at the end of the [Oct. 28th Ridder](http://fivethirtyeight.com/features/rig-the-election-with-math/).

## References
[^birdimg]: By <a href="//commons.wikimedia.org/w/index.php?title=User:Jmalvin17&amp;action=edit&amp;redlink=1" class="new" title="User:Jmalvin17 (page does not exist)">Jackie malvin</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/4.0" title="Creative Commons Attribution-Share Alike 4.0">CC BY-SA 4.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=40655181">Link</a>

[^wikiga]:[https://en.wikipedia.org/wiki/Genetic_algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm)

[^beaks]:<a title="By John Gould (14.Sep.1804 - 3.Feb.1881) [Public domain], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File%3ADarwin's_finches.jpeg"></a>

[^crossoverpic]:By <a href="//commons.wikimedia.org/w/index.php?title=User:R0oland&amp;action=edit&amp;redlink=1" class="new" title="User:R0oland (page does not exist)">R0oland</a> - <span class="int-own-work" lang="en">Own work</span>, <a href="http://creativecommons.org/licenses/by-sa/3.0" title="Creative Commons Attribution-Share Alike 3.0">CC BY-SA 3.0</a>, <a href="https://commons.wikimedia.org/w/index.php?curid=29950354">Link</a>

[^tourn_select]:[https://en.wikipedia.org/wiki/Tournament_selection](https://en.wikipedia.org/wiki/Tournament_selection)

[^deap_tourn]:[http://deap.readthedocs.io/en/master/api/tools.html#deap.tools.selTournament](http://deap.readthedocs.io/en/master/api/tools.html#deap.tools.selTournament)

[^two_pc]:[https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_crossover](https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Two-point_crossover)

[^wikins]:[https://simple.wikipedia.org/wiki/Natural_selection](https://simple.wikipedia.org/wiki/Natural_selection)

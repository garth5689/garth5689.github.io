---
layout:     post
title:      Generate Boggle Boards with Genetics
date:       2016-10-31 17:00:00
author:     Andrew
header-img: img/The_family_of_Laocoon_entwined_in_coils_of_DNA.jpg
tags:       puzzles programming
---

Recently, I had a bit of fun solving a puzzle, so I decided to share it.

Each week, [FiveThirtyEight](http://fivethirtyeight.com) posts a puzzle call the Riddler.  Here is the [Oct. 21st Riddler](http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/)

> What arrangement of any letters on a Boggle board has the most points attainable?  Boggle is played with a 4-by-4 grid of letters. Points are scored by finding strings of letters — connected in any direction, horizontally, vertically or diagonally — that form valid words at least three letters long. Words 3, 4, 5, 6, 7 or 8 or more letters long score 1, 1, 2, 3, 5 and 11 points, respectively.

I decided to approach this puzzle using a genetic algorithm, using an algorithm to mimic natural selection.  This is an approach I don't have much experience with, but wanted to give it a shot.  Prior knowledge of programming, genetics, or Boggle isn't required.  Additionally, I hope everyone will be able to skip the code and still learn something! I will be including code snippets throughout this post, and the full code can be found here:.  Python 3.5 and the [deap toolbox](https://github.com/DEAP/deap) were the primarly tools used.
<!--break-->

## Genetic Algorithm Background
> Natural selection is the process where organisms with favourable traits are more likely to reproduce. In doing so, they pass on these traits to the next generation. Over time this process allows organisms to adapt to their environment. This is because the frequency of genes for favourable traits increases in the population. [^wikins]

> A genetic algorithm is a metaheuristic inspired by the process of natural selection. Genetic algorithms are commonly used to generate high-quality solutions to optimization and search problems by relying on bio-inspired operators such as mutation, crossover and selection. [^wikiga]

It may not seem obvious at first how this could be used to generate high scoring boards, but sit tight!  Natural selection typically works through the following steps, which I'll elaborate on later.

1. Start with a population of possible solutions ([population](#population))
2. Evaluate them to determine which ones are the best (most fit) ([fitness](#fitness))
3. Select the most fit individuals ([selection](#selection))
4. The selected individuals reproduce ([mating](#mating))
5. Random mutations are introduced into the gene pool ([mutation](#mutation))
6. Repeat 2-5 for many generations.

If you would like a modern example of natural selection, check out the [peppered moth](https://en.wikipedia.org/wiki/Peppered_moth_evolution).

Now for the fun stuff!  Because scoring all possible combinations of boards is practically impossible, we'll need another solution.  

Instead, let's think about the following.  First, we could generate and score a few hundred boards.  Once they have been scored, new boards can be created by combining portions of the higher scoring boards.  Lastly, small disturbances can be introduced to the resulting boards.  At the end of this process, we will have a new population of boards based primarily on the highest scoring boards from the previous generation.  The goal is that over enough generations, the lower scoring boards will be reduced in the population and we will be left with a very high scoring board!

### Population {#population}

A **population** is a group of organisms of the same species, in a particular area, that are capable of reproducing.  For example, this could be a species of birds on an island, or a species of tree in a forest.  Within the population, an individual's physical traits are controlled by their **genome**.  Genomes are broken down into **genes**, which combine to control the physical traits of the individual.  Everyone is probably familiar with some traits that are controlled by genes, such as eye color, hair color and blood type.

When thinking about the population for our puzzle, it's not quite as intuitive as a flock of birds or forest of trees.  Additionally, unlike nature, we have complete control over the number of individuals and the initial population.  We are seeking the highest scoring individual board, so it makes sense for the population to be a big group of boards.

| This is an individual board:   |      ![boggle board]({{ site.baseurl }}/img/boggle_individual.jpg)      |



which will be represented by a 16 character string: `SERSPATGLINESERS`.  This string can be roughly translated to our Boggle board's genome, and each individual letter can be thought of as a gene.
and the population may look something like this:
![boggle board population]({{ site.baseurl }}/img/boggle_population.jpg)

Because we don't know what kind of solution we might get, it makes sense to create the initial population randomly.  If there is some prior knowledge about good solutions, those can be used as seed values as well.  Once the population is created, we need to determine which solutions should continue on.


{% highlight python %}
import random
from deap import base, creator, tools, algorithms

# Define the size of the board (assume square)
# Start with standard 4x4 board
SIZE = 4

def generate_random_boggle_letters():
    return random.choice(string.ascii_lowercase)

# First the overall simulation needs to be set up.
# The creator is used to set up the weights for our algorithm.
# Because board score is the only fitness,
# and we want that to be maximized, the weight will be 1.
# A weight of -1 would indicate that we want to minimize.
creator.create("BoggleFitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness = creator.BoggleFitnessMax)

# toolbox contains the evolutionary operators.
# This is how parameters for the algorithm are added
# and removed.
toolbox = base.Toolbox()

# Register the function to generate random letters
toolbox.register("rand_letter",generate_random_boggle_letters)

# Register the individual.  This will be composed of repeating the
# toolbox.rand_letter function n times.  In this case n will be 16, because
# we have a 4x4 board.
toolbox.register("individual",
                 tools.initRepeat,
                 creator.Individual,
                 toolbox.rand_letter,
                 n=SIZE**2)
# Register the population. The population will be composed of repeating individuals
toolbox.register("population",tools.initRepeat,list,toolbox.individual)

# Set the intial population to 200 boards.
pop = toolbox.population(n=200)
{% endhighlight %}

### Fitness[^fitness] {#fitness}
In the natural world, each individual does not have an equal chance to pass their genes onto the next generation.  Fitness is the term to describe the probability that an individual will contribute to the genes of subsequent generations.  Individuals that have the best chance of reproducing are the most "fit" (hence, "survival of the fittest").  The most fit individuals are not necessarily the strongest, fastest or biggest.  For exampl, a particular gene that controls coloring could have a sizable impact on reproduction if it provides great camouflage.

In the natural world, fitness is not as obvious as a single number.  One great thing about our problem is that Boggle boards can be scored easily, which gives each board a very clear fitness value.  Our fitness function will be the total score of all possible words in the board.  After all, this is the goal of the puzzle, so it makes sense to try to maximize this value.

The actual function to perform the scoring is probably worthy of a post in itself, however I think it would be too big of an aside.  It can be found in the code.

{% highlight python %}
toolbox.register("evaluate",solve_list)
{% endhighlight %}

### Selection {#selection}
Once the population has been evaluated for fitness, some of the individuals will reproduce to create the next generation.  In nature, the individuals that would breed would be based on their fitness, mainly the ones that survive and attract a mate.  In our case, we have complete control over this selection process.  For this problem, we'll be using tournament selection[^tourn_select][^deap_tourn].  In tournament selection, several individuals are pulled randomly from the population, where they participate in a "tournament.  One individual is picked froim the group based on their relative fitness values.  Individuals with higher fitness are more likely to be picked, but it's possible that any individual can make it out.

{% highlight python %}
toolbox.register("select",tools.selTournament, tournsize = 20)
{% endhighlight %}

### Mating {#mating}
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

{% highlight python %}
toolbox.register("mate", tools.cxTwoPoint)
{% endhighlight %}

### Mutation {#mutation}
Random mutations are the second mechanism for introducing changes into the population.  After the offspring has been produced, small mutations are introduced into the population.  Naturally this occurs through errors in DNA reproduction and damage to the DNA sequence.  One natural example of this is Charles Darwin's finches.  In the Galapagos Islands, Darwin discovered that many seemingly similar finches were actually different species.  These different species had actually developed many different beak shapes that allowed them access to new food sources.  Some beaks are sharp and pointed to catch insects, while others are broad to eat seeds from cacti.  As these beaks developed, it gave each new species access to the new food source, and a better chance of survival.  It's likely that there were unsuccessful beak mutations as well that were not favorable to reproduction.

{::options parse_block_html="true" /}
<p align="center">
<img style="display:inline-block;vertical-align:top;"  src="{{ site.baseurl }}/img/Darwin's_finches.jpeg" />
[^beaks]
</p>
{::options parse_block_html="false" /}

Algorithmically, there are many ways to approach this, but the mutation must be explicitly defined.  I've chosen to give each letter a small probability to mutate into another random letter.  The aggressiveness of the mutation depend on the supplied probability.  If a small probability is used, it's likely that only a few, if any letters will change.  There are likely other mutations that would work as well, including swapping letters, or just shifting letters.  Because there is no meaningful link between letters, I chose to mutate the letter randomly.

{% highlight python %}
def mutate_grid(individual, indpb):   
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = generate_random_boggle_letters()

    return individual,

toolbox.register("mutate", mutate_grid, indpb = 0.15)
{% endhighlight %}

## Solution



Below is the code to set up the algorithm and create the initial population.  



Many more successful solutions can be seen in the [Oct. 28th Ridder](http://fivethirtyeight.com/features/rig-the-election-with-math/).

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

[^wikins]:[https://simple.wikipedia.org/wiki/Natural_selection](https://simple.wikipedia.org/wiki/Natural_selection)

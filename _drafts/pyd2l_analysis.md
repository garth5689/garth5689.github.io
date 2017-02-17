---
layout:     post
title:      "E-Sports Betting Analysis"
date:       2014-8-12 12:00:00
author:     Andrew
header-img: img/posts/pyd2l/keyboard_header.jpg
header-credit: https://unsplash.com/@otenteko
tags:       programming gaming
---

# Background
This was a bit of experimenting that I did back in 2014.  At the time, I was very intrigued by a certain video game called [Dota 2](https://en.wikipedia.org/wiki/Dota_2).  In addition to the gameplay, there was (and probably still is) a healthy market for betting virtual items from the game on competitive matches.  The game is a 5v5 team game, and the competitive scene involves many teams will full-time professional players.

# Betting Setup
The betting was set up where individuals could wager up to 4 virtual items on a team to win a particular match.  The format was [parimutuel betting](https://en.wikipedia.org/wiki/Parimutuel_betting), where the odds are determined as the bettors place their bets.  Only when betting is closed are the final odds calculated.
<!--break-->

5/22/2014: dota2lounge now uses a different method for calculating payouts and bets, based on the steam marketplace value for the items. Means a lot of this only applies to the previous method for betting. It was still fun, but it may not be as useful if anyone was going to bet based on it. My sample includes matches #14-3098 excluding games where there was no winner on dota2lounge.


# Winner Predictions
My first question was, how good is the crowd at predicting a winner?  This plot groups the matches by the crowd odds of the favorite, and then for each group of matches, calculates the percentage of matches that were won by the favorite. Also on this plot is a 1-1 line, which the bars would overlay if the crowd was perfect at predicting winner odds (in the long run).

For example, in matches where the favorite's odd were between 75 and 78, the favorite won 76.8% of the time. The full results are below the plot.


# Potential Sources of Error
Odds are fluctuating while bets are being placed.
Small sample size

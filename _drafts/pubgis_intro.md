---
layout:     post
title:      ""
date:       2018-03-23 16:00:00
author:     Andrew
header-img: img/posts/pubgis_1/hendrik-morkel-580658-unsplash.jpg
header-credit: https://unsplash.com/@hendrikmorkel
tags:       programming PUBG 
---

Often when I share that I do programming as a hobby, I get the question "What kinds of stuff do you work on?".  My reply is usually pretty unsatisfying, and along the lines of "Just small projects here and there" or "Math puzzles and riddles".  I often don't have a nicely contained project that I can just point to.

Hopefully, the next few posts can give some insight into what types of things can be by hobby programming and don't require a large dedicated team to accomplish.  What I ended up creating was a small program that other could use to track their player's positions during matches of the video game PUBG.  The program was designed to be used alongside play and it would track the player's position through analyzing the player's minimap throughout the game.

My main motivation for writing this is to just share something I'm proud of.  I worked for several months on this project, and I know that at least some others online got some use out of it.  Although it's outdated now, it served a nice purpose and provided some learning outside of my normal programming comfort zone.

### Background
Before I get too far into the details, there's some important background information about the problem that everyone should be aware of.  At the time when I started the project, I was playing a lot of [PlayerUnknown's Battlegrounds (PUBG)](https://en.wikipedia.org/wiki/PlayerUnknown%27s_Battlegrounds).  PUBG is a first person shooter (FPS), where 100 players are dropped onto an island, where the goal is to gather weapons and eliminate all the other players.  It's a Hunger Games (or Battle Royale) type game, where the last person standing is the winner.  At the time, there was no ability to re-watch games, and limited statistics about each game, and no path information about where you went throughout the game.  Mostly as a curiosity, I wondered what my path around the island might look like for each game.

When playing PUBG, there is a small minimap in the lower right corner of the screen that shows a small amount of context, i.e. your immediate surroundings.  This map is useful for showing nearby buildings, or where your teammates are, but is zoomed in enough that it can't show you the entire map.  The whole map can be brought up, which allows your team to plan the next move.

The minimap often contains visual information such as teammates, game boundaries or danger zones as they appear.  This means that other information can make the minimap look differently, even while you may be in the same position.

### Where To Start
As I am writing this long past the time I was working on it, some details may be fuzzy.  I do remember that when I first started, it was easy to exhaust any potential official source of getting this data.  At the time, there were no replay files stored, no API to get match information, and no official statistics.

For position information, I was basically left with the minimap in the corner of the screen to work with.  But what the hell, why not try it?  At this point, I was skeptical that any consistently useful information would be able to be extracted from the minimap because 
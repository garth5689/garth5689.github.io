---
layout:     post
title:      "Laser Escape⏱️"
date:       2018-07-01 16:00:00
author:     Andrew
header-img: img/posts/laser_escape/hao-wang-217034-unsplash.jpg
header-credit: https://unsplash.com/@danranwanghao
tags:       programming electronics raspberry_pi
---

Hey everyone, I'm back after a long break to share my latest project!

For the past few months, I've been working to construct a **laser escape maze** in my basement.  Yep, you read that correctly, and I'm super excited to finally have it finished!  I'm going to share a little bit about how I built the room and what I learned along the way.

## Background


This one may take a little while to explain, so I'll start from the beginning.  Think back to your favorite heist movie.  If it's a recent one, it's possible there's a scene where the thieves are gracefully moving through the laser beams of a security system to get to the riches.  <!--break--> If you can't think of one off the top of your [head](https://www.youtube.com/watch?v=aEawL9PYh-k), [here](https://www.youtube.com/watch?v=w0Wwrb4c4uE) [are](https://www.youtube.com/watch?v=1g9QEQrHOMw) [some](https://www.youtube.com/watch?v=mr834Cs9ncs) [examples](https://www.youtube.com/watch?v=KX2_LCUkhDs).  This is a popular enough trope that  it has an entry on [tv tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/LaserHallway) and the [Mythbusters](https://www.youtube.com/watch?v=ZAv7z4Rg0W8) looked into it.

Regardless of the real life applications, a laser maze like that certainly looks fun.  The idea of potentially constructing only started when I was able to actually go through one in an arcade (back in 2016!).  The arcade version consisted of a large room, with lasers crossing it, and buttons along the walls.  The goal was to press the buttons in order, while not breaking the laser beams.  The entire run was timed so that we could compete!  All I can say is that it's seriously a ton more fun than it looks.  I hadn't experienced something like that before, and it *seemed* like something that could be done relatively easily.  So I filed it away in the back of my head, but didn't come back to it for some time.

## Concepting

The idea came back in earnest a few months later, when I got a raspberry pi for Christmas.  When I started, I knew I wanted to keep the basic core of the arcade room, but keep it simple to get the project started.  I started with the following list of ideas:
* stationary lasers from one wall to the other
* a timer
* a button to start/stop the timer
* time penalties for broken lasers

And the following items were off-limits:
* moving lasers (too many moving parts to do reliably)
* multiple buttons along walls (not enough room, too complicated)


## Hardware
To gather a hardware list, I started to research similar projects.  Thankfully, there is a pretty common beginner project for making a laser trip-wire, so I was able to use materials from that.  I bought 10 lasers, some light sensors, and some buzzers.  The great part about this project as a first project for my pi is that it doesn't require a lot of expensive components.  

The non-essentials included a nice big arcade button for maximum visibility and an LCD screen.  A laptop monitor would work just as well, but I liked having the timing device self-contained as well, and not needing a monitor in the area.  Additionally, I needed some wire, and I borrowed a soldering iron from a friend as well.

For a more in-depth look at the hardware, including how the photoresistors work (and why an asrduino might be better than a raspberry pi for this project), take a look at the more detailed hardware post!

## Software


## Layout
So far, the actual layout of the lasers has gone through 2 revisions.  TO actually affix the photoresistors to the walls, I just used tape, and ran the wires down to the floor, then along the base of the wall.  This holds them in place, but also allows for me to easily adjust them as the lasers might shift slightly over time.

The wall with the lasers is well-suited for this because there's no wall, it's just studs with no drywall.  This allows me to use some stiff wire to hold the lasers in place, and nail that wire directly into the stud.  This allows me to have good control over the direction of the laser, and if I do need to actually move it, it's easy enough to take the nails out and move those as well.

My "process" for setting up the course was to start with a few simple ones, and gradually add in more lasers interacting as you move through the course.  For the first revision however, I made the unfortunate oversight that I left too much room under the lasers, so that anyone could crawl through the whole thing.  Besides being totally unsecure, I thought that might not be in the spirit of the project, so I readjusted them.

I'm excited to see what people think about the difficulty level of the course.  I tried to make it not too tough, but there's a real possibility that people will make it through extremely quick.



Hey everyone, I'm back to share my latest project!

I've been working for the past few months to construct a laser maze in my basement.  Yes, you read that correctly, a laser maze.

This idea was formed when I attended a bachelor party at an arcade that included a laser room.  The objective was to get across the whole room, pressing buttons a series of buttons along the wall.  Each person got a time, and could watch the others compete as well!  It was a great time, and it had always been in the back of my mind as a project idea ever since.

Whenever I mention this project, everyone always has a heist scene where a thief navigates a laser maze to get to the goods.  Just to temper the expectations, it's nothing that crazy

I had previously received a raspberry pi as a gift, so it made sense to utilize that as the brain for the whole room, and add in sensors, buttons, etc. as needed.

The first step was to get all the components I needed.  Reading a few basic tutorials about trip wires, I concluded that a set of 5V lasers and light dependent resistors would work well for this project.

My favorite thing I learned during the project was how the light dependent resistors work, and specifically how they work with the raspberry pi.  Light dependent resistors are resistors that change their resistance depending on the amount of light shone onto the sensors.

One complication however is that the photoresistors are constantly varying by small amounts, thus the voltages are constantly varying.  This is a problem when working on a raspberry pi, as it doesn't have any analog inputs, only digital input/output.  Functionally, this means any input is either on or off.  This leaves us with the problem of how to turn an analog scale ,the intensity of the light on the sensor, to a value in our code that we can use.  The answer, already determined and open-sourced by someone smarter than me is to use a specific electrical circuit and pulse an output.
The genius of turning this




## Concept & Layout

I think most people's first experience with some kind of laser maze is in the movies.  Everyone can likely recall a bank robbery scene where someone must make their way through a grid of beams (probably moving) to access the treasure at the end.  Like most people, this was the extent of my involvement with that type of room, until I had the opportunity to actually go through one!  I was on a bachelor party at one of those arcade / go-karts / bowling type places in Wisconsin, and it had a very intriguing looking arcade game.  Peeking in, I was interested to see a bunch of laser beams criss-crossing the room, so someone put in a token and gave it a shot.  The goal was to progress through the room, pressing buttons along the walls as you went.  Breaking beams gave you a time penalty, and the entire process was timed, giving you a good way to compete against your friends.

While this room was the inspiration for my project, I wouldn't say that it was an immediate hit in my brain.  The idea to do this myself sat patiently and waited until the time was right.  Turns out, the right time was shortly after I received a raspberry pi a few years ago for Christmas.  Even then, I ended up buying supplies, but shelving the project due to lack of motivation.  I returned to it after a few friends had asked for help on projects of their own, and seeing others get things rolling on really neat projects gave me a kick start to finally finish it up.

My initial concept was remarkably close to both the commercial room that inspired me, and the initial concept in my head.  Initially, I wanted to have the following items:
* stationary lasers from one wall to the other
* a timer
* a button to start/stop the timer
* time penalties for broken lasers

And the following items were off-limits:
* moving lasers (too many moving parts to do reliably)
* multiple buttons along walls (not enough room)

In addition, I tend to believe in getting a minimum working product out there, so when you advance to more difficult aspects, you have the knowledge of the basic setup as well.

So let's get down to business and I'll explain what I had in mind when I started.  My number one goal was fun (obviously), and I thought that being able to compete for time would be an important part of that goal.  The location for the room was a portion of my basement approx. 10 ft. x 20 ft.  For this size room, I took a rough guess that I would need ~10 lasers.  The plan was to have them aimed at different angles and heights to create a puzzle-like experience where participants might need to think about where they would go next instead of making it an entirely dexterity-based game.

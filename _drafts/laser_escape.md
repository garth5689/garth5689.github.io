---
layout:     post
title:      ""
date:       2018-07-01 16:00:00
author:     Andrew
header-img: img/posts/laser_escape/hao-wang-217034-unsplash.jpg
header-credit: https://unsplash.com/@danranwanghao
tags:       programming electronics raspberry_pi
---

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

My initial concept was remarkably close to both the commercial room that inspired me, and the initial concept in my head.  In my initial concepting, I wanted to have the following items:
* stationary lasers from one wall to the other
* a timer
* a button to start/stop the timer
* time penalties for broken lasers

The following items were off the table for various reasons:
* moving lasers (too many moving parts to do reliably)
* multiple buttons along walls (not enough room)

In addition, I tend to believe in getting a minimum working product out there, so when you advance to more difficult aspects, you have the knowledge of the basic setup as well.

So let's get down to business.


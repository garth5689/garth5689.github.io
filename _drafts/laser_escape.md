---
layout:     post
title:      "Laser Escape: Part 1 ⏱️"
date:       2018-08-26 16:00:00
author:     Andrew
header-img: img/posts/laser_escape/hao-wang-217034-unsplash.jpg
header-credit: https://unsplash.com/@danranwanghao
tags:       programming electronics raspberry_pi
---
Hey everyone, I'm back after a long break to share my latest project!

For the past few months, I've been working to construct a **laser escape maze** in my basement.  Yep, you read that correctly, and I'm super excited to finally have it finished!  This post is going to be an overview of the project, and I'm planning to write follow-up posts with more details.

## Background
This one may take a little while to explain, so let's start at the inception of the idea.  Think back to your favorite heist movie.  If it's modern, there's likely a scene where thieves are gracefully moving through the laser beams of a security system to get to the riches.  <!--break--> If you can't think of one off the top of your [head](https://www.youtube.com/watch?v=aEawL9PYh-k), [here](https://www.youtube.com/watch?v=w0Wwrb4c4uE) [are](https://www.youtube.com/watch?v=1g9QEQrHOMw) [some](https://www.youtube.com/watch?v=mr834Cs9ncs) [examples](https://www.youtube.com/watch?v=KX2_LCUkhDs).  This is a popular enough scenario that it has an entry on [TVTropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/LaserHallway) and the [Mythbusters](https://www.youtube.com/watch?v=ZAv7z4Rg0W8) investigated it.

Regardless of the real life viability, a laser maze certainly looks fun!  The idea of constructing one started when I went through one in an arcade (back in 2016!).  The arcade version consisted of a large room, criss-crossing lasers, and buttons along the walls.  The goal was to press the buttons in order, while not breaking the laser beams.  The entire run was timed so that we could compete!  It was a blast, and I hadn't experienced something like that before.  At first glance, it *seemed* like something that could be done relatively easily, so I filed it away in the back of my head.

## Initial Concepts
The idea came back in earnest a few months later, when I got a Raspberry Pi (RPi for short) for Christmas.  Raspberry Pi is a small computer, intended for small DIY projects and teaching computer science.  When starting, I knew I wanted to simplify things down to the basic elements of the laser room.  I started with the following list of features:
* stationary lasers from one wall to the other
* a timer
* a button to start/stop the timer
* basic software to run the timer and track the number of broken beams

Something I really try to subscribe to, especially on projects like this with a ton of unknown stuff, is to start small.  This will get at least *something* working, and it can always be improved on later.  This really guided my first iteration of the project.  With that in mind, I ruled out the following:
* moving lasers (too many moving parts to do reliably)
* multiple buttons along walls (not enough room, too complicated)

## Hardware
To gather a hardware list, I started to research similar projects.  Thankfully, a single laser trip-wire is a common beginner project, so I was able to source materials from that.  I bought lasers, some light sensitive resistors, and some buzzers.  The great part about this project as a first project for my pi is that it doesn't require a lot of expensive components.

The detatiled parts lists is as follows:
* wire - $35 (need a surprising amount)
* buzzers - $4.50 for 5
* 1 uF capacitors - $5.50 for 10
* 5mm light sensitive resistors - $7 for 20
* 5V lasers - $5 for 5
* arcade button - $4.50 each
* Raspberry Pi - $35
* Total: ~$100

The great part about these parts however, is that they will all be reusable in future projects as well.

## Software
Unsurprisingly, writing the software for this project was my favorite part!  Again, following the start simple philosophy, the first thing I did was hook up a few lasers and test that breaking a beam could be successfully detected.  First surprise (previously mentioned): I couldn't just read the light sensors directly.

One important note about the raspberry pi is that it doesn't have any analog inputs, only digital ones.  Analog inputs mean that the computer can take a voltage value (within limits), and read that value directly into your software.  The type of input on the raspberry pi is digital, where incoming voltages values are translated to a True/False value.  This is best used for switches or on/off type inputs.

This is relevant to this particular project because the light sensors I bought are just simple resistors.  It would be preferable to just calculate the resistance value from analog voltage, but that can't be done.  The solution is to create a small timing circuit, which adds a little delay to the response time.

The next minor bump was getting the LCD screen updating properly.  The LCD screen works by sending commands to the screen chip over a small communication bus, and the screen updates accordingly.  The major trade off is that I would like the screen to update quickly while displaying the timer, but updating too rapidly will cause flickering and possible corruption of the data on the screen.

The most fun was adding some of the non-essentials, like name entry & data recording.  Before each run starts, the runner can enter their name via a keyboard and the LCD screen.  Once the run is completed, the name, time, and number of penalties are recorded into a .csv file to create a leaderboard.

#### Hardware - Software details
I could go on and on about this project, but because this is the overview, I'll leave off here.  Like I said, I plan to write a more detailed post in the near future with more technical details.

## Layout
Lastly, I think the most important factor to being an enjoyable experience for everyone is the layout of the lasers.  The most common question that I've gotten so far is how I came up with the laser placement.  I'd like to say there was a scientific method, but I'm going to admit that it was old fashioned trial and error.

The major goal when I started on this project was fun, and it's important to get everyone participating as well.  If it's impossible to get through without breaking any beams, everyone might get discouraged.  On the flip-side, if you can run through it with minimal effort, it becomes more of an agility challenge than a puzzle.

For my first attempt, I placed a laser, thinking about interesting ways to move past it, placing the next one, and continuing that procedure until they were all placed.  This led to an OK layout, with one major flaw.  I made the unfortunate oversight of leaving too much room under the lasers, so that anyone could crawl through the whole thing.  To me, this wasn't in the spirit of the project, so I adjusted them after a few test runs.

The second layout correct the initial mistake by dedicating a few lasers very close to the ground. I'm excited to see what people think about the difficulty level of the course.  As people continue to go through it, there's always the possibility of a third layout with lessons learned from watching people going through.

## Results
So far, a few different groups of people have made their way through the maze and I think it's been a blast watching everyone try it.  My favorite part so far has been watching different strategies develop as people go through multiple times, including some runners jumping over the first few lasers and contorting to go under the next few!

I know everyone is excited to see the leaderboard, so with further ado, here are top 10 participants so far[^footnote]:



[^footnote]: There is a lost time from Mark S.  He'll just have to re-do his run :)

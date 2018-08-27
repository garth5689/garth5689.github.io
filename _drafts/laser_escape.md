---
layout:     post
title:      "Laser Escape⏱️"
date:       2018-08-26 16:00:00
author:     Andrew
header-img: img/posts/laser_escape/hao-wang-217034-unsplash.jpg
header-credit: https://unsplash.com/@danranwanghao
tags:       programming electronics raspberry_pi
---

Hey everyone, I'm back after a long break to share my latest project!

For the past few months, I've been working to construct a **laser escape maze** in my basement.  Yep, you read that correctly, and I'm super excited to finally have it finished!  I'm going to share a little bit about how I built the room and what I learned along the way.

## Background
This one may take a little while to explain, so I'll start from the beginning.  Think back to your favorite heist movie.  If it's a recent one, it's likely there's a scene where the thieves are gracefully moving through the laser beams of a security system to get to the riches.  <!--break--> If you can't think of one off the top of your [head](https://www.youtube.com/watch?v=aEawL9PYh-k), [here](https://www.youtube.com/watch?v=w0Wwrb4c4uE) [are](https://www.youtube.com/watch?v=1g9QEQrHOMw) [some](https://www.youtube.com/watch?v=mr834Cs9ncs) [examples](https://www.youtube.com/watch?v=KX2_LCUkhDs).  This is a popular enough trope that  it has an entry on [tv tropes](https://tvtropes.org/pmwiki/pmwiki.php/Main/LaserHallway) and the [Mythbusters](https://www.youtube.com/watch?v=ZAv7z4Rg0W8) looked into it.

Regardless of the real life viability, a laser maze like that certainly looks fun!  The idea of potentially constructing one started when I was able to actually go through one in an arcade (back in 2016!).  The arcade version consisted of a large room, with lasers crossing it, and buttons along the walls.  The goal was to press the buttons in order, while not breaking the laser beams.  The entire run was timed so that we could compete!  All I can say is that it's seriously a ton more fun than it looks.  I hadn't experienced something like that before, and it *seemed* like something that could be done relatively easily.  So I filed it away in the back of my head, but didn't come back to it for some time.

## Drafting Concepts
The idea came back in earnest a few months later, when I got a raspberry pi for Christmas.  When I started, I knew I wanted to keep the basic core of the arcade room, but keep it simple to get the project started.  I started with the following list of ideas:
* stationary lasers from one wall to the other
* a timer
* a button to start/stop the timer
* time penalties for broken lasers

And the following items were off-limits:
* moving lasers (too many moving parts to do reliably)
* multiple buttons along walls (not enough room, too complicated)

## Hardware
To gather a hardware list, I started to research similar projects.  Thankfully, a laser trip-wire is a common beginner project, so I was able to use materials from that.  I bought 10 lasers, some light sensitive resistors, and some buzzers.  The great part about this project as a first project for my pi is that it doesn't require a lot of expensive components.

The non-essentials included a nice big arcade button for maximum visibility and an LCD screen.  A laptop monitor would work just as well, but I liked having the timing device self-contained as well, and not needing a monitor in the area.

<!-->
For a more in-depth look at the hardware, including how the photoresistors work (and why an asrduino might be better than a raspberry pi for this project), take a look at the more detailed hardware post!

So far, the actual layout of the lasers has gone through 2 revisions.  TO actually affix the photoresistors to the walls, I just used tape, and ran the wires down to the floor, then along the base of the wall.  This holds them in place, but also allows for me to easily adjust them as the lasers might shift slightly over time.

The wall with the lasers is well-suited for this because there's no wall, it's just studs with no drywall.  This allows me to use some stiff wire to hold the lasers in place, and nail that wire directly into the stud.  This allows me to have good control over the direction of the laser, and if I do need to actually move it, it's easy enough to take the nails out and move those as well.
<!-->

## Software
As you might expect, writing the software for this project was probably my favorite part!

#### Hardware - Software details
As this is more of an overview post, I plan on writing a more in-depth review of the technical aspects of this project.  Look for that in the near future!

## Layout
Beyond the technical aspect, the factor that has the most impact on enjoyment is the laser layout (where the lasers are pointed, how tightly they are grouped, etc.).  This has also generated the most discussion among participants.  The major goal when I started on this project was fun, the layout probably has the most control over that.  If it's impossible to get through without breaking any beams, participants might get discouraged, but if you can run through it by jumping slightly, it becomes more of an agility challenge than a puzzle.

When I created the initial layout, I started by placing a laser, thinking about interesting ways to move past it, placing the next one, and continuing that procedure until they were all placed.  This led to an OK layout, with one major flaw.  I made the unfortunate oversight of leaving too much room under the lasers, so that anyone could crawl through the whole thing.  To me, this wasn't in the spirit of the project, so I adjusted them after a few test runs.

The second layout has a few lasers very close to the ground to prevent an easy path under everything. I'm excited to see what people think about the difficulty level of the course.  I tried to make it not too tough, but there's a real possibility that people will make it through extremely quick.

## Results
So far, a few different groups of people have made their way through the maze and I think it's been a blast watching everyone try it.  My favorite part so far has been watching different strategies develop as people go through multiple times, including some runners jumping over the first few lasers and contorting to go under the next few!

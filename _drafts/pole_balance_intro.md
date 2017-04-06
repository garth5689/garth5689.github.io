---
layout:     post
title:      "Inverted Pendulum Dynamics"
date:       2017-04-04 12:00:00
author:     Andrew
header-img: img/posts/sympy_dynamics/balance_rock.jpg
header-credit: https://unsplash.com/@nbmat
tags:       programming dynamics sympy python
---

The next project I'm going to tackle involves quite a few moving parts, so I'm going to tackle them in a few different posts.  This will also serve as the introduction for what I'm shooting for as a finished project.

#### My goal is to have my raspberry pi able to balance an inverted double pendulum based on feedback from my web camera.

testing

pictures are always helpful:

![setup]({{ site.baseurl }}/img/posts/sympy_dynamics/project_setup.png)

There's many components to this, so I'll start by separating the problem into chunks:
* control
    * motor actuation
    * feedback
        * webcam video
        * video processing
    * control logic
        * neural network
            * training
            * dynamics modeling

To start, I'm going to create a plant model on my computer that I can use to test any potential controls strategies on.  When I'm testing out different strategies, it will be very beneficial to be able to restart them quickly and test many iterations rapidly.

To do this, I'll create a model on my computer that simulates the motor input, and processing delays from the webcam and then predicts the physical systems response.

The system in question here is an inverted double pendulum, with a torque applied at the base and a free pivot in the center.  Balancing of pendulua is a very well studied area, so there's tons of information about double pendulums on the internet.

The motion of a double pendulum is chaotic, governed by some ordinary differential equations.  In practice, this means that we can't get explicit equations for the motion of the two links, but we can calculate the paths of the links numerically.

In this system, there are two degrees of freedom, the two angles of the pendulum.  With these two angles, and the constants that define the links, the state of the system can be fully described.  The motion is constrained to the x-y plane.

To arrive at a set of equations that we can actually use, we'll be using the Lagrangian.

> In each case, a mathematical function called the Lagrangian is a function of the generalized coordinates, their time derivatives, and time, and contains the information about the dynamics of the system.

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

#### My goal is to have my raspberry pi able to balance an inverted pendulum based on feedback from my web camera.

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

To start, I'm going to create a plant model on my computer that I can use to test any potential controls strategies on.

The system I'm interested in is a double pendulum, with a torque applied at the base.

---
layout:     post
title:      "Inverted Pendulum Dynamics"
date:       2017-04-11 12:00:00
author:     Andrew
header-img: img/posts/pendulum_dynamics/balance_rock.jpg
header-credit: https://unsplash.com/@nbmat
tags:       programming dynamics sympy python
---

Today, we're talking double pendulums, kinematics and more!  Before you get scared off, I promise to make it accessible (why not give physics a chance).

The task at hand is to balance an inverted [double pendulum](https://en.wikipedia.org/wiki/Double_pendulum), but in this post I'm going to focus solely on modeling the system.  Modeling the system is important to understand what's happening, but I also plan to use this model to test out different strategies for actually controlling the balancing.

Testing different controls strategies with a physical setup is expensive, but I don't mean monetarily.  Time-wise, I could be running dozens or even hundreds of trials virtually before attempting anything with the physical motor and pendulum.
<!--break-->
So, with that said, lets get down to business.  Thankfully, the double pendulum is a well studied mechanical system, and myriad [academic papers](https://scholar.google.com/scholar?as_vis=1&q=double+pendulum&hl=en&as_sdt=1,16) are available on the subject.  One great resource I found was *A Mathematical Introduction to Robotic Manipulation* [^mls_textbook]

One reason the double pendulum is popular is because it's a simple example of [chaotic motion](https://en.wikipedia.org/wiki/Chaos_theory).  Chaotic motion means that the system is highly sensitive to input conditions.  Practically, this means if you were to release the pendulum from almost exactly the same spot many times in a row you would see far different outcomes each time.

This post is going to be a bit technical, but as always, I'll try my best to make it interesting for all audiences.

First things first, let's agree on what everything's going to be called:

![diagram]({{ site.baseurl }}/img/posts/pendulum_dynamics/simple_double_diagram.png)

Here is our double pendulum system.  Each link has a length $$l$$, a mass $$m$$, and it's center of mass has coordinates $$x$$, $$y$$.  The center of mass is a distance $$r$$ from the base of each link.  Motion will only be considered in the $$x-y$$ plane. 

Mechanical systems such as these can be described by the number of [degrees of freedom](https://en.wikipedia.org/wiki/Degrees_of_freedom_(mechanics)) that it has.  The degrees of freedom of a system are the independant parameters that are needed to fully describe the configuration.

If there were a physical double pendulum in front of you, image moving the links around.  You would eventually determine that there are really only two things that you would need to tell someone for them to agree that you're both looking at the same configuration of the links.

In this system, those two degrees of freedom are the angles $$\theta_0$$ and $$\theta_1$$.  The state of the system can be described completely with these two angles.  

What that means for us is that those two angles are what we want to simulate given some initial conditions.

#### WARNING: MATH

This is where we take a slight leap into some mechanics that may be a bit advanced, but try to stick it out!

There are two types of energy present in our double pendulum system:
* **[kinetic](https://en.wikipedia.org/wiki/Kinetic_energy)** ($$K$$), which comes from motion.  In this case, that motion is the swinging action of links.    
* **[potential](https://en.wikipedia.org/wiki/Potential_energy)** ($$U$$), which is the stored energy of the system.  In this case, the stored energy is contained in the link's height, from gravity.  Gravitational potential energy is why things roll downhill (basically).

We're going to use a function called the [Lagrangian](https://en.wikipedia.org/wiki/Lagrangian_mechanics) to work some magic.

Using just the potential and kinetic energy of the system, and describing the coordinates of the links, the Lagrangain can yield the equations of motion for the system.


> Any function which generates the correct equations of motion, in agreement with physical laws, can be taken as a Lagrangian. It is nevertheless possible to construct general expressions for large classes of applications.

## System State Equations

First, we'll take the $$x$$,$$y$$ coordinates for the centers of mass for the two links and put them in terms of our two degrees of freedom and the constants.

$$ \begin{align}
x_0=& r_{0} \cos{\left (\theta_0 \right )} & \\
y_0=& r_{0} \sin{\left (\theta_0 \right )} & \\
x_1=& l_{0} \cos{\left (\theta_0 \right )} + r_{1} \cos{\left (\theta_0 + \theta_1 \right )} & \\
y_1=& l_{0} \sin{\left (\theta_0 \right )} + r_{1} \sin{\left (\theta_0 + \theta_1 \right )} & \\
\end{align} 
$$

## Kinetic Energy

Kinetic energy for a moving object (non-rotational) is $$\frac{1}{2}mv^2$$, where $$v$$ is the velocity, and the kinetic energy for a rotating object $$\frac{1}{2}I\omega^2$$, where $$I$$ is the moment of inertia (a measure of how much torque it takes to rotate) and $$\omega$$ is the rotational speed of the object.

Using those equations, the total kinetic energy of the system is:

$$K = \tfrac{1}{2}I_0\omega_0^2 + \tfrac{1}{2}m_0v_0^2 + \tfrac{1}{2}I_1\omega_1^2 + \tfrac{1}{2}m_1v_1^2$$

To get our kinetic energy in terms of $$\theta_0$$ and $$\theta_1$$, some substitutions need to happen.

$$
\begin{align}
K =& \tfrac{1}{2}I_0\omega_0^2 + \tfrac{1}{2}m_0v_0^2 + \tfrac{1}{2}I_1\omega_1^2 + \tfrac{1}{2}m_1v_1^2 & \\
\omega_0 =& \dot{\theta_0} & \\
\omega_1 =& \dot{\theta_0} + \dot{\theta_1} & \\
K =& \tfrac{1}{2}I_0\dot{\theta_0}^2 + \tfrac{1}{2}m_0v_0^2 + \tfrac{1}{2}I_1(\dot{\theta_0} + \dot{\theta_1})^2 + \tfrac{1}{2}m_1v_1^2 & \\
v =& \dot{x} + \dot{y} & \\
K =& \tfrac{1}{2}I_0\dot{\theta_0}^2 + \tfrac{1}{2}m_0(\dot{x_0}^2 + \dot{y_0}^2) + \tfrac{1}{2}I_1(\dot{\theta_0} + \dot{\theta_1})^2 + \tfrac{1}{2}m_1(\dot{x_1}^2 + \dot{y_1}^2) & \\
\end{align}
$$

We'll let sympy handle the last substitution to get the equation in terms of only $$\theta$$

## Potential Energy

$$
\begin{align}
U =& m_0gy_0 + m_1gy_1 & \\
\end{align}
$$

## Lagrange

$$ L = K - U $$

Now we can substitute numbers into our equation to perform the actual calculations.


```python
from sympy import symbols, init_printing, S, Derivative, diff, simplify, solve, lambdify, cos, sin
from sympy.physics.vector import vlatex
import numpy as np
import scipy.integrate as integrate
from matplotlib import pyplot as plt
from matplotlib import animation, rc
from itertools import chain
from IPython.display import HTML, display, Math

rc('animation', html='html5')

init_printing(latex_printer=vlatex, latex_mode='equation')
```


```python
def disp(expr):
    display(Math(vlatex(simplify(expr))))
    
def disp_eq(lhs,expr):
    display(Math("$${0} = {1}$$".format(lhs, vlatex(simplify(expr)))))
```


```python
def generate_double_pendulum_odes():
    """
    :return:
     List of ODE describing system (Number = DOF of system)
     List of plotting position functions (Number = DOF of system)
    """
    t = symbols('t')
    g = symbols('g')
    l = symbols('l0:2')
    m = symbols('m0:2')
    r = symbols('r0:2')
    i = symbols('I0:2')
    tau = symbols('tau0:2')
    b = symbols('b0:2')

    g_val = S(9.8)
    l_val = [S(1.0), S(1.0)]
    m_val = [S(1.0), S(1.0)]
    r_val = [temp_l / 2 for temp_l in l_val]
    i_val = [(temp_m * temp_l ** 2) / 12 for temp_m, temp_l in zip(m_val, l_val)]
    tau_val = [S(0.0), S(0.0)]
    b_val = [S(0.0), S(0.0)]

    theta = [w(t) for w in symbols('theta0:2')]
    theta_dot = [Derivative(w, t) for w in theta]
    theta_ddot = [Derivative(w, t, t) for w in theta]

    x = [None] * 2
    y = [None] * 2
    x_dot = [None] * 2
    y_dot = [None] * 2

    x[0] = r[0] * cos(theta[0])
    y[0] = r[0] * sin(theta[0])
    x[1] = l[0] * cos(theta[0]) + r[1] * cos(theta[0] + theta[1])
    y[1] = l[0] * sin(theta[0]) + r[1] * sin(theta[0] + theta[1])

    x_dot[0] = diff(x[0], t)
    y_dot[0] = diff(y[0], t)
    x_dot[1] = diff(x[1], t)
    y_dot[1] = diff(y[1], t)

    kinetic = (m[0] * (x_dot[0] ** 2 + y_dot[0] ** 2)
               + m[1] * (x_dot[1] ** 2 + y_dot[1] ** 2)
               + i[0] * (theta_dot[0]) ** 2
               + i[1] * (theta_dot[0] + theta_dot[1]) ** 2) / 2

    potential = (m[0] * g * y[0]) + (m[1] * g * y[1])

    lagrange = kinetic - potential

    lagrangian = [None] * 2
    lagrangian[0] = diff(lagrange, theta_dot[0], t) - diff(lagrange, theta[0])
    lagrangian[1] = diff(lagrange, theta_dot[1], t) - diff(lagrange, theta[1])

    solution = solve(lagrangian, theta_ddot)

    values = [(g, g_val),
              (l[0], l_val[0]),
              (l[1], l_val[1]),
              (m[0], m_val[0]),
              (m[1], m_val[1]),
              (r[0], r_val[0]),
              (r[1], r_val[1]),
              (i[0], i_val[0]),
              (i[1], i_val[1]),
              (tau[0], tau_val[0]),
              (tau[1], tau_val[1]),
              (b[0], b_val[0]),
              (b[1], b_val[1])]

    temp_vars = symbols('z0:4')

    inputs = list(zip((theta_dot[0], theta[0], theta_dot[1], theta[1]), temp_vars))

    ode_equations = [None] * 2
    ode_equations[0] = lambdify(temp_vars, simplify(solution[theta_ddot[0]]).subs(values).subs(inputs))
    ode_equations[1] = lambdify(temp_vars, simplify(solution[theta_ddot[1]]).subs(values).subs(inputs))

    def double_pendulum_position(pos):
        result = []

        for _, theta0, _, theta1 in pos:
            x1_pos = float(l_val[0]) * np.cos(theta0)
            y1_pos = float(l_val[0]) * np.sin(theta0)

            x2_pos = x1_pos + float(l_val[1]) * np.cos(theta0 + theta1)
            y2_pos = y1_pos + float(l_val[1]) * np.sin(theta0 + theta1)

            result.append(((0, x1_pos, x2_pos), (0, y1_pos, y2_pos)))

        return result

    return ode_equations, double_pendulum_position
```


```python
def generic_deriv_handler(this_state, _, deriv_functions):
    # x_dot, x pairs
    result = [(float(func(*this_state)), this_state[(i * 2)]) for i, func in enumerate(deriv_functions)]

    flattened = chain.from_iterable(result)
    float_flattened = list(map(float, flattened))

    return np.array(float_flattened)
```


```python
def animate_system(time, time_step, initial_conditions, derivation_functions, position_function, plot_limit):

    pos = integrate.odeint(generic_deriv_handler, np.radians(initial_conditions), np.arange(0.0, time, time_step),
                           args=(derivation_functions,))

    plot_positions = position_function(pos)

    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-plot_limit, plot_limit), ylim=(-plot_limit, plot_limit))
    ax.grid()
    ax.set_aspect('equal', adjustable='box')

    line, = ax.plot([], [], 'k-', lw=4, solid_capstyle='round')
    time_template = 'time = {:0.2f}s'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        line.set_data([], [])
        time_text.set_text('')
        return line, time_text

    def animate(i):
        # TODO position func should be generator
        # TODO dependance on DOF
        thisx, thisy = plot_positions[i]

        line.set_data(thisx, thisy)
        time_text.set_text(time_template.format(time_step))
        return line, time_text

    return animation.FuncAnimation(fig, animate, frames=len(pos), interval=25, blit=True, init_func=init)
```


```python
ani = animate_system(5, 0.05, [0, 90, 0, 90], *generate_double_pendulum_odes(), 2)
```


```python
HTML(ani.to_html5_video())
```




<video width="432" height="288" controls autoplay loop>
  <source type="video/mp4" src="data:video/mp4;base64,AAAAHGZ0eXBNNFYgAAACAGlzb21pc28yYXZjMQAAAAhmcmVlAABrtm1kYXQAAAKuBgX//6rcRem9
5tlIt5Ys2CDZI+7veDI2NCAtIGNvcmUgMTQ4IHIyNzA4IDg2YjcxOTggLSBILjI2NC9NUEVHLTQg
QVZDIGNvZGVjIC0gQ29weWxlZnQgMjAwMy0yMDE2IC0gaHR0cDovL3d3dy52aWRlb2xhbi5vcmcv
eDI2NC5odG1sIC0gb3B0aW9uczogY2FiYWM9MSByZWY9MyBkZWJsb2NrPTE6MDowIGFuYWx5c2U9
MHgzOjB4MTEzIG1lPWhleCBzdWJtZT03IHBzeT0xIHBzeV9yZD0xLjAwOjAuMDAgbWl4ZWRfcmVm
PTEgbWVfcmFuZ2U9MTYgY2hyb21hX21lPTEgdHJlbGxpcz0xIDh4OGRjdD0xIGNxbT0wIGRlYWR6
b25lPTIxLDExIGZhc3RfcHNraXA9MSBjaHJvbWFfcXBfb2Zmc2V0PS0yIHRocmVhZHM9NiBsb29r
YWhlYWRfdGhyZWFkcz0xIHNsaWNlZF90aHJlYWRzPTAgbnI9MCBkZWNpbWF0ZT0xIGludGVybGFj
ZWQ9MCBibHVyYXlfY29tcGF0PTAgY29uc3RyYWluZWRfaW50cmE9MCBiZnJhbWVzPTMgYl9weXJh
bWlkPTIgYl9hZGFwdD0xIGJfYmlhcz0wIGRpcmVjdD0xIHdlaWdodGI9MSBvcGVuX2dvcD0wIHdl
aWdodHA9MiBrZXlpbnQ9MjUwIGtleWludF9taW49MjUgc2NlbmVjdXQ9NDAgaW50cmFfcmVmcmVz
aD0wIHJjX2xvb2thaGVhZD00MCByYz1jcmYgbWJ0cmVlPTEgY3JmPTIzLjAgcWNvbXA9MC42MCBx
cG1pbj0wIHFwbWF4PTY5IHFwc3RlcD00IGlwX3JhdGlvPTEuNDAgYXE9MToxLjAwAIAAAApvZYiE
AC///vau/MsrRwuVLh1Ze7NR8uhJcv2IMH1oAAADAADVaeUGh2+Cbd/ADBB7Mb96mR2oOPhx+wrR
oyerPlXIfDRzuRhZLLUzHRBUyFfhMrG8cAAB+TrHVzQs92p8PFTodK2l0w1v5D3+xK5Tvy4D5GCt
XkmngSQDrlTBHYGbB6zILOltpKGp3Cw8w/CrBsB9ZUEUDooZ2MOp0BbAdyz9plH00ydm6FJbUJDC
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
">
  Your browser does not support the video tag.
</video>




```python
def generate_triple_pendulum_odes():
    """
    :return:
     List of ODE describing system (Number = DOF of system)
     List of plotting position functions (Number = DOF of system)
    """
    t = symbols('t')
    g = symbols('g')
    l = symbols('l0:3')
    m = symbols('m0:3')
    r = symbols('r0:3')
    i = symbols('I0:3')
    tau = symbols('tau0:3')
    b = symbols('b0:3')

    g_val = S(9.8)
    l_val = [S(1.0)] * 3
    m_val = [S(1.0)] * 3
    r_val = [temp_l / 2 for temp_l in l_val]
    i_val = [(temp_m * temp_l ** 2) / 12 for temp_m, temp_l in zip(m_val, l_val)]
    tau_val = [S(0.0)] * 3
    b_val = [S(0.0)] * 3

    theta = [w(t) for w in symbols('theta0:3')]
    theta_dot = [Derivative(w, t) for w in theta]
    theta_ddot = [Derivative(w, t, t) for w in theta]

    x = [None] * 3
    y = [None] * 3
    x_dot = [None] * 3
    y_dot = [None] * 3

    x[0] = r[0] * cos(theta[0])
    y[0] = r[0] * sin(theta[0])
    x[1] = l[0] * cos(theta[0]) + r[1] * cos(theta[0] + theta[1])
    y[1] = l[0] * sin(theta[0]) + r[1] * sin(theta[0] + theta[1])
    x[2] = l[0] * cos(theta[0]) + l[1] * cos(theta[0] + theta[1]) + r[2] * cos(theta[0] + theta[1] + theta[2])
    y[2] = l[0] * sin(theta[0]) + l[1] * sin(theta[0] + theta[1]) + r[2] * sin(theta[0] + theta[1] + theta[2])
    
    x_dot[0] = diff(x[0], t)
    y_dot[0] = diff(y[0], t)
    x_dot[1] = diff(x[1], t)
    y_dot[1] = diff(y[1], t)
    x_dot[2] = diff(x[2], t)
    y_dot[2] = diff(y[2], t)

    kinetic = (m[0] * (x_dot[0] ** 2 + y_dot[0] ** 2)
               + m[1] * (x_dot[1] ** 2 + y_dot[1] ** 2)
               + m[2] * (x_dot[2] ** 2 + y_dot[2] ** 2)
               + i[0] * (theta_dot[0]) ** 2
               + i[1] * (theta_dot[0] + theta_dot[1]) ** 2
               + i[2] * (theta_dot[0] + theta_dot[1] + theta_dot[2]) ** 2) / 2

    potential = (m[0] * g * y[0]) + (m[1] * g * y[1]) + (m[2] * g * y[2])

    lagrange = kinetic - potential

    lagrangian = [diff(lagrange, th_d, t) - diff(lagrange, th) for th_d,th in zip(theta_dot,theta)]

    solution = solve(lagrangian, theta_ddot)

    values = [(g, g_val),
              (l[0], l_val[0]),
              (l[1], l_val[1]),
              (l[2], l_val[2]),
              (m[0], m_val[0]),
              (m[1], m_val[1]),
              (m[2], m_val[2]),
              (r[0], r_val[0]),
              (r[1], r_val[1]),
              (r[2], r_val[2]),
              (i[0], i_val[0]),
              (i[1], i_val[1]),
              (i[2], i_val[2]),
              (tau[0], tau_val[0]),
              (tau[1], tau_val[1]),
              (tau[2], tau_val[2]),
              (b[0], b_val[0]),
              (b[1], b_val[1]),
              (b[2], b_val[2])]

    temp_vars = symbols('z0:6')

    inputs = list(zip((theta_dot[0], theta[0], theta_dot[1], theta[1], theta_dot[2], theta[2]), temp_vars))

    ode_equations = [lambdify(temp_vars, simplify(solution[th_ddot]).subs(values).subs(inputs)) for th_ddot in theta_ddot]
    
    def triple_pendulum_position(pos):
        result = []

        for _, theta0, _, theta1, _, theta2 in pos:
            x1_pos = float(l_val[0]) * np.cos(theta0)
            y1_pos = float(l_val[0]) * np.sin(theta0)

            x2_pos = x1_pos + float(l_val[1]) * np.cos(theta0 + theta1)
            y2_pos = y1_pos + float(l_val[1]) * np.sin(theta0 + theta1)

            x3_pos = x2_pos + float(l_val[2]) * np.cos(theta0 + theta1 + theta2)
            y3_pos = y2_pos + float(l_val[2]) * np.sin(theta0 + theta1 + theta2)
            
            result.append(((0, x1_pos, x2_pos, x3_pos), (0, y1_pos, y2_pos, y3_pos)))

        return result

    return ode_equations, triple_pendulum_position
```


```python
ani = animate_system(5, 0.05, [0, 0, 0, 0, 0, 0], *generate_triple_pendulum_odes(), 3)
```


```python
HTML(ani.to_html5_video())
```




<video width="432" height="288" controls autoplay loop>
  <source type="video/mp4" src="data:video/mp4;base64,AAAAHGZ0eXBNNFYgAAACAGlzb21pc28yYXZjMQAAAAhmcmVlAABj221kYXQAAAKuBgX//6rcRem9
5tlIt5Ys2CDZI+7veDI2NCAtIGNvcmUgMTQ4IHIyNzA4IDg2YjcxOTggLSBILjI2NC9NUEVHLTQg
QVZDIGNvZGVjIC0gQ29weWxlZnQgMjAwMy0yMDE2IC0gaHR0cDovL3d3dy52aWRlb2xhbi5vcmcv
eDI2NC5odG1sIC0gb3B0aW9uczogY2FiYWM9MSByZWY9MyBkZWJsb2NrPTE6MDowIGFuYWx5c2U9
MHgzOjB4MTEzIG1lPWhleCBzdWJtZT03IHBzeT0xIHBzeV9yZD0xLjAwOjAuMDAgbWl4ZWRfcmVm
PTEgbWVfcmFuZ2U9MTYgY2hyb21hX21lPTEgdHJlbGxpcz0xIDh4OGRjdD0xIGNxbT0wIGRlYWR6
b25lPTIxLDExIGZhc3RfcHNraXA9MSBjaHJvbWFfcXBfb2Zmc2V0PS0yIHRocmVhZHM9NiBsb29r
YWhlYWRfdGhyZWFkcz0xIHNsaWNlZF90aHJlYWRzPTAgbnI9MCBkZWNpbWF0ZT0xIGludGVybGFj
ZWQ9MCBibHVyYXlfY29tcGF0PTAgY29uc3RyYWluZWRfaW50cmE9MCBiZnJhbWVzPTMgYl9weXJh
bWlkPTIgYl9hZGFwdD0xIGJfYmlhcz0wIGRpcmVjdD0xIHdlaWdodGI9MSBvcGVuX2dvcD0wIHdl
aWdodHA9MiBrZXlpbnQ9MjUwIGtleWludF9taW49MjUgc2NlbmVjdXQ9NDAgaW50cmFfcmVmcmVz
aD0wIHJjX2xvb2thaGVhZD00MCByYz1jcmYgbWJ0cmVlPTEgY3JmPTIzLjAgcWNvbXA9MC42MCBx
cG1pbj0wIHFwbWF4PTY5IHFwc3RlcD00IGlwX3JhdGlvPTEuNDAgYXE9MToxLjAwAIAAAAizZYiE
AC///vau/MsrRwuVLh1Ze7NR8uhJcv2IMH1oAAADAADVaeUGU/F8HDusAMQDkKW5N1RMvqhe+MpT
mxLSARXJxzEZcSDrAABOFbni/QtH1tgyV49m/jGwUZbAceU2NiLnn34WkCPFZy3Qc3GJSQ73H6bb
l5huMyYATzZ8beET7b0YmNeWhAf46rXgMB051HOtPCLTXiVBv9ZmSvHCF7IJtMc5KvSL5ncLmTSj
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
AAABAAAAAAAAAAEAAAEAAAAAAQAAAgAAAAABAAAEAAAAAAIAAAEAAAAAAwAAAgAAAAABAAADAAAA
AAEAAAEAAAAAAQAAAgAAAAABAAAEAAAAAAIAAAEAAAAAAQAAAwAAAAABAAABAAAAAAEAAAIAAAAA
AQAABQAAAAABAAACAAAAAAEAAAAAAAAAAQAAAQAAAAABAAACAAAAAAEAAAMAAAAAAQAAAQAAAAAB
AAACAAAAAAEAAAMAAAAAAQAAAQAAAAACAAACAAAAAAEAAAMAAAAAAQAAAQAAAAABAAAEAAAAAAIA
AAEAAAAAAgAAAgAAAAABAAAEAAAAAAIAAAEAAAAAAgAAAgAAAAABAAADAAAAAAEAAAEAAAAAAQAA
BAAAAAACAAABAAAAAAEAAAMAAAAAAQAAAQAAAAABAAADAAAAAAEAAAEAAAAAAwAAAgAAAAABAAAF
AAAAAAEAAAIAAAAAAQAAAAAAAAABAAABAAAAAAEAAAMAAAAAAQAAAQAAAAABAAACAAAAAAEAAAMA
AAAAAQAAAQAAAAACAAACAAAAABxzdHNjAAAAAAAAAAEAAAABAAAAZAAAAAEAAAGkc3RzegAAAAAA
AAAAAAAAZAAAC2kAAAFnAAAAZQAAAGoAAAC9AAAA8AAAAHQAAAB1AAAAzAAAARAAAACBAAABVAAA
AJwAAADrAAABHAAAAQcAAAFDAAAA6wAAANkAAAErAAABHAAAAVgAAAEVAAABHAAAAUMAAACrAAAB
HgAAAN4AAAC4AAAA7AAAAGEAAAEwAAAAewAAAUQAAADmAAAAeQAAAJsAAAEPAAABPwAAAOoAAAC9
AAABEQAAAPoAAADHAAAA3AAAANUAAADkAAABCQAAAQwAAADjAAABQQAAANIAAAFCAAABAgAAANQA
AADgAAAAuwAAAMkAAADtAAAAdgAAAOAAAAFQAAAAiAAAAP4AAADkAAAA6AAAAHEAAADcAAAAngAA
AGQAAADsAAABEgAAAUIAAADkAAAArQAAAMYAAACqAAABPAAAAKkAAAEKAAAA3QAAAJ4AAADAAAAA
uQAAAT4AAADnAAABBwAAAQwAAAESAAABIQAAAPUAAAC3AAAA1QAAAUgAAADPAAABAwAAAOgAAAC6
AAAA6AAAAMkAAAAUc3RjbwAAAAAAAAABAAAALAAAAGJ1ZHRhAAAAWm1ldGEAAAAAAAAAIWhkbHIA
AAAAAAAAAG1kaXJhcHBsAAAAAAAAAAAAAAAALWlsc3QAAAAlqXRvbwAAAB1kYXRhAAAAAQAAAABM
YXZmNTcuNDEuMTAw
">
  Your browser does not support the video tag.
</video>




```python

```

Author. Title. Title of container (self contained if book), Other contributors (translators or editors), Version (edition), Number (vol. and/or no.), Publisher, Publication Date, Location (pages, paragraphs URL or DOI). 2nd container’s title, Other contributors, Version, Number, Publisher, Publication date, Location, Date of Access (if applicable).

[^mls_textbook]: Richard M. Murray , S. Shankar Sastry , Li Zexiang, A Mathematical Introduction to Robotic Manipulation, CRC Press, Inc., Boca Raton, FL, 1994 


```python

```

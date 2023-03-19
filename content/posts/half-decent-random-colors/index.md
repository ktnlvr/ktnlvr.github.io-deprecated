---
title: "Why Are Random Colours So Hard To Generate?"
date: 2023-03-14T12:50:45,843206163+02:00
draft: true
description: Using the little things we know about colour and human eyes to define a better random colour generation technique. Answering a personal question born out of aesthetic frustration.
---

I am not a color scientist or a psychophysisist, but I know a thing or two about colour. 
The question of generating good-looking random colour has bugged me for a while now. 
Most of the time the precision of it is really unnecessary, however, I still find it
problematic. My first encounter with it was when one of my friends decided to 
shade cubes in an application based on a seed value and a builtin `random` function.
The result was underwhelming. 5 or 6 seed values later the colours settled
on a decent pallete, but this problem left a scar. 

After some time I pulled myself together and decided to look deeper: what
was wrong about the colours that made me so negatively passionate towards
a pixel? A lot, actually. My main issue was with brightness, they all looked
awfully random. It wasn't the randomness I wanted.
I much prefer the randomness to be skewed towards whatever 
result pleases me more, and I have an feeling I'm not alone in that[^x-com-randomness].

The problem I was feeling with the random
colours was actually the problem of colour uniformity. When describing a uniform
pseudo-random number generator we say all values are equally likely. In case
of random colour generation even though they are *(mathematically) uniform*[^uniform-space-enc-of-math][^uniform-space-nlab], they
are not *perceptually uniform*. Below is the example of mathematically uniform and
perceptually uniform gradients, you can probably tell difference. 
{{< center centered="![Mathematically Uniform Strip](./math_uniform_strip.svg)" >}}
{{< center centered="![Perceptually Uniform Strip](./perceptually_uniform_strip.svg)" >}}

On the mathematical strip there are spikes at yellow, cyan and a less noticeable one
at purple. Keep in mind, we are doing phenomenology here, so the differences might
be less pronounced to you spefically. The second spectra doesn't have those spikes.

Ever wondered why heatmaps use the colours they use[^matplotlib-perceptually-uniform]? 
One of the reasons is perceptual uniformity! No surprises here. So the person reading them doesn't perceive
some areas as having more "heat".


[^uniform-space-enc-of-math]: [Uniform Space](https://encyclopediaofmath.org/wiki/Uniform_space) as formally described by the Encyclopedia Of Math.
[^uniform-space-nlab]: [Uniform Space](https://ncatlab.org/nlab/show/uniform+space) as formally described by nLab.
[^x-com-randomness]: [Is XCOM Truly Random?](https://sinepost.wordpress.com/2012/11/11/is-xcom-truly-random/) **TL;DR**
the game would sometimes miss a 98% chance of hit. Even though the internal
dice were proven to be fair, the players, nevertheless, fealt like they were
cheated. The fair randomness is not always the best pick for user experience.
[^matplotlib-perceptually-uniform]: [Here](https://matplotlib.org/stable/tutorials/colors/colormaps.html) is an example of different heatmap colour palletes from one of the most popular Python data visualization libraries.

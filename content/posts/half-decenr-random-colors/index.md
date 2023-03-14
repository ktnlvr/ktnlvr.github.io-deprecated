---
title: "Half-Decent Random Color Generation"
date: 2023-03-14T12:50:45,843206163+02:00
draft: true
description: Using the little things we know about colour and human eyes to define a better random colour generation technique.
---

I am not a color scientist, but I know a thing or two about colour. Different wavelengths 
of radiation are percieved differently by our eyes, that's what colour is. When an
object deflects a certain wavelength of colour our eyes catch it and feel it as
purple or green. An object is white when all light is reflected, black when all of it
is absorbed. Great. Light sources work differently, they emit a specific wavelength:
computer pixels emit a combination of red, green and blue of different intensities.
So if we just emit a random amount of each we get a truly random colour!

{{< sidenote text="Just assume that `random::<u8>()` gives us a random byte in range [0; 255]. It is also a *uniform* random number generator, so every possible value is as likely to appear as all the others.">}}
```rs
pub fn random_colour() -> (u8, u8, u8) {
    (random::<u8>(), random::<u8>(), random::<u8>())    
}
```

This is where I would've left the article if we literally percieved the light as RGB.
As a matter of fact, we don't. There is a lot of nuance to human vision, but
I'd like to focus on aesthetic (and arguably subjective) definition
of a *good* random colour. The problems might be apparent when we look
at some sample results.

{{< center centered="![Sample Colours](./sample.svg)" >}}

If you find that to be good enough, you are free to go. Personally, I am not satisfied. They all seem bleek, most are very dark, they are also pretty green. All of those might be issues of a specific sample, but I assure you, they are not.

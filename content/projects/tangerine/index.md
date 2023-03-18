---
title: "Tangerine"
date: 2023-03-18T23:51:36,223352835+02:00
draft: true
description: A list of lecturere notes, lab works and a curated list of exercises I could give out to my classmates I was teaching programming to.
github: https://github.com/Kittenlover229/tangerine
---

## The Story

It was the november of 2022, my second year of the IB[^ibo] program had just started. I was eager to teach computer science to someone. Previously the subjects of this urge were just my non-programmer friends, but now I could expand my audience to encorporate my classmates. When I revelead to my classmates that I was, in fact, a programmer one of them mentioned that they tried picking up Python several times but dropped it. This was my chance. After asking around we gathered a group of 6 people. Since it wasn't my first time organizing a club I knew a good half of them would drop out after first several sessions. Some have joined to acquire new social opportunities, others to enlarge their scope. It also gave us CAS[^cas] points, a scoring system required to complete the schooling program. I would be getting them for teaching, and my "students" for picking up a new skill, a symbiotic relationship in a way.

## What Was Planned?

The final goal was to make a curriculum for the "students" and dedicate some time of the week to programming practise, it would involve in-class lectures, home assignments for practising the algorithms and big projects to test their skill. Group work was also considered, but later thrown out due to low cohesion between the students.

## How Did It Go?

Designing a cirruculum from scratch was a monumental task, which I for sure couldn't handle, so I copied the lecture structure from my personal favourite Python programming lecturer, [Timofey Khirianov](https://www.youtube.com/@tkhirianov). His lectures were the basis of how I would actually structure my course. I wanted them to actually understand what programming is about and how solving actual problems feels, but you could never do that without the basics. The overall planned structure was as follows: `Flow Control, Turtle, Algos, Data Representation, Functional Programming, Type Theory, Big O, Data Structures`. Yes, it includes functional programming and type systems, because I am convinced that these two things are also essential to understanding programming as a whole. Functional Programming in combination with Type Theory teaches you to treat code as a pipeline of data, presented as datatypes. That makes your work designing a dataflow, from one representation to another. You may read any amount of articles on this topic, but you won't actually understand this until you write a `list(filter(lambda x: x % 2, map(int, input().split())))` with complete comprehension of what each identifier in this expression does.


## Conclusions

My main regret is choosing Python over C89. I was surprised to discover how *many* actual concepts in programming are inherited from C. Lists are indexed from 0 because of the array memory layout. While loops are interchangeable with for loops, since a for loop is just a fancy while. First truthy/falsy values were `int`s, since C doesn't have booleans as a separate type. These points can be explained otherwise, but I see them as stemming from C. We take all above for granted, but for someone new seing these weird conversions is confusing, hearing "Trust be, it is useful" isn't helping much. The only reason we actually know that they are useful the way they currently are is due to C bringing those ideas to the table and other languages adopting them. 

I find that emotion plays a very important role in learning. A great example is excitement, you can spend hours on end pondering a topic you are excited about. What my students had for granted (foreach loops, instance bound functions, etc) had to be manually implemented in C, so moving into a higher level language where you could say a concise `ls.append(42)` instead of `list.append(&ls, 42)` was a. 

All mentioned above convinced me that Python is not a great language for *teaching* a beginners class, C remains undeniably the best in my opinion. It has it's quirks, but many less so than Python. ~~Why is `len()` a free function again?~~


[^ibo]: [What](https://ibo.org/) even is IB Diploma Program anyway?
[^cas]: [Here](https://ibo.org/programmes/diploma-programme/curriculum/creativity-activity-and-service/) is the official description of what CAS points are according to IBO.

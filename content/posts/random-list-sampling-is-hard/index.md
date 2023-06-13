---
title: "Sampling A Random List Is Harder Than You Think"
date: 2023-06-13T13:36:20,513889181+03:00
description: A small case study into biased list sampling based on my student's experience. 
draft: false
difficulty: Beginner
---

Non-trivial probabilities aren't that difficult compared to other computer science concepts, especially if you are an experienced programmer and/or probabilist. However, that doesn't mean that rookie programmers fresh out of a bootcamp have same easy time as you, the nutella-coloured codeforces enjoyer. This is a case of one of my students who shall remain undisclosed. It happenned when as an exercise I suggested rewriting the Python's `random` builtin module entirely from scratch. Said student had to learn about pseudo-randomness in computers and I assumed they would have a great time with it.

All was good and dandy until the deal came to implementing `random.choices`. The function signature is something like `choices(population: list, weights: list, k: int) -> list` (the original definition also includes optional `cumulative_weights`, but they can be derived from `weights` if necessary). The function itself samples the `population` list with replacement, such that likelyhood of each element being drawn is determined by it's respective weight. You can already rule out that drawing with replacement simplifies the task to repeating calls of the "weighted draw" function `k` times, so let's focus our attention on that. We will also assume that there exists a function `randint(a, b)` that returns a perfectly-uniform random number in range `[a; b)` or `[a; b[`, whichever notation you prefer, also assume no error handling and perfect inputs, since it will only clutter the code.

```py
def choices(population: list, weights: list, k: int) -> list:
    return [weighted_draw(population, weights) for _ in range(k)]
```

The most naive implementation of `weighted_draw` would look something like the following:

```py
def weighted_draw(population: list, weights: list):
    weighted_population = []
    for w, p in zip(population, weights):
        weighted_population.extend(p for _ in range(w))
    return weighted_population[randint(0, len(weighted_population))]
```

It... works. Not in the nearly best way, not in all cases (e.g. fractional weights), the memory usage can be through the roof in some edgecases, but it mostly works. Not remotely good enough for production. There is a better candidate:

```py
from itertools import cycle

def rand_01():
    return randint(0, 2**32) / 2**32

def weighted_draw(population: list, weights: list):
    total_w = sum(weights)
    probabilities = map(lambda w: w / total_w, weights)
    # cycle just repeats the iterator forever
    # making this is an infinite loop
    for e, p in cycle(zip(population, probabilities)):
        if rand_01() <= p:
            return e
    raise 
```

Despite the *exceptionally poor* theoretical runtime of *O(∞)* this implementation might seem more sensible, though it raises an interesting question: are the earlier elements in the list more likely to occur when sampling? An answer might be intuitively apparent, yet it's not the same to everyone. Spoiler: no, the probability gets skewed, shame. The probability for any noninitial element to occur is exactly the probability of it to occur on its own **and** the probability of none of the previous elements to have been drawn. We can of course mitigate this be skewing every successive probability, as follows, but that seems janky, though effective.

```py 
def weighted_draw(population: list, weights: list):
    total_w = sum(weights)
    probabilities = map(lambda w: w / total_w, weights)
    previous_draw_bias = 1
    for e, p in cycle(zip(population, probabilities)):
        if rand_01() <= p / previous_draw_bias:
            return e
        else:
            previous_draw_bias *= (1 - p)
    raise 
```

Here we decide to divide `p` because even though it is the probability of drawing the element on its own, the comparison happens **iff** the previous comparisons failed, so the comparison itself is skewed. Anyhow, what gives? This didn't save us from *O(∞)*, so we are safe to forget this solution.

The following implementation employs cumulative weights and most certainly is the reason why this function in Python's standard library accepts them (cumulative weights) in the first place. For those unfamiliar with the concept, they are a prefix sum of the weights by definition, so some weight + all the weights preceding it. The cumulative weights are monotonously increasing which makes them a perfect subject for bisection (and binary search, respectively). Now we pick a random number from 0 to the maximum cumulative weight and search for its respective population element using the cumulative weights, bingo! It would look as follows in code:

```py
```

Funnily enough, the exact solution that CPython went with [^cpython-impl] for their standard library.

[^cpython-impl]: [Link](https://github.com/python/cpython/blob/46957091433bfa097d7ea19b177bf42a52412f2d/Lib/random.py#L454-L489) to CPython's implementation of `random.choices` as of writing this post.
---
title: "SKI Combinators In The World Of Templates"
date: 2023-03-30T20:19:21,513889181+03:00
draft: true
---

Combinatory logic is an alternative to lambda calculus[^nlab-lcalc], which does not use variables. In this sence it is akin to tacit (aka point-free, not to be confused with pointless) programming, a paradigm which also avoids using variables. If you are a big stack-oriented language enjoyer you already know what this is about. This idea has seen a recent explosion in popularity, due to functional languages attracting attention. A combinator is a higher-order function that uses other combinators and function application to compute.

But what does C++ have to do with any of this? Like someone who did too many extracurricular activities as a child, it is capable, but traumatized. As a result of being pulled in too many directions the language has a set of niche, but powerful features. One of these features is templates, the elder brother of generics. They can be difficult even for experienced programmers, especially when encountering something like dependent types[^dependent-T] or templated template parameters. They are complex enough to be turing complete[^turing-complete-templates]. You know what else is turing complete? SKI Combinators!

## Theory

There are several different combinator logics, but I would like to focus your attention on SKI Combinators (later SKI). I claim they are simpler to understand than the other systems, while remaining capable, besides, all the other combinator logics can be expressed using SKI. So what are S, K and I? The names of the combinators we are going to use. They can be defined as follows:

| Combinator  | Lambda Calculus | Haskell Function | Rewrite Rule      |
| ----------- | --------------- | ---------------- | ----------------- |
| I           | λx.x            | id               | **I**x → x        |
| K           | λx.λy.x         | const            | **K**xy → x       | 
| S           | λx.λy.λz.xz(yz) | flip             | **S**xyz → xz(yz) |

Hopefully one of the descriptions above is familiar to you. If not, stay tuned. What the table above describes is how each of the combinators transforms it's input.

## Putting It Together
## Conclusion

Congrats! Your favourite compiled language doubles as a proof assistant!

[^nlab-lcalc]: [Lambda Calculus](https://ncatlab.org/nlab/show/lambda-calculus) on nLab.
[^dependent-T]:[Cppreference](https://en.cppreference.com/w/cpp/language/dependent_name) on dependent types.
[^turing-complete-templates]: Oh yes, the templates really are [turing complete](https://en.cppreference.com/w/cpp/language/template_metaprogramming).

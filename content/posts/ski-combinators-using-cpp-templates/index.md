---
title: "SKI Combinators In The World Of Templates"
date: 2023-03-30T20:19:21,513889181+03:00
draft: true
---

Combinatory logic is an alternative to lambda calculus[^nlab-lcalc], which does not use variables. In this sence it is akin to tacit (aka point-free, not to be confused with pointless) programming, a paradigm which also avoids using variables. If you are a big stack-oriented language enjoyer you already know what this is about. This idea has seen a recent explosion in popularity, due to functional languages attracting attention. A combinator is a higher-order function (aka can accept other functions as arguments) that uses other combinators and function application to compute itself.

But what does C++ have to do with any of this? Like someone who did too many extracurricular activities as a child, it is capable, but traumatized. As a result of being pulled in too many directions the language has a set of niche, but powerful features. One of these features is templates, the elder brother of generics. They can be difficult even for experienced programmers, especially when encountering something like dependent types[^dependent-T] or templated template parameters. They are complex enough to be turing complete[^turing-complete-templates]. You know what else is turing complete? SKI Combinators!

## Theory

There are several different combinator logics, but I would like to focus your attention on SKI Combinators (later SKI). I claim they are simpler to understand than the other systems, while remaining capable, besides, all the other combinator logics can be expressed using SKI. So what are S, K and I? The names of the combinators we are going to use. They can be formally defined as follows:

| Combinator  | Lambda Calculus |  Rewrite Rule      | Curried Functions         |
| ----------- | --------------- |  ----------------- | ------------------------- |
| I           | λx.x            |  **I**x → x        | `f(x) = x`                |
| K           | λx.λy.x         |  **K**xy → x       | `f(x)(y) = x`             |
| S           | λx.λy.λz.xz(yz) |  **S**xyz → xz(yz) | `f(x)(y)(z) = x(z)(y(z))` |

If the formal notation doesn't give you anything to work with, worry not, you are not alone. They might seem very random, but trust me, specifically these ones are powerful enough. As previously mentioned, other combinator logics also exist, but their combinators can be expressed as a combination of I, K & S. We will discuss more complex and interesting combinators shortly.

Here, the "Curried Functions" column is of most interest to us. A curried function, is a function that instead of accepting all of it's arguments at once accepts them one by one. In languages that lack first class support for this feature this is implemented by returning a partially applied function, that partially applied function is a function with some of the arguments supplied.

```cpp
const auto classical_max = 
    [](int x, int y) -> int {
        return std::max(x, y);
    };

const auto curried_max = 
    [](int x) { 
        return [x](int y) -> int { 
            return std::max(x, y); 
        }
    };

classical_max(1, 2)  // 2
curried_max(1)(2)    // 2
```

Let's return our attention to the table, but now to the "Rewrite Rule" column. It expresses the same idea as currying, but in terms of strings. If we imagine a string `"Sa(b(c))d"` we would rearrange the terms following `K` to comply with the rewrite rule _**S**xyz → xz(yz)_, like so: `"a(d)((b(c))(d))"`. Parenthesis are giving off a strong Lisp vibe, so we'd be better off without them: `"a d (b c d)"`. Notice how we can not drop parenthesis around `b c d`, since that would make them into the arguments of `a`. We are going to be using the "as little parentheses as possible" notation extensively, so spend some time getting used to it, it is much easier on the eyes when talking about curried functions; compare `D(a)(A(b)(c))(d)(e)` and `F g (H u v) p q`. Here all the `a`s and `b`s are placeholders for other combinators to take place of, not variables in the traditional programming sense. In the context of curried function a partially-applied function is completely valid, so we are free to write just `I`, even though `I` has to accept an argument.

We have established a way of reading the notation, so let's look into how a transformation like that would actually work. It's actually rather simple: just apply the rule of the leftmost combinator to it's respective arguments, bingo! Below you can see the list of rules being applied one by one to string `"(SKII)a"`:

```
+-------------------------------------+
|    initial state is:                |
|                                     |
|    (S K I I) a                      |
+-------------------------------------+
|    apply rule Sxyz -> xz(yz)        |
|                                     |
|     S x y z            x z (y z)    |
|    (S K I I) a   ->   (K I (I I)) a |
+-------------------------------------+
|    apply rule Kxy -> x              |
|                                     |
|     K x  yyy          x             |
|    (K I (I I)) a  ->   I a          |
+-------------------------------------+
|    apply rule Ix -> x               |
|                                     |
|    I x    x                         |
|    I a -> a                         |
+-------------------------------------+
|    a                                |
|                                     |
|    no more rules to apply           |
|    transformation done              |
+-------------------------------------+
```

Feel free to look over it several times and try doing it by yourself, that will only help your understanding of combinators. If you want to validate your understanding try simplifying `S(K(SI))K`, we will return to that specific combinator in the next section.

## The Code

That is all well and good, but what can we do with this? We can play around a bit, trying out different combinations to see just how far we can stretch this. Sure, we can make a runtime with several types of objects all implementing some common interface, but that's no fun. I desire to compute them unusually, at compile time, just for the sake of it, for no particular reason. To do that we are going to express combinators and their half-applied states as structs, whereas function application will be actual type instantiation!

## Putting It Together
## Conclusion

Congrats! Your favourite compiled language doubles as a proof assistant!

[^nlab-lcalc]: [Lambda Calculus](https://ncatlab.org/nlab/show/lambda-calculus) on nLab.
[^dependent-T]:[Cppreference](https://en.cppreference.com/w/cpp/language/dependent_name) on dependent types.
[^turing-complete-templates]: Oh yes, the templates really are turing complete, [even cppref admits it](https://en.cppreference.com/w/cpp/language/template_metaprogramming).

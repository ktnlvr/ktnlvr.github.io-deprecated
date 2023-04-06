---
title: "SKI Combinators In The World Of Templates"
date: 2023-03-30T20:19:21,513889181+03:00
description: Describing all of SKI Combinator calculus using C++ templates.
draft: true
---

## Introduction

Combinatory logic[^comblogic-hs] is an alternative to lambda calculus[^nlab-lcalc], which does not use variables. In this sence it is akin to tacit (aka point-free, not to be confused with pointless) programming, a paradigm which also avoids using variables. If you are a big stack-oriented language enjoyer you already know what this is about. This idea has seen a recent explosion in popularity, due to functional languages attracting attention. A combinator is a higher-order function (aka can accept other functions as arguments) that uses other combinators and function application to compute itself. The only objects in SKI Calculus are combinators: no numbers, no booleans, no sum or product types, just functions. You would probably be surprised to know that functions are enough to have fun, especially if we assign special meaning to some of them, but I'm getting ahead of myself.

But what does C++ have to do with any of this? Like someone who did too many extracurricular activities as a child, it is capable, but traumatized. As a result of being pulled in too many directions the language has a set of niche, but powerful features. One of these features is templates, the elder brother of generics. They can be difficult even for experienced programmers, especially when encountering something like dependent types[^dependent-T] or templated template parameters. They are complex enough to be turing complete[^turing-complete-templates]. You know what else is turing complete? SKI Combinators!

## Theory

There are several different combinator logics, but I would like to focus your attention on SKI Combinators (later SKI). I claim they are simpler to understand than the other systems, while remaining capable, besides, all the other combinator logics can be expressed using SKI. So what are S, K and I? 

They are transformation rules. Since combinators are functions, they have arguments and return values. Think of them as rearranging operation: the arguments is the data to transform and the return value is the data rearranged. For instance, the **K** Combinator has a rule **K**xy → x. We can see it in action in an expression like "`Kab`". If we translate that into action, that would just mean "take the next two terms after you and replace yourself with the first term". That would map "`Kab`" to "`a`". We call this tranformation "applying a combinator", same way you would apply a function.

Combinators are left associative, that means that `x y z = (x y) z`. That might some non-impactful, but `K (I S)` and `(K I) S` are two very different expressions, as we will discover shortly. In this case parentheses work same way as in classical algebra.

Combinators are "curried", that is to say accept arguments in an unusual way. Instead of accepting all the arguments at once, they transition into a special "partially-applied" state, where they can accept the next argument. When all the arguments are recieved the combinator is considered fully applied and evaluated. See for yourselves in the example below:


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

Here we use two different functions. `classical_max` is a usual function, while `curried_max` is curried. That might seem like a more complicated to call the function, however, this partially applied state will allow us to generate new combinators. 


| Combinator  |  Rewrite Rule      | Example                         |
| ----------- |  ----------------- | ------------------------------- |
| I           |  **I**x → x        | (**I**u)v → uv                  |
| K           |  **K**xy → x       | **I**(**K**ab) → **I**b → b     |
| S           |  **S**xyz → xz(yz) | **SK**fg → **K**g(fg) → g       |

The table above describes how specific combinators operate on their inputs. When computing combinators we  apply the rule of the leftmost combinator step by step. If this combinator is a placeholder, we just look for the next leftmost combinator. If there are no more combinators we stop, the expression is considered "simplified" or "normalized". When something is normalized it is in its "head normal form" (SOURCE?). This term is derived from lambda calculus, but I digress. We may more closely inspect the transformation for the last example, since it is the most complex one.

**SK**fg. *Our initial state. The leftmost combinator is **S**. We rewrite our initial state according to rule **S**. In this context, `x` = **K**, `y` = `f`, `z` = `g`. They are rearanged to become* **K**g(fg). *Now we apply rule **K**. In the context of **K**, `x` = `g` and `y` = `(fg)`.* g. *No more rules to apply, simplification done.* **SK**fg → **K**g(fg) → g.

This process can go in two different ways: lazy or eager. The first approach (as already described) is evaluating the leftmost combinator, while the second one prioritizes the deepest combinator (the combinator most deeply nested in the parentheses). The result will be the same, but the intermediate steps vary. See the difference for yourself below (italicized letter after the combinator is the applied rule):

* lazy. **SKII** *S→* **KI**(**II**) *K→* **I**
* eager. **SKII** *S→* **KI**(**II**) *I→* **KII** *K→* **I**

It rarely makes sense to first evaluate the deepest expression first (but it will down the line), like in the example above eager took one more step to execute, besides, you are guaranteed to get to the same result anyway. Feel free to look over it several times and try doing it by yourself. If you want to validate your understanding try simplifying `S(K(SI))K` or `SK(KK)`; we will return to those specific combinators in the next section.

## Abuse Of Type Inference

That is all well and good, but what can we do with this? We can play around a bit, trying out different combinations to see just how far we can stretch this. Sure, we can make a runtime with several types of objects all implementing some common interface, but that's no fun. I desire to compute them unusually, at compile time, just for the sake of it, for no particular reason. To do that we are going to express combinators and their half-applied states as structs, whereas function application will be a type instantiation. 

For those unfamiliar with the lingo, type instantiation is the process of turning a type template into a type, every time you write `std::vector<int>` you instantiate a type `std::vector<int>` based on a template of `std::vector<T, Allocator>`. That's the reason for putting `<>` after a template name, even when all template parameters have a default value. 

```cpp
// Imagine all the required imports for futher snippets
using namespace std;

// Ix -> x
struct I {
    template <typename T> 
    using apply = T; 
};

static_assert(is_same_v<I::apply<int>, int>); // Passes!
static_assert(is_same_v<I::apply<I::apply<int>>, int>); // Also, passes!
```

The combinator above is our trusty identity function. It returns whatever type was it's argument. Sure, it might not seem as useful as the others, but in certain conditions we would like our combinators to not affect their inputs. You instantiate it with some other type by saying `I::apply<int>`, which will give you back `int`. No surprises here. For more complex combinators the C++'s type inference system will be the one to apply the rules, we simply need to encode them in the language that it understands, the template language.

```cpp
// Kxy -> x
struct K2 {
    template <typename X> 
    struct K1 {
        template <typename Y> 
        using apply = X;
    };

    template <typename X> 
    using apply = K1<X>;
};

using K = K2;
```
```cpp
// Sxyz -> xz(yz)
struct S3 {
  template <typename X, typename Y> 
  struct S1 {
    // FIXME?
    template <typename Z> 
    using helper = typename Y::apply<Z>;
    template <typename Z>
    using apply = typename X::apply<Z>::apply<helper<Z>>;
  };

  template <typename X> 
  struct S2 {
    template <typename Y> 
    using apply = S1<X, Y>;
  };

  template <typename X> using apply = S2<X>;
};

using S = S3;
```

A binary `K` is denoted as `K2`, while a partially-applied `K2` is denoted `K1`, the number after the combinator letter expresses its arity (the amount of arguments it accepts[^arity]).

When explainaing combinators we denoted a combinator placeholder with lowercase letters. They help make everything more visual and less abstract, so let's define that too. Since we never know how many arguments we may try and supply to the combinator we make them variadic. We will define several letters, so makes sense to turn them into a macro.

```cpp
#define define_combinator_placeholder(ch)
    template <typename... Args> 
    struct _##ch {
        template <typename X> 
        using apply = _##ch<Args..., X>; 
    }; 
    using ch = _##ch<>;

define_combinator_placeholder(a);
define_combinator_placeholder(b);
define_combinator_placeholder(c);
```

At last, we may input the previously mentioned combinator expressions and see what they evaluate to.

```cpp
// S(K(SI))K
using R = S::apply<K::apply<S::apply<I>>>::apply<K>;
using result = R::apply<a>::apply<b>;  

// SK(KK)
using I = S::apply<K>::apply<K::apply<K>>;
using result = I::apply<a>;
```

Here the **R** combinator will swap it's arguments, going from "ab" to "ba". In the second case it's called **I** for a reason. The thing is, we can express the **I** combinator in terms of **S** & **K**, it is precisely **SKK** or **SKS** or even **SK**a, where "a" is any combinator. Functionally **I** is but syntactic sugar, so the system might as well be called SK Calculus (which it is, sometimes). When the head normal form of one combinator is equal to head normal form of another, we say they are "extensionally equal". There always is an infinite amount of SK combinator sequences that are extensionally equal to some other program, since for any sequence *a* we can transform it into **SKK***a*, which we can later transform into **SKK**(**SKK***a*) and so on forever.

## Solving For Combinators

Well, we have managed to transform some expressions around, that was surely fun, but there must be a way of converting any set of inputs to any set of outputs? Such way there is, in the book "The Implementation of Functional Programming Languages"[^impl-of-fn-lang] section 16.1 the author talks about one possible way of transforming lambda calculus into SKI calculus, to avoid another layer of complexity imagine an the anonymous combinator, it's just a combinator without a name. For instance (*xy* → *xy*) is an anonymous combinator extensionally equal to **I**. They work as ordinary combinators, except they don't have a name to call them by, mostly due to the fact the we wouldn't need that name anywhere in our derivation. After all, we don't want our combinators to depend on how they are called too. As it is with ordinaray combinators, then can accept multiple arguments through currying, so (*xy* → *x*) is extensionally equal to (*x* → (*y* → *x*)).

If we invert the definitions for all our combinators we can deduce several rule on how an anonymous combinator can be transformed into an SKI Sequence. By inversing the definitions of all known combinators we get can transformations. They work as follows:

* (*x* → *x1 x2*) S⇒ **S** (*x* → *x1*) (*x* → *x2*)
* (*c* → (*x* → *c*)) K⇒ **K***cx*
* (*x* → *x*) I⇒ **I**x
Note the double arrow, it marks a reverse rewrite. A reverse arrow would be more appropriate, but it find it a bit confusing. These rules are enough to transform any anonymous combinator into terms of SKI! Let's follow an example, say we want to express some **ω***x* → *xx*:

1. (*x* → *xx*)
2. S⇒ **S** (*x* → *x*) (*x* → *x*)
3. I⇒ **SII**

Wonderful! Working backwards allowed us to display The transformation was successful, which we can verify for outselves. What about a more complex example, say **R***xy* → *yx*:

1. (*xy* → *yx*)
2. (*x* → (*y* → *yx*))
3. S⇒ (*x* → **S** (*y* → *y*) (*y* → *x*))
4. I⇒ (*x* → **SI** (*y* → *x*))
5. S⇒ **S** (*x* → **SI**) (*x* → *y* → *x*)
6. K⇒ **S**(**K**(**SI**))**K**

**S**(**K**(**SI**))**K***ab* → *ba*. Notice, how we can not apply K reduction on the last term on step 3. In that innermost anonymous combinator the resulting *x* depends on an *x*, that was supplied as the argument, which we have to preserve. If that *x* was some constant we could safely rewrite it in terms of **K**.

We also discovered that **I** can be discovered using **SK**, so let's apply the algorithm to find it again.

TODO: DO THE THING

## Boolean Logic

Boolean logic can be reconstructed using the SKI Combinators. These logic systems are interchangeable, you can easily translate one into another, but only if we stretch the definition of easy. We can safely have half-applied combinators, so let **T** and **F**, true and false respectively, be combinators too! But what arguments can they accept? All of logic can be expressed using if-then-else statements, so we can express a branch statement as either the **T** or the **F** combinator! Let **T**xy → x, **F**xy → y. Now, that we have a conditional we can devise negation, the second simplest logical operation (the first simplest one is a tautology, **I** is not that difficult to devise). If we keep using single letters to define combinators we will run out very soon, we already would have a collision of **I** the identity and **I** the implication, so we will denote logical operations with words, in this case the word is ***not***.

Let's express it directly through an if-else statement, where x is our input:&nbsp;***not***&nbsp;x&nbsp;→&nbsp;x**FT**. This is wonderful and we could just leave it like that, but this form is not SKI. What can be useful here is the undermentioned **V** combinator, from Raymond Smullyan's[^mock] book. This combinator is defined **V**xyz → zyx, which is of great use to us, since **VTF**x *V→* x**FT**, which is our definition for ***not***.

## Recursion & Loops

We already mentioned that SKI Combinators are turing complete, so why not do something that requires turing completeness? What can be more turing than a machine that halts! Behold the **ω** (*little* omega, size matters) combinator: **ω**x → xx, or in terms of SKI: **ω**x → **SII**x. All it does is applies the argument to itself, apply it twice and you have an infinite recursion: **ωω** → **ωω**, magical. This is the **Ω** (*large* omega or just omega) combinator and it doesn't care for its arguments at all. This combinator doesn't have a "normalized" or a "head-normal" form, since it will be always be stuck being itself. Funky. 

```cpp
// Since they get stuck in an infinite loop we
// can't even define them in a file without getting a compilation error
#ifdef 0

struct ω {
  template <typename X> using apply = typename X::apply<X>;
};

using Ω = ω::apply<ω>;

#endif
```

But there is much more. A *fixed-point* combinator, is such combinator that when applied to itself expands into itself, the **Ω** combinator is an example of that. The extremely powerful fixed point combinator is the **Y** Combinator[^yes-that-y-combinator].

TODO: SOLVE FOR RECURSIVE FUNCTIONS

## One J To Rule Them All

If you read this far, congratulations. You probably understand more about combinators than 99.9% of the earth's population. A rather niche skill, ey? As we already saw, complex result can emerge from rather simple (albeit seemingly random) behaviour. As mentioned in the introduction, SKI calculus is the simplest calculus there is, since all other calculi can be expressed using it. We can reduce calculus even further! Introducing ι (iota or jot), the mother of j, so let **J** be the letter to denote it. First discovered by Chris Barker[^barker-iota], if we define **J**x → x**SK**, we can reconstruct all the other combinators through it. Based on it's arguments **J** can compute into combinators of different arity, depending on "x". That makes it very special, since it's the only combinator we've seen so far with variable arity, but we will see more of that in the future. The table below shows how exactly all the combinators can be reconstructed. 

| Combinator  | Jot Expansion                                                              |
| ----------- | -------------------------------------------------------------------------- |
| J           | **J**                                                                      |
| I           | lazy. **JJ** → (**JS**)**K** → **SSKK** → **SK**(**KK**) → **I**           |
| K (*part 1*)| eager. **J**(**J**(**JJ**)) → **J**(**JI**) → **J**((**IS**)**K**) →       |
| K (*part 2*)| → **J**(**SK**) → **SKSK** → **KK**(**SK**) → **K**                        |
| S           | lazy. **J**(**J**(**J**(**JJ**))) → **JK** → **KSK** → **S**               |

This simplicity made it popular amongst logical minimalists and birthed several Turing tarpit[^turing-tarpit] languages[^iota-esolang]. Let's define that wonderful monstrosity in our C++ code. We are doing templates, haven't you forgot?

```cpp
struct J {
  template <typename X> 
  using apply = typename X::apply<S>::apply<K>;
};
```

## Conclusion

Congrats! Your favourite compiled language doubles as a proof assistant!

## Acknowledgement

Great thanks to [Giorgio Grigolo](https://grigolo.mt/) and [Dr Alexander Farrugia](https://www.um.edu.mt/profile/alexfarrugia) at [The University of Malta](um.edu.mt) for helping me with some bits of research and finding some sources. Also huge thanks to all of my friends how bothered to proofread this post many more than several times.

If you found everything above entertaining, consider learning more using the following links, organized in no particular order. This all is something I can't specifically cite any of them, but they helped me do my research.

((TODO: Add web.archive.org links to everything))

2. A [wonderful post](https://doisinkidney.com/posts/2020-10-17-ski.html) on SKI Combinators by Donnacha Oisín Kidney.
3. The Y-Combinator on [Computerphile](https://www.youtube.com/watch?v=9T8A89jgeTI&ab_channel=Computerphile) explained by Graham Hutton. 
4. [Combinatorial Ornithology](https://library.wolfram.com/infocenter/MathSource/4862/).
5. David C. Keenan's ["To Dissect A Mockingbird"](https://dkeenan.com/Lambda/), a deeper description of lots and lots of combinators.
6. "New arithmetical operators in the theory of combinators" by W.L. van der Poel, C.E. Schaap and G. van der Mey.

[^impl-of-fn-lang]:  Simon L. Peyton Jones ["The Implementation of Functional Programming Languages"](https://isbnsearch.org/isbn/0134533259)
[^comblogic-hs]: [Combinatory Logic](https://wiki.haskell.org/Combinatory_logic) on haskell.org.
[^nlab-lcalc]: [Lambda Calculus](https://ncatlab.org/nlab/show/lambda-calculus) on nLab.
[^dependent-T]:[Cppreference](https://en.cppreference.com/w/cpp/language/dependent_name) on dependent types. [Dependent Types](https://ncatlab.org/nlab/show/dependent+type+theory) on nLab.
[^turing-complete-templates]: Oh yes, the templates really are turing complete, [even cppref admits it](https://en.cppreference.com/w/cpp/language/template_metaprogramming).
[^arity]: Arity is just how many arguments the function expects. You already heard in words like "bin**ary**" and "un**ary**". [Arity](https://ncatlab.org/nlab/show/arity) on nLab (abstraction warning).
[^barker-iota]: Chrid Barker's "[Iota and Jot: the simplest language?](https://web.archive.org/web/20091116052048/http://semarch.linguistics.fas.nyu.edu/barker/Iota/)" on wayback machine.
[^turing-tarpit]: [Turing Tarpit](https://esolangs.org/wiki/Turing_tarpit) as defined by esolangs.org.
[^iota-esolang]: [Iota](https://esolangs.org/wiki/Iota), the esoteric programming language on esolangs.org.
[^yes-that-y-combinator]: Yes, if you are wondering whether [Y-Combinator](https://ycombinator.com) the website was named after this, yes. Yes it was.
[^mock]: Raymond Smullyan's ["To Mock A Mockingbird"](https://isbnsearch.org/isbn/0192801422). A gentle introduction to combinatory logic, presented as a series of recreational puzzles using bird watching metaphors.

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

Feel free to look over it several times and try doing it by yourself, that will only help your understanding of combinators. If you want to validate your understanding try simplifying `S(K(SI))K`, we will return to that specific combinator in the next section. Alternatively, you may also look at `SK(KK)`.

## Abuse Of Type Inference

That is all well and good, but what can we do with this? We can play around a bit, trying out different combinations to see just how far we can stretch this. Sure, we can make a runtime with several types of objects all implementing some common interface, but that's no fun. I desire to compute them unusually, at compile time, just for the sake of it, for no particular reason. To do that we are going to express combinators and their half-applied states as structs, whereas function application will be an type instantiation. 

For those unfamiliar with the lingo, type instantiation is the process of turning a type template into a template, every time you write `std::vector<int>` you instantiate a type `std::vector<int>` based on a template of `std::vector<T, Allocator>`. That's the reason for putting `<>` after a template name, even when all template parameters have a default value. 

```cpp
// Ix -> x
struct I {
    template <typename T> 
    using apply = T; 
};
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
#define Var(ch)
    template <typename... Args> 
    struct _##ch {
        template <typename X> 
        using apply = _##ch<Args..., X>; 
    }; 
    using ch = _##ch<>;

Var(a);
Var(b);
Var(c);
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

## More Interesting Stuff

As previously mentioned, SKI Combinators can be used to encode logic, the simplest of all logics is the boolean logic. The **K** combinator is a great starting. The **K** gives us the first of it's arguments, and if we combine **S** and **K** like **SK**, we have a combinator that gives us it's second argument. Wonderful. All of boolean logic can be encoded using *if-then-else* expressions, and the combinators above let us return one combinator or another, based on their own value. We formally define them as follows:

| Combinator  | Lambda Calculus |  Rewrite Rule      | SKI Encoded         |
| ----------- | --------------- |  ----------------- | ------------------- |
| T           | λx.λy.x         |  **T**xy → x       | `K`                 |
| F           | λx.λy.y         |  **F**xy → y       | `KS`                |

Since we have our *if-then-else* clause we can define more complex structures, like basic logic operations: not, or, and.

Not is the simplest of the bunch, we expect it to return `F` when given `T` and `T` when given `F`. But how can we actually encode behaviour if the combinator rules don't know anything about the combinators they are operating on? Simple, postfix notation. Assuming we are only going to be using the boolean logic combinators for these expressions, we can encode `not` in postfix notation like so: `FT = SKK`.

| Combinator  | Lambda Calculus |  Rewrite Rule      | SKI Encoded         |
| ----------- | --------------- |  ----------------- | ------------------- |
| T           | λx.λy.x         |  **T**xy → x       | `K`                 |
| F           | λx.λy.y         |  **F**xy → y       | `KS`                |

## Conclusion

Congrats! Your favourite compiled language doubles as a proof assistant!

## See Also

1. Raymond Smullyan's ["To Mock A Mockingbird"](https://isbnsearch.org/isbn/0192801422). A gentle introduction to combinatory logic, presented as a series of recreational puzzles using bird watching metaphors.
2. A [wonderful post](https://doisinkidney.com/posts/2020-10-17-ski.html) on SKI Combinators by Donnacha Oisín Kidney.
3. The Y-Combinator on [Computerphile](https://www.youtube.com/watch?v=9T8A89jgeTI&ab_channel=Computerphile) explained by Graham Hutton. 

[^nlab-lcalc]: [Lambda Calculus](https://ncatlab.org/nlab/show/lambda-calculus) on nLab.
[^dependent-T]:[Cppreference](https://en.cppreference.com/w/cpp/language/dependent_name) on dependent types. [Dependent Types](https://ncatlab.org/nlab/show/dependent+type+theory) on nLab.
[^turing-complete-templates]: Oh yes, the templates really are turing complete, [even cppref admits it](https://en.cppreference.com/w/cpp/language/template_metaprogramming).
[^arity]: Arity is just how many arguments the function expects. You already heard in words like "bin**ary**" and "un**ary**". [Arity](https://ncatlab.org/nlab/show/arity) on nLab (abstraction warning).

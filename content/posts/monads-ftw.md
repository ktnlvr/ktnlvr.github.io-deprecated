---
title: "Exploration and Mimicry of Monads in Non-functional Languages"
date: 2023-02-25T23:33:07,929822743+02:00
---

This article is intended to demonstrate in a usual context and aimed at one of my friends, who keeps forgetting how they work. If you are reading this, you know that's you. When thinking about monads it's important to differentiate their meaning in the world of mathematics and in the world of practical programming. Since I am not a mathematician as of writing this post I will be focusing on the practical aspect of their usage. All the examples are given in Python-esque syntax with some details ommited for brevity.

## Combating Nullability

Imagine the following: you are writing a matchmaking system and you want your players to hang out together. For that purpose you designed a system of rooms.

{{< sidenote text="`@struct` serves the same function as `@dataclass` in classical Python" >}}
```py
@struct
class Room:
    room_name: str
    password: str
    current_players: int
    max_players: int | None
```

We want to implement some logic concerning connecting to a room, which involves checking if 
there is space available for another player.

```py
def try_connect_to_room(room: Room, player: Player) -> bool:
    if room.max_players is not None:
        if room.max_players < room.current_players:
            room.connect(player)
            return True
    return False
```

This is a standard way of handling a nullable value. We can probably see ourselves writing similar code in production. Now imagine the same piece without type annotations and very little documentation. 
An experienced programer might guess that `max_players` can very well be `None`, but the language itself doesn't tell you that.
Let's try and fix that possible problem with the following structure.

{{< sidenote text="The operation of transforming a value of type `T` into `Functor[T]` is commonly called \"lifting\" or less commonly \"wrapping\". In this case the lift is `Something[T]`." >}}
```py
@struct 
class Maybe[T]:
    _value: T | None

    def fmap[P](self, f: Function[T -> P]) -> Maybe[P]:
        if self._value is not None:
            new_value: P = f(self._value)
            return Maybe[P](_value = new_value)

    def unwrap_or(self, alternative: T) -> T:
        if self._value is not None:
            return self._value
        else:
            return alternative

def Something[T](value: T) -> Maybe[T]:
    return Maybe[T](_value=value)

def Nothing[T]() -> Maybe[T]:
    return Maybe[T](_value=None)

@struct
class Room:
    # *snip*
    max_players: Maybe[int]

def try_connect_to_room(room: Room, player: Player) -> bool:
    def max_players_lt_current_players(max_players: int) -> bool:
        return max_players < room.current_players
    
    def connect_if_true(pred: bool):
        if pred:
            room.connect(player)
        return pred
                                                # Type of the expression
    did_connect = room.max_players              # Maybe[int]
        .fmap(max_players_lt_current_players)   # Maybe[bool]
        .fmap(connect_if_true)                  # Maybe[bool]
        .unwrap_or(False)                       # bool

    return did_connect
```

Whoa, that's a whole lot of complexity out of nowhere. For what sake? We already had a way of representing a possibly-missing value before, why all the fuss? This code has to handle nullability, otherwise it will definetly fail. That can guarantee the safety of the program. Might not seem like that big of a deal, but Tony Hoare, the inventor of `null` in most mainstream languages as we know it today himself, said this:

> I call it my billion-dollar mistake. It was the invention of the null reference in 1965 ... This has led to innumerable errors, vulnerabilities, and system crashes, which have probably caused a billion dollars of pain and damage in the last forty years. 

Here we used Monad's little brother, the lesser of three, a Functor.
You can call a Functor anything that has an `fmap` (functor map) function with the same signature.
Note the word "signature", the internals don't matter, it's the way it transforms the types that does. This is a common trend in functional programming languages, since all algorithms and programs are viewed as transforming data from one type into another. 

This was us handling a single nullable value, but what about chaining many nullable operations? Well, for that purpose we need a Monad. It is the same as a functor, but it has two more operations. The one we need is going to be `mmap` (monadic map) and for `Maybe[T]` it will look something like this.

```py
class Maybe[U]:
    # *snip*
    def mmap[V](self, f: Function[U -> Maybe[V]]) -> Maybe[V]:
        if self._value is None:
            return None
        else:
            new_value = f(self._value)
            return Maybe[V](_value = new_valeu)
```

The usability of this becomes even more drastic when composing a lot of nullable values together, like in the example below.

```py

# All these functions may be null, so they 
# will return either T | None or Maybe[T]
# depending on the context
def get_user(name) -> Any
def get_email(user) -> Any
def get_smpt_server(user) -> Any
def get_host(server) -> Any

# Example with all the functions returning T | None
def get_gregs_smpt_host_nullable() -> IpV4 | None:
    greg = get_user_nullable("greg")
    if user is None:
        return None
    email = get_email(greg)
    if email is None:
        return None
    server = get_smpt_server(email)
    if server is None:
        return None
    host = get_host(server)
    return host

# Same example with all functions returning Maybe[T]
def get_gregs_smpt_host_maybe() -> Maybe[IpV4]
    get_user_maybe("greg")
        .mmap(get_user)
        .mmap(get_email)
        .mmap(get_smpt_server)
        .mmap(get_host)
```

This example is of course very dramatic, but it should demonstrate the effectiveness fairly well.

## Lazy Evaluation

TODO

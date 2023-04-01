expr = "S(K(SI))K ab"

expr = expr.replace(' ', '')


def parse(input: str) -> tuple[list[str], str]:
    ls = []
    while input:
        match input[0]:
            case "(":
                parsed, input = parse(input[1:])
                ls.append(parsed)
            case ")":
                return (ls, input[1:])
            case _:
                ls.append(input[0])
                input = input[1:]
    return (ls, "")


def parse_ski(input: str) -> list[str | list]:
    return parse(input)[0]


def simplify(input: list[str | list]) -> list[str | list] | str:
    print(input)
    match input:
        case ["I", x, *rest]:
            return simplify([x] + rest)
        case ["K", x, _, *rest]:
            return simplify([x] + rest)
        case ["S", x, y, z, *rest]:
            return simplify([x, z, simplify([y, z])] + rest)
        case [[*contents], *rest]:
            return simplify(contents + rest)
        case [*prev, [*contents]]:
            return simplify(prev + contents)
        case _:
            return input

def stringify(input: list) -> str:
    match input:
        case [[*ls], *rest]:
            return f"({stringify(ls)})" + stringify(rest)
        case [*ls]:
            return ''.join(ls)
        case _:
            return input

parsed = parse_ski(expr)
print(simple := simplify(parsed))
print(stringify(simple))

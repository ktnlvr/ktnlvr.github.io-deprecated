from copy import deepcopy

expr = ""

expr = expr.replace(" ", "")


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
    match input:
        case ["I", x, *rest]:
            return simplify([x] + rest)
        case ["K", x, _, *rest]:
            return simplify([x] + rest)
        case ["S", x, y, z, *rest]:
            return simplify([x, z, simplify([y, z])] + rest)
        case [thing, [next], *rest]:
            return simplify([thing, next] + rest)
        case [[*contents], *rest]:
            return simplify(contents + rest)
        case []:
            return []
        case _:
            return input


def deepest_list(input: list[list | str]):
    for item in input:
        if type(item) == list:
            return deepest_list(item)
    else:
        return input


def transform(input: list[list | str], output: list[list | str]):
    while not simplify(input) == simplify(output):
        
    return input

def parenthesise(input: list[list | str]):
    out = [input[0]] + [parenthesise(x) for x in input[1:]]
    return out


def stringify(input: list, toplevel=False) -> str:
    match input:
        case [[*ls], *rest]:
            return f"({stringify(ls)})" + stringify(rest)
        case [*ls]:
            string = "".join(stringify(x) for x in ls)
            return f"({string})" if not toplevel else string
        case _:
            return input


parsed = parse_ski(expr)

vars = "xyz"

if __name__ == "__main__":
    print("Running in REPL mode")
    while True:
        try:
            data = input("> ").strip()

            if data.startswith("?"):
                expr = parse_ski(data[1:])
                target = input("? ").strip()
                target = simplify(parse_ski(target))
                print(
                    f"Reducing {parenthesise(expr)} to {parenthesise(target)}"
                )
                print(transform(parenthesise(expr), parenthesise(target)))

            else:
                print(
                    stringify(simplify(parse_ski(data)), toplevel=True)
                )
        except RecursionError:
            print("Recursion too deep")
            exit(-1)

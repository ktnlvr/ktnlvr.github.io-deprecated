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
        case [[*contents], *rest]:
            return simplify(contents + rest)
        case _:
            return input


def bfs(input: list[list | str], start: list[str], target: list[list | str]):
    simple_target = simplify(target)
    def mutate(combinator: str):
        transformed = []
        for i in range(len(input) + 1):
            cp = deepcopy(input)
            if i < len(input) and cp[i] == combinator:
                continue
            cp.insert(i, combinator)
            transformed.append(cp)
            try:
                if simplify(cp + start) == simple_target:
                    print('!!!!', cp)
                    exit(-1)
            except RecursionError:
                continue
        for i, item in enumerate(input):
            if type(item) is list:
                for trans in bfs(item, target=target):
                    transformed.append(
                        input[:i] + [trans] + input[i + 1 :]
                    )
        return transformed

    all = mutate("S") + mutate("K") 
    return all


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

inputs = [parsed]
for i in range(9):
    for input in inputs[::]:
        new_inputs = []
        for x in bfs(input, ['a', 'b'], ['b', 'a']):
            print(u := x)
            new_inputs.append(u)
        inputs = new_inputs

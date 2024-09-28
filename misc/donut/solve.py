import sys

sys.setrecursionlimit(10 ** 9)

# Tower of Hanoi

n = 10

# Manually input
stacks = [
    [2, 3, 6, 8, 9][::-1],
    [1, 7][::-1],
    [4, 5, 10][::-1]
]

instructions = []
visited = set()


def dfs():
    if len(stacks[-1]) == n:
        print("\n".join(f"{fro + 1}\n{to + 1}" for fro, to in instructions))
        return

    t = tuple(map(tuple, stacks))
    if t in visited:
        return
    visited.add(t)

    for i in range(3):
        for j in range(3):
            # move from i to j
            if i != j and stacks[i] and (not stacks[j] or stacks[i][-1] < stacks[j][-1]):
                stacks[j].append(stacks[i].pop())
                instructions.append((i, j))
                dfs()
                stacks[i].append(stacks[j].pop())
                instructions.pop()


dfs()

# Copy and paste output (instructions) into nc

# bctf{tHe_T0wErs_NeVER_Lie}

r = float(input("Enter the value of r: "))
print()

matrix = [[0 for _ in range(3)] for _ in range(3)]
result = [['-' for _ in range(3)] for _ in range(3)]
reward = [[r, -1, 10], [-1, -1, -1], [-1, -1, -1]]
policy = [['R', 'L', 'D'] for _ in range(3)]
prop = 0.8
otherProp = 0.1
dscont_fctr = 0.99
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]
actions = ['R', 'L', 'D', 'U']


def assign():
    policy[0][0] = '-'
    policy[0][2] = '-'


def isTerminal(i, j):
    return (i + j == 0) or (i == 0 and j == 2)


def get_base(i, j, d):
    i = min(i + dx[d], 2)
    i = max(0, i)
    j = min(j + dy[d], 2)
    j = max(0, j)
    return (i, j)


def get_other(i, j, d):
    x = 0
    y = 1
    if dx[d] == 0:
        x = 1
        y = 0
    i1 = min(i + x, 2)
    i1 = max(0, i1)
    j1 = min(j + y, 2)
    j1 = max(0, j1)
    i2 = min(i - x, 2)
    i2 = max(0, i2)
    j2 = min(j - y, 2)
    j2 = max(0, j2)
    return [(i1, j1), (i2, j2)]


def compute_func(i, j, d, V):
    if not isTerminal(i, j):
        (P1x, P1y) = get_base(i, j, d)
        [(P2x, P2y), (P3x, P3y)] = get_other(i, j, d)
        return (prop * (reward[i][j] + dscont_fctr * V[P1x][P1y])
                + otherProp * (reward[i][j] + dscont_fctr * V[P2x][P2y])
                + otherProp * (reward[i][j] + dscont_fctr * V[P3x][P3y]))
    else:
        return reward[i][j]


def policy_evaluation(V, policy):
    while True:
        delta = 0
        # Vi-1
        temp = [row[:] for row in V]
        for i in range(3):
            for j in range(3):
                v = V[i][j]
                action = policy[i][j]
                d = actions.index(action)
                V[i][j] = compute_func(i, j, d, temp)
                delta = max(delta, abs(v - V[i][j]))
        if delta < 1e-6:
            break


def policy_improvement(V, policy):
    policy_stable = True
    for i in range(3):
        for j in range(3):
            old_action = policy[i][j]
            values = []
            # Compute values for all actions
            for d in range(4):
                values.append(compute_func(i, j, d, V))
            # Get the best action
            best_action = actions[values.index(max(values))]
            policy[i][j] = best_action
            # Check if policy has changed
            if old_action != best_action:
                policy_stable = False
    return policy_stable


V = [[0 for _ in range(3)] for _ in range(3)]

iterations = 0

while True:
    iterations += 1
    policy_evaluation(V, policy)
    stable = policy_improvement(V, policy)
    if stable:
        break

assign()

print("Optimal Policy:")
for row in policy:
    print(row)

print("Optimal Value Function:")
for row in V:
    print(row)

print("Number of iterations:", iterations)

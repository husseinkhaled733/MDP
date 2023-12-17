r = float(input("Enter the value of r: "))

print()

needed = 0
matrix = [[0 for _ in range(3)] for _ in range(3)]
result = [[0 for _ in range(3)] for _ in range(3)]
reward = [[r, -1, 10], [-1, -1, -1], [-1, -1, -1]]
positions = [[[0.0] * 4 for _ in range(3)] for _ in range(3)]
temp = [row[:] for row in matrix]
actions = ['R', 'L', 'D', 'U']
policy = [[0 for _ in range(3)] for _ in range(3)]
prop = .80
otherProp = .10
dscont_fctr = 0.99
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]


def assign():
    result[0][0] = '-'  # remove it to make r is not term
    result[0][2] = '-'


def isTerminal(i, j):
    return (i + j == 0) or (i == 0 and j == 2)  # remove first


def get_base(i, j, d):
    i = min(i + dx[d], 2)
    i = max(0, i)
    j = min(j + dy[d], 2)
    j = max(0, j)
    return i, j


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


def compute_func(i, j, d):
    if not isTerminal(i, j):
        (P1x, P1y) = get_base(i, j, d)
        [(P2x, P2y), (P3x, P3y)] = get_other(i, j, d)
        return (prop * (reward[i][j] + dscont_fctr * temp[P1x][P1y])
                + otherProp * (reward[i][j] + dscont_fctr * temp[P2x][P2y])
                + otherProp * (reward[i][j] + dscont_fctr * temp[P3x][P3y]))
    else:

        return reward[i][j]


needed_counter = 0
flag = True
counter = 0
while (flag):
    needed_counter += 1
    counter = 0
    temp = [row[:] for row in matrix]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            for d in range(4):
                positions[i][j][d] = compute_func(i, j, d)
            max_value = max(positions[i][j])
            matrix[i][j] = max_value
            max_index = positions[i][j].index(max_value)
            result[i][j] = actions[max_index]
            if abs(matrix[i][j] - temp[i][j]) <= .000001:
                counter += 1

    if counter == 9:
        needed = needed_counter
        needed_counter = 0
        flag = False

assign()
print("The number of iteration needed : ")
print(needed)
print("This 3d Array for 4 dirction for all  postions ")
for i in range(3):
    for j in range(3):
        print("For {}, {}: ".format(i, j), end="")
        for k in range(4):
            print(positions[i][j][k], end=" ")
        print()  # Move to the next line after printing the 4 values

print()
print("Array of results for all postions")
for row in range(3):
    for k in range(3):
        print(result[row][k], end=" ")
    print()
print()
print("This 2d Array for all  postions ")
for row in range(3):
    for k in range(3):
        print(matrix[row][k], end=" ")
    print()

# Global declrations
sensor_right = 0.7
p_move = 0.8
sensor_wrong = 1 - sensor_right
p_stay = 1 - p_move


def localize(colors, measurements, motions, sensor_right, p_move):
    # we first ensure p is a grid of uniform distribution with the same dimensions as 'colors'
    # Uniform distribution = robot is in maximum confusion with regards to its location
    pinit = 1.0 / float(len(colors)) / float(len(colors[0]))
    p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]
    return(p)


def move(p, p_move, motions):
    # create a new grid to account for the robot movements along with the respective probabilities
    q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    for i in range(len(p)):
        for j in range(len(p[i])):
            # each value in this grid q is a result of the sum of the chances of the robot completing its motion and not completing its motion
            # think Theorem of Total Probability
            q[i][j] = (p_move * p[i - motions[0] % len(p)][j - motions[1] % len(p)]) + p_stay * p[i][j]
    return(q)


def sense(p, colors, sensor_right, measurements):
        # here in this function we calculate the required probabilites and then normalize them
    q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
    s = 0.0
    for i in range(len(p)):
        for j in range(len(p[i])):
            hit = (measurements == colors[i][j])
            q[i][j] = p[i][j] * (sensor_right * hit + sensor_wrong * (1 - hit))
            s += q[i][j]
    for i in range(len(q)):
        for j in range(len(p[i])):
            q[i][j] /= s
    return(q)


def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x), r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')


colors = [['R', 'G', 'G', 'R', 'R'],
          ['G', 'R', 'G', 'R', 'R'],
          ['R', 'G', 'R', 'G', 'R'],
          ['G', 'R', 'R', 'R', 'R']]
measurements = ['R', 'R', 'R', 'R', 'R']
motions = [[0, 0], [0, 1], [1, 0], [1, 0], [0, 1]]
p = localize(colors, measurements, motions, sensor_right, p_move)

# We first move the robot via the move function
# Then we read the sensor readings via sense function

for i in range(len(measurements)):
    p = move(p, p_move, motions[i])
    p = sense(p, colors, sensor_right, measurements[i])
show(p)

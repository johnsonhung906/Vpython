from vpython import *

def af_col_v(m1, m2, v1, v2, x1, x2): # function after collision velocity
    v1_prime = v1 + 2*(m2/(m1+m2))*(x1-x2) * dot (v2-v1, x1-x2) / dot (x1-x2, x1-x2)
    v2_prime = v2 + 2*(m1/(m1+m2))*(x2-x1) * dot (v1-v2, x2-x1) / dot (x2-x1, x2-x1)
    return (v1_prime, v2_prime)

#parameters
size, m = 0.2, 1
k = 150000
sin = 0.22214
L = 2
N = 2
d = [-0.8 + 0.4 * i - 2 * sin for i in range(N)] + [-0.8 + 0.4 * i for i in range(N, 5)]
scene = canvas(width=600, height=600, center=vec(0, 0, 0), background=vec(0, 0, 0), align='left')
# floor = box(pos = vec(0, -2, 0), length=2, height=0.005, width=2, color=color.blue)
balls = []
springs = []

#setting initial positions
for i in range(5):
    if i <= N - 1:
        ball = sphere(pos=vec(d[i], size - 0.95, 0), radius=size, color=color.white)
        ball.v = vec(0, 0, 0)
        balls.append(ball)
    else:
        ball = sphere(pos=vec(d[i], size - 1, 0), radius=size, color=color.white)
        ball.v = vec(0, 0, 0)
        balls.append(ball)
    spring = cylinder(pos=vec(-0.8 + 0.4 * i, size + 1, 0), radius=0.02)
    spring.axis = ball.pos - spring.pos
    springs.append(spring)
    #ball on the top of spring
    sphere(pos=vec(-0.8 + 0.4*i, size + 1, 0), radius=size/4, color=color.white)

# graph
ku_t_graph = graph(width=400, align='right', title='<b>instant_kinetic/potential_energy</b>'
                   , xtitle='<i>time(s)</i>', ytitle='<i>energy</i>')
funct1 = gcurve(graph=ku_t_graph, color=color.red, width=4)
funct2 = gcurve(graph=ku_t_graph, color=color.blue, width=4)

ku_t_over_graph = graph(width=400, align='right', title='<b>average_kinetic/potential_energy</b>'
                        ,xtitle = '<i>time(s)</i>', ytitle='<i>energy</i>')
funct3 = gcurve(graph=ku_t_over_graph, color=color.red, width=4)
funct4 = gcurve(graph=ku_t_over_graph, color=color.blue, width=4)

#parameters
g = vector(0, -9.8, 0)
dt = 0.0001
t = 0
total_k = 0
total_u = 0

while True:
    rate(5000)
    t += dt

    # plot graph
    instant_k = 0
    instant_u = 0
    for s in range(5):
        instant_k += 0.5 * m * (mag(balls[s].v) ** 2)
        instant_u += m * mag(g) * (balls[s].pos.y - (size - 1))

    funct1.plot(pos=(t, instant_k))
    funct2.plot(pos=(t, instant_u))

    total_k += instant_k
    total_u += instant_u

    funct3.plot(pos=(t, total_k * dt/t))
    funct4.plot(pos=(t, total_u * dt/t))

    # motion
    for i in range(5):
        springs[i].axis = balls[i].pos - springs[i].pos
        spring_force = -k * (mag(springs[i].axis) - L) * springs[i].axis.norm()
        balls[i].a = g + spring_force / m
        balls[i].v += balls[i].a * dt
        balls[i].pos += balls[i].v * dt
        for r in range(4):
            if (mag(balls[r].pos - balls[r + 1].pos) <= size * 2) and dot(balls[r].pos - balls[r + 1].pos,
                                                                          balls[r].v - balls[r + 1].v) <= 0:
                (balls[r].v, balls[r + 1].v) = af_col_v(m, m, balls[r].v, balls[r + 1].v, balls[r].pos,balls[r + 1].pos)


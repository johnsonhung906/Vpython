from vpython import *
g = 9.8
size = 0.25
scene = canvas(width=700, height=500, center = vec(0,5,0), background = vec(0.5,0.5,0),align = 'left')
#ball
ball = sphere(radius = size, color=color.red, make_trail = True, trail_radius = 0.05)
ball.pos = vec(-15, size, 0)
theta = pi/4
ball.v =  vec(20*cos(theta), 20*sin(theta), 0)
#floor
floor = box(length=30, height=0.05, width=10, color=color.blue)
C_drag = 0.9
#arrow
v_a = arrow(color = color.yellow, shaftwidth=0.1)
v_a.pos = ball.pos
v_a.axis = ball.v/3
#graph
v_t_graph = graph(width = 400, height = 400,align = 'right',title='<b>v-t graph</b>',xtitle = '<i>time(s)</i>',ytitle='<i>velocity(m/s)</i>')
funct = gcurve(graph = v_t_graph, color = color.red, width = 4)

dt = 0.0001
times = 0
max_height = 0
travel_dis = 0
t = 0
while times <= 2:
    t += dt
    rate(4000)
    v = (((ball.v.x)**2 + (ball.v.y)**2)**0.5)
    travel_dis += v*dt
    ball.v += vec(0, -g, 0) * dt - C_drag*ball.v*dt
    ball.pos += ball.v*dt
    v_a.pos = ball.pos
    v_a.axis = ball.v/3
    if ball.pos.y <= size and ball.v.y <0:
        ball.v.y = -ball.v.y
        times += 1
    if ball.pos.y > max_height:
        max_height = ball.pos.y
    funct1.plot(pos=(t, v))
msg = text(text = 'largest height = ' + str(max_height) + 'm', pos = vec(-10, 18, 0))
msg = text(text = 'total distance = ' + str(travel_dis) + 'm', pos = vec(-10, 15, 0))
msg = text(text = 'displacement = ' + str(ball.pos.x+15) + 'm', pos = vec(-10, 12, 0))

import numpy as np
from vpython import *
A, N = 0.10, 50
size, m, k, d = 0.06, 0.1, 10.0, 0.4
scene = canvas(title='Wave vector', width=800, height=300, background=vec(0.5,0.5,0), center = vec(0, 0, 0))
d_graph = graph(width = 400, height = 400, title='<b>dispersion relationship</b>',xtitle = '<i>wave vector</i>',ytitle='<i>angular frequency</i>')
func = gcurve(graph = d_graph, color = color.red, width = 4)

Unit_K = 2 * pi/(N*d)

for n in range(1, N//2):
    Wavevector = n * Unit_K
    phase = Wavevector * arange(N) * d
    ball_pos, ball_v, spring_len = np.arange(N)*d + A*np.sin(phase), np.zeros(N), np.ones(N)*d
    ori_second = ball_pos[1]
    t, dt = 0, 0.0003
    f = False
    while True:
        t += dt
        if ball_pos[1] < ori_second:
            f = True
        if f and ball_pos[1] > ori_second:
            break
        spring_len[:-1] = [ball_pos[i] - ball_pos[i+1] for i in range(N-1)]
        spring_len[-1] = ball_pos[-1] - ball_pos[0] - N*d
        ball_v[1:] += [(k*(spring_len[i]-spring_len[i+1])/m*dt) for i in range(N-1)]#6
        ball_v[0] += k*(spring_len[-1] - spring_len[0])/m*dt
        ball_pos += ball_v*dt
    func.plot(pos = (Wavevector, 2*pi/t))

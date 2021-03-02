from vpython import *
from diatomic import *
N = 20 # 20 molecules
L = ((24.4E-3/(6E23))*N)**(1/3.0)/50 # 2L is the length of the cubic container box, the number is made up
m = 14E-3/6E23 # average mass of O and C
k, T = 1.38E-23, 298.0 # some constants to set up the initial speed
initial_v = (3*k*T/m)**0.5 # some constant
scene = canvas(width = 400, height =400, align = 'left', background = vec(1, 1, 1))
container = box(length = 2*L, height = 2*L, width = 2*L, opacity=0.4, color = color.yellow )
energies = graph(width = 600, align = 'left', ymin=0)

c_avg_com_K = gcurve(color = color.green)
c_avg_v_P = gcurve(color = color.red)
c_avg_v_K = gcurve(color = color.purple)
c_avg_r_K = gcurve(color = color.blue)

def collide(a, b):
    if(mag(a.pos - b.pos) <= 2*size) and dot(a.pos-b.pos, a.v-b.v) < 0:
        a.v, b.v = collision(a, b)
    return a.v, b.v

def hit_wall(a):
    if abs(a.pos.x) >= L - size and a.pos.x * a.v.x > 0:
        a.v.x = -a.v.x
    if abs(a.pos.y) >= L - size and a.pos.y * a.v.y > 0:
        a.v.y = -a.v.y
    if abs(a.pos.z) >= L - size and a.pos.z * a.v.z > 0:
        a.v.z = -a.v.z
    return a.v

COs=[]

for i in range(N): # initialize the 20 CO molecules
    O_pos = vec(random()-0.5, random()-0.5, random()-0.5)*L # random() yields a random number between 0 and 1
    CO = CO_molecule(pos=O_pos, axis = vector(1.0*d, 0, 0)) # generate one CO molecule
    CO.C.v = vector(initial_v*random(), initial_v*random(), initial_v*random()) # set up the initial velocity of C randomly
    CO.O.v = vector(initial_v*random(), initial_v*random(), initial_v*random()) # set up the initial velocity of O randomly
    COs.append(CO) # store this molecule into list COs
times = 0 # number of loops that has been run

dt = 5E-16
t = 0
v_K, v_P, r_K, com_K = [0]*4
while True:
    t += dt
    rate(3000)
    for CO in COs:
        CO.time_lapse(dt)
    for i in range(N-1): # the first N-1 molecules
        for j in range(i+1,N): # from i+1 to the last molecules, to avoid double checking
            ## change this to check and handle the collisions between the atoms of different molecules
            COs[i].O.v, COs[j].O.v = collide(COs[i].O, COs[j].O)
            COs[i].C.v, COs[j].O.v = collide(COs[i].C, COs[j].O)
            COs[i].O.v, COs[j].C.v = collide(COs[i].O, COs[j].C)
            COs[i].C.v, COs[j].C.v = collide(COs[i].C, COs[j].C)

    for CO in COs:
        CO.C.v = hit_wall(CO.C)
        CO.O.v = hit_wall(CO.O)
        com_K += CO.com_K()
        v_P += CO.v_P()
        v_K += CO.v_K()
        r_K += CO.r_K()
        
    ## sum com_K, v_K, v_P, and r_K for all molecules, respectively, to get total_com_K, total_v_K, total_v_P, total_r_K at the
    ## current moment
    avg_com_K = com_K*dt/t
    avg_v_K = v_K*dt/t
    avg_v_P = v_P*dt/t
    avg_r_K = r_K*dt/t
    print(avg_com_K)
    ## calculate avg_com_K to be the time average of total_com_K since the beginning of the simulation, and do the same
    ## for others.
    ## plot avg_com_K, avg_v_K, avg_v_P, and avg_r_K
    c_avg_r_K.plot(pos = (t, avg_r_K))
    c_avg_v_K.plot(pos = (t, avg_v_K))
    c_avg_com_K.plot(pos = (t, avg_com_K))
    c_avg_v_P.plot(pos = (t, avg_v_P))
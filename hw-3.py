from vpython import*
mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun':1.99E30}
radius = {'earth': 6.371E6*10, 'moon': 1.317E6*10, 'sun':6.95E8*10} #10 times larger for better view
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145*pi/180.0
G = 6.673E-11


def g_force(A, B):
    return -G * A.m * B.m / mag2(A.pos-B.pos) * norm(A.pos-B.pos)


scene = canvas(width=800, height=800, background=vector(0, 0, 0))
#scene.forward = vector(0, -1, 0)
scene.lights = []
local_light(pos=vector(0, 0, 0))
earth = sphere(pos=vec(earth_orbit['r']+cos(theta)*moon_orbit['r']*mass['moon']/(mass['earth']+mass['moon'])
               , sin(theta)*moon_orbit['r']*mass['moon']/(mass['earth']+mass['moon']), 0)
               , radius=radius['earth'], m=mass['earth'], texture={'file':textures.earth})
earth.v = vector(0, 0, -earth_orbit['v'])+vector(0, 0, moon_orbit['v']*mass['moon']/(mass['earth']+mass['moon']))
moon = sphere(pos=vec(earth_orbit['r']-cos(theta)*moon_orbit['r']*mass['earth']/(mass['earth']+mass['moon'])
               , -sin(theta)*moon_orbit['r']*mass['earth']/(mass['earth']+mass['moon']), 0)
               , m=mass['moon'], radius=radius['moon'], color=color.gray(0.5))
moon.v = vec(0, 0, moon_orbit["v"]-earth_orbit["v"])
sun = sphere(pos=vec(0, 0, 0), m=mass['sun'], radius=radius['sun'], color=color.yellow, emissive=True)
sun.v = vec(0, 0, 0)
#stars = [earth, moon, sun, earth, sun, moon, earth]

dt = 60*16
t = 0
n = 0
quarter = 0
start = 1
s_t = 0
scene.camera.follow(earth)

while True:
    rate(6000)
    t = t + dt
    sun.a = (g_force(sun, moon) + g_force(sun, earth)) / sun.m
    sun.v += sun.a * dt
    sun.pos += sun.v * dt

    earth.a = (g_force(earth, moon)+g_force(earth, sun))/earth.m
    earth.v += earth.a * dt
    earth.pos += earth.v * dt

    moon.a = (g_force(moon, earth) + g_force(moon, sun)) / moon.m
    moon.v += moon.a * dt
    moon.pos += moon.v * dt

    if cross(moon.pos - earth.pos, moon.v - earth.v).x < 0 and start == 1:
        start += 1
        s_t = t

    if cross(moon.pos - earth.pos, moon.v - earth.v).x > 0 and start == 2:
        start += 1
        quarter1 = 4 * (t - s_t)
        print("The period of precession: " + str(quarter1 / (86400 * 365.25)) + "years")

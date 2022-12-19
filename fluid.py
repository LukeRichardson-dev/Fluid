import math
import numpy as np
from numpy import random


def create_basic_fluid(w=20, h=20):

    return create_vector_field(w, h), create_density_field(w, h)

def create_vector_field(w, h):

    return random.uniform(-2, 2, size=(w, h, 2))

def create_density_field(w, h):

    return random.rand(w, h)


def diffuse(df, k):
    
    w, h = df.shape

    new = df.copy()
    buffer = new.copy()

    for _ in range(3):

        for x, c in enumerate(df):
            for y, d in enumerate(c):

                u, d, l, r = new[x, (y + 1) % h], \
                    new[x, (y - 1)], \
                    new[(x - 1), y], \
                    new[(x + 1) % w, y]
                
                s = (u + d + l + r) / 4
                buffer[x, y] = (d + k * s) / (1 + k)
        new = buffer.copy()

    return new

def lerp(a, b, k):
    return a + k * (b - a)

def advectate(vf, df, dt):
    w, h = df.shape
    new = np.zeros(df.shape)
    for x, c in enumerate(vf):
        for y, v in enumerate(c):
            f = ((x - v[0]) * dt, (y - v[1]) * dt) 
            i = (math.floor(f[0]) % w, math.floor(f[1]) % h)
            j = (f[0] - i[0], f[1] - i[1])
            ri = (i[0] + 1) % w
            ui = (i[1] + 1) % h
            z1 = lerp(df[i[0], i[1]], df[ri, i[1]], j[0])
            z2 = lerp(df[i[0], ui], df[ri, ui], j[0])
            new[x, y] = lerp(z1, z2, j[1])

    return new

def curl(vf):
    w, h, _ = vf.shape
    deltas = np.zeros((w, h))

    for x, c in enumerate(vf):
        for y, _ in enumerate(c):

            dvx = vf[(x + 1) % h, y][0] - vf[x - 1, y][0]
            dvy = vf[x, (y + 1) % h][1] - vf[x, y - 1][1]
            dvxy = (dvx + dvy) / 2
            deltas[x, y] = dvxy

    pf = deltas.copy()
    for _ in range(5):
        buffer = pf.copy()
        for x, c in enumerate(deltas):
            for y, v in enumerate(c):

                u, d, l, r = buffer[x, (y + 1) % h], \
                    buffer[x, (y - 1)], \
                    buffer[(x - 1), y], \
                    buffer[(x + 1) % w, y]
                
                pf[x, y] = ((u + d + l + r) - v) / 4
        buffer = pf.copy()

    dpf = np.zeros(vf.shape)
    for x, c in enumerate(vf):
        for y, v in enumerate(c):
    
            u, d, l, r = buffer[x, (y + 1) % h], \
                    buffer[x, (y - 1)], \
                    buffer[(x - 1), y], \
                    buffer[(x + 1) % w, y]
            
            dpf[x, y, :] = [v[0] - (r - l) / 2, v[1] - (u - d) / 2]

    return pf

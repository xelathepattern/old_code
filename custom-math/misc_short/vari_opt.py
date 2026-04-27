import numpy as np

def integral(f, n=100, a=0, b=1):
    dx = (b-a)/n
    x = a
    acc = 0
    while x <= b:
        acc += (f(x+dx)-f(x))*dx
        x += dx

    return acc

def partial_at_point(f, coord, point, dx=.01):
    right_point = []
    left_point = []
    for i in range(len(point)):
        left_point.append(point[i])
        right_point.append(point[i])
        if i == coord:
            left_point[i] -= dx
            right_point[i] += dx
    return (f(right_point) - f(left_point)) / (2*dx)

def partial(f, coord, dx=.01):
    return lambda point: partial_at_point(f, coord, point, dx=dx)

def grad_at_point(f, coord, point, dx=.01):
    out = []
    for i in range(len(point)):
        out.append(partial_at_point(f,coord,point,dx=dx))
    return out

def minimize(f, guess_0, df=.01, step=.1, dx=.01):
    this_f = f(guess_0)
    this_x = guess_0
    while abs(this_f) < df:
        this_x += -1 * grad_at_point(f,coord,point,dx=dx) * step
        this_f = f(this_x)


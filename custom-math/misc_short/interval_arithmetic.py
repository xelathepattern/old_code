# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:19:24 2022

@author: Xela
"""


from __future__ import annotations #postpone evaluation of annotations to allow for things like using a class as a type within a function in the class.
from typing import Callable, Union

from tqdm import tqdm

import itertools

import numpy as np
import gmpy2 as gp
gp.get_context().precision=32

import matplotlib.pyplot as plt




def Lower(num, ctx=None) -> gp.mpfr:
    if ctx is None:
        ctx = gp.get_context()

    prev_round = ctx.round

    ctx.round = gp.RoundDown
    lb = gp.mpfr(num)

    ctx.round = prev_round #reset the rounding to what it was before

    return lb

def Upper(num, ctx=None) -> gp.mpfr:
    if ctx is None:
        ctx = gp.get_context()

    prev_round = ctx.round

    ctx.round = gp.RoundUp
    ub = gp.mpfr(num)

    ctx.round = prev_round #reset the rounding to what it was before

    return ub


class MultiInterval():
    def __init__(self: MultiInterval, intervals: list[Union[PureInterval, MultiInterval]]) -> None: #!!!allow construction from MultiInterval
        self.intervals = intervals
        self.lowest = min(intervals, key=lambda interval: interval.low)
        self.highest = max(intervals, key=lambda interval: interval.high)

    def __repr__(self: MultiInterval) -> str:
        intervals_str_list = (f"PureInterval({interval.low}, {interval.high}), " for interval in self.intervals)

        intervals_str = ''
        for interval_str in intervals_str_list:
            intervals_str += interval_str
        return f"MultiInterval([{intervals_str[:-2]}])" #[:-2] to truncate trailing ", "

    def __str__(self: MultiInterval) -> str:
        intervals_str_list = [f"[{interval.low}, {interval.high}] ∪ " for interval in self.intervals]

        intervals_str = ''
        for interval_str in intervals_str_list:
            intervals_str += interval_str
        return intervals_str[:-3] #leave off final " ∪ "

    @staticmethod
    def Binary_Multi_Extend(interval_func: Callable[[PureInterval, PureInterval], list[MultiInterval]]) -> Callable[MultiInterval, MultiInterval]:
        return lambda left, right: MultiInterval(list(map(lambda interval_pair: interval_func(*interval_pair), itertools.product(left.intervals, right.intervals))))

    def __mul__(self: MultiInterval, other: MultiInterval) -> MultiInterval:
        return MultiInterval.Binary_Multi_Extend(PureInterval.__mul__)(self, other)

class PureInterval(MultiInterval): #!!!implement extensions of piecewise monotonic functions
    def __init__(self: PureInterval, low: float, high: float, round_out=True) -> None:
        if round_out:
            self.low, self.high = Lower(low), Upper(high)
        else:
            self.low, self.high = low, high

    def __repr__(self: PureInterval) -> str:
        return f"PureInterval({self.low}, {self.high})"

    def __str__(self: PureInterval) -> str:
        return f"[{self.low}, {self.high}]"


    def __neg__(self: PureInterval) -> PureInterval:
        return PureInterval(-self.high, -self.low)

    def __add__(self: PureInterval, other: PureInterval) -> PureInterval:
        return PureInterval(self.low + other.low, self.high + other.high)

    def __sub__(self: PureInterval, other: PureInterval) -> PureInterval:
        return PureInterval(self.low - other.high, self.high - other.low)

    def __mul__(self: PureInterval, other: Union(PureInterval, float, int)) -> PureInterval:
        if type(other) == PureInterval:
            extremes = (self.low*other.low, self.low*other.high, self.high*other.low, self.high*other.high)
            return PureInterval(min(extremes), max(extremes))
        elif type(other) == float or type(other) == int:
            extremes = (self.low*other, self.low*other, self.high*other, self.high*other)
            return PureInterval(min(extremes), max(extremes))

    def __rmul__(self: PureInterval, other: Union(float, int)) -> PureInterval:
        extremes = (self.low*other, self.low*other, self.high*other, self.high*other)
        return PureInterval(min(extremes), max(extremes))


    def __truediv__(self: PureInterval, other: PureInterval) -> MultiInterval:
        return self * (1/other)

    def __rtruediv__(self: PureInterval, other: float) -> MultiInterval:
        low, high = self.low, self.high
        if low == 0:
            return PureInterval(1/high, gp.inf())
        elif high == 0:
            return PureInterval(-gp.inf(), 1/low)
        elif low < 0 < high:
            return MultiInterval([PureInterval(-gp.inf(), 1/low), PureInterval(1/high, gp.inf())])
        else:
            return PureInterval(1/high, 1/low)

def ODE_Solve(state_derivs, initial_state, initial_t, end_t, dt, store_states=True):
    current_t = initial_t
    current_state = initial_state
    history = []
    with tqdm(total=int(gp.ceil((end_t-initial_t)/dt)), disable=False) as pbar:
        while current_t < end_t:
            if store_states:
                history.append(current_state)

            current_state_derivs = state_derivs(current_state, current_t)
            new_state = [current_state[j] + current_state_derivs[j]*dt for j in range(len(current_state))]
            current_state = new_state
            #input(current_state) if len(history)%100==0 else print(end='')
            current_t += dt
            pbar.update(1)

    return history if store_states else current_state




t_init = 0
t_end = 1
dt = .001
init_state = [PureInterval(gp.const_pi() - 1, gp.const_pi() + 1),PureInterval(0, 0)]
#out1=ODE_Solve(lambda ys, t: [ys[1], -ys[0]], [2,0], t_init, t_end, dt)
#out2=ODE_Solve(lambda ys, t: [ys[1], -ys[0]], [PureInterval(1.999, 2.001),PureInterval(0,0)], t_init, t_end, dt)
out2=ODE_Solve(lambda ys, t: [ys[1], -9.81*PureInterval(gp.cos(ys[0].low), gp.cos(ys[0].high))], init_state, t_init, t_end, dt)

plt.fill_between(np.arange(t_init, t_init+dt*len(out2), dt), [float(this_state_intervals[0].low) for this_state_intervals in out2], [float(this_state_intervals[0].high) for this_state_intervals in out2], alpha=.5, color='teal')

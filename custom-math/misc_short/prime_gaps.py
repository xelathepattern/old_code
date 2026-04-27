from tqdm import tqdm

from sympy import nextprime

import matplotlib.pyplot as plt


def prime_freq(limit):
    freq = dict()
    n = 2
    pbar = tqdm(total = int(limit))
    while n < limit:
        nextn = nextprime(n)
        diff = nextn - n
        n = nextn;
        if diff in freq:
            freq[diff] += 1
        else:
            freq[diff] = 1
        pbar.update(int(diff))

    pbar.close()
    return freq


n = int(1.5e7)

ten_freq =  prime_freq(n)


xVals = list(ten_freq.keys())
yVals = list(ten_freq.values())

fig, ax = plt.subplots()

ax.plot(xVals, yVals, '.')
ax.set_title("%s Primes" % eval('n'))

ax.set_yscale("log", )#nonposy='clip')

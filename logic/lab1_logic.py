import math

DEFAULT_M = 2 ** 29 - 1
DEFAULT_A = 16 ** 3
DEFAULT_C = 6765
DEFAULT_X0 = 23
DEFAULT_COUNT = 10000

def lcg_generator(x0, a, c, m, count):
    x = x0
    results = []
    for _ in range(count):
        x = (a * x + c) % m
        results.append(x)
    return results

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def cesaro_test(sequence):
    n = len(sequence)
    if n < 2:
        return 0

    coprime_count = 0
    n_pairs = n // 2

    for i in range(n_pairs):
        num1 = sequence[2 * i]
        num2 = sequence[2 * i + 1]

        if gcd(num1, num2) == 1:
            coprime_count += 1

    if n_pairs == 0:
        return 0

    prob = coprime_count / n_pairs

    if prob > 0:
        try:
            pi_estimate = math.sqrt(6 / prob)
            return pi_estimate
        except ValueError:
            return 0
    return 0

def find_period_floyd(x0, a, c, m):
    slow = x0
    fast = x0

    while True:
        slow = (a * slow + c) % m
        fast = (a * fast + c) % m
        fast = (a * fast + c) % m

        if slow == fast:
            break

    period_length = 0
    while True:
        slow = (a * slow + c) % m
        period_length += 1
        if slow == fast:
            return period_length
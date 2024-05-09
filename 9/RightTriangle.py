import math
import timeit
from pathlib import Path


def rightTriangle1(N):
    def maxNrest(v1, v2, v3):
        '''
        Return v1 ~ v3 as a 3-tuple, such that the 1st element is the max 
            and the 2nd and 3rd elements are the rest
        '''        
        if v1 >= v2 and v1 >= v3: return v1, v2, v3
        elif v2 >= v1 and v2 >= v3: return v2, v1, v3
        else: return v3, v1, v2
    
    count = 0
    for A in range(1, (N+1)**2 - 1): # Choose A > O
        x1, y1 = A // (N+1), A % (N+1)                 
        for B in range(A + 1, (N+1)**2): # Choose B > A
            x2, y2 = B // (N+1), B % (N+1)
            lmax, l1, l2 = maxNrest(x1**2 + y1**2, x2**2 + y2**2, (x1-x2)**2 + (y1-y2)**2)
            if lmax == l1 + l2: count += 1

    return count


def gcd(a, b):
    while b != 0:
        if a > b: a, b = b, a % b
        else: b = b % a
    return a


def rightTriangle2(N):
    answer = 0
    answer += N ** 2 * 3

    for x in range (1, N+1):
        for y in range (1, x+1):
            c = x ** 2 / y + y #c는 y절편
            d = y ** 2 / x + x #d는 x절편

            a = min(math.floor(c), N) - y
            b = min(math.floor(d), N) - x

            if a == 0 and b == 0: continue

            gcdV = gcd(x, y)
            current = math.floor(a / (x / gcdV)) + math.floor(b / (y / gcdV))
            if x == y: answer += current
            else: answer += current * 2

    return answer

#//

def speedCompare2(N):
    g = N * N * 2
    for i in range(1, N*N):
        a = gcd(i, i+1)
        b = gcd(i+1, i+2)
        c = i*i + i*i / (i+1)
        d = i*i + i*i / (i+3)
        e = (min(math.floor(i), N) - i) / (d / a)
        f = (min(math.floor(i), N) - i) / (c / b)
        g += f + d


if __name__ == "__main__":
    # # Test for in-class problems
    # functions = [rightTriangle1]
    # for f in functions:
    #     for i in range(1, 6):
    #         print(i, f(i))
    #     print()
    #
    #     n, repeat = 10, 10
    #     tRightTriangle = timeit.timeit(lambda: f(n), number=repeat)/repeat
    #     print(f"{f.__name__}({n}) took {tRightTriangle} seconds on average")

    # Test for after-class problems
    print()
    print("Correctness test for rightTriangle2()")
    correct = True
    for N in range(1, 21):
        result1, result2 = rightTriangle1(N), rightTriangle2(N)
        if result1 == result2: print("P ", end='')
        else:
            print(f"Fail with N={N}: output {result2} != expected output {result1}")
            correct = False
            break
    
    print()
    print()
    print("Speed test for rightTriangle2()")    
    if not correct: print("fail (since the algorithm is not correct)")
    else:                
        N, repeat = 20, 5
        tSpeedCompare1 = timeit.timeit(lambda: rightTriangle1(N), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: rightTriangle2(N), number=repeat)/repeat    
        print(f"For input N = {N}")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and rightTriangle1 {tSpeedCompare1:.10f}")    
        if tSubmittedCode * 200 < tSpeedCompare1: print("pass")
        else: print("fail")
        print()

        N, repeat = 20, 5
        tSpeedCompare2 = timeit.timeit(lambda: speedCompare2(N), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: rightTriangle2(N), number=repeat)/repeat    
        print(f"For input N = {N}")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and speedCompare2 {tSpeedCompare2:.10f}")    
        if tSubmittedCode * 1.5 < tSpeedCompare2: print("pass")
        else: print("fail")
        print()
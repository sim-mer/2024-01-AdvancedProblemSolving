import math
import timeit


def findLongestAmicableChain(n):
    return []


def findSarrayDivSqrt(n):
    '''
    Find s[] array for a=0~n
    This function is used to evaluate the execution time of findLongestAmicableChain()
    '''
    s = [0 for _ in range(n+1)]
    for a in range(2,n+1):
        for i in range(1, int(math.sqrt(a))+1):
            if a % i == 0:
                s[a] += i
                tmp = int(a/i)
                if tmp != i and tmp != a: s[a] += tmp
    return s


if __name__ == "__main__":
    print("Correctness test for findLongestAmicableChain()")
    correct = True

    if sorted(findLongestAmicableChain(10)) == sorted([6]): print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findLongestAmicableChain(100)) == sorted([6]): print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findLongestAmicableChain(1000)) == sorted([220, 284]): print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findLongestAmicableChain(10000)) == sorted([220, 284]): print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    if sorted(findLongestAmicableChain(100000)) == sorted([12496, 14288, 15472, 14536, 14264]): print("P ", end='')
    else:
        print("F ", end='')
        correct = False
    
    if sorted(findLongestAmicableChain(1000000)) == sorted([14316, 19116, 31704, 47616, 83328, 177792, 295488, 629072, 589786, 294896, 358336, 418904, 366556, 274924, 275444, 243760, 376736, 381028, 285778, 152990, 122410, 97946, 48976, 45946, 22976, 22744, 19916, 17716]): print("P ", end='')
    else:
        print("F ", end='')
        correct = False
    
    print()
    print()
    print("Speed test for findLongestAmicableChain()")
    if not correct: print("fail (since the algorithm is not correct)")
    else:
        n, repeat = 10000, 10   
        tSubmittedCode = timeit.timeit(lambda: findLongestAmicableChain(n), number=repeat)/repeat
        tDivSqrt = timeit.timeit(lambda: findSarrayDivSqrt(n), number=repeat)/repeat
        print(f"Average running time of the submitted code ({tSubmittedCode:.10f}) and of the code based on division ({tDivSqrt:.10f}) for n = {n}")
        if tSubmittedCode*2 < tDivSqrt: print("pass")
        else: print("fail")      
    print()
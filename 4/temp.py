import math
def FindNstoreCycle(elements, f):
    def recur(a):
        if result[a] != None: return -1
        if a >= len(f): return -1
        if a in dictionary: return a
        else:
            dictionary[a] = len(dictionary)
            if f[a] >= len(result):
                result[a] = -1
                return -1
            firstElementInCycle = recur(f[a])

            if firstElementInCycle == -1:
                result[a] = -1
                return -1
            else:
                result[a] = f[a]
                if a == firstElementInCycle:
                    if a != 0:
                        cycleElements.append(a)
                    return -1
                else:
                    if firstElementInCycle not in cycleElements:
                        cycleElements.append(firstElementInCycle)
                    return firstElementInCycle

    result = [None for _ in range(len(elements))]
    dictionary = {}
    cycleElements = []

    for e in elements:
        dictionary.clear()
        recur(e)

    return cycleElements



def findSarrayMultSqrt(n):
    s = [0 for _ in range(n + 1)]
    for a in range(2, n + 1): s[a] = 1
    for n1 in range(2, int(math.sqrt(n)) + 1):
        for n2 in range(n1, int(n / n1) + 1):
            s[n1 * n2] += n1
            if n2 != n1: s[n1 * n2] += n2
    return s


def findLongestAmicableChain(n):
    def find_chain(m):
        chain = [m]
        next = s[m]
        while next != m:
            chain.append(next)
            next = s[next]
        return chain

    s = findSarrayMultSqrt(n)
    elements = [i for i in range(0, n + 1)]
    cycleElements = FindNstoreCycle(elements, s)

    answer = []
    max = 0

    for i in cycleElements:
        chain = find_chain(i)
        if len(chain) > max:
            max = len(chain)
            answer = chain

    return answer


print(FindNstoreCycle([1, 2, 3, 4, 5], [3, 4, 1, 2, 0]))
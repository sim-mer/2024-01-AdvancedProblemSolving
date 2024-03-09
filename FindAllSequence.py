#정수 입력 n, 1이상의 정수로 이루어졌으며 합이 n이하인 모든 수열
def findAllSequence(n):
    def recur(min, currentSum, depth):
        while currentSum + min <= n:
            sequence[depth] = min

            answer.append(sequence[0:depth + 1])

            recur(min, currentSum + min, depth + 1)

            min += 1

    sequence = [0 for _ in range(n)]
    answer = []

    recur(1, 0, 0)
    return answer

if __name__ == "__main__":
    if findAllSequence(1) == [[1]]: print("pass")
    else: print("fail")

    if findAllSequence(2) == [[1], [1, 1], [2]]: print("pass")
    else: print("fail")

    if findAllSequence(3) == [[1], [1, 1], [1, 1, 1], [1, 2], [2], [3]]: print("pass")
    else: print("fail")

    if findAllSequence(4) == [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 2], [1, 2], [1, 3], [2], [2, 2], [3], [4]]: 
        print("pass")
    else: print("fail")

    if findAllSequence(5) == [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 2], [1, 1, 3], [1, 2], [1, 2, 2], [1, 3], [1, 4], [2], [2, 2], [2, 3], [3], [4], [5]]: 
        print("pass")
    else: print("fail")

    if findAllSequence(6) == [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 2], [1, 1, 1, 2], [1, 1, 1, 3], [1, 1, 2], [1, 1, 2, 2], [1, 1, 3], [1, 1, 4], [1, 2], [1, 2, 2], [1, 2, 3], [1, 3], [1, 4], [1, 5], [2], [2, 2], [2, 2, 2], [2, 3], [2, 4], [3], [3, 3], [4], [5], [6]]: 
        print("pass")
    else: print("fail")

    if findAllSequence(7) == [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 2], [1, 1, 1, 1, 2], [1, 1, 1, 1, 3], [1, 1, 1, 2], [1, 1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 1, 4], [1, 1, 2], [1, 1, 2, 2], [1, 1, 2, 3], [1, 1, 3], [1, 1, 4], [1, 1, 5], [1, 2], [1, 2, 2], [1, 2, 2, 2], [1, 2, 3], [1, 2, 4], [1, 3], [1, 3, 3], [1, 4], [1, 5], [1, 6], [2], [2, 2], [2, 2, 2], [2, 2, 3], [2, 3], [2, 4], [2, 5], [3], [3, 3], [3, 4], [4], [5], [6], [7]]: 
        print("pass")
    else: print("fail")
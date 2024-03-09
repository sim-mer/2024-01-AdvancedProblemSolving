def findAllSequence2(maxSum, min):
    assert maxSum > 0, f"maxSum={maxSum} must be greater than 0"

    assert min > 0, f"min={min} must be greater than 0"

    sequence = [0 for _ in range(maxSum)]

    sumStack = [0 for _ in range(maxSum + 1)]  # currentSum in the stack

    minStack = [0 for _ in range(maxSum + 1)]  # min in the stack

    minStack[0] = min

    depth = 0

    while True:

        while sumStack[depth] + minStack[depth] > maxSum:

            depth -= 1

            if depth < 0: return

        sequence[depth] = minStack[depth]

        print(sequence[0:depth + 1])

        sumStack[depth + 1] = sumStack[depth] + minStack[depth]

        minStack[depth + 1] = minStack[depth]

        minStack[depth] += 1

        depth += 1


if __name__ == "__main__":
    findAllSequence2(6, 2)
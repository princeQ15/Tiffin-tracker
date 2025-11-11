"""
Day 1 exercises — 10 short practice problems (2 hours plan)

Instructions:
- Read each function docstring and run this script: it will run simple asserts to show correct outputs.
- To practice, try implementing the functions yourself: comment out the provided implementations and re-run.
- Keep this file under version control and commit after you finish each exercise.

Author: learning plan
"""
from collections import Counter
from typing import List

# 1) Swap two variables — return swapped values
def swap(a, b):
    """Return (b, a)"""
    return b, a

# 2) Check palindrome (ignore case and non-alphanumerics)
def is_palindrome(s: str) -> bool:
    filtered = ''.join(ch.lower() for ch in s if ch.isalnum())
    return filtered == filtered[::-1]

# 3) Factorial (iterative)
def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

# 4) Nth Fibonacci (iterative, 0-indexed)
def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

# 5) Sum of a list
def sum_list(nums: List[int]) -> int:
    return sum(nums)

# 6) Most frequent element in a list (return one of the most frequent)
def most_frequent(nums: List[int]):
    if not nums:
        return None
    counts = Counter(nums)
    return counts.most_common(1)[0][0]

# 7) Reverse words in a sentence (preserve word order reversed characters)
def reverse_words(sentence: str) -> str:
    return ' '.join(word[::-1] for word in sentence.split())

# 8) Prime check (simple)
def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

# 9) Remove duplicates while preserving order
def remove_duplicates(seq: List[int]) -> List[int]:
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

# 10) Count vowels in a string
def count_vowels(s: str) -> int:
    return sum(1 for ch in s.lower() if ch in 'aeiou')


# --- Quick self-check harness ---
if __name__ == '__main__':
    print('Running Day 1 quick checks...')

    # 1
    assert swap(1, 2) == (2, 1)

    # 2
    assert is_palindrome('A man, a plan, a canal: Panama') is True
    assert is_palindrome('hello') is False

    # 3
    assert factorial(0) == 1
    assert factorial(5) == 120

    # 4
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(7) == 13

    # 5
    assert sum_list([1, 2, 3, 4]) == 10

    # 6
    assert most_frequent([1,2,2,3,3,3,2,2]) in (2,)

    # 7
    assert reverse_words('hello world') == 'olleh dlrow'

    # 8
    assert is_prime(2) is True
    assert is_prime(15) is False

    # 9
    assert remove_duplicates([1,2,2,3,1]) == [1,2,3]

    # 10
    assert count_vowels('Education') == 5

    print('All checks passed. To practice, comment out implementations and re-run.')

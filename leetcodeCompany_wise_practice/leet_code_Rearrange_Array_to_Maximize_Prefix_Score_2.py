from re import X


def maxScore(nums):
    nums.sort(reverse=True)
    prefix_sum = 0
    count = 0
    for num in nums:
        prefix_sum += num
        if prefix_sum > 0:
            count += 1
        else:
            break
    return count

# Test cases
if __name__ == "__main__":
    # Test case 1
    nums1 = [4, -1, 0, 3]
    print(f"Input: {nums1}")
    print(f"Output: {maxScore(nums1)}")  # Expected: 2
    
    # Test case 2
    nums2 = [-2, -3, 0, 1]
    print(f"\nInput: {nums2}")
    print(f"Output: {maxScore(nums2)}")  # Expected: 1
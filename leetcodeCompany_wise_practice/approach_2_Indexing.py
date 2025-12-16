from typing import List

class Solution:
    def maxScore(self, nums: List[int]) -> int:
        # Sort the array in descending order to maximize the prefix sum
        nums.sort(reverse=True)
        
        prefix_sum = 0
        score = 0
        
        for num in nums:
            prefix_sum += num
            # If prefix sum is positive, it contributes to the score
            if prefix_sum > 0:
                score += 1
            else:
                # Since the array is sorted in descending order,
                # once we hit a non-positive prefix sum, we can break early
                break
                
        return score

# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Test case 1
    nums1 = [2, -1, 0, 1, -3, 3, -3]
    print(f"Test case 1: {nums1}")
    print(f"Expected output: 6")
    print(f"Actual output: {sol.maxScore(nums1)}\n")
    
    # Test case 2: All positive numbers
    nums2 = [1, 2, 3, 4, 5]
    print(f"Test case 2: {nums2}")
    print(f"Expected output: 5")
    print(f"Actual output: {sol.maxScore(nums2)}\n")
    
    # Test case 3: All negative numbers
    nums3 = [-1, -2, -3]
    print(f"Test case 3: {nums3}")
    print(f"Expected output: 0")
    print(f"Actual output: {sol.maxScore(nums3)}\n")
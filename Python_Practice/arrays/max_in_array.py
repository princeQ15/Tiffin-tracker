def find_max(arr):
    """
    Find the maximum element in a list of integers.
    
    Args:
        arr (list): List of integers
        
    Returns:
        int: The maximum element in the list
        
    Raises:
        ValueError: If the input list is empty
    """
    if not arr:
        raise ValueError("Input list cannot be empty")
        
    max_num = arr[0]
    for num in arr[1:]:
        if num > max_num:
            max_num = num
    return max_num

def linear_search(arr, target):
    """
    Search for a target value in a list using linear search.
    
    Args:
        arr (list): List to search in
        target: Value to find
        
    Returns:
        int: Index of the target if found, -1 otherwise
    """
    for i, num in enumerate(arr):
        if num == target:
            return i
    return -1

if __name__ == "__main__":
    # Test cases for find_max
    test_cases = [
        [1, 2, 3, 4, 5],  # Sorted ascending
        [5, 4, 3, 2, 1],  # Sorted descending
        [1, 3, 2, 5, 4],  # Unsorted
        [42],              # Single element
        [-5, -1, -3, -2], # Negative numbers
    ]
    
    for test in test_cases:
        print(f"Array: {test}")
        print(f"Max element: {find_max(test)}")
        print("-" * 30)
    
    # Test case for empty list (should raise error)
    try:
        find_max([])
    except ValueError as e:
        print(f"Test empty list: {e}")
    
    # Test linear_search
    arr = [10, 20, 30, 40, 50]
    targets = [30, 100, 10, 40]
    for target in targets:
        idx = linear_search(arr, target)
        if idx != -1:
            print(f"{target} found at index {idx}")
        else:
            print(f"{target} not found in the array")

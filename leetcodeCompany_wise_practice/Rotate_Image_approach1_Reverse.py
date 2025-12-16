from typing import List

def rotate(matrix: List[List[int]]) -> None:
    """
    Rotate the matrix 90 degrees clockwise in-place.
    """
    # Reverse the matrix vertically
    matrix.reverse()
    
    # Transpose the matrix
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            # Swap elements across the diagonal
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

# Example usage
if __name__ == "__main__":
    # Test case
    matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    
    print("Original matrix:")
    for row in matrix:
        print(row)
    
    rotate(matrix)
    
    print("\nAfter rotation:")
    for row in matrix:
        print(row)
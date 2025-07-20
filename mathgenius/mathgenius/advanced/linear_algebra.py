"""Linear algebra operations module for advanced mathematical computations."""
import numpy as np
from scipy.linalg import solve, det, inv, eig, svd, qr, lu, lstsq
from scipy.sparse import csr_matrix, linalg as sparse_linalg
from mathgenius.core.validation import validate_numbers
from mathgenius.core.errors import ValidationError, CalculationError


def matrix_add(matrix_a, matrix_b):
    """
    Add two matrices element-wise.
    
    Args:
        matrix_a (list|np.ndarray): First matrix
        matrix_b (list|np.ndarray): Second matrix
        
    Returns:
        np.ndarray: Sum of the matrices
        
    Raises:
        ValidationError: If matrices are invalid or incompatible
        CalculationError: If addition fails
    """
    try:
        # Convert to numpy arrays
        a = np.array(matrix_a)
        b = np.array(matrix_b)
        
        # Validate dimensions
        if a.shape != b.shape:
            raise ValidationError(f"Matrix dimensions must match: {a.shape} vs {b.shape}")
            
        # Perform addition
        result = a + b
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to add matrices: {str(e)}")


def matrix_multiply(matrix_a, matrix_b):
    """
    Multiply two matrices using matrix multiplication.
    
    Args:
        matrix_a (list|np.ndarray): First matrix
        matrix_b (list|np.ndarray): Second matrix
        
    Returns:
        np.ndarray: Product of the matrices
        
    Raises:
        ValidationError: If matrices are invalid or incompatible
        CalculationError: If multiplication fails
    """
    try:
        # Convert to numpy arrays
        a = np.array(matrix_a)
        b = np.array(matrix_b)
        
        # Validate dimensions for matrix multiplication
        if len(a.shape) != 2 or len(b.shape) != 2:
            raise ValidationError("Both inputs must be 2D matrices")
            
        if a.shape[1] != b.shape[0]:
            raise ValidationError(f"Matrix dimensions incompatible for multiplication: {a.shape} and {b.shape}")
            
        # Perform multiplication
        result = np.dot(a, b)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to multiply matrices: {str(e)}")


def matrix_transpose(matrix):
    """
    Compute transpose of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        np.ndarray: Transpose of the matrix
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If transpose fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Perform transpose
        result = a.T
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to transpose matrix: {str(e)}")


def matrix_inverse(matrix):
    """
    Compute inverse of a square matrix.
    
    Args:
        matrix (list|np.ndarray): Input square matrix
        
    Returns:
        np.ndarray: Inverse of the matrix
        
    Raises:
        ValidationError: If matrix is invalid or not square
        CalculationError: If matrix is singular or inversion fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        if a.shape[0] != a.shape[1]:
            raise ValidationError("Matrix must be square for inversion")
            
        # Check if matrix is singular
        if np.abs(np.linalg.det(a)) < 1e-14:
            raise CalculationError("Matrix is singular (determinant is zero)")
            
        # Perform inversion
        result = inv(a)
        return result
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute matrix inverse: {str(e)}")


def matrix_determinant(matrix):
    """
    Compute determinant of a square matrix.
    
    Args:
        matrix (list|np.ndarray): Input square matrix
        
    Returns:
        float: Determinant of the matrix
        
    Raises:
        ValidationError: If matrix is invalid or not square
        CalculationError: If determinant computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        if a.shape[0] != a.shape[1]:
            raise ValidationError("Matrix must be square for determinant")
            
        # Compute determinant
        result = det(a)
        return float(result)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute determinant: {str(e)}")


def eigenvalues_eigenvectors(matrix):
    """
    Compute eigenvalues and eigenvectors of a square matrix.
    
    Args:
        matrix (list|np.ndarray): Input square matrix
        
    Returns:
        tuple: (eigenvalues, eigenvectors) as numpy arrays
        
    Raises:
        ValidationError: If matrix is invalid or not square
        CalculationError: If eigenvalue computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        if a.shape[0] != a.shape[1]:
            raise ValidationError("Matrix must be square for eigenvalue computation")
            
        # Compute eigenvalues and eigenvectors
        eigenvals, eigenvecs = eig(a)
        
        return eigenvals, eigenvecs
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute eigenvalues/eigenvectors: {str(e)}")


def solve_linear_system(matrix_a, vector_b):
    """
    Solve linear system Ax = b.
    
    Args:
        matrix_a (list|np.ndarray): Coefficient matrix A
        vector_b (list|np.ndarray): Right-hand side vector b
        
    Returns:
        np.ndarray: Solution vector x
        
    Raises:
        ValidationError: If inputs are invalid
        CalculationError: If system cannot be solved
    """
    try:
        # Convert to numpy arrays
        a = np.array(matrix_a)
        b = np.array(vector_b)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Matrix A must be 2D")
            
        if len(b.shape) != 1:
            raise ValidationError("Vector b must be 1D")
            
        if a.shape[0] != b.shape[0]:
            raise ValidationError(f"Matrix and vector dimensions incompatible: {a.shape[0]} vs {b.shape[0]}")
            
        # Solve linear system
        if a.shape[0] == a.shape[1]:
            # Square system
            x = solve(a, b)
        else:
            # Overdetermined/underdetermined system - use least squares
            x, residuals, rank, s = lstsq(a, b)
            
        return x
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to solve linear system: {str(e)}")


def matrix_rank(matrix):
    """
    Compute rank of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        int: Rank of the matrix
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If rank computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Compute rank
        rank = np.linalg.matrix_rank(a)
        return int(rank)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute matrix rank: {str(e)}")


def matrix_nullspace(matrix):
    """
    Compute null space of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        np.ndarray: Null space basis vectors
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If null space computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Compute null space using SVD
        u, s, vh = svd(a)
        
        # Find null space vectors (where singular values are effectively zero)
        tolerance = 1e-10
        null_mask = s <= tolerance
        
        # Extract null space from right singular vectors
        # The null space consists of the right singular vectors corresponding to zero singular values
        null_space = vh[len(s) - np.sum(null_mask):, :].T
        
        return null_space
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute null space: {str(e)}")


def lu_decomposition(matrix):
    """
    Compute LU decomposition of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        tuple: (P, L, U) where PA = LU
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If LU decomposition fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Compute LU decomposition
        p, l, u = lu(a)
        
        return p, l, u
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute LU decomposition: {str(e)}")


def qr_decomposition(matrix):
    """
    Compute QR decomposition of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        tuple: (Q, R) where A = QR
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If QR decomposition fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Compute QR decomposition
        q, r = qr(a)
        
        return q, r
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute QR decomposition: {str(e)}")


def svd_decomposition(matrix):
    """
    Compute Singular Value Decomposition (SVD) of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        tuple: (U, S, Vt) where A = U * S * Vt
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If SVD computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Compute SVD
        u, s, vt = svd(a)
        
        return u, s, vt
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute SVD: {str(e)}")


def vector_norm(vector, ord=2):
    """
    Compute norm of a vector.
    
    Args:
        vector (list|np.ndarray): Input vector
        ord (int|float|str): Order of the norm
        
    Returns:
        float: Norm of the vector
        
    Raises:
        ValidationError: If vector is invalid
        CalculationError: If norm computation fails
    """
    try:
        # Convert to numpy array
        v = np.array(vector)
        
        # Validate dimensions
        if len(v.shape) != 1:
            raise ValidationError("Input must be a 1D vector")
            
        # Compute norm
        norm = np.linalg.norm(v, ord=ord)
        return float(norm)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute vector norm: {str(e)}")


def matrix_condition_number(matrix):
    """
    Compute condition number of a matrix.
    
    Args:
        matrix (list|np.ndarray): Input matrix
        
    Returns:
        float: Condition number
        
    Raises:
        ValidationError: If matrix is invalid
        CalculationError: If condition number computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        # Compute condition number
        cond = np.linalg.cond(a)
        return float(cond)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute condition number: {str(e)}")


def matrix_trace(matrix):
    """
    Compute trace (sum of diagonal elements) of a square matrix.
    
    Args:
        matrix (list|np.ndarray): Input square matrix
        
    Returns:
        float: Trace of the matrix
        
    Raises:
        ValidationError: If matrix is invalid or not square
        CalculationError: If trace computation fails
    """
    try:
        # Convert to numpy array
        a = np.array(matrix)
        
        # Validate dimensions
        if len(a.shape) != 2:
            raise ValidationError("Input must be a 2D matrix")
            
        if a.shape[0] != a.shape[1]:
            raise ValidationError("Matrix must be square for trace computation")
            
        # Compute trace
        trace = np.trace(a)
        return float(trace)
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute trace: {str(e)}")


def vector_projection(vector_a, vector_b):
    """
    Compute projection of vector a onto vector b.
    
    Args:
        vector_a (list|np.ndarray): Vector to project
        vector_b (list|np.ndarray): Vector to project onto
        
    Returns:
        np.ndarray: Projection of a onto b
        
    Raises:
        ValidationError: If vectors are invalid
        CalculationError: If projection computation fails
    """
    try:
        # Convert to numpy arrays
        a = np.array(vector_a)
        b = np.array(vector_b)
        
        # Validate dimensions
        if len(a.shape) != 1 or len(b.shape) != 1:
            raise ValidationError("Both inputs must be 1D vectors")
            
        if a.shape[0] != b.shape[0]:
            raise ValidationError(f"Vector dimensions must match: {a.shape[0]} vs {b.shape[0]}")
            
        # Check if b is zero vector
        if np.allclose(b, 0):
            raise CalculationError("Cannot project onto zero vector")
            
        # Compute projection
        projection = (np.dot(a, b) / np.dot(b, b)) * b
        return projection
        
    except ValidationError:
        raise
    except Exception as e:
        raise CalculationError(f"Failed to compute vector projection: {str(e)}")

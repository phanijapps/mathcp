"""Test suite for advanced linear algebra operations."""
import pytest
import numpy as np
from mathgenius.advanced.linear_algebra import (
    matrix_add, matrix_multiply, matrix_transpose, matrix_inverse,
    matrix_determinant, eigenvalues_eigenvectors, solve_linear_system,
    matrix_rank, matrix_nullspace, lu_decomposition, qr_decomposition,
    svd_decomposition, vector_norm, matrix_condition_number, matrix_trace,
    vector_projection
)
from mathgenius.core.errors import ValidationError, CalculationError


class TestMatrixOperations:
    """Test basic matrix operations."""
    
    def test_matrix_add_basic(self):
        """Test basic matrix addition."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        result = matrix_add(a, b)
        expected = np.array([[6, 8], [10, 12]])
        np.testing.assert_array_equal(result, expected)
    
    def test_matrix_add_incompatible_dimensions(self):
        """Test matrix addition with incompatible dimensions."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6, 7], [8, 9, 10]]
        with pytest.raises(ValidationError):
            matrix_add(a, b)
    
    def test_matrix_multiply_basic(self):
        """Test basic matrix multiplication."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        result = matrix_multiply(a, b)
        expected = np.array([[19, 22], [43, 50]])
        np.testing.assert_array_equal(result, expected)
    
    def test_matrix_multiply_incompatible_dimensions(self):
        """Test matrix multiplication with incompatible dimensions."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6, 7]]
        with pytest.raises(ValidationError):
            matrix_multiply(a, b)
    
    def test_matrix_transpose_basic(self):
        """Test matrix transpose."""
        a = [[1, 2, 3], [4, 5, 6]]
        result = matrix_transpose(a)
        expected = np.array([[1, 4], [2, 5], [3, 6]])
        np.testing.assert_array_equal(result, expected)
    
    def test_matrix_transpose_invalid_input(self):
        """Test matrix transpose with invalid input."""
        with pytest.raises(ValidationError):
            matrix_transpose([1, 2, 3])  # 1D array


class TestMatrixProperties:
    """Test matrix property calculations."""
    
    def test_matrix_determinant_basic(self):
        """Test determinant calculation."""
        a = [[1, 2], [3, 4]]
        result = matrix_determinant(a)
        expected = -2  # 1*4 - 2*3 = -2
        assert abs(result - expected) < 1e-10
    
    def test_matrix_determinant_3x3(self):
        """Test determinant of 3x3 matrix."""
        a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = matrix_determinant(a)
        expected = 0  # This matrix is singular
        assert abs(result - expected) < 1e-10
    
    def test_matrix_determinant_non_square(self):
        """Test determinant with non-square matrix."""
        a = [[1, 2, 3], [4, 5, 6]]
        with pytest.raises(ValidationError):
            matrix_determinant(a)
    
    def test_matrix_trace_basic(self):
        """Test trace calculation."""
        a = [[1, 2], [3, 4]]
        result = matrix_trace(a)
        expected = 5  # 1 + 4 = 5
        assert abs(result - expected) < 1e-10
    
    def test_matrix_trace_non_square(self):
        """Test trace with non-square matrix."""
        a = [[1, 2, 3], [4, 5, 6]]
        with pytest.raises(ValidationError):
            matrix_trace(a)
    
    def test_matrix_rank_basic(self):
        """Test rank calculation."""
        a = [[1, 2], [3, 4]]
        result = matrix_rank(a)
        expected = 2
        assert result == expected
    
    def test_matrix_rank_singular(self):
        """Test rank of singular matrix."""
        a = [[1, 2], [2, 4]]  # Second row is 2 * first row
        result = matrix_rank(a)
        expected = 1
        assert result == expected


class TestMatrixInverse:
    """Test matrix inversion."""
    
    def test_matrix_inverse_basic(self):
        """Test matrix inversion."""
        a = [[1, 2], [3, 4]]
        result = matrix_inverse(a)
        # Check that A * A^(-1) = I
        identity = matrix_multiply(a, result)
        expected_identity = np.eye(2)
        np.testing.assert_array_almost_equal(identity, expected_identity)
    
    def test_matrix_inverse_singular(self):
        """Test inversion of singular matrix."""
        a = [[1, 2], [2, 4]]  # Singular matrix
        with pytest.raises(CalculationError):
            matrix_inverse(a)
    
    def test_matrix_inverse_non_square(self):
        """Test inversion of non-square matrix."""
        a = [[1, 2, 3], [4, 5, 6]]
        with pytest.raises(ValidationError):
            matrix_inverse(a)


class TestEigenvalues:
    """Test eigenvalue and eigenvector calculations."""
    
    def test_eigenvalues_eigenvectors_basic(self):
        """Test eigenvalue and eigenvector calculation."""
        a = [[1, 2], [2, 1]]
        eigenvals, eigenvecs = eigenvalues_eigenvectors(a)
        
        # Check that we have the correct number of eigenvalues and eigenvectors
        assert len(eigenvals) == 2
        assert eigenvecs.shape == (2, 2)
        
        # Check that Av = λv for each eigenvalue and eigenvector
        for i in range(len(eigenvals)):
            v = eigenvecs[:, i]
            lhs = matrix_multiply(a, v.reshape(-1, 1)).flatten()
            rhs = eigenvals[i] * v
            np.testing.assert_array_almost_equal(lhs, rhs)
    
    def test_eigenvalues_eigenvectors_non_square(self):
        """Test eigenvalues with non-square matrix."""
        a = [[1, 2, 3], [4, 5, 6]]
        with pytest.raises(ValidationError):
            eigenvalues_eigenvectors(a)


class TestLinearSystems:
    """Test linear system solving."""
    
    def test_solve_linear_system_basic(self):
        """Test solving basic linear system."""
        # System: x + 2y = 5, 3x + 4y = 11
        a = [[1, 2], [3, 4]]
        b = [5, 11]
        result = solve_linear_system(a, b)
        
        # Check solution: x = 1, y = 2
        expected = np.array([1, 2])
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_solve_linear_system_overdetermined(self):
        """Test solving overdetermined system."""
        # More equations than unknowns
        a = [[1, 2], [3, 4], [5, 6]]
        b = [5, 11, 17]
        result = solve_linear_system(a, b)
        
        # Should find least squares solution
        assert len(result) == 2
    
    def test_solve_linear_system_incompatible_dimensions(self):
        """Test solving system with incompatible dimensions."""
        a = [[1, 2], [3, 4]]
        b = [5, 11, 17]  # Wrong size
        with pytest.raises(ValidationError):
            solve_linear_system(a, b)


class TestMatrixDecompositions:
    """Test matrix decomposition methods."""
    
    def test_lu_decomposition_basic(self):
        """Test LU decomposition."""
        a = [[1, 2], [3, 4]]
        p, l, u = lu_decomposition(a)
        
        # Check that P * A = L * U
        pa = matrix_multiply(p, a)
        lu = matrix_multiply(l, u)
        np.testing.assert_array_almost_equal(pa, lu)
    
    def test_qr_decomposition_basic(self):
        """Test QR decomposition."""
        a = [[1, 2], [3, 4]]
        q, r = qr_decomposition(a)
        
        # Check that A = Q * R
        qr = matrix_multiply(q, r)
        np.testing.assert_array_almost_equal(qr, a)
        
        # Check that Q is orthogonal (Q^T * Q = I)
        qt = matrix_transpose(q)
        qtq = matrix_multiply(qt, q)
        np.testing.assert_array_almost_equal(qtq, np.eye(2))
    
    def test_svd_decomposition_basic(self):
        """Test SVD decomposition."""
        a = [[1, 2], [3, 4]]
        u, s, vt = svd_decomposition(a)
        
        # Reconstruct matrix from SVD
        s_matrix = np.diag(s)
        reconstructed = matrix_multiply(matrix_multiply(u, s_matrix), vt)
        np.testing.assert_array_almost_equal(reconstructed, a)


class TestVectorOperations:
    """Test vector operations."""
    
    def test_vector_norm_basic(self):
        """Test vector norm calculation."""
        v = [3, 4]
        result = vector_norm(v)
        expected = 5  # sqrt(3^2 + 4^2) = 5
        assert abs(result - expected) < 1e-10
    
    def test_vector_norm_different_orders(self):
        """Test vector norm with different orders."""
        v = [1, 2, 3]
        
        # L1 norm
        result = vector_norm(v, ord=1)
        expected = 6  # |1| + |2| + |3| = 6
        assert abs(result - expected) < 1e-10
        
        # L2 norm
        result = vector_norm(v, ord=2)
        expected = np.sqrt(14)  # sqrt(1^2 + 2^2 + 3^2) = sqrt(14)
        assert abs(result - expected) < 1e-10
        
        # L∞ norm
        result = vector_norm(v, ord=np.inf)
        expected = 3  # max(|1|, |2|, |3|) = 3
        assert abs(result - expected) < 1e-10
    
    def test_vector_norm_invalid_input(self):
        """Test vector norm with invalid input."""
        with pytest.raises(ValidationError):
            vector_norm([[1, 2], [3, 4]])  # 2D array
    
    def test_vector_projection_basic(self):
        """Test vector projection."""
        a = [1, 2]
        b = [3, 0]
        result = vector_projection(a, b)
        expected = np.array([1, 0])  # Projection of [1,2] onto [3,0] = [1,0]
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_vector_projection_zero_vector(self):
        """Test projection onto zero vector."""
        a = [1, 2]
        b = [0, 0]
        with pytest.raises(CalculationError):
            vector_projection(a, b)
    
    def test_vector_projection_incompatible_dimensions(self):
        """Test projection with incompatible dimensions."""
        a = [1, 2]
        b = [3, 0, 1]
        with pytest.raises(ValidationError):
            vector_projection(a, b)


class TestMatrixConditionNumber:
    """Test matrix condition number."""
    
    def test_matrix_condition_number_basic(self):
        """Test condition number calculation."""
        a = [[1, 2], [3, 4]]
        result = matrix_condition_number(a)
        
        # Condition number should be positive
        assert result > 0
        
        # For this matrix, condition number should be reasonable
        assert result < 100
    
    def test_matrix_condition_number_identity(self):
        """Test condition number of identity matrix."""
        a = [[1, 0], [0, 1]]
        result = matrix_condition_number(a)
        expected = 1  # Identity matrix has condition number 1
        assert abs(result - expected) < 1e-10


class TestMatrixNullspace:
    """Test null space calculation."""
    
    def test_matrix_nullspace_basic(self):
        """Test null space calculation."""
        # Matrix with non-trivial null space
        a = [[1, 2], [2, 4]]  # Second row is 2 * first row
        result = matrix_nullspace(a)
        
        # For a 2x2 matrix with rank 1, null space should have dimension 1
        assert result.shape[1] >= 1
    
    def test_matrix_nullspace_full_rank(self):
        """Test null space of full rank matrix."""
        a = [[1, 2], [3, 4]]  # Full rank matrix
        result = matrix_nullspace(a)
        
        # Full rank matrix should have trivial null space
        assert result.shape[1] == 0


if __name__ == "__main__":
    pytest.main([__file__])

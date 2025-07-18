"""Unified API dispatcher for mathgenius."""
from mathgenius.arithmetic.operations import add, subtract, multiply, divide, power, modulo
from mathgenius.algebra.equations import solve_linear, solve_quadratic
from mathgenius.algebra.polynomials import expand_expr, factor_expr, simplify_expr
from mathgenius.geometry.shapes import (
    triangle_area, triangle_perimeter, triangle_area_heron,
    circle_area, circle_circumference,
    rectangle_area, rectangle_perimeter,
    polygon_area, polygon_perimeter,
    sphere_volume, sphere_surface_area,
    cylinder_volume, cylinder_surface_area,
    cube_volume, cube_surface_area,
    pyramid_volume, pyramid_surface_area
)
from mathgenius.geometry.trigonometry import (
    sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh,
    degrees_to_radians, radians_to_degrees
)
from mathgenius.geometry.coordinates import (
    distance_2d, distance_3d, midpoint_2d, midpoint_3d,
    slope, line_equation, line_intersection, point_to_line_distance
)
from mathgenius.geometry.spatial import (
    vector_add, vector_subtract, vector_dot_product, vector_cross_product,
    vector_magnitude, vector_normalize, angle_between_vectors,
    rotate_point, translate_point, scale_point
)
from mathgenius.advanced.calculus import (
    differentiate, integrate_definite, integrate_indefinite, compute_limit,
    taylor_series, partial_derivative, gradient, hessian_matrix,
    numerical_derivative, numerical_integral
)
from mathgenius.advanced.linear_algebra import (
    matrix_add, matrix_multiply, matrix_transpose, matrix_inverse,
    matrix_determinant, eigenvalues_eigenvectors, solve_linear_system,
    matrix_rank, matrix_nullspace, lu_decomposition, qr_decomposition,
    svd_decomposition, vector_norm, matrix_condition_number, matrix_trace,
    vector_projection
)
from mathgenius.advanced.statistics import (
    mean, median, mode, variance, standard_deviation,
    correlation_coefficient, covariance, normal_distribution_pdf,
    normal_distribution_cdf, binomial_distribution_pmf, poisson_distribution_pmf,
    t_test_one_sample, t_test_two_sample, chi_square_test, linear_regression,
    confidence_interval, z_score, percentile
)
from mathgenius.advanced.symbolic import (
    parse_expression, create_symbol, expand_expression, factor_expression,
    simplify_expression, collect_terms, solve_equation, solve_differential_equation,
    substitute_expression, evaluate_expression, expression_to_latex,
    expression_to_string, symbolic_integrate, symbolic_differentiate,
    symbolic_limit, symbolic_series, create_rational, is_polynomial
)

__all__ = [
    # Arithmetic
    "add", "subtract", "multiply", "divide", "power", "modulo",
    # Algebra
    "solve_linear", "solve_quadratic",
    "expand_expr", "factor_expr", "simplify_expr",
    # Geometry - Shapes
    "triangle_area", "triangle_perimeter", "triangle_area_heron",
    "circle_area", "circle_circumference",
    "rectangle_area", "rectangle_perimeter",
    "polygon_area", "polygon_perimeter",
    "sphere_volume", "sphere_surface_area",
    "cylinder_volume", "cylinder_surface_area",
    "cube_volume", "cube_surface_area",
    "pyramid_volume", "pyramid_surface_area",
    # Geometry - Trigonometry
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sinh", "cosh", "tanh",
    "degrees_to_radians", "radians_to_degrees",
    # Geometry - Coordinates
    "distance_2d", "distance_3d", "midpoint_2d", "midpoint_3d",
    "slope", "line_equation", "line_intersection", "point_to_line_distance",
    # Geometry - Spatial
    "vector_add", "vector_subtract", "vector_dot_product", "vector_cross_product",
    "vector_magnitude", "vector_normalize", "angle_between_vectors",
    "rotate_point", "translate_point", "scale_point",
    # Advanced - Calculus
    "differentiate", "integrate_definite", "integrate_indefinite", "compute_limit",
    "taylor_series", "partial_derivative", "gradient", "hessian_matrix",
    "numerical_derivative", "numerical_integral",
    # Advanced - Linear Algebra
    "matrix_add", "matrix_multiply", "matrix_transpose", "matrix_inverse",
    "matrix_determinant", "eigenvalues_eigenvectors", "solve_linear_system",
    "matrix_rank", "matrix_nullspace", "lu_decomposition", "qr_decomposition",
    "svd_decomposition", "vector_norm", "matrix_condition_number", "matrix_trace",
    "vector_projection",
    # Advanced - Statistics
    "mean", "median", "mode", "variance", "standard_deviation",
    "correlation_coefficient", "covariance", "normal_distribution_pdf",
    "normal_distribution_cdf", "binomial_distribution_pmf", "poisson_distribution_pmf",
    "t_test_one_sample", "t_test_two_sample", "chi_square_test", "linear_regression",
    "confidence_interval", "z_score", "percentile",
    # Advanced - Symbolic Mathematics
    "parse_expression", "create_symbol", "expand_expression", "factor_expression",
    "simplify_expression", "collect_terms", "solve_equation", "solve_differential_equation",
    "substitute_expression", "evaluate_expression", "expression_to_latex",
    "expression_to_string", "symbolic_integrate", "symbolic_differentiate",
    "symbolic_limit", "symbolic_series", "create_rational", "is_polynomial"
]

"""Geometry module for mathgenius."""

from .shapes import (
    triangle_area, triangle_perimeter, 
    circle_area, circle_circumference,
    rectangle_area, rectangle_perimeter,
    polygon_area, polygon_perimeter,
    sphere_volume, sphere_surface_area,
    cylinder_volume, cylinder_surface_area,
    cube_volume, cube_surface_area,
    pyramid_volume, pyramid_surface_area
)

from .trigonometry import (
    sin, cos, tan, asin, acos, atan,
    sinh, cosh, tanh,
    degrees_to_radians, radians_to_degrees
)

from .coordinates import (
    distance_2d, distance_3d, midpoint_2d, midpoint_3d,
    slope, line_equation, line_intersection, point_to_line_distance
)

from .spatial import (
    vector_add, vector_subtract, vector_dot_product, vector_cross_product,
    vector_magnitude, vector_normalize, angle_between_vectors,
    rotate_point, translate_point, scale_point
)

__all__ = [
    # Shapes
    "triangle_area", "triangle_perimeter", 
    "circle_area", "circle_circumference",
    "rectangle_area", "rectangle_perimeter",
    "polygon_area", "polygon_perimeter",
    "sphere_volume", "sphere_surface_area",
    "cylinder_volume", "cylinder_surface_area",
    "cube_volume", "cube_surface_area",
    "pyramid_volume", "pyramid_surface_area",
    
    # Trigonometry
    "sin", "cos", "tan", "asin", "acos", "atan",
    "sinh", "cosh", "tanh",
    "degrees_to_radians", "radians_to_degrees",
    
    # Coordinates
    "distance_2d", "distance_3d", "midpoint_2d", "midpoint_3d",
    "slope", "line_equation", "line_intersection", "point_to_line_distance",
    
    # Spatial
    "vector_add", "vector_subtract", "vector_dot_product", "vector_cross_product",
    "vector_magnitude", "vector_normalize", "angle_between_vectors",
    "rotate_point", "translate_point", "scale_point"
]

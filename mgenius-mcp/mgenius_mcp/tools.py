"""Tool discovery and registration system for MCP server."""

import inspect
import logging
from typing import Dict, Any, List, Callable, Optional, Union
from dataclasses import dataclass
from enum import Enum

import mathgenius.api.dispatcher as dispatcher

logger = logging.getLogger(__name__)


class ToolCategory(Enum):
    """Categories for mathematical tools."""
    ARITHMETIC = "arithmetic"
    ALGEBRA = "algebra"
    GEOMETRY = "geometry"
    TRIGONOMETRY = "trigonometry"
    CALCULUS = "calculus"
    LINEAR_ALGEBRA = "linear_algebra"
    STATISTICS = "statistics"
    SYMBOLIC = "symbolic"


@dataclass
class MCPToolMetadata:
    """Metadata for an MCP tool."""
    name: str
    description: str
    category: ToolCategory
    function: Callable
    parameters: Dict[str, Any]
    return_type: Optional[type] = None
    examples: Optional[List[Dict[str, Any]]] = None


class ToolDiscovery:
    """Tool discovery system for mathematical functions."""
    
    def __init__(self):
        self.discovered_tools: Dict[str, MCPToolMetadata] = {}
        self.category_mapping = self._create_category_mapping()
    
    def _create_category_mapping(self) -> Dict[str, ToolCategory]:
        """Create mapping from function names to tool categories."""
        return {
            # Arithmetic
            "add": ToolCategory.ARITHMETIC,
            "subtract": ToolCategory.ARITHMETIC,
            "multiply": ToolCategory.ARITHMETIC,
            "divide": ToolCategory.ARITHMETIC,
            "power": ToolCategory.ARITHMETIC,
            "modulo": ToolCategory.ARITHMETIC,
            
            # Algebra
            "solve_linear": ToolCategory.ALGEBRA,
            "solve_quadratic": ToolCategory.ALGEBRA,
            "expand_expr": ToolCategory.ALGEBRA,
            "factor_expr": ToolCategory.ALGEBRA,
            "simplify_expr": ToolCategory.ALGEBRA,
            
            # Geometry
            "triangle_area": ToolCategory.GEOMETRY,
            "triangle_perimeter": ToolCategory.GEOMETRY,
            "triangle_area_heron": ToolCategory.GEOMETRY,
            "circle_area": ToolCategory.GEOMETRY,
            "circle_circumference": ToolCategory.GEOMETRY,
            "rectangle_area": ToolCategory.GEOMETRY,
            "rectangle_perimeter": ToolCategory.GEOMETRY,
            "polygon_area": ToolCategory.GEOMETRY,
            "polygon_perimeter": ToolCategory.GEOMETRY,
            "sphere_volume": ToolCategory.GEOMETRY,
            "sphere_surface_area": ToolCategory.GEOMETRY,
            "cylinder_volume": ToolCategory.GEOMETRY,
            "cylinder_surface_area": ToolCategory.GEOMETRY,
            "cube_volume": ToolCategory.GEOMETRY,
            "cube_surface_area": ToolCategory.GEOMETRY,
            "pyramid_volume": ToolCategory.GEOMETRY,
            "pyramid_surface_area": ToolCategory.GEOMETRY,
            "distance_2d": ToolCategory.GEOMETRY,
            "distance_3d": ToolCategory.GEOMETRY,
            "midpoint_2d": ToolCategory.GEOMETRY,
            "midpoint_3d": ToolCategory.GEOMETRY,
            "slope": ToolCategory.GEOMETRY,
            "line_equation": ToolCategory.GEOMETRY,
            "line_intersection": ToolCategory.GEOMETRY,
            "point_to_line_distance": ToolCategory.GEOMETRY,
            "vector_add": ToolCategory.GEOMETRY,
            "vector_subtract": ToolCategory.GEOMETRY,
            "vector_dot_product": ToolCategory.GEOMETRY,
            "vector_cross_product": ToolCategory.GEOMETRY,
            "vector_magnitude": ToolCategory.GEOMETRY,
            "vector_normalize": ToolCategory.GEOMETRY,
            "angle_between_vectors": ToolCategory.GEOMETRY,
            "rotate_point": ToolCategory.GEOMETRY,
            "translate_point": ToolCategory.GEOMETRY,
            "scale_point": ToolCategory.GEOMETRY,
            
            # Trigonometry
            "sin": ToolCategory.TRIGONOMETRY,
            "cos": ToolCategory.TRIGONOMETRY,
            "tan": ToolCategory.TRIGONOMETRY,
            "asin": ToolCategory.TRIGONOMETRY,
            "acos": ToolCategory.TRIGONOMETRY,
            "atan": ToolCategory.TRIGONOMETRY,
            "sinh": ToolCategory.TRIGONOMETRY,
            "cosh": ToolCategory.TRIGONOMETRY,
            "tanh": ToolCategory.TRIGONOMETRY,
            "degrees_to_radians": ToolCategory.TRIGONOMETRY,
            "radians_to_degrees": ToolCategory.TRIGONOMETRY,
            
            # Calculus
            "differentiate": ToolCategory.CALCULUS,
            "integrate_definite": ToolCategory.CALCULUS,
            "integrate_indefinite": ToolCategory.CALCULUS,
            "compute_limit": ToolCategory.CALCULUS,
            "taylor_series": ToolCategory.CALCULUS,
            "partial_derivative": ToolCategory.CALCULUS,
            "gradient": ToolCategory.CALCULUS,
            "hessian_matrix": ToolCategory.CALCULUS,
            "numerical_derivative": ToolCategory.CALCULUS,
            "numerical_integral": ToolCategory.CALCULUS,
            
            # Linear Algebra
            "matrix_add": ToolCategory.LINEAR_ALGEBRA,
            "matrix_multiply": ToolCategory.LINEAR_ALGEBRA,
            "matrix_transpose": ToolCategory.LINEAR_ALGEBRA,
            "matrix_inverse": ToolCategory.LINEAR_ALGEBRA,
            "matrix_determinant": ToolCategory.LINEAR_ALGEBRA,
            "eigenvalues_eigenvectors": ToolCategory.LINEAR_ALGEBRA,
            "solve_linear_system": ToolCategory.LINEAR_ALGEBRA,
            "matrix_rank": ToolCategory.LINEAR_ALGEBRA,
            "matrix_nullspace": ToolCategory.LINEAR_ALGEBRA,
            "lu_decomposition": ToolCategory.LINEAR_ALGEBRA,
            "qr_decomposition": ToolCategory.LINEAR_ALGEBRA,
            "svd_decomposition": ToolCategory.LINEAR_ALGEBRA,
            "vector_norm": ToolCategory.LINEAR_ALGEBRA,
            "matrix_condition_number": ToolCategory.LINEAR_ALGEBRA,
            "matrix_trace": ToolCategory.LINEAR_ALGEBRA,
            "vector_projection": ToolCategory.LINEAR_ALGEBRA,
            
            # Statistics
            "mean": ToolCategory.STATISTICS,
            "median": ToolCategory.STATISTICS,
            "mode": ToolCategory.STATISTICS,
            "variance": ToolCategory.STATISTICS,
            "standard_deviation": ToolCategory.STATISTICS,
            "correlation_coefficient": ToolCategory.STATISTICS,
            "covariance": ToolCategory.STATISTICS,
            "normal_distribution_pdf": ToolCategory.STATISTICS,
            "normal_distribution_cdf": ToolCategory.STATISTICS,
            "binomial_distribution_pmf": ToolCategory.STATISTICS,
            "poisson_distribution_pmf": ToolCategory.STATISTICS,
            "t_test_one_sample": ToolCategory.STATISTICS,
            "t_test_two_sample": ToolCategory.STATISTICS,
            "chi_square_test": ToolCategory.STATISTICS,
            "linear_regression": ToolCategory.STATISTICS,
            "confidence_interval": ToolCategory.STATISTICS,
            "z_score": ToolCategory.STATISTICS,
            "percentile": ToolCategory.STATISTICS,
            
            # Symbolic
            "parse_expression": ToolCategory.SYMBOLIC,
            "create_symbol": ToolCategory.SYMBOLIC,
            "expand_expression": ToolCategory.SYMBOLIC,
            "factor_expression": ToolCategory.SYMBOLIC,
            "simplify_expression": ToolCategory.SYMBOLIC,
            "collect_terms": ToolCategory.SYMBOLIC,
            "solve_equation": ToolCategory.SYMBOLIC,
            "solve_differential_equation": ToolCategory.SYMBOLIC,
            "substitute_expression": ToolCategory.SYMBOLIC,
            "evaluate_expression": ToolCategory.SYMBOLIC,
            "expression_to_latex": ToolCategory.SYMBOLIC,
            "expression_to_string": ToolCategory.SYMBOLIC,
            "symbolic_integrate": ToolCategory.SYMBOLIC,
            "symbolic_differentiate": ToolCategory.SYMBOLIC,
            "symbolic_limit": ToolCategory.SYMBOLIC,
            "symbolic_series": ToolCategory.SYMBOLIC,
            "create_rational": ToolCategory.SYMBOLIC,
            "is_polynomial": ToolCategory.SYMBOLIC,
        }
    
    def discover_tools(self, enabled_categories: Optional[List[ToolCategory]] = None) -> Dict[str, MCPToolMetadata]:
        """Discover all mathematical tools from the dispatcher."""
        logger.info("Starting tool discovery...")
        
        if enabled_categories is None:
            enabled_categories = list(ToolCategory)
        
        for name in dispatcher.__all__:
            if hasattr(dispatcher, name):
                func = getattr(dispatcher, name)
                
                # Get category for this function
                category = self.category_mapping.get(name, ToolCategory.ARITHMETIC)
                
                # Skip if category is not enabled
                if category not in enabled_categories:
                    continue
                
                # Extract metadata
                metadata = self._extract_tool_metadata(name, func, category)
                
                if metadata:
                    self.discovered_tools[name] = metadata
                    logger.debug(f"Discovered tool: {name} ({category.value})")
        
        logger.info(f"Discovered {len(self.discovered_tools)} tools")
        return self.discovered_tools
    
    def _extract_tool_metadata(self, name: str, func: Callable, category: ToolCategory) -> Optional[MCPToolMetadata]:
        """Extract metadata from a function."""
        try:
            # Get function signature
            sig = inspect.signature(func)
            
            # Get docstring
            doc = func.__doc__ or f"Mathematical function: {name}"
            
            # Extract parameters
            parameters = self._extract_parameters(sig)
            
            # Get return type
            return_type = sig.return_annotation if sig.return_annotation != inspect.Parameter.empty else None
            
            # Create tool metadata
            metadata = MCPToolMetadata(
                name=name,
                description=doc.strip(),
                category=category,
                function=func,
                parameters=parameters,
                return_type=return_type
            )
            
            return metadata
            
        except Exception as e:
            logger.warning(f"Failed to extract metadata for {name}: {e}")
            return None
    
    def _extract_parameters(self, sig: inspect.Signature) -> Dict[str, Any]:
        """Extract parameter information from function signature."""
        parameters = {}
        
        for param_name, param in sig.parameters.items():
            param_info = {
                "name": param_name,
                "required": param.default == inspect.Parameter.empty,
            }
            
            # Add type information
            if param.annotation != inspect.Parameter.empty:
                param_info["type"] = self._get_json_type(param.annotation)
            
            # Add default value
            if param.default != inspect.Parameter.empty:
                param_info["default"] = param.default
            
            parameters[param_name] = param_info
        
        return parameters
    
    def _get_json_type(self, python_type: type) -> str:
        """Convert Python type to JSON schema type."""
        type_mapping = {
            int: "integer",
            float: "number",
            str: "string",
            bool: "boolean",
            list: "array",
            dict: "object",
            tuple: "array",
        }
        
        # Handle Union types (like Optional)
        if hasattr(python_type, "__origin__"):
            if python_type.__origin__ == Union:
                # For Optional types, return the non-None type
                args = python_type.__args__
                non_none_types = [arg for arg in args if arg != type(None)]
                if non_none_types:
                    return self._get_json_type(non_none_types[0])
        
        return type_mapping.get(python_type, "string")
    
    def get_tools_by_category(self, category: ToolCategory) -> Dict[str, MCPToolMetadata]:
        """Get tools filtered by category."""
        return {
            name: metadata
            for name, metadata in self.discovered_tools.items()
            if metadata.category == category
        }
    
    def get_tool_names(self) -> List[str]:
        """Get list of all discovered tool names."""
        return list(self.discovered_tools.keys())
    
    def get_categories(self) -> List[ToolCategory]:
        """Get list of all available categories."""
        return list(set(metadata.category for metadata in self.discovered_tools.values()))


class ToolRegistry:
    """Registry for managing MCP tools."""
    
    def __init__(self):
        self.registered_tools: Dict[str, Any] = {}
        self.discovery = ToolDiscovery()
    
    def register_tools(self, enabled_categories: Optional[List[ToolCategory]] = None) -> int:
        """Register all discovered tools."""
        logger.info("Registering MCP tools...")
        
        # Discover tools
        discovered_tools = self.discovery.discover_tools(enabled_categories)
        
        # Register each tool
        for name, metadata in discovered_tools.items():
            try:
                mcp_tool = self._create_mcp_tool(metadata)
                self.registered_tools[name] = mcp_tool
                logger.debug(f"Registered MCP tool: {name}")
            except Exception as e:
                logger.error(f"Failed to register tool {name}: {e}")
        
        logger.info(f"Registered {len(self.registered_tools)} MCP tools")
        return len(self.registered_tools)
    
    def _create_mcp_tool(self, metadata: MCPToolMetadata) -> Any:
        """Create an MCP tool from metadata."""
        # This will create the actual MCP tool object
        # For now, we'll return a placeholder
        return {
            "name": metadata.name,
            "description": metadata.description,
            "category": metadata.category.value,
            "parameters": metadata.parameters,
            "function": metadata.function
        }
    
    def get_tool(self, name: str) -> Optional[Any]:
        """Get a registered tool by name."""
        return self.registered_tools.get(name)
    
    def get_all_tools(self) -> Dict[str, Any]:
        """Get all registered tools."""
        return self.registered_tools.copy()
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """Get information about all registered tools."""
        return [
            {
                "name": name,
                "description": tool.get("description", ""),
                "category": tool.get("category", ""),
                "parameters": tool.get("parameters", {})
            }
            for name, tool in self.registered_tools.items()
        ]

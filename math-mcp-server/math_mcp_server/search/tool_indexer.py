"""Tool documentation indexer for mathematical functions."""

import inspect
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel

import mathgenius.api.dispatcher as math_dispatcher


logger = logging.getLogger(__name__)


@dataclass
class ToolMetadata:
    """Metadata for a mathematical tool/function."""
    
    name: str
    primary_description: str
    category: str
    alternative_names: List[str]
    purpose: str
    use_cases: List[str]
    mathematical_context: str
    real_world_applications: List[str]
    parameters: Dict[str, Dict[str, Any]]
    basic_examples: List[str]
    practical_examples: List[str]
    keywords: List[str]
    common_phrases: List[str]
    error_scenarios: List[str]
    function_obj: Any


class ToolIndexer:
    """Extracts and indexes mathematical tool documentation."""
    
    def __init__(self):
        """Initialize the tool indexer."""
        self.tools: Dict[str, ToolMetadata] = {}
        self._function_categories = self._get_function_categories()
        
    def _get_function_categories(self) -> Dict[str, str]:
        """Map function names to their mathematical categories."""
        return {
            # Arithmetic
            "add": "arithmetic", "subtract": "arithmetic", "multiply": "arithmetic", 
            "divide": "arithmetic", "power": "arithmetic", "modulo": "arithmetic",
            
            # Algebra
            "solve_linear": "algebra", "solve_quadratic": "algebra",
            "expand_expr": "algebra", "factor_expr": "algebra", "simplify_expr": "algebra",
            
            # Geometry - Shapes
            "triangle_area": "geometry", "triangle_perimeter": "geometry", "triangle_area_heron": "geometry",
            "circle_area": "geometry", "circle_circumference": "geometry",
            "rectangle_area": "geometry", "rectangle_perimeter": "geometry",
            "polygon_area": "geometry", "polygon_perimeter": "geometry",
            "sphere_volume": "geometry", "sphere_surface_area": "geometry",
            "cylinder_volume": "geometry", "cylinder_surface_area": "geometry",
            "cube_volume": "geometry", "cube_surface_area": "geometry",
            "pyramid_volume": "geometry", "pyramid_surface_area": "geometry",
            
            # Trigonometry
            "sin": "trigonometry", "cos": "trigonometry", "tan": "trigonometry",
            "asin": "trigonometry", "acos": "trigonometry", "atan": "trigonometry",
            "sinh": "trigonometry", "cosh": "trigonometry", "tanh": "trigonometry",
            "degrees_to_radians": "trigonometry", "radians_to_degrees": "trigonometry",
            
            # Coordinates
            "distance_2d": "coordinates", "distance_3d": "coordinates", 
            "midpoint_2d": "coordinates", "midpoint_3d": "coordinates",
            "slope": "coordinates", "line_equation": "coordinates", 
            "line_intersection": "coordinates", "point_to_line_distance": "coordinates",
            
            # Spatial/Vector
            "vector_add": "vectors", "vector_subtract": "vectors", 
            "vector_dot_product": "vectors", "vector_cross_product": "vectors",
            "vector_magnitude": "vectors", "vector_normalize": "vectors", 
            "angle_between_vectors": "vectors", "rotate_point": "vectors", 
            "translate_point": "vectors", "scale_point": "vectors",
            
            # Calculus
            "differentiate": "calculus", "integrate_definite": "calculus", 
            "integrate_indefinite": "calculus", "compute_limit": "calculus",
            "taylor_series": "calculus", "partial_derivative": "calculus", 
            "gradient": "calculus", "hessian_matrix": "calculus",
            "numerical_derivative": "calculus", "numerical_integral": "calculus",
            
            # Linear Algebra
            "matrix_add": "linear_algebra", "matrix_multiply": "linear_algebra", 
            "matrix_transpose": "linear_algebra", "matrix_inverse": "linear_algebra",
            "matrix_determinant": "linear_algebra", "eigenvalues_eigenvectors": "linear_algebra", 
            "solve_linear_system": "linear_algebra", "matrix_rank": "linear_algebra", 
            "matrix_nullspace": "linear_algebra", "lu_decomposition": "linear_algebra", 
            "qr_decomposition": "linear_algebra", "svd_decomposition": "linear_algebra", 
            "vector_norm": "linear_algebra", "matrix_condition_number": "linear_algebra", 
            "matrix_trace": "linear_algebra", "vector_projection": "linear_algebra",
            
            # Statistics
            "mean": "statistics", "median": "statistics", "mode": "statistics", 
            "variance": "statistics", "standard_deviation": "statistics",
            "correlation_coefficient": "statistics", "covariance": "statistics", 
            "normal_distribution_pdf": "statistics", "normal_distribution_cdf": "statistics", 
            "binomial_distribution_pmf": "statistics", "poisson_distribution_pmf": "statistics",
            "t_test_one_sample": "statistics", "t_test_two_sample": "statistics", 
            "chi_square_test": "statistics", "linear_regression": "statistics",
            "confidence_interval": "statistics", "z_score": "statistics", "percentile": "statistics",
            
            # Symbolic Mathematics
            "parse_expression": "symbolic", "create_symbol": "symbolic", 
            "expand_expression": "symbolic", "factor_expression": "symbolic",
            "simplify_expression": "symbolic", "collect_terms": "symbolic", 
            "solve_equation": "symbolic", "solve_differential_equation": "symbolic",
            "substitute_expression": "symbolic", "evaluate_expression": "symbolic", 
            "expression_to_latex": "symbolic", "expression_to_string": "symbolic", 
            "symbolic_integrate": "symbolic", "symbolic_differentiate": "symbolic",
            "symbolic_limit": "symbolic", "symbolic_series": "symbolic", 
            "create_rational": "symbolic", "is_polynomial": "symbolic"
        }
    
    def index_all_tools(self) -> Dict[str, ToolMetadata]:
        """Index all mathematical tools from mathgenius dispatcher."""
        logger.info("Starting tool indexing process...")
        
        # Get all available functions from dispatcher
        all_functions = math_dispatcher.__all__
        
        for func_name in all_functions:
            try:
                func_obj = getattr(math_dispatcher, func_name)
                metadata = self._generate_tool_metadata(func_name, func_obj)
                self.tools[func_name] = metadata
                logger.debug(f"Indexed tool: {func_name}")
            except Exception as e:
                logger.error(f"Failed to index tool {func_name}: {e}")
                
        logger.info(f"Successfully indexed {len(self.tools)} mathematical tools")
        return self.tools
    
    def _generate_tool_metadata(self, func_name: str, func_obj: Any) -> ToolMetadata:
        """Generate comprehensive metadata for a mathematical function."""
        
        # Get function signature and docstring
        signature = inspect.signature(func_obj)
        docstring = inspect.getdoc(func_obj) or "Mathematical function"
        
        # Get category
        category = self._function_categories.get(func_name, "mathematics")
        
        # Generate comprehensive documentation
        metadata = ToolMetadata(
            name=func_name,
            primary_description=self._generate_primary_description(func_name, docstring),
            category=category,
            alternative_names=self._generate_alternative_names(func_name),
            purpose=self._generate_purpose(func_name, category),
            use_cases=self._generate_use_cases(func_name, category),
            mathematical_context=self._generate_mathematical_context(func_name, category),
            real_world_applications=self._generate_real_world_applications(func_name, category),
            parameters=self._extract_parameters(signature),
            basic_examples=self._generate_basic_examples(func_name, signature),
            practical_examples=self._generate_practical_examples(func_name, category),
            keywords=self._generate_keywords(func_name, category),
            common_phrases=self._generate_common_phrases(func_name, category),
            error_scenarios=self._generate_error_scenarios(func_name, category),
            function_obj=func_obj
        )
        
        return metadata
    
    def _generate_primary_description(self, func_name: str, docstring: str) -> str:
        """Generate primary description for the function."""
        # Use docstring if available, otherwise generate from function name
        if docstring and len(docstring.strip()) > 10:
            return docstring.strip().split('\n')[0]
        
        # Generate description from function name
        descriptions = {
            "add": "Add two or more numbers together",
            "subtract": "Subtract one number from another",
            "multiply": "Multiply two or more numbers",
            "divide": "Divide one number by another",
            "power": "Raise a number to a power",
            "modulo": "Find the remainder after division",
            "triangle_area": "Calculate the area of a triangle",
            "circle_area": "Calculate the area of a circle",
            "sin": "Calculate the sine of an angle",
            "cos": "Calculate the cosine of an angle",
            "distance_2d": "Calculate distance between two points in 2D space",
            "matrix_multiply": "Multiply two matrices",
            "mean": "Calculate the arithmetic mean of a dataset",
            "solve_linear": "Solve a linear equation",
            "differentiate": "Find the derivative of a mathematical expression",
        }
        
        return descriptions.get(func_name, f"Perform {func_name.replace('_', ' ')} operation")
    
    def _generate_alternative_names(self, func_name: str) -> List[str]:
        """Generate alternative names and synonyms for the function."""
        alternatives = {
            "add": ["sum", "addition", "plus", "combine"],
            "subtract": ["minus", "subtraction", "difference"],
            "multiply": ["times", "multiplication", "product"],
            "divide": ["division", "quotient", "ratio"],
            "triangle_area": ["triangular area", "area of triangle"],
            "circle_area": ["circular area", "area of circle"],
            "distance_2d": ["2D distance", "euclidean distance", "point distance"],
            "mean": ["average", "arithmetic mean", "expected value"],
            "sin": ["sine function", "trigonometric sine"],
            "matrix_multiply": ["matrix product", "matrix multiplication"],
        }
        
        return alternatives.get(func_name, [func_name.replace('_', ' ')])
    
    def _generate_purpose(self, func_name: str, category: str) -> str:
        """Generate purpose statement for the function."""
        purposes = {
            "arithmetic": f"Perform basic {func_name.replace('_', ' ')} arithmetic operation",
            "algebra": f"Solve algebraic problems using {func_name.replace('_', ' ')}",
            "geometry": f"Calculate geometric properties using {func_name.replace('_', ' ')}",
            "trigonometry": f"Compute trigonometric values using {func_name.replace('_', ' ')}",
            "calculus": f"Perform calculus operations using {func_name.replace('_', ' ')}",
            "statistics": f"Analyze statistical data using {func_name.replace('_', ' ')}",
            "linear_algebra": f"Perform linear algebra operations using {func_name.replace('_', ' ')}",
            "symbolic": f"Manipulate symbolic expressions using {func_name.replace('_', ' ')}",
        }
        
        return purposes.get(category, f"Perform mathematical operation: {func_name.replace('_', ' ')}")
    
    def _generate_use_cases(self, func_name: str, category: str) -> List[str]:
        """Generate use cases for the function."""
        use_cases = {
            "arithmetic": ["Basic calculations", "Financial computations", "Engineering calculations"],
            "geometry": ["Area and volume calculations", "Construction planning", "Engineering design"],
            "statistics": ["Data analysis", "Research studies", "Quality control"],
            "calculus": ["Physics problems", "Engineering optimization", "Rate of change analysis"],
            "linear_algebra": ["Computer graphics", "Machine learning", "Engineering systems"],
        }
        
        return use_cases.get(category, ["Mathematical computations", "Problem solving"])
    
    def _generate_mathematical_context(self, func_name: str, category: str) -> str:
        """Generate mathematical context for the function."""
        contexts = {
            "triangle_area": "Uses the formula Area = (1/2) × base × height",
            "circle_area": "Uses the formula Area = π × radius²",
            "distance_2d": "Uses the Euclidean distance formula: √[(x₂-x₁)² + (y₂-y₁)²]",
            "sin": "Trigonometric function representing the ratio of opposite side to hypotenuse",
            "mean": "Central tendency measure calculated as sum of values divided by count",
        }
        
        return contexts.get(func_name, f"Mathematical operation in {category} domain")
    
    def _generate_real_world_applications(self, func_name: str, category: str) -> List[str]:
        """Generate real-world applications for the function."""
        applications = {
            "geometry": ["Architecture", "Construction", "Land surveying", "Computer graphics"],
            "statistics": ["Market research", "Medical studies", "Quality control", "Sports analytics"],
            "calculus": ["Physics modeling", "Economics optimization", "Engineering design"],
            "trigonometry": ["Navigation", "Signal processing", "Computer graphics", "Astronomy"],
        }
        
        return applications.get(category, ["Scientific computing", "Engineering applications"])
    
    def _extract_parameters(self, signature: inspect.Signature) -> Dict[str, Dict[str, Any]]:
        """Extract parameter information from function signature."""
        parameters = {}
        
        for param_name, param in signature.parameters.items():
            param_info = {
                "type": self._get_param_type(param),
                "description": f"Input parameter for {param_name}",
                "required": param.default == inspect.Parameter.empty,
                "default": None if param.default == inspect.Parameter.empty else param.default
            }
            parameters[param_name] = param_info
            
        return parameters
    
    def _get_param_type(self, param: inspect.Parameter) -> str:
        """Get parameter type as string."""
        if param.annotation != inspect.Parameter.empty:
            if hasattr(param.annotation, '__name__'):
                return param.annotation.__name__
            else:
                return str(param.annotation)
        return "Any"
    
    def _generate_basic_examples(self, func_name: str, signature: inspect.Signature) -> List[str]:
        """Generate basic usage examples for the function."""
        param_names = list(signature.parameters.keys())
        
        examples = {
            "add": ["add(5, 3) = 8", "add(10, 20, 30) = 60"],
            "triangle_area": ["triangle_area(3, 4) = 6.0", "triangle_area(10, 5) = 25.0"],
            "sin": ["sin(0) = 0.0", "sin(π/2) ≈ 1.0"],
            "distance_2d": ["distance_2d((0,0), (3,4)) = 5.0"],
            "mean": ["mean([1, 2, 3, 4, 5]) = 3.0"],
        }
        
        if func_name in examples:
            return examples[func_name]
        
        # Generate generic example
        if len(param_names) == 1:
            return [f"{func_name}(value) → result"]
        elif len(param_names) == 2:
            return [f"{func_name}(a, b) → result"]
        else:
            return [f"{func_name}(...) → result"]
    
    def _generate_practical_examples(self, func_name: str, category: str) -> List[str]:
        """Generate practical usage examples."""
        examples = {
            "triangle_area": ["Calculate area of triangular garden plot", "Find roof area for materials"],
            "distance_2d": ["Calculate travel distance between cities", "Measure spacing in design"],
            "mean": ["Calculate average test scores", "Find mean temperature"],
            "sin": ["Calculate wave amplitude", "Determine shadow length"],
        }
        
        return examples.get(func_name, [f"Practical {category} calculation"])
    
    def _generate_keywords(self, func_name: str, category: str) -> List[str]:
        """Generate searchable keywords for the function."""
        base_keywords = [func_name, func_name.replace('_', ' '), category]
        
        category_keywords = {
            "arithmetic": ["math", "calculation", "number", "compute"],
            "geometry": ["shape", "area", "volume", "perimeter", "surface"],
            "trigonometry": ["angle", "sine", "cosine", "tangent", "radian", "degree"],
            "statistics": ["data", "average", "distribution", "probability"],
            "calculus": ["derivative", "integral", "limit", "differential"],
            "linear_algebra": ["matrix", "vector", "system", "linear"],
            "symbolic": ["expression", "equation", "symbol", "algebraic"],
        }
        
        return base_keywords + category_keywords.get(category, ["mathematics"])
    
    def _generate_common_phrases(self, func_name: str, category: str) -> List[str]:
        """Generate common phrases users might search for."""
        phrases = {
            "triangle_area": ["find triangle area", "calculate triangular area", "area of triangle"],
            "add": ["add numbers", "sum values", "addition operation"],
            "distance_2d": ["distance between points", "find distance", "calculate distance"],
            "mean": ["calculate average", "find mean", "arithmetic mean"],
            "sin": ["sine of angle", "trigonometric sine", "sin function"],
        }
        
        return phrases.get(func_name, [f"calculate {func_name.replace('_', ' ')}", f"find {func_name.replace('_', ' ')}"])
    
    def _generate_error_scenarios(self, func_name: str, category: str) -> List[str]:
        """Generate common error scenarios for the function."""
        common_errors = {
            "divide": ["Division by zero", "Non-numeric inputs"],
            "triangle_area": ["Negative dimensions", "Zero area inputs"],
            "sin": ["Invalid angle format", "Angle out of expected range"],
            "matrix_multiply": ["Incompatible matrix dimensions", "Non-numeric matrix elements"],
        }
        
        return common_errors.get(func_name, ["Invalid input parameters", "Computation domain errors"])
    
    def get_all_searchable_content(self, tool_name: str) -> str:
        """Get all searchable content for a tool as a single string."""
        if tool_name not in self.tools:
            return ""
        
        metadata = self.tools[tool_name]
        
        # Combine all searchable fields
        content_parts = [
            metadata.name,
            metadata.primary_description,
            metadata.category,
            metadata.purpose,
            metadata.mathematical_context,
            " ".join(metadata.alternative_names),
            " ".join(metadata.use_cases),
            " ".join(metadata.real_world_applications),
            " ".join(metadata.basic_examples),
            " ".join(metadata.practical_examples),
            " ".join(metadata.keywords),
            " ".join(metadata.common_phrases),
            " ".join([f"{k}: {v.get('description', '')}" for k, v in metadata.parameters.items()])
        ]
        
        return " ".join(filter(None, content_parts))

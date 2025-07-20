"""JSON Schema generation and validation for MCP mathematical operations."""

import json
import logging
from typing import Dict, Any, List, Optional, Union, Type, get_type_hints
from dataclasses import dataclass
from enum import Enum
import inspect
import re

logger = logging.getLogger(__name__)


class JSONSchemaType(Enum):
    """JSON Schema types."""
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"
    NULL = "null"


@dataclass
class ParameterConstraint:
    """Represents constraints for a parameter."""
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    exclusive_maximum: Optional[float] = None
    multiple_of: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None
    unique_items: Optional[bool] = None
    enum: Optional[List[Any]] = None
    const: Optional[Any] = None


class SchemaGenerator:
    """Generates JSON schemas for mathematical operations."""
    
    def __init__(self):
        self.mathematical_constraints = self._create_mathematical_constraints()
        self.type_mapping = self._create_type_mapping()
    
    def _create_mathematical_constraints(self) -> Dict[str, ParameterConstraint]:
        """Create mathematical constraints for common parameters."""
        return {
            # Geometric constraints
            "radius": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "side": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "length": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "width": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "height": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "base": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "area": ParameterConstraint(minimum=0),
            "volume": ParameterConstraint(minimum=0),
            
            # Trigonometric constraints
            "angle": ParameterConstraint(minimum=-360, maximum=360),
            "angle_rad": ParameterConstraint(minimum=-6.28318530718, maximum=6.28318530718),
            
            # Statistical constraints
            "sample_size": ParameterConstraint(minimum=1, multiple_of=1),
            "degrees_of_freedom": ParameterConstraint(minimum=1, multiple_of=1),
            "confidence_level": ParameterConstraint(minimum=0, maximum=1, exclusive_minimum=0, exclusive_maximum=1),
            "probability": ParameterConstraint(minimum=0, maximum=1),
            
            # Matrix constraints
            "dimension": ParameterConstraint(minimum=1, multiple_of=1),
            "rank": ParameterConstraint(minimum=0, multiple_of=1),
            
            # Numerical constraints
            "precision": ParameterConstraint(minimum=1, maximum=50, multiple_of=1),
            "tolerance": ParameterConstraint(minimum=0, exclusive_minimum=0),
            "iterations": ParameterConstraint(minimum=1, maximum=10000, multiple_of=1),
            
            # Coordinate constraints
            "x": ParameterConstraint(),
            "y": ParameterConstraint(),
            "z": ParameterConstraint(),
        }
    
    def _create_type_mapping(self) -> Dict[Type, JSONSchemaType]:
        """Create mapping from Python types to JSON Schema types."""
        return {
            int: JSONSchemaType.INTEGER,
            float: JSONSchemaType.NUMBER,
            str: JSONSchemaType.STRING,
            bool: JSONSchemaType.BOOLEAN,
            list: JSONSchemaType.ARRAY,
            tuple: JSONSchemaType.ARRAY,
            dict: JSONSchemaType.OBJECT,
            type(None): JSONSchemaType.NULL,
        }
    
    def generate_schema(self, tool_name: str, function: callable) -> Dict[str, Any]:
        """Generate JSON schema for a mathematical function."""
        logger.debug(f"Generating schema for {tool_name}")
        
        # Get function signature
        sig = inspect.signature(function)
        
        # Get function docstring
        docstring = function.__doc__ or f"Mathematical function: {tool_name}"
        
        # Create base schema
        schema = {
            "type": "object",
            "title": f"{tool_name} Parameters",
            "description": docstring.strip(),
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
        
        # Process parameters
        for param_name, param in sig.parameters.items():
            param_schema = self._generate_parameter_schema(param_name, param, tool_name)
            schema["properties"][param_name] = param_schema
            
            # Add to required if no default value
            if param.default == inspect.Parameter.empty:
                schema["required"].append(param_name)
        
        # Add examples if available
        examples = self._generate_examples(tool_name, schema)
        if examples:
            schema["examples"] = examples
        
        return schema
    
    def _generate_parameter_schema(self, param_name: str, param: inspect.Parameter, tool_name: str) -> Dict[str, Any]:
        """Generate schema for a single parameter."""
        param_schema = {
            "description": f"Parameter {param_name} for {tool_name}"
        }
        
        # Get type information
        param_type = param.annotation
        if param_type == inspect.Parameter.empty:
            param_type = self._infer_type_from_name(param_name, tool_name)
        
        # Set JSON Schema type
        json_type = self._get_json_schema_type(param_type)
        param_schema["type"] = json_type.value
        
        # Add default value if present
        if param.default != inspect.Parameter.empty:
            param_schema["default"] = param.default
        
        # Add mathematical constraints
        constraints = self._get_parameter_constraints(param_name, tool_name)
        if constraints:
            param_schema.update(self._constraint_to_schema(constraints))
        
        # Add format hints
        format_hint = self._get_format_hint(param_name, json_type)
        if format_hint:
            param_schema["format"] = format_hint
        
        # Add examples
        examples = self._get_parameter_examples(param_name, param_type, tool_name)
        if examples:
            param_schema["examples"] = examples
        
        return param_schema
    
    def _infer_type_from_name(self, param_name: str, tool_name: str) -> Type:
        """Infer parameter type from its name and context."""
        # Common parameter name patterns
        if param_name in ["x", "y", "z", "a", "b", "c", "radius", "side", "length", "width", "height", "base", "angle"]:
            return float
        elif param_name in ["n", "count", "size", "dimension", "precision", "iterations"]:
            return int
        elif param_name.endswith("_list") or param_name.endswith("_array") or param_name == "coordinates":
            return list
        elif param_name.endswith("_dict") or param_name == "matrix":
            return dict
        elif param_name.startswith("is_") or param_name.startswith("has_") or param_name.endswith("_flag"):
            return bool
        else:
            return str
    
    def _get_json_schema_type(self, python_type: Type) -> JSONSchemaType:
        """Convert Python type to JSON Schema type."""
        # Handle Union types (like Optional)
        if hasattr(python_type, "__origin__"):
            if python_type.__origin__ == Union:
                # For Optional types, return the non-None type
                args = python_type.__args__
                non_none_types = [arg for arg in args if arg != type(None)]
                if non_none_types:
                    return self._get_json_schema_type(non_none_types[0])
        
        # Handle List types
        if hasattr(python_type, "__origin__") and python_type.__origin__ == list:
            return JSONSchemaType.ARRAY
        
        # Handle Dict types
        if hasattr(python_type, "__origin__") and python_type.__origin__ == dict:
            return JSONSchemaType.OBJECT
        
        # Direct mapping
        return self.type_mapping.get(python_type, JSONSchemaType.STRING)
    
    def _get_parameter_constraints(self, param_name: str, tool_name: str) -> Optional[ParameterConstraint]:
        """Get constraints for a parameter based on its name and context."""
        # Direct name match
        if param_name in self.mathematical_constraints:
            return self.mathematical_constraints[param_name]
        
        # Pattern matching
        if "radius" in param_name.lower():
            return self.mathematical_constraints["radius"]
        elif "angle" in param_name.lower():
            if "rad" in param_name.lower():
                return self.mathematical_constraints["angle_rad"]
            else:
                return self.mathematical_constraints["angle"]
        elif any(word in param_name.lower() for word in ["side", "length", "width", "height", "base"]):
            return self.mathematical_constraints["side"]
        elif "precision" in param_name.lower():
            return self.mathematical_constraints["precision"]
        elif "tolerance" in param_name.lower():
            return self.mathematical_constraints["tolerance"]
        elif "iteration" in param_name.lower():
            return self.mathematical_constraints["iterations"]
        elif "confidence" in param_name.lower():
            return self.mathematical_constraints["confidence_level"]
        elif "probability" in param_name.lower():
            return self.mathematical_constraints["probability"]
        
        # Tool-specific constraints
        if tool_name.startswith("asin") or tool_name.startswith("acos"):
            if param_name in ["x", "value"]:
                return ParameterConstraint(minimum=-1, maximum=1)
        elif tool_name == "divide" or tool_name == "modulo":
            if param_name in ["b", "divisor", "denominator"]:
                return ParameterConstraint(const=None)  # Cannot be zero, but we'll handle this in validation
        elif "sqrt" in tool_name:
            if param_name in ["x", "value"]:
                return ParameterConstraint(minimum=0)
        elif "log" in tool_name:
            if param_name in ["x", "value"]:
                return ParameterConstraint(minimum=0, exclusive_minimum=0)
        
        return None
    
    def _constraint_to_schema(self, constraint: ParameterConstraint) -> Dict[str, Any]:
        """Convert parameter constraint to JSON Schema properties."""
        schema_props = {}
        
        if constraint.minimum is not None:
            schema_props["minimum"] = constraint.minimum
        if constraint.maximum is not None:
            schema_props["maximum"] = constraint.maximum
        if constraint.exclusive_minimum is not None:
            schema_props["exclusiveMinimum"] = constraint.exclusive_minimum
        if constraint.exclusive_maximum is not None:
            schema_props["exclusiveMaximum"] = constraint.exclusive_maximum
        if constraint.multiple_of is not None:
            schema_props["multipleOf"] = constraint.multiple_of
        if constraint.min_length is not None:
            schema_props["minLength"] = constraint.min_length
        if constraint.max_length is not None:
            schema_props["maxLength"] = constraint.max_length
        if constraint.pattern is not None:
            schema_props["pattern"] = constraint.pattern
        if constraint.min_items is not None:
            schema_props["minItems"] = constraint.min_items
        if constraint.max_items is not None:
            schema_props["maxItems"] = constraint.max_items
        if constraint.unique_items is not None:
            schema_props["uniqueItems"] = constraint.unique_items
        if constraint.enum is not None:
            schema_props["enum"] = constraint.enum
        if constraint.const is not None:
            schema_props["const"] = constraint.const
        
        return schema_props
    
    def _get_format_hint(self, param_name: str, json_type: JSONSchemaType) -> Optional[str]:
        """Get format hint for a parameter."""
        if json_type == JSONSchemaType.STRING:
            if "expression" in param_name.lower():
                return "mathematical-expression"
            elif "equation" in param_name.lower():
                return "mathematical-equation"
        elif json_type == JSONSchemaType.NUMBER:
            if "angle" in param_name.lower():
                return "angle"
            elif "coordinate" in param_name.lower():
                return "coordinate"
        
        return None
    
    def _get_parameter_examples(self, param_name: str, param_type: Type, tool_name: str) -> Optional[List[Any]]:
        """Get examples for a parameter."""
        # Common examples based on parameter name
        if param_name in ["x", "y", "z"]:
            return [1.0, 2.5, -1.5]
        elif param_name in ["radius", "side", "length", "width", "height"]:
            return [1.0, 5.0, 10.0]
        elif param_name == "angle":
            return [0, 30, 45, 90, 180]
        elif param_name == "angle_rad":
            return [0, 0.523599, 0.785398, 1.570796, 3.141593]
        elif param_name in ["a", "b", "c"]:
            if "triangle" in tool_name:
                return [3.0, 4.0, 5.0]
            else:
                return [1.0, 2.0, 3.0]
        elif param_name == "expression":
            return ["x^2 + 2*x + 1", "sin(x) + cos(x)", "log(x) + exp(x)"]
        elif param_name == "equation":
            return ["x^2 - 4 = 0", "2*x + 3 = 7", "x^2 + x - 6 = 0"]
        elif param_name == "matrix":
            return [[[1, 2], [3, 4]], [[1, 0], [0, 1]]]
        elif param_name == "vector":
            return [[1, 2, 3], [0, 1, 0]]
        elif param_name == "coordinates":
            return [[0, 0], [1, 1], [2, 3]]
        
        return None
    
    def _generate_examples(self, tool_name: str, schema: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Generate complete examples for a tool."""
        examples = []
        
        # Tool-specific examples
        if tool_name == "add":
            examples.extend([
                {"a": 2, "b": 3},
                {"a": 1.5, "b": 2.5},
                {"a": -1, "b": 1}
            ])
        elif tool_name == "circle_area":
            examples.extend([
                {"radius": 1.0},
                {"radius": 5.0},
                {"radius": 10.0}
            ])
        elif tool_name == "solve_quadratic":
            examples.extend([
                {"a": 1, "b": -5, "c": 6},
                {"a": 1, "b": 0, "c": -4},
                {"a": 2, "b": 4, "c": 2}
            ])
        elif tool_name == "sin":
            examples.extend([
                {"x": 0},
                {"x": 1.570796},  # π/2
                {"x": 3.141593}   # π
            ])
        elif tool_name == "matrix_multiply":
            examples.extend([
                {
                    "a": [[1, 2], [3, 4]],
                    "b": [[5, 6], [7, 8]]
                },
                {
                    "a": [[1, 0], [0, 1]],
                    "b": [[2, 3], [4, 5]]
                }
            ])
        
        return examples if examples else None


class SchemaValidator:
    """Validates parameters against JSON schemas."""
    
    def __init__(self):
        self.schemas: Dict[str, Dict[str, Any]] = {}
    
    def register_schema(self, tool_name: str, schema: Dict[str, Any]) -> None:
        """Register a schema for a tool."""
        self.schemas[tool_name] = schema
        logger.debug(f"Registered schema for {tool_name}")
    
    def validate(self, tool_name: str, parameters: Dict[str, Any]) -> List[str]:
        """Validate parameters against the tool's schema."""
        if tool_name not in self.schemas:
            return [f"No schema found for tool: {tool_name}"]
        
        schema = self.schemas[tool_name]
        errors = []
        
        # Check required parameters
        required_params = schema.get("required", [])
        for param in required_params:
            if param not in parameters:
                errors.append(f"Required parameter '{param}' is missing")
        
        # Validate each parameter
        for param_name, param_value in parameters.items():
            if param_name in schema.get("properties", {}):
                param_schema = schema["properties"][param_name]
                param_errors = self._validate_parameter(param_name, param_value, param_schema)
                errors.extend(param_errors)
            elif not schema.get("additionalProperties", True):
                errors.append(f"Unknown parameter '{param_name}' is not allowed")
        
        return errors
    
    def _validate_parameter(self, param_name: str, value: Any, param_schema: Dict[str, Any]) -> List[str]:
        """Validate a single parameter."""
        errors = []
        
        # Type validation
        expected_type = param_schema.get("type")
        if expected_type and not self._check_type(value, expected_type):
            errors.append(f"Parameter '{param_name}' must be of type {expected_type}")
            return errors  # Don't continue if type is wrong
        
        # Numeric constraints
        if expected_type in ["number", "integer"]:
            errors.extend(self._validate_numeric_constraints(param_name, value, param_schema))
        
        # String constraints
        elif expected_type == "string":
            errors.extend(self._validate_string_constraints(param_name, value, param_schema))
        
        # Array constraints
        elif expected_type == "array":
            errors.extend(self._validate_array_constraints(param_name, value, param_schema))
        
        # Object constraints
        elif expected_type == "object":
            errors.extend(self._validate_object_constraints(param_name, value, param_schema))
        
        # Enum validation
        if "enum" in param_schema:
            if value not in param_schema["enum"]:
                errors.append(f"Parameter '{param_name}' must be one of {param_schema['enum']}")
        
        # Const validation
        if "const" in param_schema:
            if value != param_schema["const"]:
                errors.append(f"Parameter '{param_name}' must be {param_schema['const']}")
        
        return errors
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected JSON Schema type."""
        type_checks = {
            "string": lambda v: isinstance(v, str),
            "number": lambda v: isinstance(v, (int, float)),
            "integer": lambda v: isinstance(v, int),
            "boolean": lambda v: isinstance(v, bool),
            "array": lambda v: isinstance(v, (list, tuple)),
            "object": lambda v: isinstance(v, dict),
            "null": lambda v: v is None
        }
        
        return type_checks.get(expected_type, lambda v: True)(value)
    
    def _validate_numeric_constraints(self, param_name: str, value: Union[int, float], param_schema: Dict[str, Any]) -> List[str]:
        """Validate numeric constraints."""
        errors = []
        
        if "minimum" in param_schema and value < param_schema["minimum"]:
            errors.append(f"Parameter '{param_name}' must be >= {param_schema['minimum']}")
        
        if "maximum" in param_schema and value > param_schema["maximum"]:
            errors.append(f"Parameter '{param_name}' must be <= {param_schema['maximum']}")
        
        if "exclusiveMinimum" in param_schema and value <= param_schema["exclusiveMinimum"]:
            errors.append(f"Parameter '{param_name}' must be > {param_schema['exclusiveMinimum']}")
        
        if "exclusiveMaximum" in param_schema and value >= param_schema["exclusiveMaximum"]:
            errors.append(f"Parameter '{param_name}' must be < {param_schema['exclusiveMaximum']}")
        
        if "multipleOf" in param_schema and value % param_schema["multipleOf"] != 0:
            errors.append(f"Parameter '{param_name}' must be a multiple of {param_schema['multipleOf']}")
        
        return errors
    
    def _validate_string_constraints(self, param_name: str, value: str, param_schema: Dict[str, Any]) -> List[str]:
        """Validate string constraints."""
        errors = []
        
        if "minLength" in param_schema and len(value) < param_schema["minLength"]:
            errors.append(f"Parameter '{param_name}' must be at least {param_schema['minLength']} characters")
        
        if "maxLength" in param_schema and len(value) > param_schema["maxLength"]:
            errors.append(f"Parameter '{param_name}' must be at most {param_schema['maxLength']} characters")
        
        if "pattern" in param_schema and not re.match(param_schema["pattern"], value):
            errors.append(f"Parameter '{param_name}' must match pattern {param_schema['pattern']}")
        
        return errors
    
    def _validate_array_constraints(self, param_name: str, value: List[Any], param_schema: Dict[str, Any]) -> List[str]:
        """Validate array constraints."""
        errors = []
        
        if "minItems" in param_schema and len(value) < param_schema["minItems"]:
            errors.append(f"Parameter '{param_name}' must have at least {param_schema['minItems']} items")
        
        if "maxItems" in param_schema and len(value) > param_schema["maxItems"]:
            errors.append(f"Parameter '{param_name}' must have at most {param_schema['maxItems']} items")
        
        if "uniqueItems" in param_schema and param_schema["uniqueItems"] and len(value) != len(set(value)):
            errors.append(f"Parameter '{param_name}' must have unique items")
        
        return errors
    
    def _validate_object_constraints(self, param_name: str, value: Dict[str, Any], param_schema: Dict[str, Any]) -> List[str]:
        """Validate object constraints."""
        errors = []
        
        # Additional validation for objects can be added here
        return errors
    
    def get_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get schema for a tool."""
        return self.schemas.get(tool_name)
    
    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered schemas."""
        return self.schemas.copy()


class ValidationMiddleware:
    """Middleware for validating MCP requests."""
    
    def __init__(self, validator: SchemaValidator):
        self.validator = validator
    
    async def validate_request(self, tool_name: str, parameters: Dict[str, Any]) -> Optional[str]:
        """Validate an MCP request."""
        errors = self.validator.validate(tool_name, parameters)
        
        if errors:
            return "; ".join(errors)
        
        return None

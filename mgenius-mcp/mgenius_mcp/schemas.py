"""JSON Schema generation and validation for mathematical operations."""

import json
import logging
from typing import Dict, Any, Optional, List, Union, Type, get_type_hints, get_origin, get_args
from dataclasses import dataclass
import inspect

from .tools import MCPToolMetadata, ToolCategory

logger = logging.getLogger(__name__)


@dataclass
class ValidationError:
    """Represents a validation error."""
    field: str
    message: str
    value: Any = None


class SchemaGenerator:
    """Generates JSON schemas for mathematical operations."""
    
    def __init__(self):
        self.mathematical_constraints = self._create_mathematical_constraints()
    
    def _create_mathematical_constraints(self) -> Dict[str, Dict[str, Any]]:
        """Create mathematical constraints for different types of operations."""
        return {
            # Arithmetic constraints
            "divide": {
                "b": {"not": {"const": 0}, "description": "Divisor cannot be zero"}
            },
            "power": {
                "base": {"description": "Base number"},
                "exponent": {"description": "Exponent"}
            },
            "modulo": {
                "b": {"not": {"const": 0}, "description": "Divisor cannot be zero"}
            },
            
            # Geometry constraints
            "circle_area": {
                "radius": {"minimum": 0, "description": "Radius must be non-negative"}
            },
            "circle_circumference": {
                "radius": {"minimum": 0, "description": "Radius must be non-negative"}
            },
            "sphere_volume": {
                "radius": {"minimum": 0, "description": "Radius must be non-negative"}
            },
            "sphere_surface_area": {
                "radius": {"minimum": 0, "description": "Radius must be non-negative"}
            },
            "cylinder_volume": {
                "radius": {"minimum": 0, "description": "Radius must be non-negative"},
                "height": {"minimum": 0, "description": "Height must be non-negative"}
            },
            "cylinder_surface_area": {
                "radius": {"minimum": 0, "description": "Radius must be non-negative"},
                "height": {"minimum": 0, "description": "Height must be non-negative"}
            },
            "cube_volume": {
                "side": {"minimum": 0, "description": "Side length must be non-negative"}
            },
            "cube_surface_area": {
                "side": {"minimum": 0, "description": "Side length must be non-negative"}
            },
            "triangle_area": {
                "base": {"minimum": 0, "description": "Base must be non-negative"},
                "height": {"minimum": 0, "description": "Height must be non-negative"}
            },
            "triangle_area_heron": {
                "a": {"minimum": 0, "description": "Side length must be positive"},
                "b": {"minimum": 0, "description": "Side length must be positive"},
                "c": {"minimum": 0, "description": "Side length must be positive"}
            },
            "rectangle_area": {
                "length": {"minimum": 0, "description": "Length must be non-negative"},
                "width": {"minimum": 0, "description": "Width must be non-negative"}
            },
            "rectangle_perimeter": {
                "length": {"minimum": 0, "description": "Length must be non-negative"},
                "width": {"minimum": 0, "description": "Width must be non-negative"}
            },
            
            # Trigonometry constraints
            "asin": {
                "x": {"minimum": -1, "maximum": 1, "description": "Input must be between -1 and 1"}
            },
            "acos": {
                "x": {"minimum": -1, "maximum": 1, "description": "Input must be between -1 and 1"}
            },
            
            # Statistics constraints
            "variance": {
                "data": {"type": "array", "minItems": 1, "description": "Data must be non-empty"}
            },
            "standard_deviation": {
                "data": {"type": "array", "minItems": 1, "description": "Data must be non-empty"}
            },
            "correlation_coefficient": {
                "x": {"type": "array", "minItems": 2, "description": "X data must have at least 2 elements"},
                "y": {"type": "array", "minItems": 2, "description": "Y data must have at least 2 elements"}
            },
            "t_test_one_sample": {
                "data": {"type": "array", "minItems": 2, "description": "Data must have at least 2 elements"}
            },
            "t_test_two_sample": {
                "data1": {"type": "array", "minItems": 2, "description": "Data1 must have at least 2 elements"},
                "data2": {"type": "array", "minItems": 2, "description": "Data2 must have at least 2 elements"}
            },
            
            # Linear Algebra constraints
            "matrix_inverse": {
                "matrix": {"description": "Matrix must be square and non-singular"}
            },
            "matrix_determinant": {
                "matrix": {"description": "Matrix must be square"}
            },
            "eigenvalues_eigenvectors": {
                "matrix": {"description": "Matrix must be square"}
            }
        }
    
    def generate_schema(self, metadata: MCPToolMetadata) -> Dict[str, Any]:
        """Generate JSON schema for a mathematical tool."""
        schema = {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
            "title": f"Schema for {metadata.name}",
            "description": metadata.description
        }
        
        # Add parameters to schema
        for param_name, param_info in metadata.parameters.items():
            property_schema = self._generate_parameter_schema(
                param_name, param_info, metadata.name
            )
            schema["properties"][param_name] = property_schema
            
            # Add to required if parameter is required
            if param_info.get("required", False):
                schema["required"].append(param_name)
        
        # Add mathematical constraints
        self._add_mathematical_constraints(schema, metadata.name)
        
        return schema
    
    def _generate_parameter_schema(self, param_name: str, param_info: Dict[str, Any], function_name: str) -> Dict[str, Any]:
        """Generate schema for a single parameter."""
        property_schema = {}
        
        # Set basic type
        param_type = param_info.get("type", "string")
        property_schema["type"] = param_type
        
        # Add description
        if "description" in param_info:
            property_schema["description"] = param_info["description"]
        else:
            property_schema["description"] = f"Parameter {param_name} for {function_name}"
        
        # Add default value
        if "default" in param_info:
            property_schema["default"] = param_info["default"]
        
        # Add type-specific constraints
        if param_type == "number":
            property_schema.update(self._get_number_constraints(param_name, function_name))
        elif param_type == "integer":
            property_schema.update(self._get_integer_constraints(param_name, function_name))
        elif param_type == "string":
            property_schema.update(self._get_string_constraints(param_name, function_name))
        elif param_type == "array":
            property_schema.update(self._get_array_constraints(param_name, function_name))
        elif param_type == "object":
            property_schema.update(self._get_object_constraints(param_name, function_name))
        
        return property_schema
    
    def _get_number_constraints(self, param_name: str, function_name: str) -> Dict[str, Any]:
        """Get constraints for number parameters."""
        constraints = {}
        
        # Check for specific mathematical constraints
        if function_name in self.mathematical_constraints:
            func_constraints = self.mathematical_constraints[function_name]
            if param_name in func_constraints:
                constraints.update(func_constraints[param_name])
        
        # General number constraints
        if param_name in ["radius", "side", "length", "width", "height", "base"]:
            constraints["minimum"] = 0
        
        return constraints
    
    def _get_integer_constraints(self, param_name: str, function_name: str) -> Dict[str, Any]:
        """Get constraints for integer parameters."""
        constraints = {}
        
        # Check for specific mathematical constraints
        if function_name in self.mathematical_constraints:
            func_constraints = self.mathematical_constraints[function_name]
            if param_name in func_constraints:
                constraints.update(func_constraints[param_name])
        
        # General integer constraints
        if param_name in ["n", "degree", "precision"]:
            constraints["minimum"] = 0
        
        return constraints
    
    def _get_string_constraints(self, param_name: str, function_name: str) -> Dict[str, Any]:
        """Get constraints for string parameters."""
        constraints = {}
        
        # Mathematical expression constraints
        if param_name in ["expression", "expr", "equation", "formula"]:
            constraints["pattern"] = r"^[a-zA-Z0-9+\-*/()^.,\s=<>!]+$"
            constraints["minLength"] = 1
            constraints["maxLength"] = 1000
        
        # Variable name constraints
        if param_name in ["variable", "var", "symbol"]:
            constraints["pattern"] = r"^[a-zA-Z][a-zA-Z0-9_]*$"
            constraints["minLength"] = 1
            constraints["maxLength"] = 50
        
        return constraints
    
    def _get_array_constraints(self, param_name: str, function_name: str) -> Dict[str, Any]:
        """Get constraints for array parameters."""
        constraints = {}
        
        # Check for specific mathematical constraints
        if function_name in self.mathematical_constraints:
            func_constraints = self.mathematical_constraints[function_name]
            if param_name in func_constraints:
                constraints.update(func_constraints[param_name])
        
        # General array constraints
        if param_name in ["data", "points", "values"]:
            constraints["items"] = {"type": "number"}
            constraints["minItems"] = 1
            constraints["maxItems"] = 10000
        
        if param_name in ["matrix", "matrices"]:
            constraints["items"] = {
                "type": "array",
                "items": {"type": "number"}
            }
            constraints["minItems"] = 1
            constraints["maxItems"] = 1000
        
        if param_name in ["vector", "vectors"]:
            constraints["items"] = {"type": "number"}
            constraints["minItems"] = 1
            constraints["maxItems"] = 1000
        
        return constraints
    
    def _get_object_constraints(self, param_name: str, function_name: str) -> Dict[str, Any]:
        """Get constraints for object parameters."""
        constraints = {}
        
        # Coordinate constraints
        if param_name in ["point", "point1", "point2"]:
            constraints["properties"] = {
                "x": {"type": "number"},
                "y": {"type": "number"}
            }
            constraints["required"] = ["x", "y"]
            constraints["additionalProperties"] = False
        
        if param_name in ["point3d", "point1_3d", "point2_3d"]:
            constraints["properties"] = {
                "x": {"type": "number"},
                "y": {"type": "number"},
                "z": {"type": "number"}
            }
            constraints["required"] = ["x", "y", "z"]
            constraints["additionalProperties"] = False
        
        return constraints
    
    def _add_mathematical_constraints(self, schema: Dict[str, Any], function_name: str) -> None:
        """Add mathematical constraints to the schema."""
        if function_name in self.mathematical_constraints:
            func_constraints = self.mathematical_constraints[function_name]
            
            # Add constraints to properties
            for param_name, constraints in func_constraints.items():
                if param_name in schema["properties"]:
                    schema["properties"][param_name].update(constraints)
    
    def generate_all_schemas(self, tools: Dict[str, MCPToolMetadata]) -> Dict[str, Dict[str, Any]]:
        """Generate schemas for all tools."""
        schemas = {}
        
        logger.info(f"Generating schemas for {len(tools)} tools...")
        
        for name, metadata in tools.items():
            try:
                schema = self.generate_schema(metadata)
                schemas[name] = schema
                logger.debug(f"Generated schema for {name}")
            except Exception as e:
                logger.error(f"Failed to generate schema for {name}: {e}")
        
        logger.info(f"Generated {len(schemas)} schemas")
        return schemas


class SchemaValidator:
    """Validates input data against JSON schemas."""
    
    def __init__(self, schemas: Dict[str, Dict[str, Any]]):
        self.schemas = schemas
    
    def validate(self, tool_name: str, data: Dict[str, Any]) -> List[ValidationError]:
        """Validate data against the schema for a specific tool."""
        if tool_name not in self.schemas:
            return [ValidationError("tool", f"Unknown tool: {tool_name}")]
        
        schema = self.schemas[tool_name]
        errors = []
        
        # Validate required fields
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in data:
                errors.append(ValidationError(field, f"Required field '{field}' is missing"))
        
        # Validate each field in data
        properties = schema.get("properties", {})
        for field, value in data.items():
            if field in properties:
                field_errors = self._validate_field(field, value, properties[field])
                errors.extend(field_errors)
            elif not schema.get("additionalProperties", True):
                errors.append(ValidationError(field, f"Additional field '{field}' is not allowed"))
        
        return errors
    
    def _validate_field(self, field_name: str, value: Any, field_schema: Dict[str, Any]) -> List[ValidationError]:
        """Validate a single field."""
        errors = []
        
        # Check type
        expected_type = field_schema.get("type")
        if expected_type and not self._check_type(value, expected_type):
            errors.append(ValidationError(
                field_name, 
                f"Expected type {expected_type}, got {type(value).__name__}",
                value
            ))
            return errors  # Skip further validation if type is wrong
        
        # Check constraints based on type
        if expected_type == "number" or expected_type == "integer":
            errors.extend(self._validate_number(field_name, value, field_schema))
        elif expected_type == "string":
            errors.extend(self._validate_string(field_name, value, field_schema))
        elif expected_type == "array":
            errors.extend(self._validate_array(field_name, value, field_schema))
        elif expected_type == "object":
            errors.extend(self._validate_object(field_name, value, field_schema))
        
        return errors
    
    def _check_type(self, value: Any, expected_type: str) -> bool:
        """Check if value matches expected type."""
        type_mapping = {
            "number": (int, float),
            "integer": int,
            "string": str,
            "boolean": bool,
            "array": (list, tuple),
            "object": dict
        }
        
        expected_python_type = type_mapping.get(expected_type)
        if expected_python_type:
            return isinstance(value, expected_python_type)
        
        return True
    
    def _validate_number(self, field_name: str, value: Union[int, float], schema: Dict[str, Any]) -> List[ValidationError]:
        """Validate number constraints."""
        errors = []
        
        # Check minimum
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(ValidationError(
                field_name,
                f"Value {value} is below minimum {schema['minimum']}",
                value
            ))
        
        # Check maximum
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(ValidationError(
                field_name,
                f"Value {value} is above maximum {schema['maximum']}",
                value
            ))
        
        # Check exclusiveMinimum
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            errors.append(ValidationError(
                field_name,
                f"Value {value} must be greater than {schema['exclusiveMinimum']}",
                value
            ))
        
        # Check exclusiveMaximum
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            errors.append(ValidationError(
                field_name,
                f"Value {value} must be less than {schema['exclusiveMaximum']}",
                value
            ))
        
        return errors
    
    def _validate_string(self, field_name: str, value: str, schema: Dict[str, Any]) -> List[ValidationError]:
        """Validate string constraints."""
        errors = []
        
        # Check minLength
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(ValidationError(
                field_name,
                f"String length {len(value)} is below minimum {schema['minLength']}",
                value
            ))
        
        # Check maxLength
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(ValidationError(
                field_name,
                f"String length {len(value)} is above maximum {schema['maxLength']}",
                value
            ))
        
        # Check pattern
        if "pattern" in schema:
            import re
            if not re.match(schema["pattern"], value):
                errors.append(ValidationError(
                    field_name,
                    f"String does not match required pattern: {schema['pattern']}",
                    value
                ))
        
        return errors
    
    def _validate_array(self, field_name: str, value: List[Any], schema: Dict[str, Any]) -> List[ValidationError]:
        """Validate array constraints."""
        errors = []
        
        # Check minItems
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(ValidationError(
                field_name,
                f"Array length {len(value)} is below minimum {schema['minItems']}",
                value
            ))
        
        # Check maxItems
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(ValidationError(
                field_name,
                f"Array length {len(value)} is above maximum {schema['maxItems']}",
                value
            ))
        
        # Check items
        if "items" in schema:
            item_schema = schema["items"]
            for i, item in enumerate(value):
                item_errors = self._validate_field(f"{field_name}[{i}]", item, item_schema)
                errors.extend(item_errors)
        
        return errors
    
    def _validate_object(self, field_name: str, value: Dict[str, Any], schema: Dict[str, Any]) -> List[ValidationError]:
        """Validate object constraints."""
        errors = []
        
        # Check required properties
        if "required" in schema:
            for required_prop in schema["required"]:
                if required_prop not in value:
                    errors.append(ValidationError(
                        f"{field_name}.{required_prop}",
                        f"Required property '{required_prop}' is missing",
                        value
                    ))
        
        # Check properties
        if "properties" in schema:
            for prop_name, prop_value in value.items():
                if prop_name in schema["properties"]:
                    prop_schema = schema["properties"][prop_name]
                    prop_errors = self._validate_field(f"{field_name}.{prop_name}", prop_value, prop_schema)
                    errors.extend(prop_errors)
                elif not schema.get("additionalProperties", True):
                    errors.append(ValidationError(
                        f"{field_name}.{prop_name}",
                        f"Additional property '{prop_name}' is not allowed",
                        value
                    ))
        
        return errors
    
    def is_valid(self, tool_name: str, data: Dict[str, Any]) -> bool:
        """Check if data is valid for a specific tool."""
        errors = self.validate(tool_name, data)
        return len(errors) == 0
    
    def get_validation_errors_message(self, errors: List[ValidationError]) -> str:
        """Get a formatted error message from validation errors."""
        if not errors:
            return "No validation errors"
        
        messages = []
        for error in errors:
            if error.value is not None:
                messages.append(f"{error.field}: {error.message} (value: {error.value})")
            else:
                messages.append(f"{error.field}: {error.message}")
        
        return "; ".join(messages)


class ValidationMiddleware:
    """Middleware for validating MCP requests."""
    
    def __init__(self, validator: SchemaValidator):
        self.validator = validator
    
    async def validate_request(self, tool_name: str, parameters: Dict[str, Any]) -> Optional[str]:
        """Validate MCP request parameters."""
        errors = self.validator.validate(tool_name, parameters)
        
        if errors:
            error_message = self.validator.get_validation_errors_message(errors)
            logger.warning(f"Validation failed for {tool_name}: {error_message}")
            return error_message
        
        logger.debug(f"Validation passed for {tool_name}")
        return None

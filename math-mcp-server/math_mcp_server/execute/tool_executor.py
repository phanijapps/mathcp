"""Tool executor for mathematical functions."""

import logging
import inspect
import time
import asyncio
from typing import Any, Dict, Optional, Union, List
from dataclasses import dataclass
import traceback

import mathgenius.api.dispatcher as math_dispatcher
from ..config import config


logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result from tool execution."""
    
    success: bool
    result: Any
    tool_name: str
    parameters: Dict[str, Any]
    execution_time: float
    timestamp: float
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ToolExecutor:
    """Executor for mathematical tools with parameter validation and error handling."""
    
    def __init__(self):
        """Initialize the tool executor."""
        self._available_tools = self._get_available_tools()
        self._parameter_validators = self._setup_parameter_validators()
        
    def _get_available_tools(self) -> Dict[str, Any]:
        """Get all available mathematical tools from dispatcher."""
        tools = {}
        
        for func_name in math_dispatcher.__all__:
            try:
                func_obj = getattr(math_dispatcher, func_name)
                tools[func_name] = func_obj
            except Exception as e:
                logger.error(f"Failed to load tool {func_name}: {e}")
                
        logger.info(f"Loaded {len(tools)} mathematical tools")
        return tools
    
    def _setup_parameter_validators(self) -> Dict[str, Dict[str, Any]]:
        """Setup parameter validation rules for mathematical functions."""
        validators = {}
        
        # Define specific validation rules for known functions
        validation_rules = {
            "divide": {
                "b": {"not_zero": True, "type": [int, float]}
            },
            "power": {
                "base": {"type": [int, float]},
                "exponent": {"type": [int, float]}
            },
            "triangle_area": {
                "base": {"positive": True, "type": [int, float]},
                "height": {"positive": True, "type": [int, float]}
            },
            "circle_area": {
                "radius": {"positive": True, "type": [int, float]}
            },
            "distance_2d": {
                "point1": {"type": [list, tuple], "length": 2},
                "point2": {"type": [list, tuple], "length": 2}
            },
            "sin": {
                "angle": {"type": [int, float]}
            },
            "cos": {
                "angle": {"type": [int, float]}
            },
            "matrix_multiply": {
                "matrix1": {"type": [list]},
                "matrix2": {"type": [list]}
            }
        }
        
        return validation_rules
    
    async def execute_tool(
        self, 
        tool_name: str, 
        parameters: Dict[str, Any],
        timeout: Optional[float] = None
    ) -> ExecutionResult:
        """Execute a mathematical tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters to pass to the tool
            timeout: Execution timeout in seconds
            
        Returns:
            ExecutionResult with success status, result, and metadata
        """
        start_time = time.time()
        timestamp = time.time()
        
        # Set default timeout
        if timeout is None:
            timeout = config.execution_timeout
            
        try:
            # Validate tool exists
            if tool_name not in self._available_tools:
                return ExecutionResult(
                    success=False,
                    result=None,
                    tool_name=tool_name,
                    parameters=parameters,
                    execution_time=0.0,
                    timestamp=timestamp,
                    error_message=f"Tool '{tool_name}' not found",
                    error_type="ToolNotFoundError"
                )
            
            # Get the function
            func = self._available_tools[tool_name]
            
            # Validate parameters
            validation_result = self._validate_parameters(tool_name, func, parameters)
            if not validation_result["valid"]:
                return ExecutionResult(
                    success=False,
                    result=None,
                    tool_name=tool_name,
                    parameters=parameters,
                    execution_time=time.time() - start_time,
                    timestamp=timestamp,
                    error_message=validation_result["error"],
                    error_type="ParameterValidationError"
                )
            
            # Execute with timeout
            if config.log_execution_requests:
                logger.info(f"Executing {tool_name} with parameters: {parameters}")
            
            # Execute the function with timeout protection
            try:
                result = await asyncio.wait_for(
                    self._execute_function(func, validation_result["validated_params"]),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                return ExecutionResult(
                    success=False,
                    result=None,
                    tool_name=tool_name,
                    parameters=parameters,
                    execution_time=timeout,
                    timestamp=timestamp,
                    error_message=f"Execution timeout after {timeout} seconds",
                    error_type="TimeoutError"
                )
            
            execution_time = time.time() - start_time
            
            # Log successful execution
            if config.log_execution_requests:
                logger.info(f"Successfully executed {tool_name} in {execution_time:.3f}s")
            
            return ExecutionResult(
                success=True,
                result=result,
                tool_name=tool_name,
                parameters=parameters,
                execution_time=execution_time,
                timestamp=timestamp,
                metadata={
                    "function_signature": str(inspect.signature(func)),
                    "result_type": type(result).__name__
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_message = str(e)
            error_type = type(e).__name__
            
            logger.error(f"Tool execution failed for {tool_name}: {error_message}")
            logger.debug(f"Full traceback: {traceback.format_exc()}")
            
            return ExecutionResult(
                success=False,
                result=None,
                tool_name=tool_name,
                parameters=parameters,
                execution_time=execution_time,
                timestamp=timestamp,
                error_message=error_message,
                error_type=error_type
            )
    
    async def _execute_function(self, func: Any, parameters: Dict[str, Any]) -> Any:
        """Execute a function with validated parameters."""
        # Check if function is async
        if inspect.iscoroutinefunction(func):
            return await func(**parameters)
        else:
            # Run sync function in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: func(**parameters))
    
    def _validate_parameters(
        self, 
        tool_name: str, 
        func: Any, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate parameters for a mathematical function.
        
        Returns:
            Dictionary with validation result and validated parameters
        """
        try:
            # Get function signature
            sig = inspect.signature(func)
            
            # Check for required parameters
            validated_params = {}
            
            for param_name, param in sig.parameters.items():
                # Check if parameter is provided
                if param_name in parameters:
                    param_value = parameters[param_name]
                    
                    # Apply type conversion if needed
                    converted_value = self._convert_parameter_type(param_value, param)
                    
                    # Apply specific validation rules
                    validation_error = self._apply_validation_rules(
                        tool_name, param_name, converted_value
                    )
                    if validation_error:
                        return {"valid": False, "error": validation_error}
                    
                    validated_params[param_name] = converted_value
                    
                elif param.default == inspect.Parameter.empty:
                    # Required parameter is missing
                    return {
                        "valid": False, 
                        "error": f"Required parameter '{param_name}' is missing"
                    }
            
            # Check for extra parameters
            extra_params = set(parameters.keys()) - set(sig.parameters.keys())
            if extra_params:
                logger.warning(f"Ignoring extra parameters for {tool_name}: {extra_params}")
            
            return {"valid": True, "validated_params": validated_params}
            
        except Exception as e:
            return {"valid": False, "error": f"Parameter validation failed: {str(e)}"}
    
    def _convert_parameter_type(self, value: Any, param: inspect.Parameter) -> Any:
        """Convert parameter value to expected type."""
        # If parameter has type annotation, try to convert
        if param.annotation != inspect.Parameter.empty:
            expected_type = param.annotation
            
            # Handle Union types (e.g., Union[int, float])
            if hasattr(expected_type, '__origin__') and expected_type.__origin__ is Union:
                # Try each type in the Union
                for union_type in expected_type.__args__:
                    try:
                        return union_type(value)
                    except (ValueError, TypeError):
                        continue
                # If no conversion worked, return original value
                return value
            
            # Handle basic type conversions
            try:
                if expected_type in [int, float, str, bool]:
                    return expected_type(value)
                elif expected_type in [list, tuple]:
                    if isinstance(value, (list, tuple)):
                        return expected_type(value)
                    else:
                        # Try to convert string representation to list
                        if isinstance(value, str):
                            import ast
                            return expected_type(ast.literal_eval(value))
            except (ValueError, TypeError, SyntaxError):
                # If conversion fails, return original value
                pass
        
        return value
    
    def _apply_validation_rules(
        self, 
        tool_name: str, 
        param_name: str, 
        value: Any
    ) -> Optional[str]:
        """Apply specific validation rules for parameters.
        
        Returns:
            Error message if validation fails, None if validation passes
        """
        # Get validation rules for this tool and parameter
        tool_rules = self._parameter_validators.get(tool_name, {})
        param_rules = tool_rules.get(param_name, {})
        
        if not param_rules:
            return None  # No specific rules, validation passes
        
        # Check type constraints
        if "type" in param_rules:
            expected_types = param_rules["type"]
            if not isinstance(expected_types, list):
                expected_types = [expected_types]
            
            if not any(isinstance(value, t) for t in expected_types):
                type_names = [t.__name__ for t in expected_types]
                return f"Parameter '{param_name}' must be one of types: {type_names}"
        
        # Check positive constraint
        if param_rules.get("positive", False):
            if isinstance(value, (int, float)) and value <= 0:
                return f"Parameter '{param_name}' must be positive"
        
        # Check not_zero constraint
        if param_rules.get("not_zero", False):
            if isinstance(value, (int, float)) and value == 0:
                return f"Parameter '{param_name}' cannot be zero"
        
        # Check length constraint
        if "length" in param_rules:
            expected_length = param_rules["length"]
            if hasattr(value, '__len__') and len(value) != expected_length:
                return f"Parameter '{param_name}' must have length {expected_length}"
        
        # Check range constraints
        if "min" in param_rules:
            if isinstance(value, (int, float)) and value < param_rules["min"]:
                return f"Parameter '{param_name}' must be >= {param_rules['min']}"
        
        if "max" in param_rules:
            if isinstance(value, (int, float)) and value > param_rules["max"]:
                return f"Parameter '{param_name}' must be <= {param_rules['max']}"
        
        return None  # All validations passed
    
    def get_tool_signature(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get the signature and documentation for a tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Dictionary with tool signature information
        """
        if tool_name not in self._available_tools:
            return None
        
        func = self._available_tools[tool_name]
        sig = inspect.signature(func)
        doc = inspect.getdoc(func)
        
        # Extract parameter information
        parameters = {}
        for param_name, param in sig.parameters.items():
            param_info = {
                "name": param_name,
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                "required": param.default == inspect.Parameter.empty,
                "default": param.default if param.default != inspect.Parameter.empty else None
            }
            parameters[param_name] = param_info
        
        return {
            "name": tool_name,
            "signature": str(sig),
            "docstring": doc,
            "parameters": parameters,
            "validation_rules": self._parameter_validators.get(tool_name, {})
        }
    
    def get_available_tools(self) -> List[str]:
        """Get list of all available tool names.
        
        Returns:
            List of tool names
        """
        return list(self._available_tools.keys())
    
    def get_tool_count(self) -> int:
        """Get the number of available tools.
        
        Returns:
            Number of available tools
        """
        return len(self._available_tools)

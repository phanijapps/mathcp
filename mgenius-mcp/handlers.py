"""MCP request handlers for mathematical operations."""

import asyncio
import logging
import json
from typing import Dict, Any, Optional, List, Callable, Union
from dataclasses import dataclass
from datetime import datetime
import traceback

from .tools import ToolRegistry, MCPToolMetadata, ToolCategory
from .schema_validation import SchemaValidator, ValidationMiddleware

logger = logging.getLogger(__name__)


@dataclass
class MCPRequest:
    """Represents an MCP request."""
    tool_name: str
    parameters: Dict[str, Any]
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None


@dataclass
class MCPResponse:
    """Represents an MCP response."""
    success: bool
    result: Any = None
    error: Optional[str] = None
    request_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    execution_time: Optional[float] = None


class MCPToolHandler:
    """Handler for individual MCP tools."""
    
    def __init__(self, metadata: MCPToolMetadata):
        self.metadata = metadata
        self.function = metadata.function
        self.name = metadata.name
        self.category = metadata.category
        self.call_count = 0
        self.total_execution_time = 0.0
    
    async def execute(self, parameters: Dict[str, Any]) -> MCPResponse:
        """Execute the mathematical function with given parameters."""
        start_time = datetime.now()
        
        try:
            # Validate parameters match function signature
            validated_params = self._validate_and_prepare_parameters(parameters)
            
            # Execute the function
            if asyncio.iscoroutinefunction(self.function):
                result = await self.function(**validated_params)
            else:
                # Run synchronous function in thread pool to avoid blocking
                result = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: self.function(**validated_params)
                )
            
            # Convert result to JSON-serializable format
            serialized_result = self._serialize_result(result)
            
            # Update statistics
            execution_time = (datetime.now() - start_time).total_seconds()
            self.call_count += 1
            self.total_execution_time += execution_time
            
            return MCPResponse(
                success=True,
                result=serialized_result,
                timestamp=datetime.now(),
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Error executing {self.name}: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            
            return MCPResponse(
                success=False,
                error=str(e),
                timestamp=datetime.now(),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    def _validate_and_prepare_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and prepare parameters for function execution."""
        validated_params = {}
        
        # Check required parameters
        for param_name, param_info in self.metadata.parameters.items():
            if param_info.get("required", False) and param_name not in parameters:
                raise ValueError(f"Required parameter '{param_name}' is missing")
        
        # Prepare parameters
        for param_name, param_info in self.metadata.parameters.items():
            if param_name in parameters:
                value = parameters[param_name]
                # Convert and validate parameter
                converted_value = self._convert_parameter(param_name, value, param_info)
                validated_params[param_name] = converted_value
            elif "default" in param_info:
                validated_params[param_name] = param_info["default"]
        
        return validated_params
    
    def _convert_parameter(self, param_name: str, value: Any, param_info: Dict[str, Any]) -> Any:
        """Convert parameter to appropriate type."""
        param_type = param_info.get("type", "string")
        
        try:
            if param_type == "integer":
                return int(value)
            elif param_type == "number":
                return float(value)
            elif param_type == "string":
                return str(value)
            elif param_type == "boolean":
                if isinstance(value, bool):
                    return value
                elif isinstance(value, str):
                    return value.lower() in ("true", "1", "yes", "on")
                else:
                    return bool(value)
            elif param_type == "array":
                if isinstance(value, (list, tuple)):
                    return list(value)
                else:
                    raise ValueError(f"Parameter '{param_name}' must be an array")
            elif param_type == "object":
                if isinstance(value, dict):
                    return value
                else:
                    raise ValueError(f"Parameter '{param_name}' must be an object")
            else:
                return value
        except (ValueError, TypeError) as e:
            raise ValueError(f"Cannot convert parameter '{param_name}' to {param_type}: {e}")
    
    def _serialize_result(self, result: Any) -> Any:
        """Serialize result to JSON-compatible format."""
        if result is None:
            return None
        
        # Handle basic types
        if isinstance(result, (int, float, str, bool)):
            return result
        
        # Handle lists and tuples
        if isinstance(result, (list, tuple)):
            return [self._serialize_result(item) for item in result]
        
        # Handle dictionaries
        if isinstance(result, dict):
            return {key: self._serialize_result(value) for key, value in result.items()}
        
        # Handle NumPy arrays (if present)
        if hasattr(result, "tolist"):
            return result.tolist()
        
        # Handle complex numbers
        if isinstance(result, complex):
            return {"real": result.real, "imag": result.imag}
        
        # Handle SymPy expressions (if present)
        if hasattr(result, "evalf"):
            try:
                return str(result)
            except:
                pass
        
        # Handle other objects by converting to string
        try:
            return str(result)
        except:
            return f"<{type(result).__name__} object>"
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics for this tool."""
        return {
            "name": self.name,
            "category": self.category.value,
            "call_count": self.call_count,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": (
                self.total_execution_time / self.call_count if self.call_count > 0 else 0
            )
        }


class MCPHandlerRegistry:
    """Registry for MCP tool handlers."""
    
    def __init__(self):
        self.handlers: Dict[str, MCPToolHandler] = {}
        self.tool_registry = ToolRegistry()
        self.validator: Optional[SchemaValidator] = None
        self.validation_middleware: Optional[ValidationMiddleware] = None
    
    def register_all_handlers(self, enabled_categories: Optional[List[ToolCategory]] = None) -> int:
        """Register all mathematical tool handlers."""
        logger.info("Registering MCP tool handlers...")
        
        # Register tools in the tool registry
        tool_count = self.tool_registry.register_tools(enabled_categories)
        
        # Create handlers for each tool
        discovered_tools = self.tool_registry.discovery.discovered_tools
        
        for name, metadata in discovered_tools.items():
            handler = MCPToolHandler(metadata)
            self.handlers[name] = handler
            logger.debug(f"Registered handler for {name}")
        
        logger.info(f"Registered {len(self.handlers)} MCP tool handlers")
        return len(self.handlers)
    
    def set_validator(self, validator: SchemaValidator) -> None:
        """Set the schema validator."""
        self.validator = validator
        self.validation_middleware = ValidationMiddleware(validator)
    
    async def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle an MCP request."""
        logger.debug(f"Handling request for tool: {request.tool_name}")
        
        # Check if handler exists
        if request.tool_name not in self.handlers:
            return MCPResponse(
                success=False,
                error=f"Unknown tool: {request.tool_name}",
                request_id=request.request_id,
                timestamp=datetime.now()
            )
        
        # Validate request parameters
        if self.validation_middleware:
            validation_error = await self.validation_middleware.validate_request(
                request.tool_name, request.parameters
            )
            if validation_error:
                return MCPResponse(
                    success=False,
                    error=f"Validation error: {validation_error}",
                    request_id=request.request_id,
                    timestamp=datetime.now()
                )
        
        # Execute the tool
        handler = self.handlers[request.tool_name]
        response = await handler.execute(request.parameters)
        
        # Set request ID if provided
        response.request_id = request.request_id
        
        return response
    
    def get_handler(self, tool_name: str) -> Optional[MCPToolHandler]:
        """Get a handler by tool name."""
        return self.handlers.get(tool_name)
    
    def get_all_handlers(self) -> Dict[str, MCPToolHandler]:
        """Get all registered handlers."""
        return self.handlers.copy()
    
    def get_handler_statistics(self) -> Dict[str, Any]:
        """Get statistics for all handlers."""
        return {
            name: handler.get_statistics()
            for name, handler in self.handlers.items()
        }
    
    def get_tools_by_category(self, category: ToolCategory) -> List[str]:
        """Get tool names by category."""
        return [
            name for name, handler in self.handlers.items()
            if handler.category == category
        ]
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """Get information about all tools."""
        return [
            {
                "name": name,
                "description": handler.metadata.description,
                "category": handler.category.value,
                "parameters": handler.metadata.parameters,
                "call_count": handler.call_count,
                "average_execution_time": (
                    handler.total_execution_time / handler.call_count 
                    if handler.call_count > 0 else 0
                )
            }
            for name, handler in self.handlers.items()
        ]


class MCPRequestRouter:
    """Router for MCP requests."""
    
    def __init__(self, handler_registry: MCPHandlerRegistry):
        self.handler_registry = handler_registry
        self.request_count = 0
        self.error_count = 0
    
    async def route_request(self, tool_name: str, parameters: Dict[str, Any], request_id: Optional[str] = None) -> MCPResponse:
        """Route an MCP request to the appropriate handler."""
        self.request_count += 1
        
        # Create request object
        request = MCPRequest(
            tool_name=tool_name,
            parameters=parameters,
            request_id=request_id,
            timestamp=datetime.now()
        )
        
        # Handle the request
        response = await self.handler_registry.handle_request(request)
        
        # Update error count
        if not response.success:
            self.error_count += 1
        
        return response
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing statistics."""
        return {
            "total_requests": self.request_count,
            "error_count": self.error_count,
            "success_rate": (
                (self.request_count - self.error_count) / self.request_count 
                if self.request_count > 0 else 0
            )
        }


class MCPBatchHandler:
    """Handler for batch MCP requests."""
    
    def __init__(self, router: MCPRequestRouter):
        self.router = router
    
    async def handle_batch(self, requests: List[Dict[str, Any]]) -> List[MCPResponse]:
        """Handle multiple MCP requests in parallel."""
        logger.info(f"Processing batch of {len(requests)} requests")
        
        # Create tasks for all requests
        tasks = []
        for i, request_data in enumerate(requests):
            tool_name = request_data.get("tool_name", "")
            parameters = request_data.get("parameters", {})
            request_id = request_data.get("request_id", f"batch_{i}")
            
            task = self.router.route_request(tool_name, parameters, request_id)
            tasks.append(task)
        
        # Execute all requests in parallel
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_responses = []
        for i, response in enumerate(responses):
            if isinstance(response, Exception):
                processed_responses.append(MCPResponse(
                    success=False,
                    error=str(response),
                    request_id=f"batch_{i}",
                    timestamp=datetime.now()
                ))
            else:
                processed_responses.append(response)
        
        return processed_responses


# Helper functions for creating MCP responses
def create_success_response(result: Any, request_id: Optional[str] = None, execution_time: Optional[float] = None) -> Dict[str, Any]:
    """Create a successful MCP response."""
    return {
        "success": True,
        "result": result,
        "request_id": request_id,
        "timestamp": datetime.now().isoformat(),
        "execution_time": execution_time
    }


def create_error_response(error: str, request_id: Optional[str] = None) -> Dict[str, Any]:
    """Create an error MCP response."""
    return {
        "success": False,
        "error": error,
        "request_id": request_id,
        "timestamp": datetime.now().isoformat()
    }


def create_validation_error_response(validation_errors: List[str], request_id: Optional[str] = None) -> Dict[str, Any]:
    """Create a validation error MCP response."""
    return {
        "success": False,
        "error": f"Validation errors: {'; '.join(validation_errors)}",
        "request_id": request_id,
        "timestamp": datetime.now().isoformat()
    }

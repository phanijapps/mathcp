"""Test suite for MCP server components."""

import pytest
import asyncio
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to sys.path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mgenius_mcp.config import MCPConfig
from mgenius_mcp.tools import ToolDiscovery, ToolRegistry, ToolCategory
from mgenius_mcp.schema_validation import SchemaGenerator, SchemaValidator
from mgenius_mcp.error_handling import ErrorHandler, ErrorType, MathematicalError
from mgenius_mcp.handlers import MCPHandlerRegistry, MCPRequest, MCPResponse


class TestMCPConfig:
    """Test MCP configuration."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = MCPConfig()
        
        assert config.host == "localhost"
        assert config.port == 8000
        assert config.debug is False
        assert config.protocol_version == "1.0"
        assert config.server_name == "mgenius-mcp"
        assert config.precision == 15
        assert config.enable_arithmetic is True
        assert config.enable_algebra is True
    
    def test_from_env(self):
        """Test configuration from environment variables."""
        with patch.dict(os.environ, {
            'MCP_HOST': 'test-host',
            'MCP_PORT': '9000',
            'MCP_DEBUG': 'true',
            'MCP_ENABLE_ARITHMETIC': 'false'
        }):
            config = MCPConfig.from_env()
            
            assert config.host == "test-host"
            assert config.port == 9000
            assert config.debug is True
            assert config.enable_arithmetic is False
    
    def test_get_enabled_tools(self):
        """Test getting enabled tools."""
        config = MCPConfig(
            enable_arithmetic=True,
            enable_algebra=False,
            enable_geometry=True
        )
        
        enabled_tools = config.get_enabled_tools()
        
        assert enabled_tools["arithmetic"] is True
        assert enabled_tools["algebra"] is False
        assert enabled_tools["geometry"] is True


class TestToolDiscovery:
    """Test tool discovery system."""
    
    def test_discovery_initialization(self):
        """Test tool discovery initialization."""
        discovery = ToolDiscovery()
        
        assert len(discovery.category_mapping) > 0
        assert "add" in discovery.category_mapping
        assert discovery.category_mapping["add"] == ToolCategory.ARITHMETIC
    
    def test_discover_tools(self):
        """Test tool discovery."""
        discovery = ToolDiscovery()
        
        # Mock the dispatcher module
        with patch('mgenius_mcp.tools.dispatcher') as mock_dispatcher:
            mock_dispatcher.__all__ = ["add", "subtract", "sin", "cos"]
            
            # Mock functions
            mock_add = Mock()
            mock_add.__doc__ = "Add two numbers"
            mock_add.__name__ = "add"
            
            mock_subtract = Mock()
            mock_subtract.__doc__ = "Subtract two numbers"
            mock_subtract.__name__ = "subtract"
            
            mock_sin = Mock()
            mock_sin.__doc__ = "Calculate sine"
            mock_sin.__name__ = "sin"
            
            mock_cos = Mock()
            mock_cos.__doc__ = "Calculate cosine"
            mock_cos.__name__ = "cos"
            
            mock_dispatcher.add = mock_add
            mock_dispatcher.subtract = mock_subtract
            mock_dispatcher.sin = mock_sin
            mock_dispatcher.cos = mock_cos
            
            # Mock inspect.signature
            with patch('inspect.signature') as mock_signature:
                mock_signature.return_value.parameters = {}
                
                discovered_tools = discovery.discover_tools()
                
                assert len(discovered_tools) == 4
                assert "add" in discovered_tools
                assert "subtract" in discovered_tools
                assert "sin" in discovered_tools
                assert "cos" in discovered_tools
                
                assert discovered_tools["add"].category == ToolCategory.ARITHMETIC
                assert discovered_tools["sin"].category == ToolCategory.TRIGONOMETRY
    
    def test_get_tools_by_category(self):
        """Test getting tools by category."""
        discovery = ToolDiscovery()
        
        # Add some mock tools
        from mgenius_mcp.tools import MCPToolMetadata
        discovery.discovered_tools = {
            "add": MCPToolMetadata("add", "Add", ToolCategory.ARITHMETIC, Mock(), {}),
            "sin": MCPToolMetadata("sin", "Sine", ToolCategory.TRIGONOMETRY, Mock(), {}),
            "cos": MCPToolMetadata("cos", "Cosine", ToolCategory.TRIGONOMETRY, Mock(), {})
        }
        
        arithmetic_tools = discovery.get_tools_by_category(ToolCategory.ARITHMETIC)
        trig_tools = discovery.get_tools_by_category(ToolCategory.TRIGONOMETRY)
        
        assert len(arithmetic_tools) == 1
        assert len(trig_tools) == 2
        assert "add" in arithmetic_tools
        assert "sin" in trig_tools
        assert "cos" in trig_tools


class TestSchemaGenerator:
    """Test JSON schema generation."""
    
    def test_schema_generator_initialization(self):
        """Test schema generator initialization."""
        generator = SchemaGenerator()
        
        assert len(generator.mathematical_constraints) > 0
        assert "radius" in generator.mathematical_constraints
        assert generator.mathematical_constraints["radius"].minimum == 0
    
    def test_generate_schema(self):
        """Test schema generation for a function."""
        generator = SchemaGenerator()
        
        # Mock function
        def mock_add(a: int, b: int) -> int:
            """Add two integers."""
            return a + b
        
        schema = generator.generate_schema("add", mock_add)
        
        assert schema["type"] == "object"
        assert schema["title"] == "add Parameters"
        assert "properties" in schema
        assert "a" in schema["properties"]
        assert "b" in schema["properties"]
        assert schema["properties"]["a"]["type"] == "integer"
        assert schema["properties"]["b"]["type"] == "integer"
        assert schema["required"] == ["a", "b"]
    
    def test_parameter_constraints(self):
        """Test parameter constraint application."""
        generator = SchemaGenerator()
        
        # Mock function with radius parameter
        def mock_circle_area(radius: float) -> float:
            """Calculate circle area."""
            return 3.14159 * radius * radius
        
        schema = generator.generate_schema("circle_area", mock_circle_area)
        
        assert "radius" in schema["properties"]
        radius_schema = schema["properties"]["radius"]
        assert radius_schema["type"] == "number"
        assert "exclusiveMinimum" in radius_schema
        assert radius_schema["exclusiveMinimum"] == 0


class TestSchemaValidator:
    """Test JSON schema validation."""
    
    def test_validator_initialization(self):
        """Test validator initialization."""
        validator = SchemaValidator()
        
        assert len(validator.schemas) == 0
    
    def test_register_schema(self):
        """Test schema registration."""
        validator = SchemaValidator()
        
        schema = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
        
        validator.register_schema("add", schema)
        
        assert "add" in validator.schemas
        assert validator.schemas["add"] == schema
    
    def test_validate_valid_parameters(self):
        """Test validation with valid parameters."""
        validator = SchemaValidator()
        
        schema = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
        
        validator.register_schema("add", schema)
        
        errors = validator.validate("add", {"a": 5, "b": 3})
        
        assert len(errors) == 0
    
    def test_validate_invalid_parameters(self):
        """Test validation with invalid parameters."""
        validator = SchemaValidator()
        
        schema = {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
        
        validator.register_schema("add", schema)
        
        # Missing required parameter
        errors = validator.validate("add", {"a": 5})
        assert len(errors) == 1
        assert "Required parameter 'b' is missing" in errors[0]
        
        # Wrong type
        errors = validator.validate("add", {"a": "hello", "b": 3})
        assert len(errors) == 1
        assert "must be of type integer" in errors[0]


class TestErrorHandler:
    """Test error handling."""
    
    def test_error_handler_initialization(self):
        """Test error handler initialization."""
        handler = ErrorHandler()
        
        assert handler.max_computation_time == 30
        assert len(handler.error_patterns) > 0
        assert "division by zero" in handler.error_patterns
    
    def test_classify_error(self):
        """Test error classification."""
        handler = ErrorHandler()
        
        # Test division by zero
        zero_div_error = ZeroDivisionError("division by zero")
        error_type = handler.classify_error(zero_div_error)
        assert error_type == ErrorType.DOMAIN_ERROR
        
        # Test value error
        value_error = ValueError("invalid parameter")
        error_type = handler.classify_error(value_error)
        assert error_type == ErrorType.PARAMETER_ERROR
        
        # Test overflow error
        overflow_error = OverflowError("math range error")
        error_type = handler.classify_error(overflow_error)
        assert error_type == ErrorType.PRECISION_ERROR
    
    def test_handle_error(self):
        """Test error handling."""
        handler = ErrorHandler()
        
        from mgenius_mcp.error_handling import ErrorContext
        
        context = ErrorContext(
            tool_name="divide",
            parameters={"a": 10, "b": 0},
            error_type=ErrorType.DOMAIN_ERROR
        )
        
        error = ZeroDivisionError("division by zero")
        response = handler.handle_error(error, context)
        
        assert response["success"] is False
        assert "error" in response
        assert response["error"]["type"] == ErrorType.DOMAIN_ERROR.value
        assert "divide" in response["error"]["message"]


class TestMCPHandlerRegistry:
    """Test MCP handler registry."""
    
    def test_registry_initialization(self):
        """Test registry initialization."""
        registry = MCPHandlerRegistry()
        
        assert len(registry.handlers) == 0
        assert registry.tool_registry is not None
    
    @pytest.mark.asyncio
    async def test_handle_request(self):
        """Test request handling."""
        registry = MCPHandlerRegistry()
        
        # Mock a simple handler
        from mgenius_mcp.handlers import MCPToolHandler
        from mgenius_mcp.tools import MCPToolMetadata
        
        mock_function = Mock(return_value=8)
        metadata = MCPToolMetadata(
            name="add",
            description="Add two numbers",
            category=ToolCategory.ARITHMETIC,
            function=mock_function,
            parameters={
                "a": {"type": "integer", "required": True},
                "b": {"type": "integer", "required": True}
            }
        )
        
        handler = MCPToolHandler(metadata)
        registry.handlers["add"] = handler
        
        request = MCPRequest(
            tool_name="add",
            parameters={"a": 5, "b": 3},
            request_id="test_req"
        )
        
        response = await registry.handle_request(request)
        
        assert response.success is True
        assert response.result == 8
        assert response.request_id == "test_req"


def test_imports():
    """Test that all modules can be imported."""
    try:
        from mgenius_mcp import MCPConfig, MCPServer
        from mgenius_mcp.tools import ToolDiscovery, ToolRegistry
        from mgenius_mcp.schema_validation import SchemaGenerator, SchemaValidator
        from mgenius_mcp.error_handling import ErrorHandler, ResponseFormatter
        from mgenius_mcp.handlers import MCPHandlerRegistry, MCPRequestRouter
        
        # If we get here, all imports worked
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

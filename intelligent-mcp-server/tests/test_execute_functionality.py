"""Tests for execute functionality."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from intelligent_mcp_server.execute.tool_executor import ToolExecutor, ExecutionResult


class TestToolExecutor:
    """Test the tool executor functionality."""
    
    @patch('intelligent_mcp_server.execute.tool_executor.math_dispatcher')
    def test_executor_initialization(self, mock_dispatcher):
        """Test that executor initializes correctly."""
        mock_dispatcher.__all__ = ["add", "subtract"]
        mock_dispatcher.add = Mock()
        mock_dispatcher.subtract = Mock()
        
        executor = ToolExecutor()
        assert len(executor._available_tools) == 2
        assert "add" in executor._available_tools
        assert "subtract" in executor._available_tools
    
    def test_parameter_validators_setup(self):
        """Test parameter validation rules setup."""
        executor = ToolExecutor()
        validators = executor._parameter_validators
        
        # Test some known validation rules
        assert "divide" in validators
        assert validators["divide"]["b"]["not_zero"] is True
        
        assert "triangle_area" in validators
        assert validators["triangle_area"]["base"]["positive"] is True
    
    @pytest.mark.asyncio
    @patch('intelligent_mcp_server.execute.tool_executor.math_dispatcher')
    async def test_execute_tool_success(self, mock_dispatcher):
        """Test successful tool execution."""
        # Mock dispatcher
        mock_add = Mock(return_value=8)
        mock_dispatcher.__all__ = ["add"]
        mock_dispatcher.add = mock_add
        
        executor = ToolExecutor()
        
        # Mock signature inspection
        with patch('inspect.signature') as mock_sig:
            # Mock parameter signature
            mock_param = Mock()
            mock_param.default = Mock()
            mock_param.default.__class__ = type(Mock().empty)  # Not empty
            mock_param.annotation = int
            
            mock_signature = Mock()
            mock_signature.parameters = {"a": mock_param, "b": mock_param}
            mock_sig.return_value = mock_signature
            
            result = await executor.execute_tool("add", {"a": 3, "b": 5})
        
        assert result.success is True
        assert result.result == 8
        assert result.tool_name == "add" 
        assert result.execution_time >= 0
    
    @pytest.mark.asyncio
    async def test_execute_tool_not_found(self):
        """Test execution with non-existent tool."""
        executor = ToolExecutor()
        
        result = await executor.execute_tool("nonexistent_tool", {})
        
        assert result.success is False
        assert result.error_type == "ToolNotFoundError"
        assert "not found" in result.error_message
    
    @pytest.mark.asyncio
    @patch('intelligent_mcp_server.execute.tool_executor.math_dispatcher')
    async def test_execute_tool_validation_error(self, mock_dispatcher):
        """Test execution with parameter validation error."""
        # Mock dispatcher
        mock_divide = Mock()
        mock_dispatcher.__all__ = ["divide"]
        mock_dispatcher.divide = mock_divide
        
        executor = ToolExecutor()
        
        # Mock signature with validation rules
        with patch('inspect.signature') as mock_sig:
            mock_param_a = Mock()
            mock_param_a.default = Mock()
            mock_param_a.default.__class__ = type(Mock().empty)
            mock_param_a.annotation = float
            
            mock_param_b = Mock()
            mock_param_b.default = Mock() 
            mock_param_b.default.__class__ = type(Mock().empty)
            mock_param_b.annotation = float
            
            mock_signature = Mock()
            mock_signature.parameters = {"a": mock_param_a, "b": mock_param_b}
            mock_sig.return_value = mock_signature
            
            # Test division by zero validation
            result = await executor.execute_tool("divide", {"a": 10, "b": 0})
        
        assert result.success is False
        assert result.error_type == "ParameterValidationError"
        assert "cannot be zero" in result.error_message
    
    def test_convert_parameter_type(self):
        """Test parameter type conversion."""
        executor = ToolExecutor()
        
        # Mock parameter with int annotation
        mock_param = Mock()
        mock_param.annotation = int
        
        # Test conversion
        result = executor._convert_parameter_type("123", mock_param)
        assert result == 123
        assert isinstance(result, int)
        
        # Test list conversion
        mock_param.annotation = list
        result = executor._convert_parameter_type((1, 2, 3), mock_param)
        assert result == [1, 2, 3]
        assert isinstance(result, list)
    
    def test_apply_validation_rules(self):
        """Test parameter validation rules application."""
        executor = ToolExecutor()
        
        # Test positive constraint
        error = executor._apply_validation_rules("triangle_area", "base", -5)
        assert error is not None
        assert "must be positive" in error
        
        # Test not_zero constraint  
        error = executor._apply_validation_rules("divide", "b", 0)
        assert error is not None
        assert "cannot be zero" in error
        
        # Test valid value
        error = executor._apply_validation_rules("triangle_area", "base", 10)
        assert error is None
    
    @patch('intelligent_mcp_server.execute.tool_executor.math_dispatcher')
    def test_get_tool_signature(self, mock_dispatcher):
        """Test getting tool signature information."""
        # Mock function with signature
        mock_func = Mock()
        mock_func.__doc__ = "Test function documentation"
        
        mock_dispatcher.__all__ = ["test_func"]
        mock_dispatcher.test_func = mock_func
        
        executor = ToolExecutor()
        
        with patch('inspect.signature') as mock_sig, patch('inspect.getdoc') as mock_doc:
            # Mock parameter
            mock_param = Mock()
            mock_param.annotation = int
            mock_param.default = Mock() 
            mock_param.default.__class__ = type(Mock().empty)
            
            mock_signature = Mock()
            mock_signature.parameters = {"param1": mock_param}
            mock_sig.return_value = mock_signature
            mock_doc.return_value = "Test documentation"
            
            result = executor.get_tool_signature("test_func")
        
        assert result is not None
        assert result["name"] == "test_func"
        assert "parameters" in result
        assert "param1" in result["parameters"]
    
    @patch('intelligent_mcp_server.execute.tool_executor.math_dispatcher')
    def test_get_available_tools(self, mock_dispatcher):
        """Test getting list of available tools."""
        mock_dispatcher.__all__ = ["add", "subtract", "multiply"]
        mock_dispatcher.add = Mock()
        mock_dispatcher.subtract = Mock()
        mock_dispatcher.multiply = Mock()
        
        executor = ToolExecutor()
        tools = executor.get_available_tools()
        
        assert len(tools) == 3
        assert "add" in tools
        assert "subtract" in tools
        assert "multiply" in tools


class TestExecutionResult:
    """Test the ExecutionResult dataclass."""
    
    def test_execution_result_creation(self):
        """Test creating an ExecutionResult."""
        result = ExecutionResult(
            success=True,
            result=42,
            tool_name="test_tool",
            parameters={"param": "value"},
            execution_time=0.1,
            timestamp=1234567890.0
        )
        
        assert result.success is True
        assert result.result == 42
        assert result.tool_name == "test_tool"
        assert result.parameters == {"param": "value"}
        assert result.execution_time == 0.1
        assert result.timestamp == 1234567890.0
        assert result.error_message is None
        assert result.error_type is None
        assert result.metadata is None
    
    def test_execution_result_with_error(self):
        """Test creating an ExecutionResult with error."""
        result = ExecutionResult(
            success=False,
            result=None,
            tool_name="test_tool",
            parameters={},
            execution_time=0.05,
            timestamp=1234567890.0,
            error_message="Test error",
            error_type="TestError"
        )
        
        assert result.success is False
        assert result.result is None
        assert result.error_message == "Test error"
        assert result.error_type == "TestError"


@pytest.mark.integration
class TestExecuteIntegration:
    """Integration tests for execute functionality."""
    
    @pytest.mark.asyncio
    async def test_execute_workflow(self):
        """Test complete execute workflow (requires actual dependencies)."""
        try:
            # This test requires actual mathgenius module
            import mathgenius.api.dispatcher
            
            # Create tool executor
            executor = ToolExecutor()
            
            # Test that executor loads tools
            tools = executor.get_available_tools()
            assert len(tools) > 0
            
            # For now, just test that the executor can be created
            assert executor is not None
            
        except ImportError:
            pytest.skip("mathgenius module not available for integration test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

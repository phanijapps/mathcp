"""Error handling and response formatting for MCP mathematical operations."""

import logging
import traceback
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Types of errors that can occur."""
    VALIDATION_ERROR = "validation_error"
    MATHEMATICAL_ERROR = "mathematical_error"
    COMPUTATION_ERROR = "computation_error"
    TIMEOUT_ERROR = "timeout_error"
    SERVER_ERROR = "server_error"
    UNKNOWN_TOOL_ERROR = "unknown_tool_error"
    PARAMETER_ERROR = "parameter_error"
    DOMAIN_ERROR = "domain_error"
    CONVERGENCE_ERROR = "convergence_error"
    PRECISION_ERROR = "precision_error"


@dataclass
class ErrorContext:
    """Context information for an error."""
    tool_name: str
    parameters: Dict[str, Any]
    error_type: ErrorType
    original_error: Optional[Exception] = None
    timestamp: Optional[datetime] = None
    request_id: Optional[str] = None


class MathematicalError(Exception):
    """Base class for mathematical errors."""
    def __init__(self, message: str, error_type: ErrorType = ErrorType.MATHEMATICAL_ERROR, context: Optional[ErrorContext] = None):
        super().__init__(message)
        self.error_type = error_type
        self.context = context
        self.timestamp = datetime.now()


class DomainError(MathematicalError):
    """Error for mathematical domain violations."""
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(message, ErrorType.DOMAIN_ERROR, context)


class ConvergenceError(MathematicalError):
    """Error for convergence failures."""
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(message, ErrorType.CONVERGENCE_ERROR, context)


class PrecisionError(MathematicalError):
    """Error for precision-related issues."""
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(message, ErrorType.PRECISION_ERROR, context)


class TimeoutError(MathematicalError):
    """Error for computation timeouts."""
    def __init__(self, message: str, context: Optional[ErrorContext] = None):
        super().__init__(message, ErrorType.TIMEOUT_ERROR, context)


class ErrorHandler:
    """Handles and categorizes errors from mathematical operations."""
    
    def __init__(self, max_computation_time: int = 30):
        self.max_computation_time = max_computation_time
        self.error_patterns = self._create_error_patterns()
        self.recovery_strategies = self._create_recovery_strategies()
    
    def _create_error_patterns(self) -> Dict[str, ErrorType]:
        """Create patterns for error classification."""
        return {
            # Division by zero
            "division by zero": ErrorType.DOMAIN_ERROR,
            "divide by zero": ErrorType.DOMAIN_ERROR,
            "ZeroDivisionError": ErrorType.DOMAIN_ERROR,
            
            # Invalid domain
            "math domain error": ErrorType.DOMAIN_ERROR,
            "invalid value": ErrorType.DOMAIN_ERROR,
            "out of domain": ErrorType.DOMAIN_ERROR,
            "invalid domain": ErrorType.DOMAIN_ERROR,
            
            # Convergence issues
            "convergence": ErrorType.CONVERGENCE_ERROR,
            "failed to converge": ErrorType.CONVERGENCE_ERROR,
            "no convergence": ErrorType.CONVERGENCE_ERROR,
            "divergence": ErrorType.CONVERGENCE_ERROR,
            
            # Precision issues
            "precision": ErrorType.PRECISION_ERROR,
            "overflow": ErrorType.PRECISION_ERROR,
            "underflow": ErrorType.PRECISION_ERROR,
            "inf": ErrorType.PRECISION_ERROR,
            "nan": ErrorType.PRECISION_ERROR,
            
            # Parameter errors
            "invalid parameter": ErrorType.PARAMETER_ERROR,
            "missing parameter": ErrorType.PARAMETER_ERROR,
            "wrong parameter": ErrorType.PARAMETER_ERROR,
            "parameter type": ErrorType.PARAMETER_ERROR,
            
            # Computation errors
            "singular matrix": ErrorType.COMPUTATION_ERROR,
            "not invertible": ErrorType.COMPUTATION_ERROR,
            "cannot solve": ErrorType.COMPUTATION_ERROR,
            "no solution": ErrorType.COMPUTATION_ERROR,
            
            # Timeout errors
            "timeout": ErrorType.TIMEOUT_ERROR,
            "time limit": ErrorType.TIMEOUT_ERROR,
            "computation too long": ErrorType.TIMEOUT_ERROR,
        }
    
    def _create_recovery_strategies(self) -> Dict[ErrorType, str]:
        """Create recovery strategies for different error types."""
        return {
            ErrorType.DOMAIN_ERROR: "Check input values are within valid mathematical domain",
            ErrorType.CONVERGENCE_ERROR: "Try adjusting precision or iteration limits",
            ErrorType.PRECISION_ERROR: "Use higher precision arithmetic or check for numerical stability",
            ErrorType.PARAMETER_ERROR: "Verify all required parameters are provided with correct types",
            ErrorType.COMPUTATION_ERROR: "Check mathematical conditions (e.g., matrix invertibility)",
            ErrorType.TIMEOUT_ERROR: "Reduce problem size or increase computation time limit"
        }
    
    def classify_error(self, error: Exception, context: Optional[ErrorContext] = None) -> ErrorType:
        """Classify an error based on its message and type."""
        error_message = str(error).lower()
        error_type_name = type(error).__name__
        
        # Check for specific error patterns
        for pattern, error_type in self.error_patterns.items():
            if pattern.lower() in error_message or pattern in error_type_name:
                return error_type
        
        # Check by exception type
        if isinstance(error, (ValueError, TypeError)):
            return ErrorType.PARAMETER_ERROR
        elif isinstance(error, ZeroDivisionError):
            return ErrorType.DOMAIN_ERROR
        elif isinstance(error, OverflowError):
            return ErrorType.PRECISION_ERROR
        elif isinstance(error, TimeoutError):
            return ErrorType.TIMEOUT_ERROR
        else:
            return ErrorType.COMPUTATION_ERROR
    
    def handle_error(self, error: Exception, context: ErrorContext) -> Dict[str, Any]:
        """Handle an error and return a formatted response."""
        error_type = self.classify_error(error, context)
        
        # Create user-friendly error message
        user_message = self._create_user_message(error, error_type, context)
        
        # Log the error
        self._log_error(error, error_type, context)
        
        # Get recovery strategy
        recovery_strategy = self.recovery_strategies.get(error_type, "Please check your input parameters")
        
        # Create error response
        response = {
            "success": False,
            "error": {
                "type": error_type.value,
                "message": user_message,
                "recovery_strategy": recovery_strategy,
                "tool_name": context.tool_name,
                "timestamp": context.timestamp.isoformat() if context.timestamp else datetime.now().isoformat(),
                "request_id": context.request_id
            }
        }
        
        # Add debug information in development mode
        if logger.isEnabledFor(logging.DEBUG):
            response["error"]["debug"] = {
                "original_error": str(error),
                "error_type": type(error).__name__,
                "traceback": traceback.format_exc()
            }
        
        return response
    
    def _create_user_message(self, error: Exception, error_type: ErrorType, context: ErrorContext) -> str:
        """Create a user-friendly error message."""
        tool_name = context.tool_name
        
        if error_type == ErrorType.DOMAIN_ERROR:
            return f"Invalid input for {tool_name}: {self._get_domain_specific_message(error, tool_name)}"
        elif error_type == ErrorType.PARAMETER_ERROR:
            return f"Parameter error in {tool_name}: {str(error)}"
        elif error_type == ErrorType.CONVERGENCE_ERROR:
            return f"Convergence error in {tool_name}: The computation did not converge to a solution"
        elif error_type == ErrorType.PRECISION_ERROR:
            return f"Precision error in {tool_name}: The computation resulted in numerical instability"
        elif error_type == ErrorType.TIMEOUT_ERROR:
            return f"Timeout error in {tool_name}: The computation exceeded the time limit"
        elif error_type == ErrorType.COMPUTATION_ERROR:
            return f"Computation error in {tool_name}: {str(error)}"
        else:
            return f"Error in {tool_name}: {str(error)}"
    
    def _get_domain_specific_message(self, error: Exception, tool_name: str) -> str:
        """Get domain-specific error message."""
        error_str = str(error).lower()
        
        # Specific messages for common mathematical domain errors
        if "divide" in error_str or "zero" in error_str:
            if tool_name in ["divide", "modulo"]:
                return "Division by zero is not allowed"
            elif "determinant" in tool_name:
                return "Matrix is singular (determinant is zero)"
            else:
                return "Division by zero encountered"
        
        elif "sqrt" in error_str or "square root" in error_str:
            return "Square root of negative number is not allowed for real numbers"
        
        elif "log" in error_str or "logarithm" in error_str:
            return "Logarithm of zero or negative number is not allowed"
        
        elif "asin" in tool_name or "acos" in tool_name:
            return "Input must be between -1 and 1 for inverse trigonometric functions"
        
        elif "matrix" in tool_name and "singular" in error_str:
            return "Matrix is singular and cannot be inverted"
        
        elif "radius" in str(error).lower():
            return "Radius must be positive"
        
        elif "negative" in error_str:
            return "Input must be non-negative"
        
        else:
            return str(error)
    
    def _log_error(self, error: Exception, error_type: ErrorType, context: ErrorContext) -> None:
        """Log the error with appropriate level."""
        log_message = f"Error in {context.tool_name}: {error} (type: {error_type.value})"
        
        if error_type in [ErrorType.SERVER_ERROR, ErrorType.TIMEOUT_ERROR]:
            logger.error(log_message)
            logger.debug(f"Error context: {context}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
        elif error_type in [ErrorType.DOMAIN_ERROR, ErrorType.PARAMETER_ERROR]:
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def is_recoverable(self, error_type: ErrorType) -> bool:
        """Check if an error type is recoverable."""
        recoverable_types = [
            ErrorType.DOMAIN_ERROR,
            ErrorType.PARAMETER_ERROR,
            ErrorType.VALIDATION_ERROR
        ]
        return error_type in recoverable_types


class ResponseFormatter:
    """Formats responses for MCP mathematical operations."""
    
    def __init__(self, precision: int = 15):
        self.precision = precision
    
    def format_success_response(self, result: Any, tool_name: str, execution_time: Optional[float] = None, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Format a successful response."""
        formatted_result = self._format_mathematical_result(result, tool_name)
        
        response = {
            "success": True,
            "result": formatted_result,
            "metadata": {
                "tool_name": tool_name,
                "timestamp": datetime.now().isoformat(),
                "execution_time": execution_time,
                "request_id": request_id
            }
        }
        
        return response
    
    def _format_mathematical_result(self, result: Any, tool_name: str) -> Any:
        """Format mathematical result based on tool type."""
        if result is None:
            return None
        
        # Handle different types of mathematical results
        if isinstance(result, (int, bool)):
            return result
        
        elif isinstance(result, float):
            # Format floating point numbers with appropriate precision
            if abs(result) < 1e-10:  # Very small numbers
                return 0.0
            elif abs(result) > 1e10:  # Very large numbers
                return f"{result:.6e}"
            else:
                return round(result, self.precision)
        
        elif isinstance(result, complex):
            return {
                "real": self._format_mathematical_result(result.real, tool_name),
                "imaginary": self._format_mathematical_result(result.imag, tool_name),
                "string": str(result)
            }
        
        elif isinstance(result, (list, tuple)):
            return [self._format_mathematical_result(item, tool_name) for item in result]
        
        elif isinstance(result, dict):
            return {
                key: self._format_mathematical_result(value, tool_name)
                for key, value in result.items()
            }
        
        elif hasattr(result, "tolist"):  # NumPy arrays
            return self._format_mathematical_result(result.tolist(), tool_name)
        
        elif hasattr(result, "__iter__") and not isinstance(result, str):
            return [self._format_mathematical_result(item, tool_name) for item in result]
        
        else:
            return str(result)
    
    def format_error_response(self, error: Exception, context: ErrorContext, error_handler: ErrorHandler) -> Dict[str, Any]:
        """Format an error response."""
        return error_handler.handle_error(error, context)
    
    def format_validation_error_response(self, validation_errors: List[str], tool_name: str, request_id: Optional[str] = None) -> Dict[str, Any]:
        """Format a validation error response."""
        return {
            "success": False,
            "error": {
                "type": ErrorType.VALIDATION_ERROR.value,
                "message": f"Validation failed for {tool_name}",
                "validation_errors": validation_errors,
                "tool_name": tool_name,
                "timestamp": datetime.now().isoformat(),
                "request_id": request_id
            }
        }
    
    def format_batch_response(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format a batch response."""
        successful_count = sum(1 for r in responses if r.get("success", False))
        
        return {
            "success": successful_count == len(responses),
            "results": responses,
            "metadata": {
                "total_requests": len(responses),
                "successful_requests": successful_count,
                "failed_requests": len(responses) - successful_count,
                "timestamp": datetime.now().isoformat()
            }
        }


class PerformanceMonitor:
    """Monitors performance and handles timeouts."""
    
    def __init__(self, max_computation_time: int = 30):
        self.max_computation_time = max_computation_time
        self.performance_metrics = {}
    
    def record_execution(self, tool_name: str, execution_time: float, success: bool) -> None:
        """Record execution metrics."""
        if tool_name not in self.performance_metrics:
            self.performance_metrics[tool_name] = {
                "total_calls": 0,
                "successful_calls": 0,
                "total_time": 0.0,
                "max_time": 0.0,
                "min_time": float('inf')
            }
        
        metrics = self.performance_metrics[tool_name]
        metrics["total_calls"] += 1
        metrics["total_time"] += execution_time
        metrics["max_time"] = max(metrics["max_time"], execution_time)
        metrics["min_time"] = min(metrics["min_time"], execution_time)
        
        if success:
            metrics["successful_calls"] += 1
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report for all tools."""
        report = {}
        
        for tool_name, metrics in self.performance_metrics.items():
            report[tool_name] = {
                "total_calls": metrics["total_calls"],
                "successful_calls": metrics["successful_calls"],
                "success_rate": metrics["successful_calls"] / metrics["total_calls"] if metrics["total_calls"] > 0 else 0,
                "average_time": metrics["total_time"] / metrics["total_calls"] if metrics["total_calls"] > 0 else 0,
                "max_time": metrics["max_time"],
                "min_time": metrics["min_time"] if metrics["min_time"] != float('inf') else 0
            }
        
        return report
    
    def check_timeout(self, execution_time: float) -> bool:
        """Check if execution time exceeds limit."""
        return execution_time > self.max_computation_time
    
    def get_slow_operations(self, threshold: float = 1.0) -> List[str]:
        """Get operations that are consistently slow."""
        slow_ops = []
        
        for tool_name, metrics in self.performance_metrics.items():
            if metrics["total_calls"] > 0:
                avg_time = metrics["total_time"] / metrics["total_calls"]
                if avg_time > threshold:
                    slow_ops.append(tool_name)
        
        return slow_ops

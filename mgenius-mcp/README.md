# Math Genius MCP Server

A Model Context Protocol (MCP) server that exposes comprehensive mathematical tools from the Math Genius library.

## Overview

The Math Genius MCP server provides access to mathematical functions across multiple domains:

- **Arithmetic**: Basic operations (add, subtract, multiply, divide, power, modulo)
- **Algebra**: Equation solving, polynomial operations, expression manipulation
- **Geometry**: Shape calculations, coordinate geometry, spatial operations
- **Trigonometry**: Trigonometric functions and angle conversions
- **Calculus**: Differentiation, integration, limits, series
- **Linear Algebra**: Matrix operations, vector calculations, decompositions
- **Statistics**: Descriptive statistics, probability distributions, hypothesis testing
- **Symbolic Mathematics**: Symbolic computation, expression manipulation

## Installation

### Prerequisites

- Python 3.12 or higher
- Math Genius library installed

### Install Dependencies

```bash
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Configuration

The MCP server can be configured through environment variables or by providing a configuration object.

### Environment Variables

```bash
# Server Configuration
export MCP_HOST=localhost
export MCP_PORT=8000
export MCP_DEBUG=false

# Protocol Configuration
export MCP_PROTOCOL_VERSION=1.0
export MCP_SERVER_NAME=mgenius-mcp
export MCP_SERVER_VERSION=0.1.0

# Mathematical Configuration
export MCP_MAX_COMPUTATION_TIME=30
export MCP_PRECISION=15

# Tool Configuration (enable/disable categories)
export MCP_ENABLE_ARITHMETIC=true
export MCP_ENABLE_ALGEBRA=true
export MCP_ENABLE_GEOMETRY=true
export MCP_ENABLE_TRIGONOMETRY=true
export MCP_ENABLE_CALCULUS=true
export MCP_ENABLE_LINEAR_ALGEBRA=true
export MCP_ENABLE_STATISTICS=true
export MCP_ENABLE_SYMBOLIC=true

# Logging Configuration
export MCP_LOG_LEVEL=INFO
export MCP_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance Configuration
export MCP_MAX_CONCURRENT_REQUESTS=100
export MCP_REQUEST_TIMEOUT=60
```

## Usage

### Starting the Server

```bash
# Using the command line script
mgenius-mcp

# Or directly with Python
python -m mgenius_mcp.server
```

### Programmatic Usage

```python
import asyncio
from mgenius_mcp import MCPServer, MCPConfig

async def main():
    config = MCPConfig(
        host="localhost",
        port=8000,
        debug=True,
        enable_arithmetic=True,
        enable_algebra=True,
        # ... other configuration options
    )
    
    server = MCPServer(config)
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
```

## API Examples

### Basic Arithmetic

```json
{
  "tool_name": "add",
  "parameters": {
    "a": 5,
    "b": 3
  }
}
```

Response:
```json
{
  "success": true,
  "result": 8,
  "metadata": {
    "tool_name": "add",
    "timestamp": "2025-07-17T10:30:00Z",
    "execution_time": 0.001,
    "request_id": "req_123"
  }
}
```

### Geometry Calculations

```json
{
  "tool_name": "circle_area",
  "parameters": {
    "radius": 5.0
  }
}
```

Response:
```json
{
  "success": true,
  "result": 78.53981633974483,
  "metadata": {
    "tool_name": "circle_area",
    "timestamp": "2025-07-17T10:30:00Z",
    "execution_time": 0.002,
    "request_id": "req_124"
  }
}
```

### Calculus Operations

```json
{
  "tool_name": "differentiate",
  "parameters": {
    "expression": "x^2 + 2*x + 1",
    "variable": "x"
  }
}
```

Response:
```json
{
  "success": true,
  "result": "2*x + 2",
  "metadata": {
    "tool_name": "differentiate",
    "timestamp": "2025-07-17T10:30:00Z",
    "execution_time": 0.015,
    "request_id": "req_125"
  }
}
```

### Matrix Operations

```json
{
  "tool_name": "matrix_multiply",
  "parameters": {
    "a": [[1, 2], [3, 4]],
    "b": [[5, 6], [7, 8]]
  }
}
```

Response:
```json
{
  "success": true,
  "result": [[19, 22], [43, 50]],
  "metadata": {
    "tool_name": "matrix_multiply",
    "timestamp": "2025-07-17T10:30:00Z",
    "execution_time": 0.003,
    "request_id": "req_126"
  }
}
```

## Error Handling

The server provides comprehensive error handling with detailed error messages:

```json
{
  "success": false,
  "error": {
    "type": "domain_error",
    "message": "Invalid input for divide: Division by zero is not allowed",
    "recovery_strategy": "Check input values are within valid mathematical domain",
    "tool_name": "divide",
    "timestamp": "2025-07-17T10:30:00Z",
    "request_id": "req_127"
  }
}
```

## Health Check

Check server status:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "server_name": "mgenius-mcp",
  "server_version": "0.1.0",
  "protocol_version": "1.0",
  "enabled_tools": {
    "arithmetic": true,
    "algebra": true,
    "geometry": true,
    "trigonometry": true,
    "calculus": true,
    "linear_algebra": true,
    "statistics": true,
    "symbolic": true
  },
  "total_tools": 85,
  "performance_metrics": {
    "add": {
      "total_calls": 100,
      "successful_calls": 100,
      "success_rate": 1.0,
      "average_time": 0.001,
      "max_time": 0.003,
      "min_time": 0.0005
    }
  }
}
```

## Available Tools

### Arithmetic (6 tools)
- `add`, `subtract`, `multiply`, `divide`, `power`, `modulo`

### Algebra (5 tools)
- `solve_linear`, `solve_quadratic`, `expand_expr`, `factor_expr`, `simplify_expr`

### Geometry (26 tools)
- Shape calculations: `triangle_area`, `circle_area`, `rectangle_area`, etc.
- Coordinate geometry: `distance_2d`, `distance_3d`, `midpoint_2d`, etc.
- Spatial operations: `vector_add`, `vector_subtract`, `vector_dot_product`, etc.

### Trigonometry (11 tools)
- Basic functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Hyperbolic functions: `sinh`, `cosh`, `tanh`
- Angle conversions: `degrees_to_radians`, `radians_to_degrees`

### Calculus (10 tools)
- `differentiate`, `integrate_definite`, `integrate_indefinite`, `compute_limit`
- `taylor_series`, `partial_derivative`, `gradient`, `hessian_matrix`
- `numerical_derivative`, `numerical_integral`

### Linear Algebra (15 tools)
- Matrix operations: `matrix_add`, `matrix_multiply`, `matrix_inverse`, etc.
- Decompositions: `lu_decomposition`, `qr_decomposition`, `svd_decomposition`
- Vector operations: `vector_norm`, `vector_projection`

### Statistics (17 tools)
- Descriptive statistics: `mean`, `median`, `mode`, `variance`, `standard_deviation`
- Probability distributions: `normal_distribution_pdf`, `binomial_distribution_pmf`, etc.
- Hypothesis testing: `t_test_one_sample`, `t_test_two_sample`, `chi_square_test`

### Symbolic Mathematics (16 tools)
- Expression manipulation: `parse_expression`, `expand_expression`, `simplify_expression`
- Equation solving: `solve_equation`, `solve_differential_equation`
- Symbolic calculus: `symbolic_integrate`, `symbolic_differentiate`

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black .

# Check types
mypy .

# Lint code
flake8 .
```

### Adding New Tools

1. Add the mathematical function to the Math Genius library
2. Update the dispatcher to include the new function
3. The MCP server will automatically discover and register the new tool

## Performance

The server includes performance monitoring for all mathematical operations:

- Request tracking and timing
- Success/failure rates
- Concurrent request handling
- Timeout protection for long-running computations

## Security

- Input validation using JSON schemas
- Parameter constraint checking
- Timeout protection
- Error message sanitization
- No arbitrary code execution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation at https://docs.mathgenius.com/mcp
- Contact the team at dev@mathgenius.com

# Docker Configuration for MCP Servers

This directory contains Docker configuration for running Math and Finance MCP servers with Nginx reverse proxy.

## Configuration Overview

### Services
1. **math-mcp-server**
   - Port: 8001
   - Path: `/math/`
   - Depends on: mathgenius library

2. **yfinance-mcp-server**  
   - Port: 8002
   - Path: `/fin/`
   - Depends on: mathgenius library

3. **nginx** (Reverse Proxy)
   - Port: 80
   - Routes:
     - `/math/*` → math-mcp-server:8001
     - `/fin/*` → yfinance-mcp-server:8002

## Setup Instructions

1. Build and start services:
```bash
docker compose up --build
```

2. Access the services:
- Math MCP: http://localhost/math/
- Finance MCP: http://localhost/fin/

## MCP Server Configuration

To configure the MCP servers:

1. **Math MCP Server**:
   - Edit `math-mcp-server/config.py`
   - Set vector DB initialization in `initialize_vector_db.py`

2. **Finance MCP Server**:
   - Edit `yfinance-mcp-server/config.py`

## Nginx Configuration

- Main config: `nginx.conf`
- Mounted at: `/etc/nginx/conf.d/default.conf`

## Volumes
- Code is mounted from host for development
- Mathgenius library is shared between both MCP servers

## SSE JSON MCP Server Setup

For Server-Sent Events (SSE) with JSON responses:

1. Server Implementation (Python example):
```python
from flask import Response
import json

@app.route('/stream')
def stream_math_data():
    def generate():
        while True:
            # Get your math data here
            math_result = calculate_math_operation()  
            yield f"data: {json.dumps(math_result)}\n\n"
    
    return Response(generate(), mimetype="text/event-stream")
```

2. Client-side Usage:
```javascript
const mathStream = new EventSource('/math/stream');

mathStream.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('New math result:', data);
};
```

3. Nginx Configuration:
Ensure your nginx.conf has:
```nginx
proxy_set_header Connection '';
proxy_cache off;
proxy_buffering off;
chunked_transfer_encoding off;
```

That's it! The MCP server will now stream JSON math results.
</final_file_content>

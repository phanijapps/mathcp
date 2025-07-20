#!/usr/bin/env python3
"""
Quick test to verify tool discovery works
"""

import sys
from pathlib import Path

# Add math-genius to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_tool_discovery():
    """Test that we can discover all tools from mathgenius."""
    try:
        from simple_mcp_server import MathGeniusServer
        
        print("🔍 Testing Tool Discovery")
        print("=" * 30)
        
        server = MathGeniusServer()
        tools = server.discover_tools()
        
        print(f"✅ Discovered {len(tools)} tools")
        print("\n📋 Sample tools:")
        
        # Show first 10 tools
        for i, tool in enumerate(tools[:10]):
            print(f"  {i+1}. {tool['name']}: {tool['description']}")
            print(f"     Parameters: {list(tool['parameters'].keys())}")
        
        if len(tools) > 10:
            print(f"  ... and {len(tools) - 10} more tools")
        
        print(f"\n🎯 Total tools available: {len(tools)}")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    if test_tool_discovery():
        print("\n✅ Tool discovery works! Server is ready.")
    else:
        print("\n❌ Tool discovery failed.")
        sys.exit(1)

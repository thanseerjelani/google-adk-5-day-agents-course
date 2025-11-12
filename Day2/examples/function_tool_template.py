"""
Reusable template for creating function tools.

Copy this template when creating new tools.
"""

def my_custom_tool(param1: str, param2: int) -> dict:
    """[REPLACE] Brief description of what this tool does.
    
    [REPLACE] Detailed explanation that the LLM will read to understand
    when and how to use this tool.
    
    Args:
        param1: [REPLACE] Description of first parameter
        param2: [REPLACE] Description of second parameter
    
    Returns:
        Dictionary with status and data:
        Success: {"status": "success", "data": {...}}
        Error: {"status": "error", "error_message": "..."}
    """
    try:
        # [REPLACE] Your business logic here
        # Validate inputs
        if not param1:
            return {"status": "error", "error_message": "param1 is required"}
        
        # Process
        result = do_something(param1, param2)
        
        # Return structured success
        return {
            "status": "success",
            "data": result,
            "message": "Operation completed successfully"
        }
        
    except ValueError as e:
        return {"status": "error", "error_message": f"Validation error: {str(e)}"}
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error: {str(e)}"}

# Best Practices Checklist:
# ✅ Type hints for all parameters
# ✅ Clear, detailed docstring
# ✅ Always return dict with "status" field
# ✅ Handle errors gracefully
# ✅ Return structured data
# ✅ Include helpful error messages
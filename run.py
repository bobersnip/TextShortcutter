#!/usr/bin/env python3
"""
Simple launcher script for TextShortcutter
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the TextShortcutter application."""
    
    # Add src to Python path
    src_dir = Path(__file__).parent / "src"
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))
    
    try:
        # Import and run the main application
        from main import main as app_main
        app_main()
        
    except ImportError as e:
        print(f"Error: Could not import main application: {e}")
        print("Make sure you have installed the required dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

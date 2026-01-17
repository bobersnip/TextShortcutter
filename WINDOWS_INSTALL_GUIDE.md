# Windows PyQt5 Installation Troubleshooting Guide

## The Problem
The error you're encountering is a known Windows issue with PyQt5 installation:
```
ERROR: Could not install packages due to an OSError: [WinError 2] The system cannot find the file specified: 'C:\\Python311\\Scripts\\pylupdate5.exe' -> 'C:\\Python311\\Scripts\\pylupdate5.exe.deleteme'
```

This happens because Windows has trouble with file locking and the PyQt5 installer trying to rename files.

## Solutions (Try in Order)

### Solution 1: Use Conda (Recommended)
If you have Anaconda or Miniconda installed:
```bash
# Create a new environment
conda create -n textshortcutter python=3.11
conda activate textshortcutter

# Install PyQt5 via conda (more reliable on Windows)
conda install pyqt5 keyboard pyperclip psutil

# Run the application
python run.py
```

### Solution 2: Install PyQt5 Separately
```bash
# Install PyQt5 first with specific version
pip install PyQt5==5.15.7

# Then install other dependencies
pip install keyboard pyperclip psutil

# Finally, run the application
python run.py
```

### Solution 3: Use --no-deps Flag
```bash
# Install PyQt5 without dependencies
pip install --no-deps PyQt5

# Install other packages
pip install keyboard pyperclip psutil

# Run the application
python run.py
```

### Solution 4: Use Alternative GUI Framework
If PyQt5 continues to cause issues, I can modify the application to use Tkinter (built into Python) or another GUI framework. Let me know if you'd like this option.

### Solution 5: Windows-Specific Installation
```bash
# Run as administrator and use --user flag
pip install --user PyQt5 --no-cache-dir

# If that fails, try upgrading pip first
python -m pip install --upgrade pip
pip install --user PyQt5

# Then install other dependencies
pip install --user keyboard pyperclip psutil
```

### Solution 6: Virtual Environment
```bash
# Create a virtual environment
python -m venv textshortcutter_env

# Activate it
# On Windows:
textshortcutter_env\Scripts\activate
# On macOS/Linux:
# source textshortcutter_env/bin/activate

# Install dependencies in the virtual environment
pip install PyQt5 keyboard pyperclip psutil

# Run the application
python run.py
```

## Alternative: Use Tkinter Version

If PyQt5 continues to be problematic, I can create a version using Tkinter (Python's built-in GUI library). This would require minimal changes and would work on any Python installation.

Would you like me to:
1. Create a Tkinter version of the application?
2. Help you try the solutions above?
3. Suggest another approach?

## Quick Test

To verify if PyQt5 is working at all, try this simple test:
```python
# Create a file called test_pyqt.py
import sys
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel('PyQt5 is working!')
label.show()
print("PyQt5 imported successfully!")
sys.exit(app.exec_())
```

Run it with:
```bash
python test_pyqt.py
```

If this works, the issue might be with the specific version or installation method.

Let me know which solution you'd like to try, or if you'd prefer the Tkinter alternative!

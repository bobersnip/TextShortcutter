#!/usr/bin/env python3
"""
SystemMonitor module for TextShortcutter.

Monitors system state for security and functionality.
"""

import threading
import time
from typing import Optional
from PyQt5.QtCore import QObject, pyqtSignal


class SystemMonitor(QObject):
    """Monitors system state for security and functionality."""
    active_window_changed = pyqtSignal(str)
    clipboard_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self._current_window = ""
        self._current_clipboard = ""
        self._running = False
        self._thread = None
        
    def start_monitoring(self):
        """Start system monitoring in background thread."""
        if self._running:
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        
    def stop_monitoring(self):
        """Stop system monitoring."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self._running:
            try:
                # Check active window
                current_window = self._get_active_window()
                if current_window != self._current_window:
                    self._current_window = current_window
                    self.active_window_changed.emit(current_window)
                
                # Check clipboard
                current_clipboard = self._get_clipboard_content()
                if current_clipboard != self._current_clipboard:
                    self._current_clipboard = current_clipboard
                    self.clipboard_changed.emit(current_clipboard)
                    
                time.sleep(0.1)  # 100ms update interval
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1.0)
                
    def _get_active_window(self) -> str:
        """Get the currently active window title."""
        try:
            import pygetwindow as gw
            active = gw.getActiveWindow()
            return active.title if active else ""
        except ImportError:
            # Fallback for systems without pygetwindow
            return "Unknown"
            
    def _get_clipboard_content(self) -> str:
        """Get current clipboard content."""
        try:
            import pyperclip
            return pyperclip.paste()
        except ImportError:
            return ""
            
    def get_current_window(self) -> str:
        """Get current active window title."""
        return self._current_window

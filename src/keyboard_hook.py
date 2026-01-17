#!/usr/bin/env python3
"""
KeyboardHook module for TextShortcutter.

Handles keyboard hooking and trigger detection.
"""

from typing import List
from PyQt5.QtCore import QObject, pyqtSignal


class KeyboardHook(QObject):
    """Handles keyboard hooking and trigger detection."""
    trigger_pressed = pyqtSignal()
    key_pressed = pyqtSignal(str)
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self._hook_active = False
        self._trigger_keys = self._parse_trigger_keys(config.trigger_key)
        
    def start_hook(self):
        """Start keyboard hooking."""
        if self._hook_active:
            return
            
        self._hook_active = True
        import keyboard
        keyboard.hook(self._on_key_event)
        
    def stop_hook(self):
        """Stop keyboard hooking."""
        if not self._hook_active:
            return
            
        self._hook_active = False
        import keyboard
        keyboard.unhook_all()
        
    def _parse_trigger_keys(self, trigger_key: str) -> List[str]:
        """Parse trigger key combination into individual keys."""
        return [k.strip().lower() for k in trigger_key.split('+')]
        
    def _on_key_event(self, event):
        """Handle key press events."""
        import keyboard
        if event.event_type != keyboard.KEY_DOWN:
            return
            
        key_name = event.name.lower()
        self.key_pressed.emit(key_name)
        
        # Check if trigger key combination is pressed
        if self._is_trigger_pressed():
            self.trigger_pressed.emit()
            
    def _is_trigger_pressed(self) -> bool:
        """Check if the trigger key combination is currently pressed."""
        import keyboard
        try:
            for key in self._trigger_keys:
                if not keyboard.is_pressed(key):
                    return False
            return True
        except Exception as e:
            print(f"Error checking trigger keys: {e}")
            return False

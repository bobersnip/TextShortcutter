#!/usr/bin/env python3
"""
TextShortcutter - Secure Text Expander Application

A Python-based text expander that activates only with a configurable keybind.
Features a GUI for managing shortcuts and a popup for selecting expansions.
"""

import sys
import os
import json
import logging
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# GUI imports
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLineEdit, QTextEdit, QLabel, QTableWidget, 
    QTableWidgetItem, QSystemTrayIcon, QMenu, QComboBox, QCheckBox,
    QSpinBox, QFileDialog, QMessageBox, QDialog, QFormLayout,
    QGroupBox, QSplitter, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject, QEvent
from PyQt5.QtGui import QIcon, QKeySequence, QClipboard

# System monitoring imports
import keyboard
import pyperclip
from pynput import mouse
import psutil

# Import our separated modules
from models import Shortcut, Config
from system_monitor import SystemMonitor
from keyboard_hook import KeyboardHook
from expansion_manager import ExpansionManager
from popup_selector import PopupSelector

# Configuration
CONFIG_DIR = Path.home() / ".textshortcutter"
CONFIG_FILE = CONFIG_DIR / "config.json"
EXPANSIONS_FILE = CONFIG_DIR / "expansions.json"

# Ensure config directory exists before setting up logging
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(CONFIG_DIR / 'app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TextShortcutter")
        self.setGeometry(100, 100, 800, 600)
        
        # Set window transparency (70% opacity)
        self.setWindowOpacity(0.95)  # Slightly transparent for modern look
        
        # Apply modern styling
        self._apply_modern_styling()
        
        # Initialize components
        self.config = self._load_config()
        self.expansion_manager = ExpansionManager()
        self.system_monitor = SystemMonitor()
        self.keyboard_hook = KeyboardHook(self.config)
        
        # Setup UI
        self._setup_ui()
        self._setup_connections()
        
        # Start services
        self.system_monitor.start_monitoring()
        self.keyboard_hook.start_hook()
        
        # Setup system tray
        self._setup_tray_icon()
        
    def _apply_modern_styling(self):
        """Apply modern styling with transparency and rounded corners."""
        # Modern dark theme with neon accents
        style = """
        QMainWindow {
            background-color: rgba(30, 30, 30, 220);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 50);
        }
        
        QWidget {
            background-color: transparent;
            color: #ffffff;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        
        QGroupBox {
            border: 1px solid rgba(255, 255, 255, 60);
            border-radius: 8px;
            margin-top: 10px;
            padding: 10px;
            background-color: rgba(40, 40, 40, 180);
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 10px;
            background-color: transparent;
            color: #00d2ff;
            font-weight: bold;
            font-size: 12px;
        }
        
        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                              stop:0 #00d2ff, stop:1 #3a7bd5);
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            color: white;
            font-weight: bold;
            min-height: 30px;
        }
        
        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                              stop:0 #3a7bd5, stop:1 #00d2ff);
        }
        
        QPushButton:pressed {
            background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                              stop:0 #00a9cc, stop:1 #2f63b0);
        }
        
        QLineEdit, QTextEdit {
            background-color: rgba(50, 50, 50, 200);
            border: 1px solid rgba(255, 255, 255, 80);
            border-radius: 6px;
            padding: 8px;
            color: #ffffff;
        }
        
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #00d2ff;
        }
        
        QTableWidget {
            background-color: rgba(40, 40, 40, 180);
            border: 1px solid rgba(255, 255, 255, 60);
            border-radius: 8px;
            gridline-color: rgba(255, 255, 255, 30);
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 20);
        }
        
        QTableWidget::item:selected {
            background-color: rgba(0, 210, 255, 50);
            border: 1px solid #00d2ff;
        }
        
        QHeaderView::section {
            background-color: rgba(60, 60, 60, 200);
            border: 1px solid rgba(255, 255, 255, 60);
            padding: 8px;
            font-weight: bold;
            color: #00d2ff;
        }
        
        QScrollBar:vertical {
            background: rgba(50, 50, 50, 180);
            width: 16px;
            border-radius: 8px;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                       stop:0 #00d2ff, stop:1 #3a7bd5);
            min-height: 20px;
            border-radius: 8px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                       stop:0 #3a7bd5, stop:1 #00d2ff);
        }
        
        QCheckBox {
            spacing: 8px;
            color: #ffffff;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border-radius: 4px;
            background-color: rgba(50, 50, 50, 200);
            border: 1px solid rgba(255, 255, 255, 80);
        }
        
        QCheckBox::indicator:checked {
            background-color: #00d2ff;
            border: 1px solid #00d2ff;
        }
        
        QSpinBox {
            background-color: rgba(50, 50, 50, 200);
            border: 1px solid rgba(255, 255, 255, 80);
            border-radius: 6px;
            padding: 6px;
            color: #ffffff;
            min-height: 30px;
        }
        
        QLabel {
            color: #ffffff;
            font-size: 12px;
        }
        
        QMessageBox {
            background-color: rgba(30, 30, 30, 220);
            border-radius: 12px;
        }
        
        QDialog {
            background-color: rgba(30, 30, 30, 220);
            border-radius: 12px;
        }
        """
        
        self.setStyleSheet(style)
        
    def _setup_ui(self):
        """Setup the main UI."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Top controls
        controls_layout = QHBoxLayout()
        
        # Trigger key configuration
        trigger_group = QGroupBox("Trigger Configuration")
        trigger_layout = QHBoxLayout()
        
        self.trigger_input = QLineEdit(self.config.trigger_key)
        self.trigger_input.setPlaceholderText("e.g., ctrl+space")
        trigger_layout.addWidget(QLabel("Trigger Key:"))
        trigger_layout.addWidget(self.trigger_input)
        
        self.save_trigger_btn = QPushButton("Save Trigger")
        self.save_trigger_btn.clicked.connect(self._save_trigger)
        trigger_layout.addWidget(self.save_trigger_btn)
        
        trigger_group.setLayout(trigger_layout)
        controls_layout.addWidget(trigger_group)
        
        # Security settings
        security_group = QGroupBox("Security")
        security_layout = QHBoxLayout()
        
        security_layout.addWidget(QLabel("Security Level:"))
        self.security_slider = QSpinBox()
        self.security_slider.setRange(1, 10)
        self.security_slider.setValue(self.config.security_level)
        security_layout.addWidget(self.security_slider)
        
        self.privacy_checkbox = QCheckBox("Privacy Mode")
        self.privacy_checkbox.setChecked(self.config.privacy_mode)
        security_layout.addWidget(self.privacy_checkbox)
        
        security_group.setLayout(security_layout)
        controls_layout.addWidget(security_group)
        
        main_layout.addLayout(controls_layout)
        
        # Splitter for expansions and details
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Expansions list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Add expansion form
        add_group = QGroupBox("Add New Expansion")
        add_layout = QFormLayout()
        
        self.shortcut_input = QLineEdit()
        self.shortcut_input.setPlaceholderText("e.g., omg")
        add_layout.addRow("Shortcut:", self.shortcut_input)
        
        self.expansion_input = QTextEdit()
        self.expansion_input.setPlaceholderText("e.g., Oh my gosh!")
        add_layout.addRow("Expansion:", self.expansion_input)
        
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Optional description")
        add_layout.addRow("Description:", self.description_input)
        
        add_buttons_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Expansion")
        self.add_btn.clicked.connect(self._add_expansion)
        add_buttons_layout.addWidget(self.add_btn)
        
        self.clear_btn = QPushButton("Clear Form")
        self.clear_btn.clicked.connect(self._clear_form)
        add_buttons_layout.addWidget(self.clear_btn)
        
        add_layout.addRow(add_buttons_layout)
        add_group.setLayout(add_layout)
        left_layout.addWidget(add_group)
        
        # Expansions table
        self.expansions_table = QTableWidget()
        self.expansions_table.setColumnCount(5)
        self.expansions_table.setHorizontalHeaderLabels(["Shortcut", "Expansion", "Description", "Usage", "Enabled"])
        self.expansions_table.horizontalHeader().setStretchLastSection(True)
        self.expansions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.expansions_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        left_layout.addWidget(self.expansions_table)
        
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        
        # Right panel - Details and actions
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Selected expansion details
        details_group = QGroupBox("Selected Expansion")
        details_layout = QVBoxLayout()
        
        self.selected_shortcut = QLabel("No selection")
        self.selected_shortcut.setStyleSheet("font-weight: bold;")
        details_layout.addWidget(self.selected_shortcut)
        
        self.selected_expansion = QTextEdit()
        self.selected_expansion.setReadOnly(True)
        details_layout.addWidget(self.selected_expansion)
        
        details_buttons_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self._edit_expansion)
        details_buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self._delete_expansion)
        details_buttons_layout.addWidget(self.delete_btn)
        
        self.toggle_btn = QPushButton("Toggle Enabled")
        self.toggle_btn.clicked.connect(self._toggle_expansion)
        details_buttons_layout.addWidget(self.toggle_btn)
        
        details_layout.addLayout(details_buttons_layout)
        details_group.setLayout(details_layout)
        right_layout.addWidget(details_group)
        
        # Actions
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        
        self.test_btn = QPushButton("Test Selected Expansion")
        self.test_btn.clicked.connect(self._test_expansion)
        actions_layout.addWidget(self.test_btn)
        
        self.import_btn = QPushButton("Import Expansions")
        self.import_btn.clicked.connect(self._import_expansions)
        actions_layout.addWidget(self.import_btn)
        
        self.export_btn = QPushButton("Export Expansions")
        self.export_btn.clicked.connect(self._export_expansions)
        actions_layout.addWidget(self.export_btn)
        
        actions_group.setLayout(actions_layout)
        right_layout.addWidget(actions_group)
        
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        
        main_layout.addWidget(splitter)
        
        central_widget.setLayout(main_layout)
        
        # Load initial data
        self._refresh_expansions_list()
        
    def _setup_connections(self):
        """Setup signal connections."""
        self.system_monitor.active_window_changed.connect(self._on_window_changed)
        self.keyboard_hook.trigger_pressed.connect(self._on_trigger_pressed)
        
        self.expansions_table.itemSelectionChanged.connect(self._on_selection_changed)
        
    def _setup_tray_icon(self):
        """Setup system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme("text-editor"))
        self.tray_icon.setToolTip("TextShortcutter")
        
        # Tray menu
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        
        hide_action = tray_menu.addAction("Hide")
        hide_action.triggered.connect(self.hide)
        
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
    def _load_config(self) -> Config:
        """Load configuration from file."""
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    return Config(**data)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            
        return Config()
        
    def _save_config(self):
        """Save configuration to file."""
        try:
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config.__dict__, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            
    def _refresh_expansions_list(self):
        """Refresh the expansions table."""
        expansions = self.expansion_manager.get_all_expansions()
        self.expansions_table.setRowCount(len(expansions))
        
        for i, exp in enumerate(expansions):
            self.expansions_table.setItem(i, 0, QTableWidgetItem(exp.shortcut))
            self.expansions_table.setItem(i, 1, QTableWidgetItem(exp.expansion[:50] + "..." if len(exp.expansion) > 50 else exp.expansion))
            self.expansions_table.setItem(i, 2, QTableWidgetItem(exp.description))
            self.expansions_table.setItem(i, 3, QTableWidgetItem(str(exp.usage_count)))
            self.expansions_table.setItem(i, 4, QTableWidgetItem("Yes" if exp.enabled else "No"))
            
    def _on_window_changed(self, window_title: str):
        """Handle active window changes."""
        logger.debug(f"Active window changed: {window_title}")
        
    def _on_trigger_pressed(self):
        """Handle trigger key press.""" 
        logger.info("Trigger key pressed")
        
        # Capture the originally focused window before showing popup
        self._original_focused_window = self.system_monitor.get_current_window()
        
        # Show popup with available expansions
        expansions = self.expansion_manager.get_all_expansions()
        if expansions:
            popup = PopupSelector(expansions, self)
            popup.expansion_selected.connect(self._paste_expansion)
            popup.exec_()
        else:
            QMessageBox.information(self, "No Expansions", "No expansions configured yet.")
            
    def _paste_expansion(self, expansion_text: str):
        """Paste the selected expansion."""
        try:
            # Store current clipboard
            current_clipboard = pyperclip.paste()
            
            # Set new clipboard content
            pyperclip.copy(expansion_text)
            
            # Use the originally focused window captured before showing popup
            original_window = getattr(self, '_original_focused_window', None)
            
            # Restore focus to original window and paste
            self._paste_to_window(expansion_text, original_window)
            
            # Restore original clipboard after a short delay
            QTimer.singleShot(100, lambda: pyperclip.copy(current_clipboard))
            
            logger.info(f"Pasted expansion: {expansion_text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error pasting expansion: {e}")
            
    def _get_original_focused_window(self):
        """Get the originally focused window before the popup was shown."""
        try:
            import pygetwindow as gw
            # Get the window that was active before the popup
            # We'll use the system monitor to get the last known active window
            return self.system_monitor.get_current_window()
        except ImportError:
            logger.warning("pygetwindow not available, using fallback window detection")
            return None
            
    def _paste_to_window(self, expansion_text: str, original_window):
        """Paste the expansion to the specified window."""
        try:
            import pygetwindow as gw
            
            # Find the original window and restore focus
            if original_window:
                windows = gw.getWindowsWithTitle(original_window)
                if windows:
                    target_window = windows[0]
                    # Bring window to front and focus it
                    target_window.activate()
                    
                    # Small delay to ensure window is focused
                    import time
                    time.sleep(0.1)
                    
                    # Send Ctrl+V to paste the clipboard content
                    keyboard.press_and_release('ctrl+v')
                    
                    # Optional: restore focus back to TextShortcutter after pasting
                    # self.activateWindow()
                    return True
            
            # Fallback: if we can't find the original window, try to paste anyway
            # This maintains the original behavior as a fallback
            keyboard.press_and_release('ctrl+v')
            return True
            
        except Exception as e:
            logger.error(f"Error pasting to window: {e}")
            # Fallback to original behavior
            keyboard.press_and_release('ctrl+v')
            return False
            
    def _on_selection_changed(self):
        """Handle selection changes in the table."""
        selected_items = self.expansions_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            shortcut_item = self.expansions_table.item(row, 0)
            if shortcut_item:
                shortcut = shortcut_item.text()
                expansion = self.expansion_manager.get_expansion(shortcut)
                if expansion:
                    self.selected_shortcut.setText(f"Shortcut: {expansion.shortcut}")
                    self.selected_expansion.setText(expansion.expansion)
                    
    def _add_expansion(self):
        """Add a new expansion."""
        shortcut = self.shortcut_input.text().strip()
        expansion = self.expansion_input.toPlainText().strip()
        description = self.description_input.text().strip()
        
        if not shortcut or not expansion:
            QMessageBox.warning(self, "Invalid Input", "Please enter both shortcut and expansion.")
            return
            
        if self.expansion_manager.add_expansion(shortcut, expansion, description):
            self._refresh_expansions_list()
            self._clear_form()
            QMessageBox.information(self, "Success", "Expansion added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to add expansion.")
            
    def _clear_form(self):
        """Clear the add expansion form."""
        self.shortcut_input.clear()
        self.expansion_input.clear()
        self.description_input.clear()
        
    def _edit_expansion(self):
        """Edit selected expansion."""
        selected_items = self.expansions_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an expansion to edit.")
            return
            
        row = selected_items[0].row()
        shortcut_item = self.expansions_table.item(row, 0)
        if shortcut_item:
            shortcut = shortcut_item.text()
            expansion = self.expansion_manager.get_expansion(shortcut)
            if expansion:
                # Simple edit dialog
                dialog = QDialog(self)
                dialog.setWindowTitle("Edit Expansion")
                layout = QFormLayout()
                
                shortcut_edit = QLineEdit(expansion.shortcut)
                shortcut_edit.setDisabled(True)  # Don't allow changing shortcut for now
                layout.addRow("Shortcut:", shortcut_edit)
                
                expansion_edit = QTextEdit(expansion.expansion)
                layout.addRow("Expansion:", expansion_edit)
                
                description_edit = QLineEdit(expansion.description)
                layout.addRow("Description:", description_edit)
                
                buttons_layout = QHBoxLayout()
                save_btn = QPushButton("Save")
                save_btn.clicked.connect(lambda: self._save_expansion_changes(expansion.shortcut, expansion_edit.toPlainText(), description_edit.text(), dialog))
                buttons_layout.addWidget(save_btn)
                
                cancel_btn = QPushButton("Cancel")
                cancel_btn.clicked.connect(dialog.reject)
                buttons_layout.addWidget(cancel_btn)
                
                layout.addRow(buttons_layout)
                dialog.setLayout(layout)
                dialog.exec_()
                
    def _save_expansion_changes(self, shortcut: str, expansion: str, description: str, dialog: QDialog):
        """Save changes to an expansion."""
        if not expansion:
            QMessageBox.warning(self, "Invalid Input", "Expansion cannot be empty.")
            return
            
        # For now, we'll just update the expansion text and description
        # In a real implementation, you might want to handle this differently
        QMessageBox.information(self, "Note", "Editing functionality needs implementation.")
        dialog.accept()
        
    def _delete_expansion(self):
        """Delete selected expansion."""
        selected_items = self.expansions_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an expansion to delete.")
            return
            
        row = selected_items[0].row()
        shortcut_item = self.expansions_table.item(row, 0)
        if shortcut_item:
            shortcut = shortcut_item.text()
            
            reply = QMessageBox.question(self, "Confirm Delete", 
                                       f"Are you sure you want to delete the expansion '{shortcut}'?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                if self.expansion_manager.remove_expansion(shortcut):
                    self._refresh_expansions_list()
                    QMessageBox.information(self, "Success", "Expansion deleted successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete expansion.")
                    
    def _toggle_expansion(self):
        """Toggle selected expansion enabled/disabled."""
        # This would need implementation based on your expansion storage
        QMessageBox.information(self, "Note", "Toggle functionality needs implementation.")
        
    def _test_expansion(self):
        """Test the selected expansion."""
        selected_items = self.expansions_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select an expansion to test.")
            return
            
        row = selected_items[0].row()
        shortcut_item = self.expansions_table.item(row, 0)
        if shortcut_item:
            shortcut = shortcut_item.text()
            expansion = self.expansion_manager.get_expansion(shortcut)
            if expansion:
                QMessageBox.information(self, "Test Expansion", 
                                      f"Shortcut: {expansion.shortcut}\nExpansion: {expansion.expansion}")
                
    def _import_expansions(self):
        """Import expansions from file."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Expansions", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                count = 0
                for item in data:
                    if self.expansion_manager.add_expansion(item.get('shortcut', ''), 
                                                           item.get('expansion', ''),
                                                           item.get('description', '')):
                        count += 1
                        
                self._refresh_expansions_list()
                QMessageBox.information(self, "Import Complete", f"Imported {count} expansions.")
                
            except Exception as e:
                QMessageBox.warning(self, "Import Error", f"Failed to import: {e}")
                
    def _export_expansions(self):
        """Export expansions to file."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Expansions", "", "JSON Files (*.json)")
        if file_path:
            try:
                expansions = self.expansion_manager.get_all_expansions()
                data = [exp.__dict__ for exp in expansions]
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
                QMessageBox.information(self, "Export Complete", f"Exported {len(expansions)} expansions.")
                
            except Exception as e:
                QMessageBox.warning(self, "Export Error", f"Failed to export: {e}")
                
    def _save_trigger(self):
        """Save the trigger key configuration."""
        new_trigger = self.trigger_input.text().strip()
        if new_trigger:
            self.config.trigger_key = new_trigger
            self.keyboard_hook.config = self.config
            self.keyboard_hook._trigger_keys = self.keyboard_hook._parse_trigger_keys(new_trigger)
            self._save_config()
            QMessageBox.information(self, "Configuration Saved", f"Trigger key set to: {new_trigger}")
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid trigger key combination.")
            
    def closeEvent(self, event):
        """Handle application close event."""
        self.system_monitor.stop_monitoring()
        self.keyboard_hook.stop_hook()
        event.accept()


def main():
    """Main application entry point."""
    # Ensure config directory exists
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("TextShortcutter")
    app.setOrganizationName("Convenience Culture LLC")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

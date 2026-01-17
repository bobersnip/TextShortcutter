#!/usr/bin/env python3
"""
PopupSelector module for TextShortcutter.

Popup dialog for selecting expansions.
"""

from typing import List, Optional
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QLineEdit, QFormLayout, QGroupBox, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QKeySequence

from models import Shortcut


class PopupSelector(QDialog):
    """Popup dialog for selecting expansions."""
    
    expansion_selected = pyqtSignal(str)
    
    def __init__(self, expansions: List[Shortcut], parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.expansions = expansions
        self.selected_index = 0
        
        self._setup_ui()
        self._setup_keyboard_navigation()
        
    def _setup_ui(self):
        """Setup the popup UI."""
        self.setWindowTitle("TextShortcutter - Select Expansion")
        self.setModal(True)
        
        # Apply modern styling to popup
        popup_style = """
        QDialog {
            background-color: rgba(30, 30, 30, 220);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 60);
        }
        
        QLabel {
            color: #ffffff;
            font-size: 12px;
        }
        
        QLineEdit {
            background-color: rgba(50, 50, 50, 200);
            border: 1px solid rgba(255, 255, 255, 80);
            border-radius: 6px;
            padding: 8px;
            color: #ffffff;
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
        """
        
        self.setStyleSheet(popup_style)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("Select an expansion to paste:")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        
        # Expansions list
        self.list_widget = QTableWidget()
        self.list_widget.setColumnCount(3)
        self.list_widget.setHorizontalHeaderLabels(["Shortcut", "Expansion", "Description"])
        self.list_widget.horizontalHeader().setStretchLastSection(True)
        self.list_widget.verticalHeader().setVisible(False)
        self.list_widget.setSelectionBehavior(QTableWidget.SelectRows)
        self.list_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.list_widget.doubleClicked.connect(self._on_double_click)
        
        self._populate_list()
        layout.addWidget(self.list_widget)
        
        # Footer
        footer_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search expansions...")
        self.search_input.textChanged.connect(self._on_search_changed)
        footer_layout.addWidget(self.search_input)
        
        self.status_label = QLabel(f"Found {len(self.expansions)} expansions")
        footer_layout.addWidget(self.status_label)
        
        layout.addLayout(footer_layout)
        
        self.setLayout(layout)
        self.resize(600, 400)
        
    def _setup_keyboard_navigation(self):
        """Setup keyboard navigation for the popup."""
        self.keyPressEvent = self._on_key_press
        
    def _populate_list(self):
        """Populate the list with expansions."""
        self.list_widget.setRowCount(len(self.expansions))
        
        for i, exp in enumerate(self.expansions):
            self.list_widget.setItem(i, 0, QTableWidgetItem(exp.shortcut))
            self.list_widget.setItem(i, 1, QTableWidgetItem(exp.expansion[:50] + "..." if len(exp.expansion) > 50 else exp.expansion))
            self.list_widget.setItem(i, 2, QTableWidgetItem(exp.description))
            
        if self.expansions:
            self.list_widget.selectRow(0)
            
    def _on_search_changed(self, text: str):
        """Handle search input changes."""
        if not text:
            self.expansions = self.parent().expansion_manager.get_all_expansions()
        else:
            search_lower = text.lower()
            self.expansions = [
                exp for exp in self.parent().expansion_manager.get_all_expansions()
                if search_lower in exp.shortcut.lower() or search_lower in exp.expansion.lower()
            ]
            
        self._populate_list()
        self.status_label.setText(f"Found {len(self.expansions)} expansions")
        
    def _on_double_click(self, index):
        """Handle double-click on an expansion."""
        if index.isValid():
            self._select_expansion(index.row())
            
    def _on_key_press(self, event):
        """Handle keyboard navigation."""
        if event.key() == Qt.Key_Escape:
            self.reject()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.expansions:
                self._select_expansion(self.list_widget.currentRow())
        elif event.key() == Qt.Key_Up:
            current_row = self.list_widget.currentRow()
            if current_row > 0:
                self.list_widget.selectRow(current_row - 1)
        elif event.key() == Qt.Key_Down:
            current_row = self.list_widget.currentRow()
            if current_row < self.list_widget.rowCount() - 1:
                self.list_widget.selectRow(current_row + 1)
                
    def _select_expansion(self, row: int):
        """Select and emit the chosen expansion."""
        if 0 <= row < len(self.expansions):
            expansion = self.expansions[row]
            self.expansion_selected.emit(expansion.expansion)
            self.accept()

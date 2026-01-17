#!/usr/bin/env python3
"""
ExpansionManager module for TextShortcutter.

Manages text expansions and their storage.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import asdict

from models import Shortcut

# Configuration
EXPANSIONS_FILE = Path.home() / ".textshortcutter" / "expansions.json"

logger = logging.getLogger(__name__)


class ExpansionManager:
    """Manages text expansions and their storage."""
    
    def __init__(self, config_file: Path = EXPANSIONS_FILE):
        self.config_file = config_file
        self.expansions: Dict[str, Shortcut] = {}
        self._load_expansions()
        
    def add_expansion(self, shortcut: str, expansion: str, description: str = "") -> bool:
        """Add a new expansion."""
        if not shortcut or not expansion:
            return False
            
        shortcut = shortcut.strip().lower()
        if len(self.expansions) >= 1000:  # Max expansions limit
            return False
            
        self.expansions[shortcut] = Shortcut(
            shortcut=shortcut,
            expansion=expansion,
            description=description,
            enabled=True
        )
        self._save_expansions()
        return True
        
    def remove_expansion(self, shortcut: str) -> bool:
        """Remove an expansion."""
        if shortcut in self.expansions:
            del self.expansions[shortcut]
            self._save_expansions()
            return True
        return False
        
    def get_expansion(self, shortcut: str) -> Optional[Shortcut]:
        """Get an expansion by shortcut."""
        return self.expansions.get(shortcut.lower())
        
    def get_all_expansions(self) -> List[Shortcut]:
        """Get all expansions."""
        return list(self.expansions.values())
        
    def update_expansion_usage(self, shortcut: str):
        """Update usage statistics for an expansion."""
        expansion = self.expansions.get(shortcut.lower())
        if expansion:
            expansion.usage_count += 1
            expansion.last_used = datetime.now().isoformat()
            self._save_expansions()
            
    def _load_expansions(self):
        """Load expansions from file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        shortcut = Shortcut(**item)
                        self.expansions[shortcut.shortcut] = shortcut
        except Exception as e:
            logger.error(f"Error loading expansions: {e}")
            
    def _save_expansions(self):
        """Save expansions to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                data = [asdict(exp) for exp in self.expansions.values()]
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving expansions: {e}")

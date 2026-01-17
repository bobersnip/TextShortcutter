#!/usr/bin/env python3
"""
Models for TextShortcutter application.

Contains dataclasses and models used throughout the application.
"""

from dataclasses import dataclass, asdict, astuple
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class Shortcut:
    """Represents a text shortcut/expansion pair."""
    shortcut: str
    expansion: str
    description: str = ""
    enabled: bool = True
    usage_count: int = 0
    last_used: Optional[str] = None


@dataclass
class Config:
    """Application configuration."""
    trigger_key: str = "ctrl+space"
    security_level: int = 5
    privacy_mode: bool = False
    auto_start: bool = False
    safe_applications: List[str] = None  # type: ignore
    blocked_applications: List[str] = None  # type: ignore
    max_expansions: int = 1000
    
    def __post_init__(self):
        if self.safe_applications is None:
            self.safe_applications = []
        if self.blocked_applications is None:
            self.blocked_applications = []

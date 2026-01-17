#!/usr/bin/env python3
"""
Basic test script for TextShortcutter
"""

import sys
import os
import json
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from main import ExpansionManager, Config, Shortcut

def test_expansion_manager():
    """Test the expansion manager functionality."""
    print("Testing ExpansionManager...")
    
    # Create a test config file
    test_config_dir = Path.home() / ".textshortcutter_test"
    test_expansions_file = test_config_dir / "test_expansions.json"
    
    # Create manager
    manager = ExpansionManager(test_expansions_file)
    
    # Test adding expansions
    assert manager.add_expansion("omg", "Oh my gosh!", "Casual expression")
    assert manager.add_expansion("brb", "Be right back", "Quick response")
    assert manager.add_expansion("thx", "Thanks", "Gratitude")
    
    # Test getting expansions
    omg = manager.get_expansion("omg")
    assert omg is not None
    assert omg.expansion == "Oh my gosh!"
    assert omg.description == "Casual expression"
    
    # Test getting all expansions
    all_expansions = manager.get_all_expansions()
    assert len(all_expansions) == 3
    
    # Test usage tracking
    manager.update_expansion_usage("omg")
    omg_updated = manager.get_expansion("omg")
    assert omg_updated is not None
    assert omg_updated.usage_count == 1
    assert omg_updated.last_used is not None
    
    # Test removing expansion
    assert manager.remove_expansion("brb")
    assert manager.get_expansion("brb") is None
    
    # Test file persistence
    manager2 = ExpansionManager(test_expansions_file)
    omg_from_file = manager2.get_expansion("omg")
    assert omg_from_file is not None
    assert omg_from_file.expansion == "Oh my gosh!"
    
    print("✓ ExpansionManager tests passed!")
    
    # Cleanup
    if test_expansions_file.exists():
        test_expansions_file.unlink()
    if test_config_dir.exists():
        test_config_dir.rmdir()

def test_config():
    """Test the configuration functionality."""
    print("Testing Config...")
    
    # Test default config
    config = Config()
    assert config.trigger_key == "ctrl+space"
    assert config.security_level == 5
    assert config.privacy_mode == False
    
    # Test config serialization
    config_dict = {
        'trigger_key': 'alt+space',
        'security_level': 8,
        'privacy_mode': True,
        'safe_applications': ['Chrome', 'Firefox'],
        'blocked_applications': ['Notepad']
    }
    
    config2 = Config(**config_dict)
    assert config2.trigger_key == 'alt+space'
    assert config2.security_level == 8
    assert config2.privacy_mode == True
    assert 'Chrome' in config2.safe_applications
    assert 'Notepad' in config2.blocked_applications
    
    print("✓ Config tests passed!")

def test_dataclasses():
    """Test dataclass functionality."""
    print("Testing dataclasses...")
    
    # Test Shortcut dataclass
    shortcut = Shortcut(
        shortcut="test",
        expansion="This is a test",
        description="Test shortcut",
        enabled=True
    )
    
    assert shortcut.shortcut == "test"
    assert shortcut.expansion == "This is a test"
    assert shortcut.description == "Test shortcut"
    assert shortcut.enabled == True
    assert shortcut.usage_count == 0
    assert shortcut.last_used is None
    
    # Test serialization
    shortcut_dict = {
        'shortcut': 'test2',
        'expansion': 'Another test',
        'description': 'Another test shortcut',
        'enabled': False,
        'usage_count': 5,
        'last_used': '2023-01-01T12:00:00'
    }
    
    shortcut2 = Shortcut(**shortcut_dict)
    assert shortcut2.shortcut == 'test2'
    assert shortcut2.expansion == 'Another test'
    assert shortcut2.enabled == False
    assert shortcut2.usage_count == 5
    assert shortcut2.last_used == '2023-01-01T12:00:00'
    
    print("✓ Dataclass tests passed!")

def main():
    """Run all tests."""
    print("Running TextShortcutter basic tests...\n")
    
    try:
        test_dataclasses()
        test_config()
        test_expansion_manager()
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

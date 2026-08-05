#      TinyType is a minimal typing test software that sits in the corner of your screen while you work!
#      Copyright (C) 2026  Jon Evans
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Dict, Any
import json
import os
from PySide6.QtGui import QColor


class Config:
    """Manages application configuration and settings persistence."""
    
    def __init__(self, config_path: str = "data/config.json") -> None:
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path: str = config_path
        self.settings: Dict[str, Any] = self._load_defaults()
        self.load()
    
    def _load_defaults(self) -> Dict[str, Any]:
        """
        Load default configuration settings.
        
        Returns:
            Dictionary of default settings
        """
        return {
            "font_family": "Consolas",
            "font_size": 24,
            "untyped_color": "#808080",
            "typed_color": "#00FF00",
            "error_color": "#FF0000",
            "bg_opacity": 128,
            "move_per_word": False,
            "position": "top_center",
            "typing_width": 1200,
            "typing_height": 120,
            "show_border": False,
            "active_test": 0,
            "use_random": False,
            "typing_tests": [
                {"name": "Default", "text": ""}
            ],
            "hotkey_increase_opacity": "Ctrl+Up",
            "hotkey_decrease_opacity": "Ctrl+Down"
        }
    
    def load(self) -> None:
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                loaded: Dict[str, Any] = json.load(f)
                self.settings.update(loaded)
    
    def save(self) -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.settings[key] = value

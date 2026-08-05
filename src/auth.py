"""
Google OAuth authentication module via Cloudflare Worker.
"""
from typing import Optional, Dict, Any
import os
import json
import webbrowser
import time
import requests


class GoogleAuth:
    """Handles Google OAuth authentication via server proxy."""
    
    def __init__(
        self,
        oauth_server: str = "https://tinytype-oauth.YOUR-SUBDOMAIN.workers.dev",
        token_path: str = "data/token.json"
    ) -> None:
        """
        Initialize Google authentication.
        
        Args:
            oauth_server: URL of OAuth proxy server
            token_path: Path to store token
        """
        self.oauth_server: str = oauth_server
        self.token_path: str = token_path
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user_email: Optional[str] = None
        self._load_tokens()
    
    def _load_tokens(self) -> None:
        """Load stored tokens from disk."""
        if os.path.exists(self.token_path):
            with open(self.token_path, 'r') as f:
                data: Dict[str, Any] = json.load(f)
                self.access_token = data.get('access_token')
                self.refresh_token = data.get('refresh_token')
                self.user_email = data.get('user_email')
    
    def _save_tokens(self) -> None:
        """Save tokens to disk."""
        os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
        data: Dict[str, str] = {
            'access_token': self.access_token or '',
            'refresh_token': self.refresh_token or '',
            'user_email': self.user_email or ''
        }
        with open(self.token_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def login(self) -> bool:
        """
        Perform Google OAuth login via browser.
        
        Returns:
            True if login successful, False otherwise
        """
        if self.is_logged_in():
            return True
        
        if self.refresh_token:
            if self._refresh_access_token():
                return True
        
        auth_url: str = f"{self.oauth_server}/auth/start"
        
        webbrowser.open(auth_url)
        
        from PySide6.QtWidgets import QMessageBox, QInputDialog
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Login in Progress")
        msg.setText(
            "Your browser has been opened for Google login.\n\n"
            "After completing login, the browser will show a success message.\n"
            "Click OK once you see the success message."
        )
        msg.exec()
        
        return self._check_login_status()
    
    def _check_login_status(self) -> bool:
        """
        Check if login was successful.
        
        Returns:
            True if logged in, False otherwise
        """
        return self.is_logged_in()
    
    def _refresh_access_token(self) -> bool:
        """
        Refresh access token using refresh token.
        
        Returns:
            True if refresh successful, False otherwise
        """
        if not self.refresh_token:
            return False
        
        try:
            response = requests.post(
                f"{self.oauth_server}/auth/refresh",
                json={'refresh_token': self.refresh_token},
                timeout=10
            )
            
            if response.status_code == 200:
                data: Dict[str, Any] = response.json()
                self.access_token = data.get('access_token')
                self._save_tokens()
                self._get_user_info()
                return True
        except Exception:
            pass
        
        return False
    
    def _get_user_info(self) -> None:
        """Fetch user email from Google."""
        if not self.access_token:
            return
        
        try:
            response = requests.get(
                f"{self.oauth_server}/auth/userinfo",
                headers={'Authorization': f'Bearer {self.access_token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                data: Dict[str, Any] = response.json()
                self.user_email = data.get('email')
                self._save_tokens()
        except Exception:
            pass
    
    def update_tokens(
        self,
        access_token: str,
        refresh_token: str,
        user_email: str
    ) -> None:
        """
        Update tokens from OAuth callback.
        
        Args:
            access_token: OAuth access token
            refresh_token: OAuth refresh token
            user_email: User email address
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_email = user_email
        self._save_tokens()
    
    def logout(self) -> None:
        """Logout and remove stored credentials."""
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
        self.access_token = None
        self.refresh_token = None
        self.user_email = None
    
    def is_logged_in(self) -> bool:
        """
        Check if user is logged in.
        
        Returns:
            True if logged in, False otherwise
        """
        return self.access_token is not None

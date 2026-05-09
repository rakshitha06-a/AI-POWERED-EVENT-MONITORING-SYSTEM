import streamlit as st
import sqlite3
from datetime import datetime
import secrets

def check_authentication():
    """Check if user is authenticated"""
    if not st.session_state.get('authenticated', False):
        st.error("🔒 Access denied. Please login first.")
        st.info("Redirecting to login page...")
        st.switch_page("pages/1_Login.py")
        return False
    return True

def verify_session():
    """Verify if the current session is valid"""
    if not st.session_state.get('session_token'):
        return False
    
    conn = sqlite3.connect('admin_auth.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.id, s.expires_at, u.username, u.role 
        FROM sessions s 
        JOIN users u ON s.user_id = u.id 
        WHERE s.session_token = ? AND s.expires_at > ?
    ''', (st.session_state.session_token, datetime.now()))
    
    session = cursor.fetchone()
    conn.close()
    
    if session:
        return True
    else:
        # Clear invalid session
        st.session_state.clear()
        return False

def require_auth():
    """Decorator to require authentication for pages"""
    if not check_authentication():
        st.stop()
    
    if not verify_session():
        st.error("🔒 Session expired. Please login again.")
        st.info("Redirecting to login page...")
        st.switch_page("pages/1_Login.py")
        st.stop()

def log_user_action(action):
    """Log user actions for audit trail"""
    if st.session_state.get('user_id'):
        conn = sqlite3.connect('admin_auth.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (user_id, action, ip_address)
            VALUES (?, ?, ?)
        ''', (st.session_state.user_id, action, "web"))
        
        conn.commit()
        conn.close()

def logout():
    """Logout user and clear session"""
    if st.session_state.get('session_token'):
        # Remove session from database
        conn = sqlite3.connect('admin_auth.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM sessions WHERE session_token = ?', 
                      (st.session_state.session_token,))
        
        conn.commit()
        conn.close()
        
        # Log logout action
        log_user_action("logout")
    
    # Clear session state
    st.session_state.clear()
    
    st.success("✅ Logged out successfully!")
    st.info("Redirecting to login page...")
    st.switch_page("pages/1_Login.py")

def get_user_info():
    """Get current user information (Hardcoded for bypassed login)"""
    return {
        'user_id': 1,
        'username': 'admin',
        'role': 'admin'
    }

def is_admin():
    """Check if current user is admin"""
    user_info = get_user_info()
    return user_info and user_info['role'] == 'admin' 
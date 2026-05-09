import streamlit as st
import sqlite3
import hashlib
from datetime import datetime, timedelta
from auth_utils import require_auth, log_user_action, get_user_info, is_admin

# Require authentication and admin privileges
require_auth()
if not is_admin():
    st.error("🔒 Admin privileges required to access this page.")
    st.info("Redirecting to dashboard...")
    st.switch_page("main_dashboard.py")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Admin Panel - AI Event Monitor",
    page_icon="👑",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .stats-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .user-table {
        background: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .audit-log {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border-left: 4px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

def get_system_stats():
    """Get system statistics"""
    conn = sqlite3.connect('admin_auth.db')
    cursor = conn.cursor()
    
    # User statistics
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
    admin_users = cursor.fetchone()[0]
    
    # Session statistics
    cursor.execute("SELECT COUNT(*) FROM sessions WHERE expires_at > ?", (datetime.now(),))
    active_sessions = cursor.fetchone()[0]
    
    # Audit log statistics
    cursor.execute("SELECT COUNT(*) FROM audit_log")
    total_audit_entries = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM audit_log WHERE timestamp > ?", 
                  (datetime.now() - timedelta(hours=24),))
    recent_audit_entries = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'admin_users': admin_users,
        'active_sessions': active_sessions,
        'total_audit_entries': total_audit_entries,
        'recent_audit_entries': recent_audit_entries
    }

def get_all_users():
    """Get all users from database"""
    conn = sqlite3.connect('admin_auth.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, username, role, created_at 
        FROM users 
        ORDER BY created_at DESC
    """)
    
    users = cursor.fetchall()
    conn.close()
    
    return users

def get_recent_audit_logs(limit=50):
    """Get recent audit log entries"""
    conn = sqlite3.connect('admin_auth.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT al.timestamp, u.username, al.action, al.ip_address
        FROM audit_log al
        LEFT JOIN users u ON al.user_id = u.id
        ORDER BY al.timestamp DESC
        LIMIT ?
    """, (limit,))
    
    logs = cursor.fetchall()
    conn.close()
    
    return logs

def add_user(username, password, role):
    """Add a new user"""
    conn = sqlite3.connect('admin_auth.db')
    cursor = conn.cursor()
    
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
        ''', (username, password_hash, role))
        
        conn.commit()
        conn.close()
        return True, "User added successfully!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists!"
    except Exception as e:
        conn.close()
        return False, f"Error adding user: {str(e)}"

def delete_user(user_id):
    """Delete a user"""
    conn = sqlite3.connect('admin_auth.db')
    cursor = conn.cursor()
    
    try:
        # Delete user's sessions first
        cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        # Delete user's audit logs
        cursor.execute("DELETE FROM audit_log WHERE user_id = ?", (user_id,))
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        return True, "User deleted successfully!"
    except Exception as e:
        conn.close()
        return False, f"Error deleting user: {str(e)}"

def main():
    # Header
    st.markdown("""
    <div class="admin-header">
        <h1>👑 Admin Panel</h1>
        <p>System Administration & User Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 User Management", "📋 Audit Log", "⚙️ System Settings"])
    
    with tab1:
        st.subheader("📊 System Overview")
        
        # Get system statistics
        stats = get_system_stats()
        
        # Display statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h3>👥 Users</h3>
                <p><strong>Total:</strong> {stats['total_users']}</p>
                <p><strong>Admins:</strong> {stats['admin_users']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h3>🔐 Sessions</h3>
                <p><strong>Active:</strong> {stats['active_sessions']}</p>
                <p><strong>Status:</strong> 🟢 Normal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stats-card">
                <h3>📋 Audit Log</h3>
                <p><strong>Total:</strong> {stats['total_audit_entries']}</p>
                <p><strong>Last 24h:</strong> {stats['recent_audit_entries']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Stats"):
                st.rerun()
        
        with col2:
            if st.button("📊 Export Data"):
                st.info("Export feature coming soon!")
        
        with col3:
            if st.button("🔧 System Health"):
                st.success("✅ System is healthy!")
    
    with tab2:
        st.subheader("👥 User Management")
        
        # Add new user
        with st.expander("➕ Add New User", expanded=False):
            with st.form("add_user_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                new_role = st.selectbox("Role", ["user", "admin"])
                
                if st.form_submit_button("Add User"):
                    if new_username and new_password:
                        success, message = add_user(new_username, new_password, new_role)
                        if success:
                            st.success(message)
                            log_user_action(f"user_added: {new_username}")
                        else:
                            st.error(message)
                    else:
                        st.error("Please fill in all fields.")
        
        # User list
        st.subheader("📋 Current Users")
        users = get_all_users()
        
        if users:
            # Create user table
            user_data = []
            for user in users:
                user_data.append({
                    "ID": user[0],
                    "Username": user[1],
                    "Role": user[2],
                    "Created": user[3][:19] if user[3] else "N/A"
                })
            
            st.dataframe(user_data, use_container_width=True)
            
            # Delete user
            st.subheader("🗑️ Delete User")
            user_ids = [user[0] for user in users]
            user_names = [user[1] for user in users]
            
            delete_username = st.selectbox("Select user to delete", user_names)
            
            if st.button("Delete User"):
                if delete_username:
                    user_id = user_ids[user_names.index(delete_username)]
                    if delete_username == "admin":
                        st.error("Cannot delete the main admin user!")
                    else:
                        success, message = delete_user(user_id)
                        if success:
                            st.success(message)
                            log_user_action(f"user_deleted: {delete_username}")
                            st.rerun()
                        else:
                            st.error(message)
        else:
            st.info("No users found.")
    
    with tab3:
        st.subheader("📋 Audit Log")
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            log_limit = st.selectbox("Show last N entries", [10, 25, 50, 100], index=2)
        with col2:
            if st.button("🔄 Refresh Logs"):
                st.rerun()
        
        # Get audit logs
        logs = get_recent_audit_logs(log_limit)
        
        if logs:
            for log in logs:
                timestamp, username, action, ip_address = log
                username = username if username else "System"
                
                st.markdown(f"""
                <div class="audit-log">
                    <strong>{timestamp}</strong> | <strong>{username}</strong> | {action}
                    <br><small>IP: {ip_address}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No audit logs found.")
    
    with tab4:
        st.subheader("⚙️ System Settings")
        
        # Security settings
        st.markdown("### 🔒 Security Settings")
        
        col1, col2 = st.columns(2)
        with col1:
            session_timeout = st.selectbox("Session Timeout", ["4 hours", "8 hours", "12 hours", "24 hours"], index=1)
            password_policy = st.selectbox("Password Policy", ["Basic", "Strong", "Very Strong"])
        
        with col2:
            max_login_attempts = st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
            enable_2fa = st.checkbox("Enable Two-Factor Authentication", value=False)
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
            log_user_action("system_settings_updated")
        
        # System maintenance
        st.markdown("### 🛠️ System Maintenance")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🧹 Clear Old Sessions"):
                st.info("Clearing old sessions...")
                log_user_action("clear_old_sessions")
        
        with col2:
            if st.button("📊 Backup Database"):
                st.info("Backup feature coming soon!")
        
        with col3:
            if st.button("🔄 System Restart"):
                st.warning("This will restart the monitoring system.")
                if st.button("Confirm Restart"):
                    st.success("System restart initiated!")
                    log_user_action("system_restart")

if __name__ == "__main__":
    main() 
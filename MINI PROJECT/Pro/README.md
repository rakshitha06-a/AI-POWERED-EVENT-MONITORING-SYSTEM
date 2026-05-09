# 🎥 AI-POWERED-EVENT-MONITORING-SYSTEM

A real-time AI-powered crowd management and event monitoring system with **secure admin authentication** that detects fire/smoke, crowd surges, and unconscious persons using computer vision and machine learning.

## 🚀 Features

- **🔐 Secure Authentication**: Admin login system with session management
- **🔥 Fire/Smoke Detection**: Real-time detection of fire and smoke using color-based analysis
- **🚨 Crowd Surge Detection**: Monitors crowd density using YOLOv8 object detection with grid-based analysis
- **🧍‍♂️ Unconscious Person Detection**: Detects fallen or unconscious persons using pose analysis
- **📊 Real-time Dashboard**: Beautiful Streamlit interface with live video feed and alert system
- **⚙️ Configurable Settings**: Adjustable detection sensitivity and camera selection
- **📈 Statistics Tracking**: Monitor detection counts and system performance
- **👑 Admin Panel**: User management, audit logging, and system administration
- **🔒 Security Features**: Password hashing, session management, access control

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Webcam or camera device
- CUDA-compatible GPU (optional, for faster inference)

### Setup Instructions

1. **Navigate to the project directory**
   ```bash
   cd event_monitor_dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test the system**
   ```bash
   python test_models.py
   ```

4. **Run the system**
   ```bash
   streamlit run run_system.py
   ```

## 🔐 Authentication

### Default Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

### Security Features
- **Password Hashing**: SHA-256 encryption
- **Session Management**: 8-hour session timeout
- **Audit Logging**: All actions are logged
- **Access Control**: Role-based permissions

## 🎯 Usage

### Starting the System

1. **Run the launcher:**
   ```bash
   streamlit run run_system.py
   ```

2. **Access the login page:**
   - Go to `http://localhost:8501`
   - Click "Go to Login" or navigate to the login page

3. **Authenticate as admin:**
   - Enter username: `admin`
   - Enter password: `admin123`
   - Click "Login"

### Dashboard Interface

- **📹 Live Camera Feed**: Real-time video stream from your camera
- **🚨 Alert Panel**: Shows active alerts and system status
- **📊 Statistics**: Tracks detection counts and performance metrics
- **⚙️ Controls**: Camera selection and sensitivity settings
- **👤 User Management**: Admin features for user management

### Admin Features

#### User Management
- Add new users (admin/standard)
- Delete existing users
- View all users and their roles
- Manage user permissions

#### Audit Logging
- View all system activities
- Track user actions
- Monitor login attempts
- Export audit data

#### System Settings
- Configure security settings
- Manage session timeouts
- System maintenance tools
- Backup and restore

### Detection Models

#### Fire/Smoke Detection
- Uses HSV color space analysis
- Detects orange/yellow colors associated with fire
- Configurable sensitivity threshold

#### Crowd Surge Detection
- Uses YOLOv8 for person detection
- Grid-based analysis to monitor crowd density
- Alerts when too many people are in a single area

#### Unconscious Person Detection
- Uses YOLOv8 for person detection
- Analyzes person orientation (horizontal = potentially fallen)
- Confidence-based detection to reduce false positives

## 🔧 Configuration

### Detection Sensitivity
- **Fire Detection**: Adjust threshold (1000-5000) for fire/smoke sensitivity
- **Crowd Surge**: Set threshold (1-10) for maximum people per grid segment

### Camera Settings
- Select from multiple camera sources (0, 1, 2)
- Automatic camera detection and fallback

### Security Settings
- Session timeout configuration
- Password policy settings
- Login attempt limits
- Two-factor authentication (coming soon)

## 🐛 Troubleshooting

### Common Issues

1. **Authentication problems**
   - Verify default credentials: admin/admin123
   - Check if database file exists
   - Clear browser cache and cookies

2. **Camera not working**
   - Check if camera is connected and not in use by another application
   - Try different camera indices (0, 1, 2)
   - Ensure camera permissions are granted

3. **Models not loading**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check internet connection (models are downloaded automatically)
   - Verify CUDA installation if using GPU

4. **Performance issues**
   - Reduce detection frequency by modifying the frame skip in `main_dashboard.py`
   - Use a smaller YOLO model (change `yolov8n.pt` to `yolov8s.pt` for faster inference)
   - Ensure adequate CPU/GPU resources

### Testing

Run the test script to verify all components:
```bash
python test_models.py
```

This will test:
- Camera access
- Fire/smoke detection
- Crowd surge detection
- Unconscious person detection

## 📁 Project Structure

```
event_monitor_dashboard/
├── run_system.py           # Main launcher script
├── login.py               # Authentication login page
├── main_dashboard.py      # Main monitoring dashboard
├── admin_panel.py         # Admin management panel
├── auth_utils.py          # Authentication utilities
├── test_models.py         # Test script for all models
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── models/
    ├── __init__.py       # Package initialization
    ├── fire_smoke.py     # Fire/smoke detection model
    ├── crowd_surge.py    # Crowd surge detection model
    └── unconscious.py    # Unconscious person detection model
```

## 🔒 Security Considerations

- **Change default credentials** immediately after first login
- **Use strong passwords** for admin accounts
- **Regularly review audit logs** for suspicious activity
- **Implement network security** (firewall, VPN) for production deployment
- **Backup authentication database** regularly
- **Monitor session activity** for unauthorized access

## 🤝 Contributing

To improve the system:

1. Test with different lighting conditions
2. Adjust detection thresholds for your specific use case
3. Add new detection models as needed
4. Improve the UI/UX based on user feedback
5. Enhance security features
6. Add additional admin capabilities

## 📄 License

This project is for educational and monitoring purposes. Please ensure compliance with local regulations when deploying in production environments.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the test script to identify specific problems
3. Verify all dependencies are correctly installed
4. Check camera permissions and connectivity
5. Review authentication database integrity

---

**🎉 Enjoy your secure AI-powered event monitoring system!** 
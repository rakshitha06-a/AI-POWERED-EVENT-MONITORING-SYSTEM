# 🎥 AI-POWERED EVENT MONITORING SYSTEM

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)]()
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/rakshitha06-a/AI-POWERED-EVENT-MONITORING-SYSTEM)

A real-time AI-powered crowd management and event monitoring system with **secure admin authentication** that detects fire/smoke, crowd surges, and unconscious persons using computer vision and machine learning.

**[🌐 View on GitHub](https://github.com/rakshitha06-a/AI-POWERED-EVENT-MONITORING-SYSTEM)** | **[📧 Contact](#support)**

---

## 📋 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Authentication](#-authentication)
- [Usage Guide](#-usage)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Project Structure](#-project-structure)
- [Security](#-security-considerations)
- [Contributing](#-contributing)

---

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

1. **Clone the repository** (if working from GitHub)
   ```bash
   git clone https://github.com/rakshitha06-a/AI-POWERED-EVENT-MONITORING-SYSTEM.git
   cd AI-POWERED-EVENT-MONITORING-SYSTEM/event_monitor_dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test the system**
   ```bash
   python test_models.py
   ```

5. **Run the system**
   ```bash
   streamlit run run_system.py
   ```

---

## ⚡ Quick Start

### Get running in 3 steps:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the system
streamlit run run_system.py

# 3. Login with default credentials
# Username: admin
# Password: admin123
```

Access the system at: **http://localhost:8501**

---

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

```bash
streamlit run run_system.py
```

Then:
1. 🌐 Access: `http://localhost:8501`
2. 🔑 Login with credentials:
   - Username: `admin`
   - Password: `admin123`
3. ✅ Click "Login"

### Dashboard Interface

| Feature | Description |
|---------|-------------|
| **📹 Live Camera Feed** | Real-time video stream from your camera |
| **🚨 Alert Panel** | Active alerts and system status |
| **📊 Statistics** | Detection counts and performance metrics |
| **⚙️ Controls** | Camera selection and sensitivity settings |
| **👤 User Management** | Admin features for user control |

### 👑 Admin Features

#### User Management
- ➕ Add new users (admin/standard roles)
- ➖ Delete existing users
- 👥 View all users and their roles
- 🔐 Manage user permissions

#### 📋 Audit Logging
- 📝 View all system activities
- 👤 Track user actions
- 🔓 Monitor login attempts
- 📊 Export audit data

#### ⚙️ System Settings
- 🔒 Configure security settings
- ⏱️ Manage session timeouts
- 🛠️ System maintenance tools
- 💾 Backup and restore

### 🤖 Detection Models

#### 🔥 Fire/Smoke Detection
- **Technology**: HSV color space analysis
- **Detection**: Orange/yellow colors associated with fire
- **Customization**: Adjustable sensitivity threshold
- **Performance**: Real-time detection

#### 🚨 Crowd Surge Detection
- **Technology**: YOLOv8 object detection
- **Method**: Grid-based density analysis
- **Alert Trigger**: When people exceed grid threshold
- **Use Case**: Event safety monitoring

#### 🧍 Unconscious Person Detection
- **Technology**: YOLOv8 + pose analysis
- **Detection**: Horizontal orientation = fallen person
- **Accuracy**: Confidence-based filtering
- **Response**: Immediate alert notification

---

## 🔧 Configuration

### Detection Sensitivity

| Setting | Range | Recommendation |
|---------|-------|-----------------|
| **Fire Detection** | 1000-5000 | Adjust for lighting conditions |
| **Crowd Surge** | 1-10 persons/grid | Based on venue capacity |
| **Confidence Threshold** | 0.5-0.95 | Balance accuracy vs speed |

### Camera Settings
- Select from multiple camera sources (0, 1, 2, etc.)
- Automatic camera detection with fallback
- Resolution customization
- FPS optimization

### Security Settings
- ⏱️ Session timeout configuration (default: 8 hours)
- 🔐 Password policy settings
- 🚫 Login attempt limits
- 🔑 Two-factor authentication (coming soon)

---

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **🔑 Authentication Failed** | Verify credentials (admin/admin123), clear browser cache, check database file |
| **📷 Camera Not Working** | Verify camera connection, try different indices (0,1,2), grant permissions |
| **📦 Models Not Loading** | Run `pip install -r requirements.txt`, check internet, verify CUDA setup |
| **🐌 Performance Slow** | Reduce frame skip, use smaller YOLO model, check CPU/GPU resources |
| **🚨 False Alerts** | Adjust sensitivity thresholds, improve lighting, test in controlled environment |

### Quick Diagnostics

```bash
# Test all components
python test_models.py

# Check dependencies
pip list | grep -E "streamlit|opencv|torch|ultralytics"

# Verify camera access
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Testing

Run the comprehensive test script:
```bash
python test_models.py
```

Tests included:
- ✅ Camera access verification
- ✅ Fire/smoke detection
- ✅ Crowd surge detection
- ✅ Unconscious person detection
- ✅ Model loading and inference

## 📁 Project Structure

```
event_monitor_dashboard/
├── run_system.py              # Main launcher script
├── login.py                  # Authentication login page
├── main_dashboard.py         # Main monitoring dashboard
├── admin_panel.py            # Admin management panel
├── auth_utils.py             # Authentication utilities
├── test_models.py            # Test script for all models
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── yolov8n.pt                # YOLOv8 model weights
│
└── models/
    ├── __init__.py           # Package initialization
    ├── fire_smoke.py         # Fire/smoke detection model
    ├── crowd_surge.py        # Crowd surge detection model
    └── unconscious.py        # Unconscious person detection model

└── utils/
    ├── __init__.py
    └── loggger.py            # Logging utilities
```

---

## 🔒 Security Considerations

- **Change default credentials** immediately after first login
- **Use strong passwords** for admin accounts
- **Regularly review audit logs** for suspicious activity
- **Implement network security** (firewall, VPN) for production deployment
- **Backup authentication database** regularly
- **Monitor session activity** for unauthorized access
- **Keep dependencies updated** for security patches

---

## 🤝 Contributing

To improve the system:

1. Test with different lighting conditions
2. Adjust detection thresholds for your specific use case
3. Add new detection models as needed
4. Improve the UI/UX based on user feedback
5. Enhance security features
6. Add additional admin capabilities
7. Report bugs and suggest improvements

---

## 📄 License

This project is for educational and monitoring purposes. Please ensure compliance with local regulations when deploying in production environments.

**License Type**: MIT License

---

## 🆘 Support

### Getting Help

If you encounter issues:

1. ✅ Check the [troubleshooting section](#-troubleshooting) above
2. 🧪 Run the test script: `python test_models.py`
3. 📋 Verify all dependencies: `pip install -r requirements.txt`
4. 📷 Test camera connectivity and permissions
5. 🔍 Review authentication database integrity

### Contact

- **GitHub**: [AI-POWERED-EVENT-MONITORING-SYSTEM](https://github.com/rakshitha06-a/AI-POWERED-EVENT-MONITORING-SYSTEM)
- **Email**: rakshithaadhirla@gmail.com
- **Issues**: [Report issues on GitHub](https://github.com/rakshitha06-a/AI-POWERED-EVENT-MONITORING-SYSTEM/issues)

---

## 🎉 What's Next?

- 🎬 Record and playback event recordings
- 📱 Mobile app integration
- 🌐 Multi-camera support
- 🧠 Deep learning model improvements
- 📡 Real-time alert notifications (Email/SMS)
- 🔐 Two-factor authentication (2FA)
- 📊 Advanced analytics dashboard

---

**Made with ❤️ by [Rakshitha](https://github.com/rakshitha06-a)**

⭐ If this project helped you, please consider giving it a star on GitHub! 
# 🤖 AI Chatbot Setup Guide

## Overview
The AI Event Monitor now includes a **Gemini-powered chatbot** that can answer queries about:
- Crowd analysis in any direction (North, South, East, West, NE, NW, SE, SW)
- Fire/smoke detection status
- Unconscious person detection
- Historical alert data
- System health monitoring

## 🚀 Quick Setup

### 1. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

### 2. Configure API Key

**Option A: Using Streamlit Secrets (Recommended)**
1. Edit `.streamlit/secrets.toml`
2. Replace `your_gemini_api_key_here` with your actual API key
3. Save the file

**Option B: Using Environment Variable**
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
```

### 3. Install Dependencies
```bash
pip install google-generativeai
```

### 4. Restart Application
```bash
streamlit run main_app.py
```

## 🎯 How to Use

### Accessing the Chatbot
1. Login to the dashboard
2. In the sidebar, click "💬 Open Chat"
3. The chat interface will appear in the main area

### Example Queries
- **"How much crowd is there in the North-east direction?"**
- **"What's the current fire detection status?"**
- **"Show me today's alert statistics"**
- **"Is there any unconscious person detected?"**
- **"What's the overall system status?"**
- **"How many people are in the main area?"**

### Quick Actions
- **📊 System Status**: Get current system statistics
- **📈 Historical Data**: View alert history
- **🗑️ Clear Chat**: Clear conversation history

## 🔧 Features

### Directional Crowd Analysis
The chatbot can analyze crowd density in 8 directions:
- **North**: Top half of the camera view
- **South**: Bottom half of the camera view
- **East**: Right half of the camera view
- **West**: Left half of the camera view
- **Northeast**: Top-right quadrant
- **Northwest**: Top-left quadrant
- **Southeast**: Bottom-right quadrant
- **Southwest**: Bottom-left quadrant

### Real-time Data Integration
- Connects to live monitoring data
- Accesses historical alert logs
- Provides system health information
- Integrates with all detection models

### Intelligent Responses
- Context-aware responses
- Professional and helpful tone
- Actionable recommendations
- Error handling and fallbacks

## 🛠️ Troubleshooting

### Common Issues

**1. "AI Assistant not available"**
- Install the required package: `pip install google-generativeai`
- Restart the application

**2. "Please configure Gemini API key"**
- Follow the setup steps above
- Ensure the API key is correctly set in secrets or environment

**3. "API Error"**
- Verify your API key is valid
- Check internet connection
- Ensure you have sufficient API quota

**4. Chat not responding**
- Check if monitoring is active
- Verify camera access
- Restart the application

### API Limits
- Gemini API has rate limits
- Free tier: 15 requests per minute
- Paid tier: Higher limits available

## 🔒 Security

### API Key Security
- Never commit API keys to version control
- Use Streamlit secrets or environment variables
- Rotate keys regularly
- Monitor API usage

### Data Privacy
- Chat history is stored locally in session
- No data is sent to external services except Gemini API
- All monitoring data remains private

## 📊 Advanced Usage

### Custom Queries
You can ask complex questions like:
- "What was the peak crowd density in the last hour?"
- "Are there any patterns in fire detection alerts?"
- "Which direction has the most consistent crowd flow?"

### Integration with Monitoring
- Chatbot works alongside live monitoring
- Real-time data integration
- Historical analysis capabilities
- System status monitoring

## 🎉 Success!

Once configured, you'll have a powerful AI assistant that can:
- Answer questions about crowd management
- Provide directional analysis
- Monitor system health
- Give actionable insights
- Help with emergency situations

The chatbot makes your event monitoring system even more intelligent and user-friendly! 🚀 
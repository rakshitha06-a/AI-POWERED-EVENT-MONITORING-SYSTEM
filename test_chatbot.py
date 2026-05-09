#!/usr/bin/env python3
"""
Test script for the Gemini-powered chatbot
"""

import os
import sys
from chatbot import EventMonitorChatbot

def test_chatbot():
    """Test the chatbot functionality"""
    print("🤖 Testing Gemini Chatbot Integration")
    print("=" * 50)
    
    # Get API key from environment or secrets
    api_key = "AIzaSyDkZgeLXhKJrjclXXv27YDv0U_2o8meE6c"
    
    if not api_key or api_key == "your_gemini_api_key_here":
        print("❌ Error: No valid API key found")
        print("Please set your Gemini API key in .streamlit/secrets.toml")
        return False
    
    try:
        # Initialize chatbot
        print("🔧 Initializing chatbot...")
        chatbot = EventMonitorChatbot(api_key)
        print("✅ Chatbot initialized successfully!")
        
        # Test system status
        print("\n📊 Testing system status...")
        status = chatbot.get_system_status()
        print(f"System Status: {status['system_status']}")
        print(f"Active Sessions: {status['active_sessions']}")
        print(f"Recent Alerts: {status['recent_alerts']}")
        
        # Test basic query
        print("\n💬 Testing basic query...")
        test_query = "What's the current system status?"
        response = chatbot.process_query(test_query)
        print(f"Query: {test_query}")
        print(f"Response: {response[:200]}...")  # Show first 200 chars
        
        # Test directional query
        print("\n🧭 Testing directional query...")
        test_query = "How much crowd is there in the North-east direction?"
        response = chatbot.process_query(test_query)
        print(f"Query: {test_query}")
        print(f"Response: {response[:200]}...")
        
        # Test historical data
        print("\n📈 Testing historical data...")
        history = chatbot.get_historical_data(hours=1)
        print(f"Historical Data: {history}")
        
        print("\n🎉 All tests passed! Chatbot is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing chatbot: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        # Provide specific guidance for common errors
        if "404" in str(e) and "models" in str(e):
            print("\n🔧 This might be a model name issue. Trying alternative models...")
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                
                # List available models
                print("📋 Available models:")
                for model in genai.list_models():
                    if 'generateContent' in model.supported_generation_methods:
                        print(f"  - {model.name}")
                
            except Exception as list_error:
                print(f"Could not list models: {list_error}")
        
        return False

def main():
    """Main test function"""
    print("🚀 AI Event Monitor - Chatbot Test")
    print("=" * 50)
    
    # Check if required packages are installed
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI package is installed")
    except ImportError:
        print("❌ Google Generative AI package not found")
        print("Install with: pip install google-generativeai")
        return
    
    # Run tests
    success = test_chatbot()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Open your browser to the Streamlit app")
        print("2. Login with admin/admin123")
        print("3. Click '💬 Open Chat' in the sidebar")
        print("4. Start asking questions!")
        print("\nExample queries:")
        print("- 'How much crowd is there in the North-east direction?'")
        print("- 'What's the current fire detection status?'")
        print("- 'Show me today's alert statistics'")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key is correct")
        print("2. Ensure internet connection")
        print("3. Verify Gemini API quota")

if __name__ == "__main__":
    main() 
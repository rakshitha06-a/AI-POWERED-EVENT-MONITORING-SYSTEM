import streamlit as st
import google.generativeai as genai
import json
import sqlite3
from datetime import datetime, timedelta
import cv2
import numpy as np
from models.crowd_surge import check_crowd_surge
from models.fire_smoke import check_fire_smoke
from models.unconscious import check_unconscious

class EventMonitorChatbot:
    def __init__(self, api_key):
        """Initialize the chatbot with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.chat_history = []
        self.system_prompt = self._get_system_prompt()
        
    def _get_system_prompt(self):
        """Get the system prompt for the chatbot"""
        return """
        You are an AI Event Monitoring Assistant for a crowd management system. You can help with:

        **System Capabilities:**
        - Real-time crowd monitoring and analysis
        - Fire/smoke detection alerts
        - Unconscious person detection
        - Directional crowd analysis (North, South, East, West, NE, NW, SE, SW)
        - Historical data and statistics
        - System status and health monitoring

        **Available Data Sources:**
        - Live camera feeds from multiple locations
        - Crowd density analysis using YOLOv8
        - Fire/smoke detection using color analysis
        - Unconscious person detection using pose analysis
        - Historical alert logs and statistics
        - System audit logs

        **Response Guidelines:**
        - Be professional and helpful
        - Provide specific, actionable information
        - Use clear, concise language
        - Include relevant statistics when available
        - Suggest appropriate actions based on alerts
        - Acknowledge limitations when data is not available

        **Example Queries You Can Handle:**
        - "How much crowd is there in the North-east direction?"
        - "What's the current fire detection status?"
        - "Show me today's alert statistics"
        - "Is there any unconscious person detected?"
        - "What's the overall system status?"
        - "How many people are in the main area?"

        Always respond as a helpful AI assistant for the event monitoring system.
        """

    def get_system_status(self):
        """Get current system status and statistics"""
        try:
            # Get database statistics
            conn = sqlite3.connect('admin_auth.db')
            cursor = conn.cursor()
            
            # Get recent alerts
            cursor.execute("""
                SELECT action, COUNT(*) as count 
                FROM audit_log 
                WHERE timestamp > ? 
                AND action IN ('fire_alert_detected', 'crowd_surge_alert_detected', 'unconscious_person_alert_detected')
                GROUP BY action
            """, (datetime.now() - timedelta(hours=24),))
            
            recent_alerts = dict(cursor.fetchall())
            
            # Get active sessions
            cursor.execute("SELECT COUNT(*) FROM sessions WHERE expires_at > ?", (datetime.now(),))
            active_sessions = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'recent_alerts': recent_alerts,
                'active_sessions': active_sessions,
                'system_status': 'operational',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {
                'error': str(e),
                'system_status': 'error',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    def analyze_crowd_direction(self, frame, direction):
        """Analyze crowd in a specific direction"""
        try:
            height, width = frame.shape[:2]
            
            # Define directional regions
            regions = {
                'north': (0, 0, width, height//2),
                'south': (0, height//2, width, height),
                'east': (width//2, 0, width, height),
                'west': (0, 0, width//2, height),
                'northeast': (width//2, 0, width, height//2),
                'northwest': (0, 0, width//2, height//2),
                'southeast': (width//2, height//2, width, height),
                'southwest': (0, height//2, width//2, height)
            }
            
            if direction.lower() not in regions:
                return f"Direction '{direction}' not supported. Use: {', '.join(regions.keys())}"
            
            x1, y1, x2, y2 = regions[direction.lower()]
            region_frame = frame[y1:y2, x1:x2]
            
            # Analyze crowd in this region
            crowd_count = self._count_people_in_region(region_frame)
            density = self._calculate_density(crowd_count, (x2-x1)*(y2-y1))
            
            return {
                'direction': direction,
                'crowd_count': crowd_count,
                'density': density,
                'status': 'high' if crowd_count > 10 else 'medium' if crowd_count > 5 else 'low'
            }
            
        except Exception as e:
            return f"Error analyzing {direction} direction: {str(e)}"

    def _count_people_in_region(self, region_frame):
        """Count people in a specific region using YOLOv8"""
        try:
            from ultralytics import YOLO
            model = YOLO("yolov8n.pt")
            results = model(region_frame)
            
            person_count = 0
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    if cls == 0:  # person class
                        person_count += 1
            
            return person_count
        except Exception as e:
            return f"Error counting people: {str(e)}"

    def _calculate_density(self, person_count, area):
        """Calculate crowd density"""
        if area > 0:
            return person_count / (area / 10000)  # people per 10k pixels
        return 0

    def get_historical_data(self, hours=24):
        """Get historical alert data"""
        try:
            conn = sqlite3.connect('admin_auth.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT action, timestamp 
                FROM audit_log 
                WHERE timestamp > ? 
                AND action IN ('fire_alert_detected', 'crowd_surge_alert_detected', 'unconscious_person_alert_detected')
                ORDER BY timestamp DESC
            """, (datetime.now() - timedelta(hours=hours),))
            
            alerts = cursor.fetchall()
            conn.close()
            
            # Group by hour
            hourly_stats = {}
            for action, timestamp in alerts:
                hour = timestamp[:13]  # YYYY-MM-DD HH
                if hour not in hourly_stats:
                    hourly_stats[hour] = {'fire': 0, 'crowd': 0, 'unconscious': 0}
                
                if 'fire' in action:
                    hourly_stats[hour]['fire'] += 1
                elif 'crowd' in action:
                    hourly_stats[hour]['crowd'] += 1
                elif 'unconscious' in action:
                    hourly_stats[hour]['unconscious'] += 1
            
            return hourly_stats
            
        except Exception as e:
            return f"Error getting historical data: {str(e)}"

    def process_query(self, user_query, current_frame=None):
        """Process user query and generate response"""
        try:
            # Get system context
            system_status = self.get_system_status()
            
            # Prepare context for Gemini
            context = f"""
            System Status: {json.dumps(system_status, indent=2)}
            
            User Query: {user_query}
            
            Available Functions:
            - Crowd analysis in any direction (North, South, East, West, NE, NW, SE, SW)
            - Fire/smoke detection status
            - Unconscious person detection
            - Historical alert data
            - System health monitoring
            
            Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # Generate response using Gemini
            response = self.model.generate_content([
                self.system_prompt,
                context,
                f"User: {user_query}\nAssistant:"
            ])
            
            # Add to chat history
            self.chat_history.append({
                'user': user_query,
                'assistant': response.text,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            return response.text
            
        except Exception as e:
            return f"I apologize, but I encountered an error processing your query: {str(e)}. Please try again or contact system administrator."

    def get_chat_history(self):
        """Get chat history"""
        return self.chat_history

    def clear_chat_history(self):
        """Clear chat history"""
        self.chat_history = []

def create_chatbot_interface():
    """Create the chatbot interface for Streamlit"""
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        # You'll need to set your Gemini API key
        api_key = st.secrets.get("GEMINI_API_KEY", "your_gemini_api_key_here")
        st.session_state.chatbot = EventMonitorChatbot(api_key)
    
    # Chat interface
    st.subheader("🤖 AI Event Monitor Assistant")
    st.markdown("Ask me anything about the monitoring system, crowd analysis, or alerts!")
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
    
    # Chat input
    user_input = st.text_input("Ask a question:", placeholder="e.g., How much crowd is there in the North-east direction?")
    
    if st.button("Send"):
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            # Get response from chatbot
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.process_query(user_input)
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            st.rerun()
    
    # Quick action buttons
    st.markdown("---")
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 System Status"):
            status = st.session_state.chatbot.get_system_status()
            st.json(status)
    
    with col2:
        if st.button("📈 Historical Data"):
            history = st.session_state.chatbot.get_historical_data()
            st.json(history)
    
    with col3:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.chatbot.clear_chat_history()
            st.rerun()
    
    # Example queries
    st.markdown("---")
    st.subheader("💡 Example Queries")
    
    examples = [
        "How much crowd is there in the North-east direction?",
        "What's the current fire detection status?",
        "Show me today's alert statistics",
        "Is there any unconscious person detected?",
        "What's the overall system status?",
        "How many people are in the main area?"
    ]
    
    for example in examples:
        if st.button(example, key=f"example_{example}"):
            st.session_state.chat_history.append({
                'role': 'user',
                'content': example,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.process_query(example)
            
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            st.rerun() 
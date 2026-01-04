import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="FraudGuard™ Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'control_panel_visible' not in st.session_state:
    st.session_state.control_panel_visible = True
if 'transaction_data' not in st.session_state:
    st.session_state.transaction_data = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1

# Function to set background
def set_background():
    background_url = "https://g.foolcdn.com/image/?url=https%3A%2F%2Fg.foolcdn.com%2Feditorial%2Fimages%2F441531%2Famex-platinum-from-amex.png&w=1920&op=resize"
    
    style = f"""
    <style>
    .stApp {{
        background-image: url('{background_url}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.92);
        z-index: -1;
    }}
    
    .main-container {{
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 30px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }}
    
    .header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }}
    
    .simple-card {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(229, 231, 235, 0.8);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.03);
    }}
    
    .metric-card {{
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }}
    
    .metric-value {{
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #667eea !important;
        margin-bottom: 5px !important;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 14px 28px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2) !important;
    }}
    
    .footer {{
        text-align: center;
        padding: 25px;
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 30px;
        border-top: 1px solid rgba(229, 231, 235, 0.8);
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: #111827 !important;
    }}
    
    p, span, div {{
        color: #374151 !important;
    }}
    
    .stSelectbox > div > div > div, 
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {{
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }}
    
    .stSlider > div > div > div {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Set background
set_background()

# Main app
def main():
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header">
        <h1 style="color: white; margin-bottom: 10px; font-size: 2.5rem;">
            🛡️ FraudGuard™ Enterprise
        </h1>
        <h3 style="color: rgba(255, 255, 255, 0.95); margin: 5px 0; font-weight: 400;">
            Transaction Security Dashboard
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle button for control panel
    col_toggle, col_empty = st.columns([1, 5])
    with col_toggle:
        toggle_icon = "🔽" if st.session_state.control_panel_visible else "▶️"
        toggle_text = "Hide" if st.session_state.control_panel_visible else "Show"
        if st.button(f"{toggle_icon} {toggle_text}", key="toggle_btn"):
            st.session_state.control_panel_visible = not st.session_state.control_panel_visible
            st.rerun()
    
    # Step indicator (clean version)
    if st.session_state.current_step == 1:
        st.markdown("### 📝 Transaction Analysis")
    elif st.session_state.current_step == 2:
        st.markdown("### 🔍 Analysis Results")
    elif st.session_state.current_step == 3:
        st.markdown("### ✅ Action Completed")
    
    # Step 1: Transaction Input
    if st.session_state.current_step == 1:
        st.markdown("Enter transaction details for fraud analysis:")
        
        with st.form("transaction_input"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="simple-card">', unsafe_allow_html=True)
                st.markdown("**Transaction Information**")
                transaction_id = st.text_input("Transaction ID", value=f"TXN-{np.random.randint(100000, 999999)}")
                amount = st.number_input("Amount (USD)", min_value=0.0, max_value=100000.0, value=2475.50, step=100.0)
                merchant = st.selectbox("Merchant", ["Amazon", "Apple", "Netflix", "Uber", "Airbnb", "Walmart", "Other"], index=0)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="simple-card">', unsafe_allow_html=True)
                st.markdown("**Risk Parameters**")
                st.markdown("V14 - Structural Analysis:")
                v14 = st.slider("", 0.0, 1.0, 0.68, 0.01, label_visibility="collapsed")
                
                st.markdown("V17 - Behavioral Analysis:")
                v17 = st.slider(" ", 0.0, 1.0, 0.42, 0.01, label_visibility="collapsed")
                
                payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer"], index=0)
                st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🚀 Analyze Transaction", type="primary", use_container_width=True)
            
            if submitted:
                st.session_state.transaction_data = {
                    "id": transaction_id,
                    "amount": amount,
                    "merchant": merchant,
                    "v14": v14,
                    "v17": v17,
                    "payment_method": payment_method,
                    "timestamp": datetime.now().strftime("%H:%M")
                }
                st.session_state.current_step = 2
                st.rerun()
    
    # Step 2: Analysis Results
    elif st.session_state.current_step == 2:
        data = st.session_state.transaction_data
        
        # Calculate risk
        risk_score = min(0.05 + (data['v14'] * 0.4) + (data['v17'] * 0.35) + (data['amount'] / 10000), 0.95)
        risk_percent = risk_score * 100
        
        if risk_percent > 70:
            risk_level = "HIGH"
            risk_color = "#ef4444"
            risk_icon = "🚨"
        elif risk_percent > 40:
            risk_level = "MEDIUM"
            risk_color = "#f59e0b"
            risk_icon = "⚠️"
        else:
            risk_level = "LOW"
            risk_color = "#10b981"
            risk_icon = "✅"
        
        # Results display
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            st.markdown('<div class="simple-card">', unsafe_allow_html=True)
            st.markdown("**Risk Assessment**")
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 3rem; font-weight: 800; color: {risk_color};">
                    {risk_percent:.1f}%
                </div>
                <div style="font-size: 1.2rem; color: #374151; margin: 10px 0;">
                    Fraud Probability
                </div>
                <div style="padding: 10px 20px; background: {risk_color}; color: white; 
                     border-radius: 50px; display: inline-block; font-weight: 600; margin-top: 10px;">
                    {risk_icon} {risk_level} RISK
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_result2:
            st.markdown('<div class="simple-card">', unsafe_allow_html=True)
            st.markdown("**Transaction Details**")
            st.markdown(f"""
            <div style="margin: 10px 0;">
                <strong>ID:</strong> {data['id']}<br>
                <strong>Amount:</strong> ${data['amount']:,.2f}<br>
                <strong>Merchant:</strong> {data['merchant']}<br>
                <strong>Payment:</strong> {data['payment_method']}<br>
                <strong>V14 Score:</strong> {data['v14']:.2f}<br>
                <strong>V17 Score:</strong> {data['v17']:.2f}<br>
                <strong>Time:</strong> {data['timestamp']}
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons
            st.markdown("---")
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("✅ Approve", use_container_width=True):
                    st.session_state.current_step = 3
                    st.session_state.action = "approved"
                    st.rerun()
            
            with col_btn2:
                if st.button("⚠️ Review", use_container_width=True):
                    st.session_state.current_step = 3
                    st.session_state.action = "flagged"
                    st.rerun()
            
            with col_btn3:
                if st.button("🛑 Block", use_container_width=True):
                    st.session_state.current_step = 3
                    st.session_state.action = "blocked"
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Back button
        if st.button("← Back to Input", use_container_width=False):
            st.session_state.current_step = 1
            st.rerun()
    
    # Step 3: Action Completed
    elif st.session_state.current_step == 3:
        data = st.session_state.transaction_data
        action = st.session_state.get('action', 'reviewed')
        
        st.markdown('<div class="simple-card">', unsafe_allow_html=True)
        
        if action == "approved":
            st.markdown("### 🎉 Transaction Approved")
            st.markdown(f"Transaction **{data['id']}** has been successfully processed.")
            st.balloons()
        elif action == "flagged":
            st.markdown("### ⚠️ Transaction Flagged")
            st.markdown(f"Transaction **{data['id']}** has been flagged for manual review.")
        else:
            st.markdown("### 🛑 Transaction Blocked")
            st.markdown(f"Transaction **{data['id']}** has been blocked due to fraud risk.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Simple metrics
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.9%</div>', unsafe_allow_html=True)
            st.markdown("Accuracy")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_metric2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">48ms</div>', unsafe_allow_html=True)
            st.markdown("Speed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # New analysis button
        if st.button("🔄 Start New Analysis", type="primary", use_container_width=True):
            st.session_state.current_step = 1
            st.session_state.transaction_data = {}
            st.rerun()
    
    # Control Panel (Simple version)
    if st.session_state.control_panel_visible:
        st.markdown("---")
        st.markdown("### 🎛️ Control Panel")
        
        # Simple metrics
        col_ctl1, col_ctl2, col_ctl3, col_ctl4 = st.columns(4)
        
        with col_ctl1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">1,247</div>', unsafe_allow_html=True)
            st.markdown("Today")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_ctl2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.9%</div>', unsafe_allow_html=True)
            st.markdown("Accuracy")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_ctl3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$24.7K</div>', unsafe_allow_html=True)
            st.markdown("Saved")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_ctl4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">48ms</div>', unsafe_allow_html=True)
            st.markdown("Speed")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Simple settings
        st.markdown('<div class="simple-card">', unsafe_allow_html=True)
        st.markdown("**Settings**")
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            st.selectbox("Alert Level", ["Low", "Medium", "High"], index=1)
            st.checkbox("Auto-approve low risk", value=True)
        
        with col_set2:
            st.selectbox("Data Retention", ["30 days", "90 days", "1 year"], index=0)
            st.checkbox("Email alerts", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p style="margin: 0; font-weight: 700; color: #111827;">
            FraudGuard™ Enterprise
        </p>
        <p style="margin: 10px 0; color: #6b7280;">
            Advanced Fraud Detection System
        </p>
        <p style="margin: 0; color: #9ca3af; font-size: 0.85rem;">
            © 2024 FraudGuard Security | All rights reserved
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

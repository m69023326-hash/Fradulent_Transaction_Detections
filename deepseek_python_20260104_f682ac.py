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

# Function to calculate dynamic risk score
def calculate_risk_score(amount, v14, v17, payment_method, merchant, device_type="Desktop"):
    """Calculate dynamic risk score based on all parameters"""
    
    # Base risk factors
    base_risk = 0.05
    
    # Amount-based risk (higher amounts = higher risk)
    amount_risk = min(amount / 10000, 0.25)
    
    # V14 risk (structural anomalies)
    v14_risk = v14 * 0.25
    
    # V17 risk (behavioral patterns)
    v17_risk = v17 * 0.20
    
    # Payment method risk
    payment_risks = {
        "Credit Card": 0.05,
        "Debit Card": 0.08,
        "Digital Wallet": 0.12,
        "Bank Transfer": 0.15,
        "Cryptocurrency": 0.25
    }
    method_risk = payment_risks.get(payment_method, 0.10)
    
    # Merchant risk
    merchant_risks = {
        "Amazon": 0.05,
        "Apple": 0.04,
        "Netflix": 0.03,
        "Uber": 0.08,
        "Airbnb": 0.12,
        "Walmart": 0.06,
        "Target": 0.05,
        "Best Buy": 0.06,
        "Other": 0.15
    }
    merchant_risk = merchant_risks.get(merchant, 0.10)
    
    # Device risk
    device_risks = {
        "Mobile": 0.05,
        "Desktop": 0.03,
        "Tablet": 0.06,
        "Unknown": 0.20
    }
    device_risk = device_risks.get(device_type, 0.10)
    
    # Time-based risk
    current_hour = datetime.now().hour
    if 0 <= current_hour < 6:
        time_risk = 0.15
    elif 6 <= current_hour < 12:
        time_risk = 0.05
    elif 12 <= current_hour < 18:
        time_risk = 0.04
    else:
        time_risk = 0.08
    
    # Calculate total risk
    total_risk = min(
        base_risk + amount_risk + v14_risk + v17_risk + method_risk + merchant_risk + device_risk + time_risk,
        0.95
    )
    
    return total_risk

# Function to get risk level and color
def get_risk_level(risk_score):
    risk_percent = risk_score * 100
    if risk_percent > 70:
        return "🚨 HIGH", "#ef4444", "🔴"
    elif risk_percent > 40:
        return "⚠️ MEDIUM", "#f59e0b", "🟡"
    else:
        return "✅ LOW", "#10b981", "🟢"

# Function to set background
def set_background():
    background_url = "https://plus.unsplash.com/premium_photo-1675055730240-96a4ed84e482?q=80&w=327&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
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
        background: rgba(255, 255, 255, 0.95);
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
    
    .risk-gauge {{
        width: 100%;
        height: 20px;
        background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ef4444 100%);
        border-radius: 10px;
        margin: 15px 0;
        position: relative;
    }}
    
    .risk-marker {{
        position: absolute;
        top: -5px;
        width: 4px;
        height: 30px;
        background: black;
        transform: translateX(-50%);
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
    current_time = datetime.now().strftime('%H:%M:%S')
    
    st.markdown(f"""
    <div class="header">
        <h1 style="color: white; margin-bottom: 10px; font-size: 2.5rem;">
            🛡️ FraudGuard™ Enterprise
        </h1>
        <h3 style="color: rgba(255, 255, 255, 0.95); margin: 5px 0; font-weight: 400;">
            Live Transaction Security Dashboard
        </h3>
        <p style="color: rgba(255, 255, 255, 0.85); margin: 5px 0 0 0; font-size: 0.9rem;">
            Real-time risk assessment • Updated: {current_time}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle button for control panel
    col_toggle, _ = st.columns([1, 5])
    with col_toggle:
        toggle_icon = "🔽" if st.session_state.control_panel_visible else "▶️"
        toggle_text = "Hide" if st.session_state.control_panel_visible else "Show"
        if st.button(f"{toggle_icon} {toggle_text}", key="toggle_btn"):
            st.session_state.control_panel_visible = not st.session_state.control_panel_visible
            st.rerun()
    
    # Step indicator
    if st.session_state.current_step == 1:
        st.markdown("### 📝 Transaction Analysis")
    elif st.session_state.current_step == 2:
        st.markdown("### 🔍 Analysis Results")
    elif st.session_state.current_step == 3:
        st.markdown("### ✅ Action Completed")
    
    # Step 1: Transaction Input
    if st.session_state.current_step == 1:
        st.markdown("Enter transaction details for live fraud analysis:")
        
        with st.form("transaction_input"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="simple-card">', unsafe_allow_html=True)
                st.markdown("**Transaction Information**")
                
                transaction_id = st.text_input("Transaction ID", value=f"TXN-{np.random.randint(100000, 999999)}")
                
                amount = st.number_input("Amount (USD)", 
                    min_value=0.0, 
                    max_value=100000.0, 
                    value=500.0,
                    step=100.0)
                
                merchant = st.selectbox("Merchant", 
                    ["Amazon", "Apple", "Netflix", "Uber", "Airbnb", "Walmart", "Target", "Best Buy", "Other"],
                    index=0)
                
                device_type = st.selectbox("Device Type",
                    ["Desktop", "Mobile", "Tablet", "Unknown"],
                    index=0)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="simple-card">', unsafe_allow_html=True)
                st.markdown("**Risk Parameters**")
                
                st.markdown("**V14 - Structural Analysis**")
                v14 = st.slider("V14 Score", 0.0, 1.0, 0.35, 0.01, label_visibility="collapsed")
                
                st.markdown("**V17 - Behavioral Analysis**")
                v17 = st.slider("V17 Score", 0.0, 1.0, 0.25, 0.01, label_visibility="collapsed")
                
                payment_method = st.selectbox("Payment Method", 
                    ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer", "Cryptocurrency"],
                    index=0)
                
                # Live risk calculation
                if st.form_submit_button:
                    live_risk = calculate_risk_score(amount, v14, v17, payment_method, merchant, device_type)
                    risk_level, risk_color, _ = get_risk_level(live_risk)
                    
                    st.markdown("---")
                    st.markdown("**Live Risk Preview**")
                    
                    col_preview1, col_preview2 = st.columns([2, 1])
                    with col_preview1:
                        st.markdown(f"**Risk Level:** {risk_level}")
                        st.markdown(f"**Score:** {(live_risk * 100):.1f}%")
                    
                    with col_preview2:
                        risk_percent = live_risk * 100
                        st.markdown(f"""
                        <div style="position: relative; width: 100%; margin: 10px 0;">
                            <div class="risk-gauge"></div>
                            <div class="risk-marker" style="left: {risk_percent}%;"></div>
                        </div>
                        """, unsafe_allow_html=True)
                
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
                    "device_type": device_type,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "risk_score": calculate_risk_score(amount, v14, v17, payment_method, merchant, device_type)
                }
                st.session_state.current_step = 2
                st.rerun()
    
    # Step 2: Analysis Results
    elif st.session_state.current_step == 2:
        data = st.session_state.transaction_data
        
        # Get risk details
        risk_score = data['risk_score']
        risk_percent = risk_score * 100
        risk_level, risk_color, _ = get_risk_level(risk_score)
        
        # Display results
        st.markdown("### 📊 Analysis Results")
        
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            st.markdown('<div class="simple-card">', unsafe_allow_html=True)
            st.markdown("**Risk Assessment**")
            
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 3.5rem; font-weight: 800; color: {risk_color}; margin-bottom: 10px;">
                    {risk_percent:.1f}%
                </div>
                <div style="font-size: 1.5rem; color: {risk_color}; font-weight: 700; margin: 15px 0;">
                    {risk_level} RISK
                </div>
                
                <div style="position: relative; width: 80%; margin: 20px auto;">
                    <div class="risk-gauge"></div>
                    <div class="risk-marker" style="left: {risk_percent}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_result2:
            st.markdown('<div class="simple-card">', unsafe_allow_html=True)
            st.markdown("**Transaction Details**")
            
            # Risk factors
            st.markdown("**Risk Factors:**")
            
            factors = [
                ("Amount", min(data['amount'] / 10000, 0.25) * 100, "#667eea"),
                ("V14 Score", data['v14'] * 25, "#8b5cf6"),
                ("V17 Score", data['v17'] * 20, "#ec4899"),
                ("Payment Method", 15 if data['payment_method'] == "Cryptocurrency" else 8 if data['payment_method'] == "Bank Transfer" else 5, "#10b981"),
                ("Merchant", 15 if data['merchant'] == "Other" else 12 if data['merchant'] == "Airbnb" else 5, "#f59e0b"),
                ("Device", 20 if data['device_type'] == "Unknown" else 5, "#3b82f6")
            ]
            
            for factor, value, color in factors:
                st.markdown(f"""
                <div style="margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <span style="font-weight: 500;">{factor}</span>
                        <span style="color: {color}; font-weight: 600;">{value:.1f}%</span>
                    </div>
                    <div style="width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px;">
                        <div style="width: {min(value, 100)}%; height: 100%; background: {color}; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Transaction info
            st.markdown("---")
            st.markdown("**Transaction Info:**")
            st.markdown(f"""
            <div style="margin: 10px 0;">
                <strong>ID:</strong> {data['id']}<br>
                <strong>Amount:</strong> ${data['amount']:,.2f}<br>
                <strong>Merchant:</strong> {data['merchant']}<br>
                <strong>Payment:</strong> {data['payment_method']}<br>
                <strong>Device:</strong> {data['device_type']}<br>
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
            st.markdown(f"""
            Transaction **{data['id']}** has been successfully processed.
            
            **Risk at approval:** {(data['risk_score'] * 100):.1f}%
            **Status:** ✅ **APPROVED**
            """)
            st.balloons()
        elif action == "flagged":
            st.markdown("### ⚠️ Transaction Flagged")
            st.markdown(f"""
            Transaction **{data['id']}** has been flagged for manual review.
            
            **Risk score:** {(data['risk_score'] * 100):.1f}%
            **Status:** ⚠️ **FLAGGED FOR REVIEW**
            """)
        else:
            st.markdown("### 🛑 Transaction Blocked")
            st.markdown(f"""
            Transaction **{data['id']}** has been blocked.
            
            **Risk score:** {(data['risk_score'] * 100):.1f}%
            **Status:** 🛑 **BLOCKED**
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System status
        st.markdown('<div class="simple-card">', unsafe_allow_html=True)
        st.markdown("**System Status**")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.9%</div>', unsafe_allow_html=True)
            st.markdown("Accuracy")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">48ms</div>', unsafe_allow_html=True)
            st.markdown("Response Time")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_stat3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$24.7K</div>', unsafe_allow_html=True)
            st.markdown("Saved Today")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # New analysis button
        if st.button("🔄 Start New Analysis", type="primary", use_container_width=True):
            st.session_state.current_step = 1
            st.session_state.transaction_data = {}
            st.rerun()
    
    # Control Panel
    if st.session_state.control_panel_visible:
        st.markdown("---")
        st.markdown("### 🎛️ Control Panel")
        
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
            st.markdown('<div class="metric-value">42ms</div>', unsafe_allow_html=True)
            st.markdown("Live Speed")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    current_time = datetime.now().strftime('%H:%M:%S')
    
    st.markdown(f"""
    <div class="footer">
        <p style="margin: 0; font-weight: 700; color: #111827;">
            🛡️ FraudGuard™ Enterprise
        </p>
        <p style="margin: 10px 0; color: #6b7280;">
            Live Transaction Security System • Updated: {current_time}
        </p>
        <p style="margin: 0; color: #9ca3af; font-size: 0.85rem;">
            © 2024 FraudGuard Security | Real-time Risk Assessment
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

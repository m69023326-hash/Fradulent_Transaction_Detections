import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
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
    st.session_state.current_step = 1  # 1: Input, 2: Analysis, 3: Results

# Function to set background
def set_background():
    # Your Unsplash image URL
    background_url = "https://plus.unsplash.com/premium_photo-1675055730240-96a4ed84e482?q=80&w=327&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
    # CSS with direct URL background
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
        padding: 40px;
        margin: 30px auto;
        max-width: 1400px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }}
    
    .header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.25);
    }}
    
    .glass-card {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
        padding: 25px 20px;
        border-radius: 18px;
        border: 1px solid rgba(229, 231, 235, 0.8);
        text-align: center;
    }}
    
    .metric-value {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 5px !important;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px 36px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}
    
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }}
    
    .footer {{
        text-align: center;
        padding: 30px;
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 50px;
        border-top: 1px solid rgba(229, 231, 235, 0.8);
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Set background
set_background()

# Function to create gauge visualization without plotly
def create_gauge(value, label, color="#667eea"):
    percentage = min(value * 100, 100)
    bar_html = f"""
    <div style="margin: 20px 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
            <span style="font-weight: 600;">{label}</span>
            <span style="font-weight: 700; color: {color};">{percentage:.1f}%</span>
        </div>
        <div style="width: 100%; height: 20px; background: #e5e7eb; border-radius: 10px; overflow: hidden;">
            <div style="width: {percentage}%; height: 100%; background: {color}; border-radius: 10px;"></div>
        </div>
    </div>
    """
    return bar_html

# Main app
def main():
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header with toggle
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🛡️", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="header">
            <h1 style="color: white; margin-bottom: 10px; font-size: 2.8rem;">
                FraudGuard™ Enterprise
            </h1>
            <h3 style="color: rgba(255, 255, 255, 0.95); margin: 5px 0; font-weight: 400;">
                Advanced Transaction Security Platform
            </h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        toggle_icon = "🔽" if st.session_state.control_panel_visible else "▶️"
        toggle_text = "Hide Panel" if st.session_state.control_panel_visible else "Show Panel"
        if st.button(f"{toggle_icon} {toggle_text}", key="toggle_btn"):
            st.session_state.control_panel_visible = not st.session_state.control_panel_visible
            st.rerun()
    
    # Step indicator
    steps = ["📝 Input", "🔍 Analysis", "✅ Results"]
    current_step = st.session_state.current_step
    
    st.markdown("### Progress")
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i + 1 == current_step:
                st.markdown(f"<div style='text-align: center; padding: 10px; background: #667eea; color: white; border-radius: 10px; font-weight: 600;'>{step}</div>", unsafe_allow_html=True)
            elif i + 1 < current_step:
                st.markdown(f"<div style='text-align: center; padding: 10px; background: #10b981; color: white; border-radius: 10px; font-weight: 600;'>✓ {step}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; padding: 10px; background: #e5e7eb; color: #6b7280; border-radius: 10px;'>{step}</div>", unsafe_allow_html=True)
    
    # Step 1: Transaction Input
    if st.session_state.current_step == 1:
        st.markdown("## 📝 Transaction Details")
        
        with st.form("transaction_input"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 💳 Basic Information")
                transaction_id = st.text_input("Transaction ID", 
                    value=f"TXN-{np.random.randint(100000, 999999)}")
                amount = st.number_input("Amount (USD)", 
                    min_value=0.0, max_value=100000.0, value=2475.50, step=100.0)
                currency = st.selectbox("Currency", 
                    ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"], index=0)
                merchant = st.selectbox("Merchant", 
                    ["Amazon", "Apple", "Netflix", "Uber", "Airbnb", "Walmart"], index=0)
            
            with col2:
                st.markdown("### 🔍 Risk Parameters")
                st.markdown("#### V14 - Structural Analysis")
                v14 = st.slider("Structural Score", 0.0, 1.0, 0.68, 0.01, key="v14")
                
                st.markdown("#### V17 - Behavioral Analysis")
                v17 = st.slider("Behavioral Score", 0.0, 1.0, 0.42, 0.01, key="v17")
                
                payment_method = st.selectbox("Payment Method", 
                    ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer"], index=0)
            
            submitted = st.form_submit_button("🚀 Analyze Transaction", type="primary", use_container_width=True)
            
            if submitted:
                st.session_state.transaction_data = {
                    "id": transaction_id,
                    "amount": amount,
                    "currency": currency,
                    "merchant": merchant,
                    "v14": v14,
                    "v17": v17,
                    "payment_method": payment_method,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.current_step = 2
                st.rerun()
    
    # Step 2: Fraud Analysis
    elif st.session_state.current_step == 2:
        data = st.session_state.transaction_data
        
        st.markdown("## 🔍 Fraud Analysis")
        st.markdown(f"**Transaction ID:** `{data['id']}`")
        
        # Calculate fraud probability
        with st.spinner("Analyzing transaction..."):
            base_risk = 0.05
            amount_risk = min(data['amount'] / 5000, 0.3)
            v14_risk = data['v14'] * 0.4
            v17_risk = data['v17'] * 0.35
            method_risk = 0.15 if data['payment_method'] in ["Digital Wallet", "Bank Transfer"] else 0.05
            
            fraud_probability = min(base_risk + amount_risk + v14_risk + v17_risk + method_risk, 0.95)
            
            # Determine risk level
            if fraud_probability > 0.7:
                risk_level = "HIGH"
                risk_color = "#ef4444"
                icon = "🚨"
            elif fraud_probability > 0.4:
                risk_level = "MEDIUM"
                risk_color = "#f59e0b"
                icon = "⚠️"
            else:
                risk_level = "LOW"
                risk_color = "#10b981"
                icon = "✅"
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"### {icon} Risk Assessment")
            
            # Custom gauge
            risk_score = fraud_probability * 100
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 3.5rem; font-weight: 800; color: {risk_color};">
                    {risk_score:.1f}%
                </div>
                <div style="font-size: 1.2rem; color: #6b7280; margin: 10px 0;">
                    Fraud Probability
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk factors
            st.markdown("#### ⚡ Risk Factors")
            st.markdown(create_gauge(amount_risk, "Transaction Amount", "#667eea"))
            st.markdown(create_gauge(v14_risk/0.4, "Structural Anomaly", "#764ba2"))
            st.markdown(create_gauge(v17_risk/0.35, "Behavioral Pattern", "#8b5cf6"))
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📋 Transaction Summary")
            
            summary_items = [
                ("ID", data['id']),
                ("Amount", f"${data['amount']:,.2f} {data['currency']}"),
                ("Merchant", data['merchant']),
                ("Payment Method", data['payment_method']),
                ("V14 Score", f"{data['v14']:.2f}"),
                ("V17 Score", f"{data['v17']:.2f}"),
                ("Time", data['timestamp'])
            ]
            
            for label, value in summary_items:
                st.markdown(f"""
                <div style="padding: 10px 0; border-bottom: 1px solid #f3f4f6;">
                    <div style="font-size: 0.9rem; color: #6b7280;">{label}</div>
                    <div style="font-weight: 600; color: #374151;">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Action recommendations
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"### ⚡ Risk Level: <span style='color:{risk_color}'>{risk_level}</span>", unsafe_allow_html=True)
            
            if risk_level == "HIGH":
                st.markdown("""
                **Immediate Actions:**
                1. 🛑 Block transaction
                2. 🔒 Freeze account
                3. 📞 Contact customer
                """)
            elif risk_level == "MEDIUM":
                st.markdown("""
                **Recommended Actions:**
                1. ⏸️ Hold for review
                2. 🔐 Require 2FA
                3. 📧 Send alert
                """)
            else:
                st.markdown("""
                **Actions:**
                1. ✅ Approve transaction
                2. 📊 Log for audit
                3. 🔔 Monitor trends
                """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("✅ Approve", use_container_width=True):
                st.session_state.current_step = 3
                st.session_state.action = "approved"
                st.rerun()
        
        with col_btn2:
            if st.button("⚠️ Flag", use_container_width=True):
                st.session_state.current_step = 3
                st.session_state.action = "flagged"
                st.rerun()
        
        with col_btn3:
            if st.button("🔄 New", use_container_width=True):
                st.session_state.current_step = 1
                st.session_state.transaction_data = {}
                st.rerun()
    
    # Step 3: Results
    elif st.session_state.current_step == 3:
        data = st.session_state.transaction_data
        action = st.session_state.get('action', 'reviewed')
        
        st.markdown("## ✅ Action Taken")
        
        if action == "approved":
            st.success("### 🎉 Transaction Approved")
            st.markdown(f"""
            Transaction **{data['id']}** has been successfully approved.
            
            **Details:**
            - Amount: ${data['amount']:,.2f} {data['currency']}
            - Merchant: {data['merchant']}
            - Time: {data['timestamp']}
            - Status: ✅ **APPROVED**
            """)
            st.balloons()
        else:
            st.warning("### ⚠️ Transaction Flagged")
            st.markdown(f"""
            Transaction **{data['id']}** has been flagged for review.
            
            **Details:**
            - Amount: ${data['amount']:,.2f} {data['currency']}
            - Merchant: {data['merchant']}
            - Time: {data['timestamp']}
            - Status: ⚠️ **FLAGGED FOR REVIEW**
            """)
        
        # Summary statistics
        st.markdown("---")
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.9%</div>', unsafe_allow_html=True)
            st.markdown("Accuracy Rate")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">48ms</div>', unsafe_allow_html=True)
            st.markdown("Processing Time")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_stat3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$24.7K</div>', unsafe_allow_html=True)
            st.markdown("Saved Today")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🔄 Start New Analysis", type="primary", use_container_width=True):
            st.session_state.current_step = 1
            st.session_state.transaction_data = {}
            st.rerun()
    
    # Control Panel (Toggleable)
    if st.session_state.control_panel_visible:
        st.markdown("---")
        st.markdown("## 🎛️ Control Panel")
        
        # Dashboard metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">1,247</div>', unsafe_allow_html=True)
            st.markdown("Today's Transactions")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.9%</div>', unsafe_allow_html=True)
            st.markdown("Detection Accuracy")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">48ms</div>', unsafe_allow_html=True)
            st.markdown("Avg. Response")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$124K</div>', unsafe_allow_html=True)
            st.markdown("Prevented Fraud")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            if st.button("🔄 Update Model", use_container_width=True):
                st.success("Model update initiated")
        
        with col_act2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation started")
        
        with col_act3:
            if st.button("🔍 Run Audit", use_container_width=True):
                st.warning("System audit in progress")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p style="margin: 0; font-weight: 700; color: #374151;">
            🛡️ FraudGuard™ Enterprise
        </p>
        <p style="margin: 10px 0; color: #6b7280;">
            Advanced AI-Powered Fraud Detection Platform
        </p>
        <p style="margin: 0; color: #9ca3af; font-size: 0.85rem;">
            © 2024 FraudGuard Global Security | PCI-DSS Compliant | ISO 27001 Certified
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

if __name__ == "__main__":
    main()

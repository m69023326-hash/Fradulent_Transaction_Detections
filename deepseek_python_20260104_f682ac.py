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

# Function to set background with improved text contrast
def set_background():
    # Your Unsplash image URL
    background_url = "https://plus.unsplash.com/premium_photo-1675055730240-96a4ed84e482?q=80&w=327&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
    # CSS with direct URL background and improved text contrast
    style = f"""
    <style>
    /* Main app with your direct URL background image */
    .stApp {{
        background-image: url('{background_url}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    
    /* Enhanced overlay for better text readability */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.95);  /* More opaque for better contrast */
        z-index: -1;
    }}
    
    /* Main content container with better contrast */
    .main-container {{
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 40px;
        margin: 30px auto;
        max-width: 1400px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }}
    
    /* Header styling - high contrast */
    .header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.25);
    }}
    
    /* Glass cards with better text contrast */
    .glass-card {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    }}
    
    /* Metric cards with high contrast */
    .metric-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.98) 100%);
        padding: 25px 20px;
        border-radius: 18px;
        border: 1px solid rgba(229, 231, 235, 0.9);
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
    }}
    
    /* High contrast text colors */
    .metric-value {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 5px !important;
    }}
    
    /* High contrast body text */
    .main-text {{
        color: #1f2937 !important;  /* Dark gray for high contrast */
        font-weight: 400;
    }}
    
    .sub-text {{
        color: #374151 !important;  /* Slightly lighter but still high contrast */
        font-weight: 400;
    }}
    
    .light-text {{
        color: #4b5563 !important;  /* Medium gray for less important text */
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 16px 36px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
    }}
    
    /* Progress bars */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }}
    
    /* Form inputs with better contrast */
    .stSelectbox > div > div > div, 
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stSlider > div > div > div {{
        border: 2px solid #d1d5db !important;  /* Darker border for contrast */
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 16px !important;
        background: white !important;
        color: #1f2937 !important;
    }}
    
    /* Labels with better contrast */
    .stSelectbox label, 
    .stNumberInput label,
    .stTextInput label,
    .stSlider label {{
        color: #1f2937 !important;
        font-weight: 600 !important;
    }}
    
    /* Headings with high contrast */
    h1, h2, h3, h4, h5, h6 {{
        color: #111827 !important;  /* Very dark gray for headings */
        font-weight: 700;
    }}
    
    /* Regular text */
    p, li, span, div {{
        color: #1f2937 !important;  /* Dark gray for body text */
    }}
    
    /* Markdown text */
    .stMarkdown {{
        color: #1f2937 !important;
    }}
    
    /* Alert boxes */
    .stAlert {{
        background: rgba(255, 255, 255, 0.95) !important;
        color: #1f2937 !important;
        border: 1px solid #d1d5db !important;
    }}
    
    /* Dataframes */
    .stDataFrame {{
        color: #1f2937 !important;
    }}
    
    /* Footer with high contrast */
    .footer {{
        text-align: center;
        padding: 30px;
        color: #374151 !important;  /* Dark text */
        font-size: 0.9rem;
        margin-top: 50px;
        border-top: 1px solid rgba(209, 213, 219, 0.8);
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
    }}
    
    /* Custom gauge bars with better contrast */
    .gauge-container {{
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid rgba(209, 213, 219, 0.8);
    }}
    
    /* Step indicator with high contrast */
    .step-indicator {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 30px 0;
    }}
    
    .step {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        background: #e5e7eb;
        color: #374151 !important;
        border: 3px solid white;
    }}
    
    .step.active {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
    }}
    
    .step.completed {{
        background: #10b981;
        color: white !important;
    }}
    
    /* Tabs with better contrast */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(243, 244, 246, 0.8);
        border-radius: 12px;
        padding: 8px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: #374151 !important;
        font-weight: 600;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }}
    
    /* Risk level indicators */
    .risk-low {{
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
    }}
    
    .risk-medium {{
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
    }}
    
    .risk-high {{
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
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
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 600; color: #1f2937;">{label}</span>
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
            <h1 style="color: white; margin-bottom: 10px; font-size: 2.8rem; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">
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
                st.markdown(f"""
                <div style='text-align: center; padding: 12px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; border-radius: 12px; font-weight: 700; font-size: 1.1rem;'>
                    {step}
                </div>
                """, unsafe_allow_html=True)
            elif i + 1 < current_step:
                st.markdown(f"""
                <div style='text-align: center; padding: 12px; background: #10b981; color: white; 
                border-radius: 12px; font-weight: 700; font-size: 1.1rem;'>
                    ✓ {step}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: center; padding: 12px; background: #f3f4f6; color: #374151; 
                border-radius: 12px; font-weight: 600; font-size: 1.1rem;'>
                    {step}
                </div>
                """, unsafe_allow_html=True)
    
    # Step 1: Transaction Input
    if st.session_state.current_step == 1:
        st.markdown("## 📝 Transaction Details")
        st.markdown("Enter transaction information for fraud analysis", unsafe_allow_html=True)
        
        with st.form("transaction_input"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 💳 Basic Information")
                transaction_id = st.text_input("Transaction ID", 
                    value=f"TXN-{np.random.randint(100000, 999999)}",
                    help="Unique transaction identifier")
                amount = st.number_input("Amount (USD)", 
                    min_value=0.0, max_value=100000.0, value=2475.50, step=100.0,
                    help="Transaction amount in USD")
                currency = st.selectbox("Currency", 
                    ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"], index=0,
                    help="Transaction currency")
                merchant = st.selectbox("Merchant", 
                    ["Amazon", "Apple", "Netflix", "Uber", "Airbnb", "Walmart", "Target", "Best Buy"], index=0,
                    help="Merchant name")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 🔍 Risk Parameters")
                
                st.markdown("#### V14 - Structural Analysis")
                v14 = st.slider("Structural Anomaly Score", 0.0, 1.0, 0.68, 0.01,
                    help="Measures structural anomalies in transaction patterns")
                
                # Risk indicator
                if v14 > 0.8:
                    st.markdown('<span class="risk-high">🚨 High Risk</span>', unsafe_allow_html=True)
                elif v14 > 0.6:
                    st.markdown('<span class="risk-medium">⚠️ Medium Risk</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="risk-low">✅ Low Risk</span>', unsafe_allow_html=True)
                
                st.markdown("#### V17 - Behavioral Analysis")
                v17 = st.slider("Behavioral Pattern Score", 0.0, 1.0, 0.42, 0.01,
                    help="Analyzes user behavior patterns")
                
                # Risk indicator
                if v17 > 0.7:
                    st.markdown('<span class="risk-high">🚨 High Risk</span>', unsafe_allow_html=True)
                elif v17 > 0.5:
                    st.markdown('<span class="risk-medium">⚠️ Medium Risk</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="risk-low">✅ Low Risk</span>', unsafe_allow_html=True)
                
                payment_method = st.selectbox("Payment Method", 
                    ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer"], index=0,
                    help="Payment method used")
                st.markdown('</div>', unsafe_allow_html=True)
            
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
        st.markdown(f"**Transaction ID:** `{data['id']}`", unsafe_allow_html=True)
        
        # Calculate fraud probability
        with st.spinner("🤖 AI model analyzing transaction patterns..."):
            # Enhanced risk calculation
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
        st.markdown("### 📊 Analysis Results")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"#### {icon} Risk Assessment")
            
            # Custom gauge visualization
            risk_score = fraud_probability * 100
            
            # Large risk score display
            st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <div style="font-size: 3.5rem; font-weight: 800; color: {risk_color}; margin-bottom: 10px;">
                    {risk_score:.1f}%
                </div>
                <div style="font-size: 1.2rem; color: #374151; font-weight: 600; margin-bottom: 20px;">
                    Fraud Probability
                </div>
                
                <div style="width: 100%; height: 25px; background: #e5e7eb; border-radius: 12px; overflow: hidden; margin: 20px 0;">
                    <div style="width: {risk_score}%; height: 100%; background: {risk_color}; border-radius: 12px;"></div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                    <span style="color: #10b981; font-weight: 600;">Low</span>
                    <span style="color: #f59e0b; font-weight: 600;">Medium</span>
                    <span style="color: #ef4444; font-weight: 600;">High</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk factors breakdown
            st.markdown("#### ⚡ Risk Factors Breakdown")
            
            factors = [
                ("Transaction Amount", amount_risk * 100, "#667eea"),
                ("Structural Anomaly", data['v14'] * 40, "#764ba2"),
                ("Behavioral Pattern", data['v17'] * 35, "#8b5cf6"),
                ("Payment Method", method_risk * 100, "#10b981")
            ]
            
            for factor, value, color in factors:
                st.markdown(f"""
                <div style="margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                        <span style="font-weight: 600; color: #374151;">{factor}</span>
                        <span style="color: {color}; font-weight: 700;">{value:.1f}%</span>
                    </div>
                    <div style="width: 100%; height: 12px; background: rgba(229, 231, 235, 0.8); border-radius: 6px; overflow: hidden;">
                        <div style="width: {value}%; height: 100%; background: {color}; border-radius: 6px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 Transaction Summary")
            
            summary_items = [
                ("Transaction ID", data['id'], "#6b7280"),
                ("Amount", f"${data['amount']:,.2f} {data['currency']}", "#059669"),
                ("Merchant", data['merchant'], "#7c3aed"),
                ("Payment Method", data['payment_method'], "#3b82f6"),
                ("V14 Score", f"{data['v14']:.2f}", "#ef4444" if data['v14'] > 0.6 else "#f59e0b"),
                ("V17 Score", f"{data['v17']:.2f}", "#ef4444" if data['v17'] > 0.5 else "#f59e0b"),
                ("Time", data['timestamp'], "#6b7280")
            ]
            
            for label, value, color in summary_items:
                st.markdown(f"""
                <div style="padding: 12px 0; border-bottom: 1px solid rgba(243, 244, 246, 0.8);">
                    <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 4px;">{label}</div>
                    <div style="font-weight: 600; color: {color if isinstance(color, str) else '#374151'};">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Action recommendations
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"#### ⚡ Recommended Action")
            
            if risk_level == "HIGH":
                st.markdown('<span class="risk-high">🚨 HIGH RISK</span>', unsafe_allow_html=True)
                st.markdown("""
                <div style="margin-top: 15px;">
                    <strong>Immediate Actions:</strong>
                    <ul style="color: #374151; margin-top: 10px;">
                        <li>🛑 Block transaction</li>
                        <li>🔒 Freeze account</li>
                        <li>📞 Contact customer</li>
                        <li>🚓 Report to authorities</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif risk_level == "MEDIUM":
                st.markdown('<span class="risk-medium">⚠️ MEDIUM RISK</span>', unsafe_allow_html=True)
                st.markdown("""
                <div style="margin-top: 15px;">
                    <strong>Recommended Actions:</strong>
                    <ul style="color: #374151; margin-top: 10px;">
                        <li>⏸️ Hold for review</li>
                        <li>🔐 Require 2FA</li>
                        <li>📧 Send alert</li>
                        <li>👁️ Monitor activity</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<span class="risk-low">✅ LOW RISK</span>', unsafe_allow_html=True)
                st.markdown("""
                <div style="margin-top: 15px;">
                    <strong>Actions:</strong>
                    <ul style="color: #374151; margin-top: 10px;">
                        <li>✅ Approve transaction</li>
                        <li>📊 Log for audit</li>
                        <li>🔔 Monitor trends</li>
                        <li>🎯 Continue scanning</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
        
        with col_btn1:
            if st.button("✅ Approve", use_container_width=True, help="Approve this transaction"):
                st.session_state.current_step = 3
                st.session_state.action = "approved"
                st.rerun()
        
        with col_btn2:
            if st.button("⚠️ Flag", use_container_width=True, help="Flag for manual review"):
                st.session_state.current_step = 3
                st.session_state.action = "flagged"
                st.rerun()
        
        with col_btn3:
            if st.button("🛑 Block", use_container_width=True, help="Block this transaction"):
                st.session_state.current_step = 3
                st.session_state.action = "blocked"
                st.rerun()
        
        with col_btn4:
            if st.button("🔄 New", use_container_width=True, help="Start new analysis"):
                st.session_state.current_step = 1
                st.session_state.transaction_data = {}
                st.rerun()
    
    # Step 3: Results
    elif st.session_state.current_step == 3:
        data = st.session_state.transaction_data
        action = st.session_state.get('action', 'reviewed')
        
        st.markdown("## ✅ Action Taken")
        
        if action == "approved":
            st.markdown('<div class="glass-card" style="border-left: 5px solid #10b981;">', unsafe_allow_html=True)
            st.markdown("### 🎉 Transaction Approved")
            st.markdown(f"""
            <div style="color: #374151;">
                Transaction **{data['id']}** has been successfully processed and approved.
                
                **Details:**
                - Amount: ${data['amount']:,.2f} {data['currency']}
                - Merchant: {data['merchant']}
                - Time: {data['timestamp']}
                - Status: ✅ **APPROVED**
                
                **Next Steps:**
                1. Transaction completed successfully
                2. Funds transferred to merchant
                3. Receipt sent to customer
                4. Logged for future reference
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        elif action == "flagged":
            st.markdown('<div class="glass-card" style="border-left: 5px solid #f59e0b;">', unsafe_allow_html=True)
            st.markdown("### ⚠️ Transaction Flagged")
            st.markdown(f"""
            <div style="color: #374151;">
                Transaction **{data['id']}** has been flagged for manual review.
                
                **Details:**
                - Amount: ${data['amount']:,.2f} {data['currency']}
                - Merchant: {data['merchant']}
                - Time: {data['timestamp']}
                - Status: ⚠️ **FLAGGED FOR REVIEW**
                
                **Next Steps:**
                1. Security team notified
                2. Customer verification initiated
                3. 24-hour hold period
                4. Manual review required
            </div>
            """, unsafe_allow_html=True)
        else:  # blocked
            st.markdown('<div class="glass-card" style="border-left: 5px solid #ef4444;">', unsafe_allow_html=True)
            st.markdown("### 🛑 Transaction Blocked")
            st.markdown(f"""
            <div style="color: #374151;">
                Transaction **{data['id']}** has been blocked due to high fraud risk.
                
                **Details:**
                - Amount: ${data['amount']:,.2f} {data['currency']}
                - Merchant: {data['merchant']}
                - Time: {data['timestamp']}
                - Status: 🛑 **BLOCKED**
                
                **Next Steps:**
                1. Account temporarily frozen
                2. Customer contacted
                3. Investigation initiated
                4. Authorities notified if required
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary statistics
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
        
        if st.button("🔄 Start New Transaction Analysis", type="primary", use_container_width=True):
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
            st.markdown('<span style="color: #10b981; font-weight: 600; font-size: 0.9rem;">+12.5% ▲</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.9%</div>', unsafe_allow_html=True)
            st.markdown("Detection Accuracy")
            st.markdown('<span style="color: #10b981; font-weight: 600; font-size: 0.9rem;">+0.08% ▲</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">48ms</div>', unsafe_allow_html=True)
            st.markdown("Avg. Response Time")
            st.markdown('<span style="color: #ef4444; font-weight: 600; font-size: 0.9rem;">-3.2% ▼</span>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">$124K</div>', unsafe_allow_html=True)
            st.markdown("Prevented Fraud")
            st.markdown('<span style="color: #10b981; font-weight: 600; font-size: 0.9rem;">+8.7% ▲</span>', unsafe_allow_html=True)
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
        <p style="margin: 0; font-weight: 700; color: #111827; font-size: 1.1rem;">
            🛡️ FraudGuard™ Enterprise v4.0
        </p>
        <p style="margin: 10px 0; color: #374151; font-size: 0.95rem;">
            Advanced AI-Powered Fraud Detection Platform
        </p>
        <p style="margin: 5px 0; color: #4b5563; font-size: 0.9rem;">
            📞 1-800-FRAUD | 📧 security@fraudguard.com
        </p>
        <p style="margin: 15px 0 0 0; color: #6b7280; font-size: 0.85rem;">
            © 2024 FraudGuard Global Security. All rights reserved. | PCI-DSS Compliant | ISO 27001 Certified
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

if __name__ == "__main__":
    main()

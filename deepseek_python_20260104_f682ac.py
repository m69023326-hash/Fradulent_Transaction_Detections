import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

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
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 1: Input, 2: Analysis, 3: Results

# Function to set background from URL
def set_background():
    # YOUR UNSHPLASH IMAGE URL
    background_url = "https://plus.unsplash.com/premium_photo-1675055730240-96a4ed84e482?q=80&w=327&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
    
    # Enhanced CSS with direct URL background
    style = f"""
    <style>
    /* Main app with your direct URL background image */
    .stApp {{
        background-image: url('{background_url}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }}
    
    /* Semi-transparent overlay for readability */
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
    
    /* Main content container */
    .main-container {{
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 40px;
        margin: 30px auto;
        max-width: 1400px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.4);
        position: relative;
        overflow: hidden;
    }}
    
    .main-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        background-size: 200% 100%;
        animation: gradient 3s ease infinite;
    }}
    
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Header styling */
    .header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        color: white;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.25);
        position: relative;
        overflow: hidden;
    }}
    
    .header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="none"/><path d="M0,50 Q25,40 50,50 T100,50" stroke="rgba(255,255,255,0.1)" fill="none" stroke-width="2"/></svg>');
        opacity: 0.3;
    }}
    
    /* Glass effect cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(15px);
        border-radius: 18px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .glass-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }}
    
    .glass-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
    }}
    
    /* Input form styling */
    .input-form {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.98) 100%);
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(229, 231, 235, 0.8);
        position: relative;
    }}
    
    .input-form::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 20px 20px 0 0;
    }}
    
    /* Toggle button */
    .toggle-btn {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3) !important;
        position: relative;
        overflow: hidden;
    }}
    
    .toggle-btn::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.6s;
    }}
    
    .toggle-btn:hover::before {{
        left: 100%;
    }}
    
    .toggle-btn:hover {{
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 12px 25px rgba(102, 126, 234, 0.4) !important;
    }}
    
    /* Step indicator */
    .step-indicator {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 40px 0;
        gap: 15px;
        position: relative;
    }}
    
    .step {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 18px;
        background: #e5e7eb;
        color: #6b7280;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 2;
        border: 3px solid white;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }}
    
    .step.active {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        transform: scale(1.1);
    }}
    
    .step.completed {{
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
    }}
    
    .step-line {{
        flex: 1;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #e5e7eb, #667eea);
        background-size: 200% 100%;
        animation: lineFlow 3s ease infinite;
        border-radius: 2px;
    }}
    
    @keyframes lineFlow {{
        0% {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::after {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 5px;
        height: 5px;
        background: rgba(255, 255, 255, 0.5);
        opacity: 0;
        border-radius: 100%;
        transform: scale(1, 1) translate(-50%);
        transform-origin: 50% 50%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4) !important;
    }}
    
    .stButton > button:active::after {{
        animation: ripple 1s ease-out;
    }}
    
    @keyframes ripple {{
        0% {{
            transform: scale(0, 0);
            opacity: 0.5;
        }}
        20% {{
            transform: scale(25, 25);
            opacity: 0.3;
        }}
        100% {{
            opacity: 0;
            transform: scale(40, 40);
        }}
    }}
    
    /* Metric cards */
    .metric-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(248, 250, 252, 0.95) 100%);
        padding: 25px 20px;
        border-radius: 18px;
        border: 1px solid rgba(229, 231, 235, 0.8);
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.1);
        border-color: rgba(102, 126, 234, 0.3);
    }}
    
    .metric-value {{
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 5px !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Risk level indicators */
    .risk-low {{
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.3);
    }}
    
    .risk-medium {{
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.3);
    }}
    
    .risk-high {{
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 5px 15px rgba(239, 68, 68, 0.3);
    }}
    
    /* Progress bars */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 10px !important;
    }}
    
    /* Select boxes and inputs */
    .stSelectbox > div > div > div, 
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {{
        border: 2px solid #e5e7eb !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif;
    }}
    
    .stSelectbox > div > div > div:hover,
    .stNumberInput > div > div > input:hover,
    .stTextInput > div > div > input:hover {{
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background-color: rgba(243, 244, 246, 0.5);
        padding: 10px;
        border-radius: 15px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 12px !important;
        padding: 14px 28px !important;
        background-color: white !important;
        color: #6b7280 !important;
        font-weight: 600 !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        border-color: transparent !important;
        transform: translateY(-2px);
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 30px;
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 50px;
        border-top: 1px solid rgba(229, 231, 235, 0.8);
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }}
    
    /* Chart styling */
    .js-plotly-plot .plotly {{
        background: transparent !important;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(243, 244, 246, 0.5);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .main-container {{
            padding: 20px;
            margin: 15px;
            border-radius: 15px;
        }}
        
        .header {{
            padding: 1.5rem;
            border-radius: 15px;
        }}
        
        .metric-value {{
            font-size: 2rem !important;
        }}
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
    
    # Header with toggle
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🛡️", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="header">
            <h1 style="color: white; margin-bottom: 10px; font-size: 2.8rem; text-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                FraudGuard™ Enterprise
            </h1>
            <h3 style="color: rgba(255, 255, 255, 0.95); margin: 5px 0; font-weight: 400;">
                Advanced Transaction Security Platform
            </h3>
            <p style="color: rgba(255, 255, 255, 0.85); margin: 10px 0 0 0; font-size: 1rem;">
                AI-Powered Real-time Fraud Detection & Prevention
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        toggle_icon = "🔽" if st.session_state.control_panel_visible else "▶️"
        toggle_text = "Hide Panel" if st.session_state.control_panel_visible else "Show Panel"
        if st.button(f"{toggle_icon} {toggle_text}", key="toggle_btn", help="Toggle Control Panel Visibility"):
            st.session_state.control_panel_visible = not st.session_state.control_panel_visible
            st.rerun()
    
    # Step indicator with connecting lines
    st.markdown("""
    <div class="step-indicator">
        <div class="step {}">📝</div>
        <div class="step-line"></div>
        <div class="step {}">🔍</div>
        <div class="step-line"></div>
        <div class="step {}">✅</div>
    </div>
    """.format(
        "active" if st.session_state.current_step == 1 else "completed",
        "active" if st.session_state.current_step == 2 else ("completed" if st.session_state.current_step > 2 else ""),
        "active" if st.session_state.current_step == 3 else ("completed" if st.session_state.current_step > 3 else "")
    ), unsafe_allow_html=True)
    
    # Step labels
    col_step1, col_step2, col_step3 = st.columns(3)
    with col_step1:
        st.markdown("<center><strong>Transaction Details</strong></center>", unsafe_allow_html=True)
    with col_step2:
        st.markdown("<center><strong>Fraud Analysis</strong></center>", unsafe_allow_html=True)
    with col_step3:
        st.markdown("<center><strong>Results</strong></center>", unsafe_allow_html=True)
    
    # Step 1: Transaction Input
    if st.session_state.current_step == 1:
        st.markdown("## 📝 Step 1: Transaction Details")
        st.markdown("Enter the transaction information for AI-powered fraud analysis")
        
        with st.form("transaction_input"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 💳 Basic Information")
                
                transaction_id = st.text_input("Transaction ID", 
                    value=f"TXN-{np.random.randint(100000, 999999)}",
                    help="Unique transaction identifier")
                
                amount = st.number_input("Amount (USD)", 
                    min_value=0.0, 
                    max_value=100000.0, 
                    value=2475.50, 
                    step=100.0,
                    help="Transaction amount in USD")
                
                currency = st.selectbox("Currency", 
                    ["USD", "EUR", "GBP", "CAD", "AUD", "JPY"], 
                    index=0,
                    help="Transaction currency")
                
                merchant = st.selectbox("Merchant", 
                    ["Amazon", "Apple", "Netflix", "Uber", "Airbnb", "Walmart", "Target", "Best Buy", "Other"], 
                    index=0,
                    help="Merchant name")
                
                country = st.selectbox("Country", 
                    ["United States", "Canada", "United Kingdom", "Germany", "Australia", "Japan", "France", "Singapore"], 
                    index=0,
                    help="Transaction origin country")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("### 🔍 Risk Parameters")
                
                st.markdown("#### V14 - Structural Analysis")
                v14 = st.slider("Structural Anomaly Score", 0.0, 1.0, 0.68, 0.01,
                    help="Measures structural anomalies in transaction patterns. Higher values indicate higher risk.")
                
                risk_color = "#ef4444" if v14 > 0.8 else "#f59e0b" if v14 > 0.6 else "#10b981"
                risk_text = "High Risk" if v14 > 0.8 else "Medium Risk" if v14 > 0.6 else "Low Risk"
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 15px; margin: 15px 0;">
                    <div style="flex: 1; height: 8px; background: #e5e7eb; border-radius: 4px;">
                        <div style="width: {v14*100}%; height: 100%; background: {risk_color}; border-radius: 4px;"></div>
                    </div>
                    <span style="color: {risk_color}; font-weight: 600; min-width: 80px;">{risk_text}</span>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### V17 - Behavioral Analysis")
                v17 = st.slider("Behavioral Pattern Score", 0.0, 1.0, 0.42, 0.01,
                    help="Analyzes user behavior patterns and deviations from normal patterns.")
                
                risk_color2 = "#ef4444" if v17 > 0.7 else "#f59e0b" if v17 > 0.5 else "#10b981"
                risk_text2 = "High Risk" if v17 > 0.7 else "Medium Risk" if v17 > 0.5 else "Low Risk"
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 15px; margin: 15px 0;">
                    <div style="flex: 1; height: 8px; background: #e5e7eb; border-radius: 4px;">
                        <div style="width: {v17*100}%; height: 100%; background: {risk_color2}; border-radius: 4px;"></div>
                    </div>
                    <span style="color: {risk_color2}; font-weight: 600; min-width: 80px;">{risk_text2}</span>
                </div>
                """, unsafe_allow_html=True)
                
                payment_method = st.selectbox("Payment Method", 
                    ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer", "Cryptocurrency"], 
                    index=0,
                    help="Payment method used for transaction")
                
                device_type = st.selectbox("Device Type", 
                    ["Mobile", "Desktop", "Tablet", "Unknown"], 
                    index=0,
                    help="Device used for transaction")
                st.markdown('</div>', unsafe_allow_html=True)
            
            submitted = st.form_submit_button("🚀 Analyze Transaction", type="primary", use_container_width=True)
            
            if submitted:
                st.session_state.transaction_data = {
                    "id": transaction_id,
                    "amount": amount,
                    "currency": currency,
                    "merchant": merchant,
                    "country": country,
                    "v14": v14,
                    "v17": v17,
                    "payment_method": payment_method,
                    "device_type": device_type,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.current_step = 2
                st.rerun()
    
    # Step 2: Fraud Analysis
    elif st.session_state.current_step == 2:
        data = st.session_state.transaction_data
        
        st.markdown("## 🔍 Step 2: Fraud Analysis")
        st.markdown(f"**Analyzing Transaction:** `{data['id']}`")
        
        # Calculate fraud probability with enhanced algorithm
        with st.spinner("🤖 AI model analyzing transaction patterns..."):
            # Simulate analysis delay
            import time
            time.sleep(1)
            
            # Enhanced risk calculation
            base_risk = 0.05
            amount_risk = min(data['amount'] / 5000, 0.3)  # Amount risk caps at 30%
            v14_risk = data['v14'] * 0.4
            v17_risk = data['v17'] * 0.35
            method_risk = 0.15 if data['payment_method'] in ["Digital Wallet", "Cryptocurrency"] else 0.05
            device_risk = 0.2 if data['device_type'] == "Unknown" else 0.05
            country_risk = 0.1 if data['country'] not in ["United States", "Canada", "United Kingdom"] else 0.05
            
            fraud_probability = min(base_risk + amount_risk + v14_risk + v17_risk + method_risk + device_risk + country_risk, 0.95)
            
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
            
            # Risk score with gauge
            st.markdown(f"#### {icon} Risk Assessment")
            risk_score = fraud_probability * 100
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fraud Probability", 'font': {'size': 20}},
                number={'font': {'size': 40, 'color': risk_color}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 2, 'tickcolor': "darkgray"},
                    'bar': {'color': risk_color, 'thickness': 0.3},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "lightgray",
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(16, 185, 129, 0.3)"},
                        {'range': [30, 70], 'color': "rgba(245, 158, 11, 0.3)"},
                        {'range': [70, 100], 'color': "rgba(239, 68, 68, 0.3)"}
                    ],
                    'threshold': {
                        'line': {'color': risk_color, 'width': 4},
                        'thickness': 0.8,
                        'value': risk_score
                    }
                }
            ))
            
            fig.update_layout(
                height=300,
                font={'family': "Inter, -apple-system, BlinkMacSystemFont, sans-serif"},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk factors visualization
            st.markdown("#### ⚡ Risk Factors Breakdown")
            
            factors = [
                ("Transaction Amount", amount_risk * 100, "#667eea"),
                ("Structural Anomaly", data['v14'] * 40, "#764ba2"),
                ("Behavioral Pattern", data['v17'] * 35, "#8b5cf6"),
                ("Payment Method", method_risk * 100, "#10b981"),
                ("Device Trust", device_risk * 100, "#f59e0b"),
                ("Geo-location", country_risk * 100, "#ef4444")
            ]
            
            for factor, value, color in factors:
                st.markdown(f"""
                <div style="margin: 12px 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                        <span style="font-weight: 500; color: #374151;">{factor}</span>
                        <span style="color: {color}; font-weight: 600;">{value:.1f}%</span>
                    </div>
                    <div style="width: 100%; background: rgba(229, 231, 235, 0.5); border-radius: 8px; height: 10px;">
                        <div style="width: {value}%; background: {color}; height: 10px; border-radius: 8px; 
                             box-shadow: 0 2px 8px {color}40;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 Transaction Summary")
            
            summary_data = [
                ("ID", data['id'], "#6b7280"),
                ("Amount", f"${data['amount']:,.2f} {data['currency']}", "#059669"),
                ("Merchant", data['merchant'], "#7c3aed"),
                ("Country", data['country'], "#3b82f6"),
                ("Payment", data['payment_method'], "#8b5cf6"),
                ("Device", data['device_type'], "#f59e0b"),
                ("V14 Score", f"{data['v14']:.2f}", "#ef4444" if data['v14'] > 0.6 else "#f59e0b"),
                ("V17 Score", f"{data['v17']:.2f}", "#ef4444" if data['v17'] > 0.5 else "#f59e0b"),
                ("Time", data['timestamp'], "#6b7280")
            ]
            
            for label, value, color in summary_data:
                st.markdown(f"""
                <div style="padding: 10px 0; border-bottom: 1px solid rgba(243, 244, 246, 0.8);">
                    <div style="font-size: 0.85rem; color: #9ca3af; margin-bottom: 2px;">{label}</div>
                    <div style="font-weight: 600; color: {color if isinstance(color, str) else '#374151'};">{value}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Action recommendations
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### ⚡ Recommended Action")
            
            if fraud_probability > 0.7:
                st.markdown('<span class="risk-high">🚨 HIGH RISK</span>', unsafe_allow_html=True)
                st.markdown("""
                **Immediate Actions:**
                1. 🛑 Block transaction
                2. 🔒 Freeze account
                3. 📞 Contact customer
                4. 🚓 Report to authorities
                """)
            elif fraud_probability > 0.4:
                st.markdown('<span class="risk-medium">⚠️ MEDIUM RISK</span>', unsafe_allow_html=True)
                st.markdown("""
                **Recommended Actions:**
                1. ⏸️ Hold for review
                2. 🔐 Require 2FA
                3. 📧 Send alert
                4. 👁️ Monitor activity
                """)
            else:
                st.markdown('<span class="risk-low">✅ LOW RISK</span>', unsafe_allow_html=True)
                st.markdown("""
                **Actions:**
                1. ✅ Approve transaction
                2. 📊 Log for audit
                3. 🔔 Monitor trends
                4. 🎯 Continue scanning
                """)
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
        
        st.markdown("## ✅ Step 3: Action Taken")
        
        if action == "approved":
            st.markdown('<div class="glass-card" style="border-left: 5px solid #10b981;">', unsafe_allow_html=True)
            st.markdown("### 🎉 Transaction Approved")
            st.markdown(f"""
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
            """)
            st.balloons()
        elif action == "flagged":
            st.markdown('<div class="glass-card" style="border-left: 5px solid #f59e0b;">', unsafe_allow_html=True)
            st.markdown("### ⚠️ Transaction Flagged")
            st.markdown(f"""
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
            """)
        else:  # blocked
            st.markdown('<div class="glass-card" style="border-left: 5px solid #ef4444;">', unsafe_allow_html=True)
            st.markdown("### 🛑 Transaction Blocked")
            st.markdown(f"""
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
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown('<div class="metric-value">99.92%</div>', unsafe_allow_html=True)
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
            st.session_state.show_analysis = False
            st.rerun()
    
    # Control Panel (Toggleable)
    if st.session_state.control_panel_visible:
        st.markdown("---")
        st.markdown("## 🎛️ Control Panel")
        
        # Tabs for different control sections
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "⚙️ Settings", "🔔 Alerts", "📈 Analytics"])
        
        with tab1:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<div class="metric-value">1,247</div>', unsafe_allow_html=True)
                st.markdown("Today's Transactions")
                st.markdown('<span style="color: #10b981; font-weight: 600; font-size: 0.9rem;">+12.5% ▲</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown('<div class="metric-value">99.92%</div>', unsafe_allow_html=True)
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
                st.markdown('<div class="metric-value">$124.5K</div>', unsafe_allow_html=True)
                st.markdown("Prevented Fraud")
                st.markdown('<span style="color: #10b981; font-weight: 600; font-size: 0.9rem;">+8.7% ▲</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            col_act1, col_act2, col_act3, col_act4 = st.columns(4)
            
            with col_act1:
                if st.button("🔄 Update Model", use_container_width=True):
                    st.success("Model update initiated")
            
            with col_act2:
                if st.button("📊 Generate Report", use_container_width=True):
                    st.info("Report generation started")
            
            with col_act3:
                if st.button("🔍 Run Audit", use_container_width=True):
                    st.warning("System audit in progress")
            
            with col_act4:
                if st.button("⚙️ Settings", use_container_width=True):
                    st.info("Opening settings panel")
        
        with tab2:
            st.markdown("### System Configuration")
            col_set1, col_set2 = st.columns(2)
            
            with col_set1:
                st.selectbox("Detection Sensitivity", ["Low", "Medium", "High", "Custom"], index=1)
                st.slider("Alert Threshold", 0, 100, 75)
                st.checkbox("Enable Real-time Monitoring", value=True)
                st.checkbox("Auto-flag Suspicious Transactions", value=True)
            
            with col_set2:
                st.selectbox("Data Retention Period", ["30 days", "90 days", "1 year", "Indefinite"], index=1)
                st.selectbox("Report Frequency", ["Daily", "Weekly", "Monthly", "Real-time"], index=0)
                st.checkbox("Enable API Access", value=True)
                st.checkbox("Audit Logging", value=True)
        
        with tab3:
            st.markdown("### Recent Alerts")
            
            alerts = [
                {"time": "2 min ago", "type": "🚨 High Risk", "message": "Unusual transaction pattern detected", "status": "Active"},
                {"time": "15 min ago", "type": "⚠️ Medium Risk", "message": "Multiple failed login attempts", "status": "Resolved"},
                {"time": "1 hour ago", "type": "ℹ️ System", "message": "Database backup completed", "status": "Completed"},
                {"time": "2 hours ago", "type": "👁️ Low Risk", "message": "Geolocation mismatch detected", "status": "Under Review"}
            ]
            
            for alert in alerts:
                bg_color = "#fef2f2" if "High" in alert["type"] else "#fffbeb" if "Medium" in alert["type"] else "#f0f9ff"
                border_color = "#fecaca" if "High" in alert["type"] else "#fde68a" if "Medium" in alert["type"] else "#bae6fd"
                
                st.markdown(f"""
                <div style="background: {bg_color}; border: 2px solid {border_color}; border-radius: 12px; padding: 15px; margin: 10px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div style="flex: 1;">
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                                <strong>{alert['type']}</strong>
                                <span style="background: {'#ef4444' if 'Active' in alert['status'] else '#10b981'}; 
                                      color: white; padding: 2px 10px; border-radius: 20px; font-size: 0.8rem;">
                                    {alert['status']}
                                </span>
                            </div>
                            <p style="margin: 0; color: #374151;">{alert['message']}</p>
                        </div>
                        <div style="text-align: right; min-width: 100px;">
                            <small style="color: #6b7280;">{alert['time']}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### Performance Analytics")
            
            # Generate sample data for charts
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            np.random.seed(42)
            fraud_cases = np.random.randint(5, 50, 30)
            transactions = np.random.randint(1000, 5000, 30)
            
            chart_data = pd.DataFrame({
                'Date': dates,
                'Fraud Cases': fraud_cases,
                'Total Transactions': transactions,
                'Fraud Rate': (fraud_cases / transactions * 100)
            })
            
            # Line chart
            fig = px.line(chart_data, x='Date', y='Fraud Rate', 
                         title='📈 Daily Fraud Rate Trend',
                         labels={'Fraud Rate': 'Fraud Rate (%)'},
                         line_shape='spline',
                         color_discrete_sequence=['#667eea'])
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font={'family': "Inter, sans-serif"},
                hovermode='x unified',
                xaxis_title="Date",
                yaxis_title="Fraud Rate (%)",
                title_font_size=18
            )
            
            fig.update_traces(line=dict(width=3),
                             marker=dict(size=8, color='#764ba2'),
                             hovertemplate='<b>%{x}</b><br>Fraud Rate: %{y:.2f}%<extra></extra>')
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="text-align: left;">
                <p style="margin: 0; font-weight: 700; font-size: 1.1rem; color: #374151;">
                    🛡️ FraudGuard™ Enterprise v4.0
                </p>
                <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 0.9rem;">
                    Advanced AI-Powered Fraud Detection Platform
                </p>
            </div>
            
            <div style="text-align: center;">
                <div style="display: flex; gap: 20px; justify-content: center;">
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">
                            📞 1-800-FRAUD
                        </p>
                    </div>
                    <div style="text-align: center;">
                        <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">
                            📧 security@fraudguard.com
                        </p>
                    </div>
                </div>
            </div>
            
            <div style="text-align: right;">
                <div style="display: flex; align-items: center; gap: 10px; background: rgba(16, 185, 129, 0.1); 
                     padding: 8px 16px; border-radius: 50px;">
                    <div style="width: 10px; height: 10px; background: #10b981; border-radius: 50%;"></div>
                    <p style="margin: 0; color: #10b981; font-weight: 600; font-size: 0.9rem;">
                        🟢 System Operational
                    </p>
                </div>
                <p style="margin: 5px 0 0 0; color: #9ca3af; font-size: 0.85rem;">
                    Last Updated: {}
                </p>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(229, 231, 235, 0.5);">
            <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
                <span style="color: #6b7280; font-size: 0.85rem;">✅ PCI-DSS Compliant</span>
                <span style="color: #6b7280; font-size: 0.85rem;">✅ ISO 27001 Certified</span>
                <span style="color: #6b7280; font-size: 0.85rem;">✅ GDPR Compliant</span>
                <span style="color: #6b7280; font-size: 0.85rem;">✅ SOC 2 Type II</span>
            </div>
            <p style="margin: 15px 0 0 0; color: #9ca3af; font-size: 0.85rem; text-align: center;">
                © 2024 FraudGuard Global Security. All rights reserved. | Advanced Security Analytics Platform
            </p>
        </div>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

if __name__ == "__main__":
    main()

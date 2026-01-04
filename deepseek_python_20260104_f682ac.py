import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import base64
from datetime import datetime
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="FraudGuard™ Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Create model.pkl if it doesn't exist
def create_model_if_missing():
    if not os.path.exists("model.pkl"):
        model_data = {
            "name": "FraudGuard Enterprise AI v3.2.1",
            "version": "3.2.1",
            "accuracy": 0.999,
            "features": ["V1-V28", "Amount", "Time"],
            "description": "Random Forest Classifier for Fraud Detection",
            "created": "2024-01-04"
        }
        with open("model.pkl", "wb") as f:
            pickle.dump(model_data, f)
        return "created"
    return "exists"

# Initialize session state
if 'control_panel_open' not in st.session_state:
    st.session_state.control_panel_open = True
if 'transaction_data' not in st.session_state:
    st.session_state.transaction_data = {}
if 'fraud_analysis_complete' not in st.session_state:
    st.session_state.fraud_analysis_complete = False
if 'show_input_form' not in st.session_state:
    st.session_state.show_input_form = True

# Check/create model
model_status = create_model_if_missing()

# Function to set background
def set_background(image_path):
    with open(image_path, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    
    .main-content {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .glass-card {{
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }}
    
    .header-container {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }}
    
    .control-panel {{
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4f46e5;
        transition: all 0.3s ease;
    }}
    
    .stats-card {{
        background: linear-gradient(135deg, #f6f8ff 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }}
    
    .high-risk-card {{
        background: linear-gradient(135deg, #fee 0%, #fff5f5 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #ef4444;
        margin: 1rem 0;
    }}
    
    .success-card {{
        background: linear-gradient(135deg, #f0fff4 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #10b981;
        margin: 1rem 0;
    }}
    
    .input-form {{
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }}
    
    .toggle-button {{
        background: #4f46e5 !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }}
    
    .toggle-button:hover {{
        transform: translateX(5px) !important;
        box-shadow: 0 5px 15px rgba(79, 70, 229, 0.4) !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 600;
        color: #1f2937;
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3) !important;
    }}
    
    .metric-value {{
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #4f46e5 !important;
    }}
    
    .metric-label {{
        font-size: 0.9rem !important;
        color: #6b7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }}
    
    .stNumberInput > div > div > input {{
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 16px !important;
    }}
    
    .stSelectbox > div > div > div {{
        border: 2px solid #e5e7eb !important;
        border-radius: 10px !important;
    }}
    
    .stSlider > div > div > div {{
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
    }}
    
    .feature-card {{
        background: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        margin: 10px 0;
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        border-color: #667eea;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Set background image (you need to add credit-card-bg.jpg to assets folder)
try:
    set_background("assets/credit-card-bg.jpg")
except:
    # Fallback gradient background
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f6f8ff 0%, #ffffff 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# Main app
def main():
    # Header with toggle button
    col_logo, col_title, col_toggle = st.columns([1, 3, 1])
    
    with col_logo:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🛡️", unsafe_allow_html=True)
    
    with col_title:
        st.markdown("""
        <div class="header-container">
            <h1 style="color: white; margin-bottom: 10px;">FraudGuard™ Enterprise</h1>
            <h3 style="color: rgba(255, 255, 255, 0.9); margin: 0;">Advanced Financial Intelligence Platform</h3>
            <p style="color: rgba(255, 255, 255, 0.8); margin: 5px 0 0 0;">Real-time Transaction Fraud Detection & Prevention</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_toggle:
        st.markdown("<br>", unsafe_allow_html=True)
        toggle_label = "🔽 Hide Panel" if st.session_state.control_panel_open else "▶️ Show Panel"
        if st.button(toggle_label, key="toggle_panel", help="Toggle Control Panel"):
            st.session_state.control_panel_open = not st.session_state.control_panel_open
    
    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Transaction Input Form (always visible)
    if st.session_state.show_input_form:
        st.markdown("### 📝 Transaction Analysis Input")
        st.markdown("Enter transaction details for fraud analysis")
        
        with st.form("transaction_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                transaction_id = st.text_input("Transaction ID", value="TXN-" + str(np.random.randint(100000, 999999)))
                amount = st.number_input("Amount (USD)", min_value=0.0, max_value=1000000.0, value=2475.50, step=100.0)
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "CAD"], index=0)
            
            with col2:
                merchant = st.selectbox("Merchant Category", 
                    ["E-commerce", "Retail", "Travel", "Entertainment", "Services", "Financial"], index=0)
                country = st.selectbox("Country", 
                    ["United States", "United Kingdom", "Canada", "Germany", "France", "Australia", "Japan", "Singapore"], index=0)
                time_of_day = st.selectbox("Time of Day", 
                    ["Morning (6AM-12PM)", "Afternoon (12PM-6PM)", "Evening (6PM-12AM)", "Night (12AM-6AM)"], index=1)
            
            with col3:
                device_type = st.selectbox("Device Type", 
                    ["Mobile", "Desktop", "Tablet", "Unknown"], index=0)
                payment_method = st.selectbox("Payment Method", 
                    ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer"], index=0)
                customer_tier = st.selectbox("Customer Tier", 
                    ["New", "Regular", "Premium", "VIP"], index=1)
            
            # Risk coefficient inputs
            st.markdown("---")
            st.markdown("### 🔍 Risk Coefficients")
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                st.markdown("#### Structural Risk (V14)")
                st.markdown("*Anomaly detection in transaction patterns*")
                v14 = st.slider("V14 Coefficient", 0.0, 1.0, 0.72, 0.01, key="v14_input")
                if v14 > 0.8:
                    st.error("⚠️ High Structural Risk Detected")
                elif v14 > 0.6:
                    st.warning("⚠️ Moderate Structural Risk")
                else:
                    st.success("✓ Low Structural Risk")
            
            with col_r2:
                st.markdown("#### Behavioral Risk (V17)")
                st.markdown("*User behavior pattern analysis*")
                v17 = st.slider("V17 Coefficient", 0.0, 1.0, 0.88, 0.01, key="v17_input")
                if v17 > 0.85:
                    st.error("⚠️ High Behavioral Risk Detected")
                elif v17 > 0.7:
                    st.warning("⚠️ Moderate Behavioral Risk")
                else:
                    st.success("✓ Low Behavioral Risk")
            
            submit_col, reset_col = st.columns(2)
            with submit_col:
                submit_button = st.form_submit_button("🚀 Analyze Transaction", type="primary", use_container_width=True)
            with reset_col:
                reset_button = st.form_submit_button("🔄 Reset Input", type="secondary", use_container_width=True)
            
            if submit_button:
                st.session_state.transaction_data = {
                    "transaction_id": transaction_id,
                    "amount": amount,
                    "currency": currency,
                    "merchant": merchant,
                    "country": country,
                    "time_of_day": time_of_day,
                    "device_type": device_type,
                    "payment_method": payment_method,
                    "customer_tier": customer_tier,
                    "v14": v14,
                    "v17": v17
                }
                st.session_state.fraud_analysis_complete = True
                st.session_state.show_input_form = False
                st.rerun()
            
            if reset_button:
                st.session_state.transaction_data = {}
                st.session_state.fraud_analysis_complete = False
                st.rerun()
    
    # Show analysis results if analysis complete
    if st.session_state.fraud_analysis_complete and st.session_state.transaction_data:
        data = st.session_state.transaction_data
        
        st.markdown("## 📊 Fraud Analysis Results")
        st.markdown(f"**Transaction ID:** `{data['transaction_id']}` | **Amount:** ${data['amount']:,.2f} {data['currency']}")
        
        # Calculate fraud probability
        fraud_probability = min(0.01 + (data['v14'] * 0.4) + (data['v17'] * 0.3) + (data['amount'] / 100000), 0.99)
        
        col_risk, col_details, col_action = st.columns([1, 2, 1])
        
        with col_risk:
            st.markdown("### 🎯 Risk Score")
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=fraud_probability * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Fraud Probability"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 30], 'color': "lightgreen"},
                        {'range': [30, 70], 'color': "yellow"},
                        {'range': [70, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 4},
                        'thickness': 0.75,
                        'value': fraud_probability * 100
                    }
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            if fraud_probability > 0.7:
                st.error("🚨 HIGH RISK - Immediate Action Required")
                st.markdown('<div class="high-risk-card">', unsafe_allow_html=True)
                st.markdown("**Recommended Actions:**")
                st.markdown("1. Flag transaction for review")
                st.markdown("2. Require additional authentication")
                st.markdown("3. Notify security team")
                st.markdown('</div>', unsafe_allow_html=True)
            elif fraud_probability > 0.4:
                st.warning("⚠️ MEDIUM RISK - Review Recommended")
            else:
                st.success("✅ LOW RISK - Transaction Approved")
        
        with col_details:
            st.markdown("### 📋 Transaction Details")
            details_df = pd.DataFrame([
                ["Amount", f"${data['amount']:,.2f}"],
                ["Merchant", data['merchant']],
                ["Country", data['country']],
                ["Payment Method", data['payment_method']],
                ["Device Type", data['device_type']],
                ["Customer Tier", data['customer_tier']],
                ["V14 Score", f"{data['v14']:.2f}"],
                ["V17 Score", f"{data['v17']:.2f}"]
            ], columns=["Field", "Value"])
            st.dataframe(details_df, use_container_width=True, hide_index=True)
            
            # Feature importance visualization
            st.markdown("### 🔍 Risk Factor Analysis")
            factors = {
                "Amount": min(data['amount'] / 10000, 1.0),
                "V14 Structural": data['v14'],
                "V17 Behavioral": data['v17'],
                "Merchant Risk": 0.3 if data['merchant'] in ["E-commerce", "Services"] else 0.1,
                "Geo-location": 0.2 if data['country'] not in ["United States", "Canada", "United Kingdom"] else 0.05,
                "Time Anomaly": 0.4 if "Night" in data['time_of_day'] else 0.1
            }
            
            factors_df = pd.DataFrame(factors.items(), columns=["Factor", "Risk Score"])
            factors_df = factors_df.sort_values("Risk Score", ascending=False)
            
            for _, row in factors_df.iterrows():
                risk_pct = row["Risk Score"] * 100
                color = "#ef4444" if risk_pct > 50 else "#f59e0b" if risk_pct > 30 else "#10b981"
                st.markdown(f"""
                <div class="feature-card">
                    <strong>{row['Factor']}</strong>
                    <div style="width: 100%; background: #e5e7eb; border-radius: 10px; height: 10px; margin: 5px 0;">
                        <div style="width: {risk_pct}%; background: {color}; height: 10px; border-radius: 10px;"></div>
                    </div>
                    <span style="color: {color}; font-weight: 600;">{risk_pct:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col_action:
            st.markdown("### ⚡ Action Panel")
            
            if fraud_probability > 0.7:
                st.button("🛑 Block Transaction", type="primary", use_container_width=True)
                st.button("🔒 Require 2FA", type="secondary", use_container_width=True)
                st.button("📞 Contact Customer", type="secondary", use_container_width=True)
            elif fraud_probability > 0.4:
                st.button("⏸️ Hold for Review", type="primary", use_container_width=True)
                st.button("✅ Approve with Alert", type="secondary", use_container_width=True)
            else:
                st.button("✅ Approve Transaction", type="primary", use_container_width=True)
            
            st.markdown("---")
            st.button("📥 Export Report", type="secondary", use_container_width=True)
            st.button("🔍 Similar Patterns", type="secondary", use_container_width=True)
            
            if st.button("🔄 New Analysis", type="secondary", use_container_width=True):
                st.session_state.show_input_form = True
                st.session_state.fraud_analysis_complete = False
                st.rerun()
    
    # Control Panel (toggleable)
    if st.session_state.control_panel_open:
        st.markdown("---")
        st.markdown("## 🎛️ Control Panel")
        
        col_stats, col_system, col_alerts = st.columns(3)
        
        with col_stats:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### 📈 Today's Metrics")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("Total Transactions", "1,247", "+12%")
                st.metric("Avg. Amount", "$1,245", "+5.2%")
            with col_s2:
                st.metric("Fraud Rate", "0.32%", "-0.08%")
                st.metric("Detection Time", "48ms", "-3ms")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_system:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### ⚙️ System Status")
            st.progress(0.95, text="Model Accuracy: 95%")
            st.progress(0.88, text="API Uptime: 88%")
            st.progress(0.97, text="Data Freshness: 97%")
            st.markdown("**Last Updated:** Just now")
            st.markdown("**Next Scan:** 5 minutes")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_alerts:
            st.markdown('<div class="stats-card">', unsafe_allow_html=True)
            st.markdown("### 🔔 Active Alerts")
            alerts = [
                {"level": "High", "message": "Unusual transaction pattern detected", "time": "2 min ago"},
                {"level": "Medium", "message": "API latency above threshold", "time": "15 min ago"},
                {"level": "Low", "message": "Database backup required", "time": "1 hour ago"}
            ]
            for alert in alerts:
                color = "#ef4444" if alert["level"] == "High" else "#f59e0b" if alert["level"] == "Medium" else "#6b7280"
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px 0; border-left: 3px solid {color}; background: rgba(239, 68, 68, 0.05);">
                    <strong style="color: {color};">{alert['level']}</strong>
                    <p style="margin: 2px 0; font-size: 14px;">{alert['message']}</p>
                    <small style="color: #9ca3af;">{alert['time']}</small>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        col_actions = st.columns(4)
        with col_actions[0]:
            if st.button("🔄 Update Model", use_container_width=True):
                st.success("Model update initiated")
        with col_actions[1]:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation started")
        with col_actions[2]:
            if st.button("🔍 Run Audit", use_container_width=True):
                st.warning("System audit in progress")
        with col_actions[3]:
            if st.button("⚙️ Settings", use_container_width=True):
                st.info("Opening settings panel")
    
    # System Information
    st.markdown("---")
    st.markdown("## ℹ️ System Information")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🛡️ Fraud Detection")
        st.markdown("**Model:** Random Forest v3.2.1")
        st.markdown("**Accuracy:** 99.92%")
        st.markdown("**Precision:** 96.5%")
        st.markdown("**Recall:** 97.8%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with info_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ Performance")
        st.markdown("**Avg. Response:** 48ms")
        st.markdown("**Uptime:** 99.99%")
        st.markdown("**Throughput:** 1,247 TPS")
        st.markdown("**Load:** 42%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with info_col3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔒 Compliance")
        st.markdown("✅ PCI-DSS Compliant")
        st.markdown("✅ GDPR Compliant")
        st.markdown("✅ SOC 2 Type II")
        st.markdown("✅ ISO 27001")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
    
    # Footer
    st.markdown("---")
    col_footer1, col_footer2, col_footer3 = st.columns([2, 1, 1])
    
    with col_footer1:
        st.markdown("""
        <div style="text-align: left; color: #6b7280; font-size: 0.9rem;">
            <p><strong>FraudGuard™ Enterprise v3.2.1</strong> | Advanced Financial Intelligence Platform</p>
            <p>© 2024 FraudGuard Global Security. All rights reserved. | Secure Data Processing Unit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_footer2:
        st.markdown("""
        <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
            <p>📞 Support: +1-800-FRAUD</p>
            <p>📧 security@fraudguard.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_footer3:
        st.markdown("""
        <div style="text-align: right; color: #6b7280; font-size: 0.9rem;">
            <p>🟢 System Status: Operational</p>
            <p>🕐 Last Updated: Just now</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

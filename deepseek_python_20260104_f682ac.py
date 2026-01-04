import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime, timedelta
import random

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

# Generate realistic sample data
def generate_sample_data():
    # Recent transactions
    transactions = []
    for i in range(8):
        amount = random.uniform(50, 5000)
        risk = random.choice(['Low', 'Medium', 'High'])
        status = 'Approved' if risk == 'Low' else 'Under Review' if risk == 'Medium' else 'Blocked'
        transactions.append({
            'ID': f"TXN-{10000+i}",
            'Amount': f"${amount:,.2f}",
            'Merchant': random.choice(['Amazon', 'Apple', 'Netflix', 'Uber', 'Airbnb', 'Walmart', 'Target']),
            'Risk': risk,
            'Status': status,
            'Time': (datetime.now() - timedelta(hours=random.randint(1, 24))).strftime("%H:%M")
        })
    
    # Top merchants by fraud attempts
    merchants = [
        {'Name': 'Amazon', 'Attempts': 42, 'Success Rate': '98.5%'},
        {'Name': 'Apple', 'Attempts': 38, 'Success Rate': '97.2%'},
        {'Name': 'Netflix', 'Attempts': 29, 'Success Rate': '99.1%'},
        {'Name': 'Uber', 'Attempts': 25, 'Success Rate': '96.8%'},
        {'Name': 'Airbnb', 'Attempts': 22, 'Success Rate': '95.4%'}
    ]
    
    # Fraud patterns detected
    patterns = [
        {'Pattern': 'Rapid Multi-transaction', 'Frequency': 'High', 'Risk': '87%'},
        {'Pattern': 'Geo-location Mismatch', 'Frequency': 'Medium', 'Risk': '72%'},
        {'Pattern': 'Unusual Time Activity', 'Frequency': 'Low', 'Risk': '58%'},
        {'Pattern': 'Amount Spike Detection', 'Frequency': 'High', 'Risk': '91%'},
        {'Pattern': 'Device Fingerprint Change', 'Frequency': 'Medium', 'Risk': '65%'}
    ]
    
    # System performance metrics
    performance = {
        'uptime': '99.98%',
        'response_time': '42ms',
        'accuracy': '99.92%',
        'throughput': '1,247 TPS',
        'false_positives': '0.08%'
    }
    
    return {
        'transactions': transactions,
        'merchants': merchants,
        'patterns': patterns,
        'performance': performance
    }

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
        background: rgba(255, 255, 255, 0.95);
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
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(248, 250, 252, 0.98) 100%);
        padding: 25px 20px;
        border-radius: 18px;
        border: 1px solid rgba(229, 231, 235, 0.9);
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
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
    
    /* Table styling */
    .data-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }}
    
    .data-table th {{
        background: #f8fafc;
        padding: 12px;
        text-align: left;
        color: #374151;
        font-weight: 600;
        border-bottom: 2px solid #e5e7eb;
    }}
    
    .data-table td {{
        padding: 12px;
        border-bottom: 1px solid #f3f4f6;
        color: #1f2937;
    }}
    
    .data-table tr:hover {{
        background: #f9fafb;
    }}
    
    /* Status badges */
    .status-approved {{
        background: #d1fae5;
        color: #065f46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    
    .status-review {{
        background: #fef3c7;
        color: #92400e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    
    .status-blocked {{
        background: #fee2e2;
        color: #991b1b;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    
    /* Risk indicators */
    .risk-low {{
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
    }}
    
    .risk-medium {{
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
    }}
    
    .risk-high {{
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: white !important;
        padding: 8px 16px;
        border-radius: 50px;
        font-weight: 600;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Set background
set_background()

# Generate sample data
sample_data = generate_sample_data()

# Main app
def main():
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header">
        <h1 style="color: white; margin-bottom: 10px; font-size: 2.8rem;">
            FraudGuard™ Enterprise
        </h1>
        <h3 style="color: rgba(255, 255, 255, 0.95); margin: 5px 0; font-weight: 400;">
            Advanced Transaction Security Platform
        </h3>
        <p style="color: rgba(255, 255, 255, 0.85); margin: 10px 0 0 0;">
            Real-time AI-powered fraud detection & prevention
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top Metrics Row
    st.markdown("## 📊 Live Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">1,247</div>', unsafe_allow_html=True)
        st.markdown("Transactions Today")
        st.markdown('<span style="color: #10b981; font-weight: 600;">+12.5% from yesterday</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">$24.7K</div>', unsafe_allow_html=True)
        st.markdown("Fraud Prevented")
        st.markdown('<span style="color: #10b981; font-weight: 600;">Saved this week</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">99.92%</div>', unsafe_allow_html=True)
        st.markdown("Detection Accuracy")
        st.markdown('<span style="color: #10b981; font-weight: 600;">Industry leading</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-value">42ms</div>', unsafe_allow_html=True)
        st.markdown("Avg Response Time")
        st.markdown('<span style="color: #ef4444; font-weight: 600;">-3.2ms improvement</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Transactions and Fraud Patterns
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Recent Transactions")
        
        # Create transactions table
        html_table = """
        <table class="data-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Amount</th>
                    <th>Merchant</th>
                    <th>Risk</th>
                    <th>Status</th>
                    <th>Time</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for tx in sample_data['transactions']:
            status_class = f"status-{tx['Status'].lower().replace(' ', '-')}"
            html_table += f"""
            <tr>
                <td><strong>{tx['ID']}</strong></td>
                <td>{tx['Amount']}</td>
                <td>{tx['Merchant']}</td>
                <td>
                    <span class="{'risk-high' if tx['Risk'] == 'High' else 'risk-medium' if tx['Risk'] == 'Medium' else 'risk-low'}">
                        {tx['Risk']}
                    </span>
                </td>
                <td><span class="{status_class}">{tx['Status']}</span></td>
                <td>{tx['Time']}</td>
            </tr>
            """
        
        html_table += """
            </tbody>
        </table>
        """
        st.markdown(html_table, unsafe_allow_html=True)
        
        # Additional stats
        st.markdown("---")
        col_stat1, col_stat2 = st.columns(2)
        with col_stat1:
            st.metric("Avg Transaction", "$1,245", "+5.2%")
        with col_stat2:
            st.metric("Fraud Rate", "0.32%", "-0.08%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Fraud Patterns Detected")
        
        # Create patterns table
        html_patterns = """
        <table class="data-table">
            <thead>
                <tr>
                    <th>Pattern Type</th>
                    <th>Frequency</th>
                    <th>Risk Score</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for pattern in sample_data['patterns']:
            risk_color = "#ef4444" if float(pattern['Risk'].strip('%')) > 80 else "#f59e0b" if float(pattern['Risk'].strip('%')) > 60 else "#10b981"
            freq_color = "#ef4444" if pattern['Frequency'] == 'High' else "#f59e0b" if pattern['Frequency'] == 'Medium' else "#10b981"
            
            html_patterns += f"""
            <tr>
                <td><strong>{pattern['Pattern']}</strong></td>
                <td><span style="color: {freq_color}; font-weight: 600;">{pattern['Frequency']}</span></td>
                <td><span style="color: {risk_color}; font-weight: 700;">{pattern['Risk']}</span></td>
            </tr>
            """
        
        html_patterns += """
            </tbody>
        </table>
        """
        st.markdown(html_patterns, unsafe_allow_html=True)
        
        # Pattern statistics
        st.markdown("---")
        st.markdown("**Top Detected Patterns This Week:**")
        
        patterns_df = pd.DataFrame(sample_data['patterns'])
        for _, row in patterns_df.iterrows():
            risk_pct = float(row['Risk'].strip('%'))
            st.markdown(f"""
            <div style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-weight: 500;">{row['Pattern']}</span>
                    <span style="font-weight: 600;">{risk_pct}%</span>
                </div>
                <div style="width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px;">
                    <div style="width: {risk_pct}%; height: 100%; background: #667eea; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Merchant Analysis and System Status
    col_mid_left, col_mid_right = st.columns(2)
    
    with col_mid_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏪 Top Merchants Analysis")
        
        # Merchants table
        html_merchants = """
        <table class="data-table">
            <thead>
                <tr>
                    <th>Merchant</th>
                    <th>Fraud Attempts</th>
                    <th>Success Rate</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for merchant in sample_data['merchants']:
            attempts_color = "#ef4444" if merchant['Attempts'] > 35 else "#f59e0b" if merchant['Attempts'] > 25 else "#10b981"
            html_merchants += f"""
            <tr>
                <td><strong>{merchant['Name']}</strong></td>
                <td><span style="color: {attempts_color}; font-weight: 600;">{merchant['Attempts']}</span></td>
                <td><span style="color: #10b981; font-weight: 600;">{merchant['Success Rate']}</span></td>
            </tr>
            """
        
        html_merchants += """
            </tbody>
        </table>
        """
        st.markdown(html_merchants, unsafe_allow_html=True)
        
        # Chart-like visualization
        st.markdown("---")
        st.markdown("**Fraud Attempts Distribution:**")
        
        max_attempts = max(m['Attempts'] for m in sample_data['merchants'])
        for merchant in sample_data['merchants']:
            percentage = (merchant['Attempts'] / max_attempts) * 100
            color = "#ef4444" if merchant['Attempts'] > 35 else "#f59e0b" if merchant['Attempts'] > 25 else "#10b981"
            
            st.markdown(f"""
            <div style="margin: 8px 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 500;">{merchant['Name']}</span>
                    <span style="font-weight: 600; color: {color};">{merchant['Attempts']} attempts</span>
                </div>
                <div style="width: 100%; height: 6px; background: #e5e7eb; border-radius: 3px;">
                    <div style="width: {percentage}%; height: 100%; background: {color}; border-radius: 3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_mid_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ⚙️ System Status")
        
        # Performance metrics
        perf = sample_data['performance']
        
        st.markdown(f"""
        <div style="margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-weight: 500;">System Uptime</span>
                <span style="color: #10b981; font-weight: 700;">{perf['uptime']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-weight: 500;">Avg Response Time</span>
                <span style="color: #3b82f6; font-weight: 700;">{perf['response_time']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-weight: 500;">Detection Accuracy</span>
                <span style="color: #10b981; font-weight: 700;">{perf['accuracy']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-weight: 500;">Throughput (TPS)</span>
                <span style="color: #8b5cf6; font-weight: 700;">{perf['throughput']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                <span style="font-weight: 500;">False Positive Rate</span>
                <span style="color: #ef4444; font-weight: 700;">{perf['false_positives']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # System health indicators
        st.markdown("---")
        st.markdown("**System Health:**")
        
        indicators = [
            {"name": "API Service", "status": "🟢 Healthy", "color": "#10b981"},
            {"name": "Database", "status": "🟢 Healthy", "color": "#10b981"},
            {"name": "ML Model", "status": "🟡 Warning", "color": "#f59e0b"},
            {"name": "Logging", "status": "🟢 Healthy", "color": "#10b981"},
            {"name": "Backup", "status": "🔴 Critical", "color": "#ef4444"}
        ]
        
        for indicator in indicators:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">
                <span style="font-weight: 500;">{indicator['name']}</span>
                <span style="color: {indicator['color']}; font-weight: 600;">{indicator['status']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Last updated
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
            Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Transaction Analysis Form (Toggleable)
    if st.session_state.control_panel_visible:
        st.markdown("---")
        st.markdown("## 🔍 Transaction Analysis")
        
        with st.form("transaction_analysis"):
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                st.markdown("### 💳 Transaction Details")
                transaction_id = st.text_input("Transaction ID", value=f"TXN-{np.random.randint(100000, 999999)}")
                amount = st.number_input("Amount (USD)", min_value=0.0, max_value=100000.0, value=2475.50, step=100.0)
                currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "CAD", "AUD"], index=0)
                merchant = st.selectbox("Merchant", ["Amazon", "Apple", "Netflix", "Uber", "Airbnb", "Walmart"], index=0)
            
            with col_form2:
                st.markdown("### 📊 Risk Parameters")
                v14 = st.slider("V14 Structural Risk", 0.0, 1.0, 0.68, 0.01)
                v17 = st.slider("V17 Behavioral Risk", 0.0, 1.0, 0.42, 0.01)
                payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Digital Wallet", "Bank Transfer"], index=0)
                device_type = st.selectbox("Device Type", ["Mobile", "Desktop", "Tablet", "Unknown"], index=0)
            
            submitted = st.form_submit_button("🚀 Analyze Transaction", type="primary", use_container_width=True)
            
            if submitted:
                # Calculate risk score
                risk_score = min(0.05 + (v14 * 0.4) + (v17 * 0.35) + (amount / 10000), 0.95)
                
                st.session_state.transaction_data = {
                    'id': transaction_id,
                    'amount': amount,
                    'currency': currency,
                    'merchant': merchant,
                    'v14': v14,
                    'v17': v17,
                    'payment_method': payment_method,
                    'device_type': device_type,
                    'risk_score': risk_score,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Show analysis results
                st.markdown("### 📊 Analysis Results")
                
                risk_color = "#ef4444" if risk_score > 0.7 else "#f59e0b" if risk_score > 0.4 else "#10b981"
                risk_level = "HIGH" if risk_score > 0.7 else "MEDIUM" if risk_score > 0.4 else "LOW"
                
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 20px; border-radius: 15px; background: rgba(255, 255, 255, 0.9);">
                        <div style="font-size: 3rem; font-weight: 800; color: {risk_color};">
                            {(risk_score * 100):.1f}%
                        </div>
                        <div style="font-size: 1.2rem; color: #374151; margin-top: 10px;">
                            Fraud Probability
                        </div>
                        <div style="margin-top: 15px;">
                            <span class="{'risk-high' if risk_level == 'HIGH' else 'risk-medium' if risk_level == 'MEDIUM' else 'risk-low'}">
                                {risk_level} RISK
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_res2:
                    st.markdown("**Risk Factors:**")
                    factors = [
                        ("Amount", min(amount / 5000, 0.3)),
                        ("V14 Score", v14 * 0.4),
                        ("V17 Score", v17 * 0.35),
                        ("Payment Method", 0.15 if payment_method in ["Digital Wallet", "Bank Transfer"] else 0.05),
                        ("Device", 0.2 if device_type == "Unknown" else 0.05)
                    ]
                    
                    for factor, value in factors:
                        factor_pct = value * 100
                        color = "#ef4444" if factor_pct > 50 else "#f59e0b" if factor_pct > 30 else "#10b981"
                        st.markdown(f"""
                        <div style="margin: 10px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span>{factor}</span>
                                <span style="color: {color}; font-weight: 600;">{factor_pct:.1f}%</span>
                            </div>
                            <div style="width: 100%; height: 6px; background: #e5e7eb; border-radius: 3px;">
                                <div style="width: {factor_pct}%; height: 100%; background: {color}; border-radius: 3px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <div style="text-align: left;">
                <p style="margin: 0; font-weight: 700; color: #111827; font-size: 1.1rem;">
                    🛡️ FraudGuard™ Enterprise v4.0
                </p>
                <p style="margin: 5px 0 0 0; color: #374151; font-size: 0.9rem;">
                    Advanced AI-Powered Fraud Detection Platform
                </p>
            </div>
            
            <div style="text-align: center;">
                <div style="display: flex; gap: 30px;">
                    <div>
                        <p style="margin: 0; color: #374151; font-weight: 600;">📞 Support</p>
                        <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 0.9rem;">1-800-FRAUD-GUARD</p>
                    </div>
                    <div>
                        <p style="margin: 0; color: #374151; font-weight: 600;">📧 Email</p>
                        <p style="margin: 5px 0 0 0; color: #6b7280; font-size: 0.9rem;">security@fraudguard.com</p>
                    </div>
                </div>
            </div>
            
            <div style="text-align: right;">
                <div style="background: rgba(16, 185, 129, 0.1); padding: 8px 16px; border-radius: 50px;">
                    <p style="margin: 0; color: #10b981; font-weight: 600;">
                        🟢 System Operational
                    </p>
                </div>
            </div>
        </div>
        
        <div style="border-top: 1px solid rgba(229, 231, 235, 0.5); padding-top: 20px;">
            <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 15px;">
                <span style="color: #6b7280; font-size: 0.85rem;">✅ PCI-DSS Compliant</span>
                <span style="color: #6b7280; font-size: 0.85rem;">✅ ISO 27001 Certified</span>
                <span style="color: #6b7280; font-size: 0.85rem;">✅ GDPR Compliant</span>
                <span style="color: #6b7280; font-size: 0.85rem;">✅ SOC 2 Type II</span>
            </div>
            <p style="margin: 0; color: #9ca3af; font-size: 0.85rem; text-align: center;">
                © 2024 FraudGuard Global Security. All rights reserved. | Advanced Security Analytics Platform
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container

if __name__ == "__main__":
    main()

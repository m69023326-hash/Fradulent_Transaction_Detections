import streamlit as st
import plotly.graph_objects as go
from streamlit_gauge import gauge
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

# Custom CSS
def local_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css()

# Main app layout
def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">FraudGuard™ Enterprise</h1>
        <h2 class="sub-title">FraudGuard™ Financial Intelligence</h2>
        <h3 class="dashboard-title">Enterprise Fraud Monitoring Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Control Panel
        st.markdown("""
        <div class="control-panel">
            <h3 class="panel-title">Control Panel</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Transaction Value
        st.markdown("### Amount Transaction Value (USD)")
        transaction_value = st.slider(
            "Transaction Value (USD)",
            min_value=0,
            max_value=1000000,
            value=500000,
            step=1000,
            label_visibility="collapsed"
        )
        st.markdown(f"**${transaction_value:,.2f}**")
        
        # Risk Coefficients
        col1_1, col1_2 = st.columns(2)
        
        with col1_1:
            st.markdown("### V14 Coefficient")
            st.markdown("**Structural Risk**")
            v14_value = st.slider(
                "V14 Value",
                min_value=0.0,
                max_value=1.0,
                value=0.75,
                step=0.01,
                label_visibility="collapsed"
            )
            st.progress(v14_value)
            st.markdown(f"**{v14_value:.2f}**")
        
        with col1_2:
            st.markdown("### V17 Coefficient")
            st.markdown("**Behavioral 10.0**")
            v17_value = st.slider(
                "V17 Value",
                min_value=0.0,
                max_value=1.0,
                value=0.82,
                step=0.01,
                label_visibility="collapsed"
            )
            st.progress(v17_value)
            st.markdown(f"**{v17_value:.2f}**")
        
        # PCI-DSS Compliance
        st.markdown("---")
        st.markdown("""
        <div class="compliance-badge">
            <h4>✓ Standard: PCI-DSS Compliant</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Transaction Security Analysis
        st.markdown("---")
        st.markdown("""
        <div class="analysis-section">
            <h3>Transaction Security Analysis</h3>
            <div class="analysis-content">
                <h4>Understanding the FraudGuard™ AI</h4>
                <p>Our system leverages a Random Forest ensemble model trained on customer and financial data. 
                It uses integrated (O'Brien's) feature engineering for real-world performance evaluation in a timely manner.</p>
                
                <p>H1 tips Structural Risk at runtime, fluidized transactional analysis, and material security measures.</p>
                
                <ul>
                    <li>V14 (structural anomaly detection in structure/value): Traps negative outliers in transaction volume</li>
                    <li>High negative value detection ensures low false positive rate (99.90% accuracy)</li>
                </ul>
                
                <p>This architecture ensures high detection rates (99.90%), protecting both merchants and customers.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Network Stats
        st.markdown("""
        <div class="stats-panel">
            <h3 class="panel-title">Network Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # System Accuracy Gauge
        st.markdown("### System Accuracy")
        fig1 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=99.9,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Accuracy %"},
            delta={'reference': 96.6, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 90], 'color': "lightgray"},
                    {'range': [90, 96], 'color': "gray"},
                    {'range': [96, 100], 'color': "darkgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 99.9
                }
            }
        ))
        fig1.update_layout(height=250)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("*Random uniform -3.3%*")
        
        # Fraud Recall Gauge
        st.markdown("### Fraud Recall")
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=97.5,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Recall %"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 85], 'color': "lightgray"},
                    {'range': [85, 95], 'color': "lightgreen"},
                    {'range': [95, 100], 'color': "green"}
                ]
            }
        ))
        fig2.update_layout(height=200)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Processing Time Gauge
        st.markdown("### Processing Time")
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=48,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ms"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ]
            }
        ))
        fig3.update_layout(height=200)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("*Model Error: f randasilift 48ms*")
    
    # Security Scan Button and Report Card
    st.markdown("---")
    
    col_btn, col_report = st.columns([1, 3])
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🛡️ EXECUTE SECURITY SCAN", type="primary", use_container_width=True):
            st.session_state.scan_executed = True
        else:
            st.session_state.scan_executed = getattr(st.session_state, 'scan_executed', False)
        
        if st.session_state.scan_executed:
            st.error("Model Error: model.pkl not found.")
    
    with col_report:
        st.markdown("""
        <div class="report-card">
            <h3>Report Card</h3>
            <div class="high-risk">
                <h4>🚨 HIGH RISK IDENTIFIED</h4>
                <ul>
                    <li>Technician funds secured for review</li>
                    <li>Authorization from external vendors (K17) required</li>
                    <li>System Action: File not found. Escalating to L2 support</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>© 2026 FraudGuard Global Security | Secure Data Processing Unit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Try to import plotly with fallback
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not installed. Install with: pip install plotly")

# Page configuration
st.set_page_config(
    page_title="FraudGuard™ Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
def local_css():
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback CSS if file not found
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .header-container {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .main-title {
            color: white !important;
            font-size: 2.5rem !important;
        }
        
        .sub-title {
            color: #dbeafe !important;
            font-size: 1.8rem !important;
        }
        
        .control-panel, .stats-panel, .report-card {
            background: rgba(30, 41, 59, 0.8);
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #334155;
            margin: 1rem 0;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            border: none;
            padding: 0.8rem 2rem;
            font-size: 1.2rem;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

local_css()

# Helper function for gauges (fallback if plotly not available)
def create_gauge(value, title, color):
    if PLOTLY_AVAILABLE:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': color}}
        ))
        fig.update_layout(height=200)
        return fig
    else:
        # Fallback: show metric cards instead
        st.metric(label=title, value=f"{value}%")

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
                label_visibility="collapsed",
                key="v14"
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
                label_visibility="collapsed",
                key="v17"
            )
            st.progress(v17_value)
            st.markdown(f"**{v17_value:.2f}**")
        
        # PCI-DSS Compliance
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(90deg, #065f46 0%, #10b981 100%); 
                    padding: 0.8rem; border-radius: 8px; text-align: center;">
            <h4 style="color: white !important; margin: 0 !important;">✓ Standard: PCI-DSS Compliant</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Transaction Security Analysis
        st.markdown("---")
        with st.container():
            st.markdown("### Transaction Security Analysis")
            st.markdown("**Understanding the FraudGuard™ AI**")
            st.markdown("""
            Our system leverages a Random Forest ensemble model trained on customer and financial data. 
            It uses integrated (O'Brien's) feature engineering for real-world performance evaluation in a timely manner.
            
            H1 tips Structural Risk at runtime, fluidized transactional analysis, and material security measures.
            
            - **V14 (structural anomaly detection in structure/value):** Traps negative outliers in transaction volume
            - **High negative value detection ensures low false positive rate (99.90% accuracy)**
            
            This architecture ensures high detection rates (99.90%), protecting both merchants and customers.
            """)
    
    with col2:
        # Network Stats
        st.markdown("""
        <div class="stats-panel">
            <h3 class="panel-title">Network Stats</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # System Accuracy
        st.markdown("### System Accuracy")
        if PLOTLY_AVAILABLE:
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
                    ]
                }
            ))
            fig1.update_layout(height=250)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.markdown("### 99.9%")
            st.progress(0.999)
        st.markdown("*Random uniform -3.3%*")
        
        # Fraud Recall
        st.markdown("### Fraud Recall")
        if PLOTLY_AVAILABLE:
            fig2 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=97.5,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Recall %"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkgreen"}}
            ))
            fig2.update_layout(height=200)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.markdown("### 97.5%")
            st.progress(0.975)
        
        # Processing Time
        st.markdown("### Processing Time")
        if PLOTLY_AVAILABLE:
            fig3 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=48,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "ms"},
                gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "darkblue"}}
            ))
            fig3.update_layout(height=200)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.markdown("### 48ms")
            st.progress(0.48)
        st.markdown("*Model Error: f randasilift 48ms*")
    
    # Security Scan Button and Report Card
    st.markdown("---")
    
    col_btn, col_report = st.columns([1, 3])
    
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🛡️ EXECUTE SECURITY SCAN", type="primary", use_container_width=True):
            st.session_state.scan_executed = True
            st.error("Model Error: model.pkl not found.")
        else:
            st.session_state.scan_executed = getattr(st.session_state, 'scan_executed', False)
    
    with col_report:
        st.markdown("""
        <div class="report-card" style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); 
                    padding: 1.5rem; border-radius: 10px; border: 2px solid #dc2626;">
            <h3 style="color: white !important;">Report Card</h3>
            <div style="background: rgba(127, 29, 29, 0.8); padding: 1rem; border-radius: 8px;">
                <h4 style="color: #fecaca !important;">🚨 HIGH RISK IDENTIFIED</h4>
                <ul style="color: #fecaca;">
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
    <div style="text-align: center; padding: 1rem; color: #94a3b8; border-top: 1px solid #334155;">
        <p>© 2026 FraudGuard Global Security | Secure Data Processing Unit</p>
    </div>
    """, unsafe_allow_html=True)

    # Installation instructions if plotly not available
    if not PLOTLY_AVAILABLE:
        st.warning("""
        **Note:** For full features (interactive gauges), install plotly:
        ```bash
        pip install plotly
        ```
        Then restart the app.
        """)

if __name__ == "__main__":
    main()

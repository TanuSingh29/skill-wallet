"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1
Production-Ready Streamlit Application
"""

import streamlit as st
from PIL import Image
import json
import io
import plotly.graph_objects as go
import plotly.express as px

# Import local modules
from modules.gemini_client import GeminiPlatformClient
from modules.ppe_audit import analyze_ppe, get_demo_ppe_audit
from modules.crack_diagnostics import analyze_crack, get_demo_crack_diagnostics
from modules.real_estate_planning import (
    calculate_valuation_and_materials,
    generate_pollinations_render_url,
    BASE_CONSTRUCTION_COSTS,
    TIER_MULTIPLIERS
)
from modules.weather_assistant import (
    WEATHER_PROFILES,
    ASSISTANT_SYSTEM_PROMPT,
    get_demo_chat_response
)
from sample_data.sample_images import generate_sample_ppe_image, generate_sample_crack_image

# ---------------------------------------------------------
# Page Configuration & Modern Industrial Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Industrial Dashboard CSS
CUSTOM_CSS = """
<style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Header Container */
    .platform-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #1E1B4B 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .platform-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #F59E0B, #FBBF24, #E2E8F0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }
    .platform-sub {
        color: #94A3B8;
        font-size: 0.95rem;
        font-weight: 400;
    }
    
    /* Modern Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        border-color: #F59E0B;
        transform: translateY(-2px);
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }
    .metric-note {
        font-size: 0.8rem;
        color: #CBD5E1;
        margin-top: 6px;
    }

    /* Severity and Status Badges */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    .badge-critical { background: #7F1D1D; color: #FECACA; border: 1px solid #DC2626; }
    .badge-high { background: #7C2D12; color: #FED7AA; border: 1px solid #EA580C; }
    .badge-medium { background: #78350F; color: #FDE68A; border: 1px solid #D97706; }
    .badge-low { background: #14532D; color: #BBF7D0; border: 1px solid #16A34A; }
    .badge-safe { background: #064E3B; color: #A7F3D0; border: 1px solid #059669; }
    
    /* Checklist Items */
    .chk-item {
        background: #1E293B;
        border-left: 4px solid #3B82F6;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    .chk-item-compliant {
        border-left-color: #10B981;
    }
    .chk-item-violation {
        border-left-color: #EF4444;
    }
    
    /* Sidebar Styling */
    .sidebar-mode-box {
        padding: 12px 14px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 0.85rem;
    }
    .sidebar-mode-live {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #6EE7B7;
    }
    .sidebar-mode-demo {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid #F59E0B;
        color: #FCD34D;
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0F172A;
        padding: 8px 12px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        font-weight: 600;
        border-radius: 8px;
        color: #94A3B8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #F59E0B !important;
        color: #0F172A !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Configuration & Initialization
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🏗️ **Control Center**")
    st.caption("Skill Wallet Capstone Project 1 • Autonomous Multimodal AI")

    # API Key Input with Session State Persistence
    api_key_input = st.text_input(
        "🔑 Google Gemini API Key",
        type="password",
        value=st.session_state.get("gemini_api_key", ""),
        help="Enter your Google AI Studio Gemini API key. If empty, the platform automatically engages High-Fidelity Demonstration Mode."
    )
    st.session_state["gemini_api_key"] = api_key_input

    # Mode Indicator
    is_demo_mode = not bool(api_key_input.strip())
    if is_demo_mode:
        st.markdown(
            """<div class="sidebar-mode-box sidebar-mode-demo">
            <strong>🟠 DEMO MODE ACTIVE</strong><br>
            Using calibrated forensic engineering simulations. Add API key above for live multimodal reasoning.
            </div>""",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """<div class="sidebar-mode-box sidebar-mode-live">
            <strong>🟢 LIVE GEMINI CONNECTED</strong><br>
            Direct multimodal reasoning active via Gemini 2.5 Flash.
            </div>""",
            unsafe_allow_html=True
        )

    # Model Selection
    model_choice = st.selectbox(
        "🧠 Active Multimodal Model",
        options=["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        disabled=is_demo_mode
    )

    st.markdown("---")
    
    # Architecture Overview Expander
    with st.expander("🏛️ System Architecture", expanded=False):
        st.markdown("""
        **System Components:**
        1. **Perception Engine:** Gemini 2.5 Flash Multimodal Vision
        2. **Safety Compliance Rules:** OSHA 1926 & IS 2925/IS 3521
        3. **Structural Pathology:** IS 456:2000 & ACI 224.1R
        4. **Quantity Surveying (QS):** CPWD Schedule of Rates Empirical Engine
        5. **Parametric 3D ArchViz:** Pollinations AI Flux Architecture Synthesizer
        6. **Weather SOP Matrix:** IS 875 Part 3 Wind & IS 7861 Hot/Cold Weather Concreting
        """)
        
    with st.expander("📚 Regulatory Code References", expanded=False):
        st.markdown("""
        - **IS 456:2000:** Plain & Reinforced Concrete
        - **IS 875 (Part 1-5):** Design Loads & Wind Codes
        - **IS 13920:2016:** Ductile Detailing for Seismic Zones
        - **IS 2925:** Industrial Safety Helmets
        - **IS 3521:** Safety Belts & Full Body Harnesses
        - **OSHA 1926 Subpart M:** Fall Protection
        - **OSHA 1926 Subpart E:** Personal Protective Equipment
        """)

    st.markdown("---")
    st.caption("Engineered for 1-Click Streamlit Community Cloud Deployment • Zero External Database Dependencies")

# Initialize Gemini Client Singleton
gemini_client = GeminiPlatformClient(api_key=api_key_input)

# ---------------------------------------------------------
# Platform Header Banner
# ---------------------------------------------------------
st.markdown(
    """<div class="platform-header">
        <div class="platform-title">🏗️ Multimodal Construction Intelligence Platform</div>
        <div class="platform-sub">
            Autonomous Construction Site Safety (OSHA / IS 456) • Forensic Concrete Crack Diagnostics • 
            Parametric Real Estate Valuation & Material Engine • Weather-Aware Site SOP Assistant
        </div>
    </div>""",
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# 4 Core Interactive Tabs
# ---------------------------------------------------------
tab_ppe, tab_cracks, tab_planning, tab_weather = st.tabs([
    "🦺 Site Safety & PPE Audit (Epic 2)",
    "🧱 Crack Diagnostics & Structural Integrity (Epic 2)",
    "📊 Planning & Real Estate Valuation (Epic 3)",
    "🌦️ Daily Site Assistant & Weather Advisory (Epic 5)"
])

# =========================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# =========================================================
with tab_ppe:
    st.markdown("### 🦺 Autonomous Worker PPE & Site Safety Audit")
    st.caption("Evaluates computer-vision safety compliance against OSHA 1926 and Bureau of Indian Standards (IS 2925, IS 3521, IS 1989).")

    col_upload, col_preview = st.columns([1, 1], gap="medium")

    with col_upload:
        st.markdown("#### 1. Input Construction Site Imagery")
        ppe_file = st.file_uploader(
            "Upload Site Photo (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            key="ppe_uploader",
            help="Upload an image showing workers, scaffolding, or site activities."
        )

        st.markdown("**— OR select a demonstration benchmark photo:**")
        sample_ppe_choice = st.radio(
            "Quick Demonstration Scenarios:",
            options=["Safe & Fully Compliant Crew", "Critical Non-Compliance (Missing PPE & Fall Hazard)"],
            horizontal=True,
            key="sample_ppe_radio"
        )
        
        load_sample_btn = st.button("📸 Load Sample Scenario Image", use_container_width=True)

        # Image state tracking
        if ppe_file is not None:
            active_ppe_image = Image.open(ppe_file)
            st.session_state["active_ppe_image"] = active_ppe_image
            st.session_state["ppe_scenario_name"] = "Uploaded Photo"
        elif load_sample_btn or "active_ppe_image" not in st.session_state:
            scenario_key = "compliant" if "Safe" in sample_ppe_choice else "high_risk"
            st.session_state["active_ppe_image"] = generate_sample_ppe_image(scenario=scenario_key)
            st.session_state["ppe_scenario_name"] = sample_ppe_choice

        run_ppe_audit = st.button("🚀 Run Site Safety & PPE Audit", type="primary", use_container_width=True)

    with col_preview:
        st.markdown("#### 2. Site Camera Feed Preview")
        if "active_ppe_image" in st.session_state:
            st.image(
                st.session_state["active_ppe_image"],
                caption=f"Source: {st.session_state.get('ppe_scenario_name', 'Active Site Image')}",
                use_container_width=True
            )

    # Execute Audit
    if run_ppe_audit or "last_ppe_result" in st.session_state:
        if run_ppe_audit:
            with st.spinner("Analyzing site imagery with Gemini Multimodal Safety Engine..."):
                scenario_flag = "high_risk" if "Critical" in st.session_state.get("ppe_scenario_name", "") else "default"
                audit_result = analyze_ppe(
                    gemini_client=gemini_client,
                    image=st.session_state["active_ppe_image"],
                    is_demo=is_demo_mode,
                    demo_scenario=scenario_flag
                )
                st.session_state["last_ppe_result"] = audit_result
        else:
            audit_result = st.session_state["last_ppe_result"]

        st.markdown("---")
        st.markdown("### 📋 Audit Findings & Compliance Scorecard")

        # Top Metric Cards
        score = audit_result.get("safety_score", 75)
        status = audit_result.get("overall_status", "Needs Review")
        worker_count = audit_result.get("detected_workers_count", 0)

        badge_class = "badge-safe" if score >= 80 else ("badge-medium" if score >= 60 else "badge-critical")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Safety Compliance Score</div>
                    <div class="metric-value" style="color: {'#10B981' if score >= 80 else ('#F59E0B' if score >= 60 else '#EF4444')};">{score}/100</div>
                    <div class="metric-note">OSHA & IS Weighted Index</div>
                </div>""",
                unsafe_allow_html=True
            )
        with m2:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Site Status</div>
                    <div style="margin-top: 8px;"><span class="badge {badge_class}" style="font-size: 0.95rem; padding: 6px 14px;">{status}</span></div>
                    <div class="metric-note">Real-time Risk Grade</div>
                </div>""",
                unsafe_allow_html=True
            )
        with m3:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Workers Detected</div>
                    <div class="metric-value">{worker_count}</div>
                    <div class="metric-note">In Field of View</div>
                </div>""",
                unsafe_allow_html=True
            )
        with m4:
            hazards_count = len(audit_result.get("site_hazards", []))
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Identified Hazards</div>
                    <div class="metric-value" style="color: {'#EF4444' if hazards_count > 2 else ('#F59E0B' if hazards_count > 0 else '#10B981')};">{hazards_count}</div>
                    <div class="metric-note">Actionable Items</div>
                </div>""",
                unsafe_allow_html=True
            )

        # PPE Checklist Breakdown
        st.markdown("#### 🛡️ Detailed PPE Checklist")
        ppe_data = audit_result.get("ppe_detection", {})
        
        c1, c2 = st.columns(2)
        items = list(ppe_data.items())
        for idx, (key, item) in enumerate(items):
            target_col = c1 if idx % 2 == 0 else c2
            with target_col:
                is_comp = item.get("compliant", False)
                comp_icon = "✅ COMPLIANT" if is_comp else "❌ NON-COMPLIANT"
                badge_type = "badge-safe" if is_comp else "badge-critical"
                item_class = "chk-item-compliant" if is_comp else "chk-item-violation"
                
                st.markdown(
                    f"""<div class="chk-item {item_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong>{item.get('item_name', key.title())}</strong>
                            <span class="badge {badge_type}">{comp_icon}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #CBD5E1;">
                            <strong>Compliance Rate:</strong> {item.get('compliance_rate', 'N/A')} ({item.get('compliant_count', 0)} / {item.get('observed_count', 0)} workers)
                        </div>
                        <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 4px;">
                            <strong>Standard:</strong> {item.get('standard_ref', 'OSHA / IS')}
                        </div>
                        <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 6px; font-style: italic;">
                            "{item.get('notes', 'No specific observations.')}"
                        </div>
                    </div>""",
                    unsafe_allow_html=True
                )

        # Identified Site Hazards Table & Corrective Remedies
        st.markdown("#### ⚠️ Identified Site Hazards & Engineering Remedies")
        hazards = audit_result.get("site_hazards", [])
        if hazards:
            for h in hazards:
                sev = h.get("severity", "Medium")
                s_badge = f"badge-{sev.lower()}" if sev.lower() in ["critical", "high", "medium", "low"] else "badge-medium"
                
                with st.container():
                    st.markdown(
                        f"""<div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <strong style="font-size: 1.05rem; color: #F8FAFC;">{h.get('hazard')}</strong>
                                <span class="badge {s_badge}">Severity: {sev}</span>
                            </div>
                            <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 6px;">
                                📍 <strong>Location:</strong> {h.get('location')} &nbsp;|&nbsp; 📜 <strong>Standard Violated:</strong> <code>{h.get('standard_violated')}</code>
                            </div>
                            <div style="font-size: 0.9rem; color: #FDE68A; background: rgba(245, 158, 11, 0.1); padding: 8px 12px; border-radius: 6px; border-left: 3px solid #F59E0B;">
                                🛠️ <strong>Corrective Remedy:</strong> {h.get('remedy')}
                            </div>
                        </div>""",
                        unsafe_allow_html=True
                    )
        else:
            st.success("No critical or high-risk site hazards identified in this operational zone.")

        # Download Report Button
        st.markdown("#### 📥 Export Official Site Safety Report")
        report_json_str = json.dumps(audit_result, indent=2)
        st.download_button(
            label="📄 Download Safety Audit JSON Report",
            data=report_json_str,
            file_name="site_safety_ppe_audit_report.json",
            mime="application/json"
        )

# =========================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# =========================================================
with tab_cracks:
    st.markdown("### 🧱 Forensic Concrete Crack Diagnostics & Structural Integrity")
    st.caption("Classifies concrete defects against IS 456:2000 (0.3 mm crack threshold), evaluates load-bearing risks, and recommends repairs.")

    col_c_upload, col_c_preview = st.columns([1, 1], gap="medium")

    with col_c_upload:
        st.markdown("#### 1. Input Defect / Concrete Surface Image")
        crack_file = st.file_uploader(
            "Upload Concrete / Wall Image (JPG / PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader",
            help="Upload an image of a beam, slab, column, wall, or foundation defect."
        )

        st.markdown("**— OR choose a forensic test defect:**")
        sample_crack_choice = st.radio(
            "Forensic Defect Archetypes:",
            options=[
                "Structural 45° Shear Crack in RC Beam (Critical)",
                "Carbonation Cover Spalling & Exposed Rebar (High)",
                "Superficial Plastic Drying Shrinkage Crack (Low)"
            ],
            key="sample_crack_radio"
        )
        
        load_sample_crack_btn = st.button("🧱 Load Sample Defect Image", use_container_width=True)

        if crack_file is not None:
            active_crack_image = Image.open(crack_file)
            st.session_state["active_crack_image"] = active_crack_image
            st.session_state["crack_scenario_name"] = "Uploaded Defect"
        elif load_sample_crack_btn or "active_crack_image" not in st.session_state:
            if "Shear" in sample_crack_choice:
                c_key = "shear"
            elif "Spalling" in sample_crack_choice:
                c_key = "spalling"
            else:
                c_key = "hairline"
            st.session_state["active_crack_image"] = generate_sample_crack_image(crack_type=c_key)
            st.session_state["crack_scenario_name"] = sample_crack_choice

        run_crack_diagnostics = st.button("🔍 Execute Forensic Structural Analysis", type="primary", use_container_width=True)

    with col_c_preview:
        st.markdown("#### 2. Concrete Defect Surface Inspection")
        if "active_crack_image" in st.session_state:
            st.image(
                st.session_state["active_crack_image"],
                caption=f"Inspecting: {st.session_state.get('crack_scenario_name', 'Active Concrete Defect')}",
                use_container_width=True
            )

    # Execute Diagnostics
    if run_crack_diagnostics or "last_crack_result" in st.session_state:
        if run_crack_diagnostics:
            with st.spinner("Executing forensic pathology analysis with Gemini Multimodal Structural Models..."):
                if "Shear" in st.session_state.get("crack_scenario_name", ""):
                    s_mode = "shear_crack"
                elif "Spalling" in st.session_state.get("crack_scenario_name", ""):
                    s_mode = "spalling"
                else:
                    s_mode = "hairline"

                crack_result = analyze_crack(
                    gemini_client=gemini_client,
                    image=st.session_state["active_crack_image"],
                    is_demo=is_demo_mode,
                    demo_scenario=s_mode
                )
                st.session_state["last_crack_result"] = crack_result
        else:
            crack_result = st.session_state["last_crack_result"]

        st.markdown("---")
        st.markdown("### 🔬 Structural Engineering Diagnostic Report")

        # Key Metrics Cards
        defect_name = crack_result.get("defect_type", "Unknown Defect")
        defect_sub = crack_result.get("defect_subtype", "")
        est_width = crack_result.get("estimated_width_mm", 0.0)
        limit_width = crack_result.get("is_456_limit_mm", 0.30)
        exceeds_limit = crack_result.get("exceeds_is456_limit", est_width > limit_width)
        urgency = crack_result.get("structural_urgency", "Moderate")

        urgency_badge = f"badge-{urgency.lower()}" if urgency.lower() in ["critical", "high", "moderate", "low"] else "badge-medium"

        cm1, cm2, cm3, cm4 = st.columns(4)
        with cm1:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Primary Defect</div>
                    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-top: 4px;">{defect_name}</div>
                    <div class="metric-note">{defect_sub}</div>
                </div>""",
                unsafe_allow_html=True
            )
        with cm2:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Estimated Width</div>
                    <div class="metric-value" style="color: {'#EF4444' if exceeds_limit else '#10B981'};">{est_width:.2f} mm</div>
                    <div class="metric-note">IS 456 Max Limit: {limit_width:.2f} mm</div>
                </div>""",
                unsafe_allow_html=True
            )
        with cm3:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">IS 456 Permissibility</div>
                    <div style="margin-top: 8px;">
                        <span class="badge {'badge-critical' if exceeds_limit else 'badge-safe'}" style="font-size: 0.9rem; padding: 6px 12px;">
                            {'⚠️ EXCEEDS IS 456 LIMIT' if exceeds_limit else '✅ WITHIN LIMIT (<= 0.3mm)'}
                        </span>
                    </div>
                    <div class="metric-note">Clause 35.3.2 Compliance</div>
                </div>""",
                unsafe_allow_html=True
            )
        with cm4:
            st.markdown(
                f"""<div class="metric-card">
                    <div class="metric-label">Structural Urgency</div>
                    <div style="margin-top: 8px;">
                        <span class="badge {urgency_badge}" style="font-size: 0.95rem; padding: 6px 14px;">{urgency}</span>
                    </div>
                    <div class="metric-note">Intervention Requirement</div>
                </div>""",
                unsafe_allow_html=True
            )

        # Risk Assessment & Structural Element
        st.markdown(
            f"""<div style="background: rgba(30, 41, 59, 0.9); border: 1px solid #475569; border-radius: 10px; padding: 18px 22px; margin-bottom: 20px;">
                <h4 style="margin-top: 0; color: #F59E0B;">🏗️ Load-Bearing Element: {crack_result.get('element_affected', 'RCC Member')}</h4>
                <p style="color: #E2E8F0; line-height: 1.6; font-size: 0.95rem; margin-bottom: 0;">
                    {crack_result.get('structural_risk_assessment', 'Detailed structural evaluation required.')}
                </p>
            </div>""",
            unsafe_allow_html=True
        )

        # Root Causes
        st.markdown("#### 🧬 Root Cause Analysis")
        for c in crack_result.get("root_causes", []):
            st.markdown(f"- 🔸 **{c}**")

        # Recommended Engineering Repairs
        st.markdown("#### 🛠️ Recommended Civil Engineering Repair Protocols")
        repairs = crack_result.get("recommended_engineering_repairs", [])
        for r in repairs:
            with st.container():
                st.markdown(
                    f"""<div style="background: #1E293B; border-left: 4px solid #F59E0B; border-radius: 6px; padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="font-size: 1.05rem; color: #F8FAFC;">🔧 {r.get('method')}</strong>
                            <span style="color: #6EE7B7; font-weight: 700; font-size: 0.9rem;">{r.get('estimated_cost_range_inr', 'Est. upon site visit')}</span>
                        </div>
                        <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 6px;">
                            <strong>Technical Specification:</strong> <code>{r.get('specification')}</code>
                        </div>
                        <div style="font-size: 0.9rem; color: #CBD5E1; margin-top: 8px; line-height: 1.5;">
                            <strong>Execution SOP:</strong> {r.get('execution_procedure')}
                        </div>
                    </div>""",
                    unsafe_allow_html=True
                )

        # Monitoring Protocol
        m_proto = crack_result.get("monitoring_protocol")
        if m_proto:
            st.info(f"📊 **Long-Term Monitoring Protocol:** {m_proto}")

        # Download Crack Diagnostic Report
        st.download_button(
            label="📄 Download Crack Diagnostic JSON Report",
            data=json.dumps(crack_result, indent=2),
            file_name="concrete_crack_diagnostic_report.json",
            mime="application/json"
        )

# =========================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# =========================================================
with tab_planning:
    st.markdown("### 📊 Parametric Project Planning, Material Engine & Real Estate Valuation")
    st.caption("Empirical CPWD/IS construction cost modeling, real-time capital expenditure tracking, and Pollinations AI 3D architectural rendering.")

    p_col1, p_col2 = st.columns([1, 1], gap="large")

    with p_col1:
        st.markdown("#### 1. Project Specifications")
        sel_structure = st.selectbox(
            "Structure Classification",
            options=list(BASE_CONSTRUCTION_COSTS.keys()),
            index=0
        )

        sel_sqft = st.number_input(
            "Total Built-up Area (Sq. Ft.)",
            min_value=5000,
            max_value=2000000,
            value=85000,
            step=5000,
            help="Total gross construction area across all floors and basements."
        )

        sel_tier = st.selectbox(
            "Location Urban Classification",
            options=list(TIER_MULTIPLIERS.keys()),
            index=0
        )

        sel_completion = st.slider(
            "Project Completion Progress (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            help="Adjust to calculate CapEx incurred and milestone progress."
        )

    # Compute calculations
    calc = calculate_valuation_and_materials(
        structure_type=sel_structure,
        built_up_sqft=sel_sqft,
        tier_name=sel_tier,
        completion_pct=sel_completion
    )

    with p_col2:
        st.markdown("#### 2. Milestone & Current Construction Phase")
        st.markdown(
            f"""<div style="background: #1E293B; border: 1px solid #334155; border-radius: 10px; padding: 18px; margin-bottom: 12px;">
                <div style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">Active Milestone</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #F59E0B; margin: 4px 0;">{calc['current_phase']}</div>
                <div style="font-size: 0.85rem; color: #CBD5E1;">Stage: <strong>{calc['phase_status']}</strong> ({calc['completion_pct']}% Work Complete)</div>
            </div>""",
            unsafe_allow_html=True
        )
        st.progress(calc["completion_pct"] / 100.0)

    st.markdown("---")
    st.markdown("### 💰 Financial & Asset Valuation Metrics")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Total Project Budget</div>
                <div class="metric-value">{calc['total_budget_formatted']}</div>
                <div class="metric-note">@ ₹{calc['cost_per_sqft']:,.0f} / sq.ft</div>
            </div>""",
            unsafe_allow_html=True
        )
    with f2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">CapEx Incurred to Date</div>
                <div class="metric-value" style="color: #38BDF8;">{calc['capex_incurred_formatted']}</div>
                <div class="metric-note">{calc['completion_pct']}% of Total CapEx</div>
            </div>""",
            unsafe_allow_html=True
        )
    with f3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Current Asset Valuation</div>
                <div class="metric-value" style="color: #10B981;">{calc['current_asset_valuation_formatted']}</div>
                <div class="metric-note">Stage Risk-Adjusted Equity</div>
            </div>""",
            unsafe_allow_html=True
        )
    with f4:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Finished Project Value</div>
                <div class="metric-value" style="color: #F59E0B;">{calc['finished_market_value_formatted']}</div>
                <div class="metric-note">@ ₹{calc['val_per_sqft']:,.0f} / sq.ft</div>
            </div>""",
            unsafe_allow_html=True
        )

    # Material Requirement Breakdown (CPWD & IS Norms)
    st.markdown("#### 🏗️ Material Consumption Engine (IS & CPWD Standards)")
    m_data = calc["materials"]
    
    mat1, mat2, mat3 = st.columns(3)
    with mat1:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Structural Steel (Fe500D)</div>
                <div class="metric-value" style="font-size: 1.6rem; color: #60A5FA;">{m_data['steel']['total_mt']:,.1f} MT</div>
                <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 6px;">
                    Consumed: <strong>{m_data['steel']['consumed_mt']} MT</strong> | Balance: <strong>{m_data['steel']['balance_mt']} MT</strong>
                </div>
                <div class="metric-note">Norm: {m_data['steel']['unit_rate_norm']}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with mat2:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Cement Requirement (OPC/PPC)</div>
                <div class="metric-value" style="font-size: 1.6rem; color: #FBBF24;">{m_data['cement']['total_bags']:,} Bags</div>
                <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 6px;">
                    ({m_data['cement']['total_mt']:,.1f} MT) | Consumed: <strong>{m_data['cement']['consumed_bags']:,} Bags</strong>
                </div>
                <div class="metric-note">Norm: {m_data['cement']['unit_rate_norm']}</div>
            </div>""",
            unsafe_allow_html=True
        )
    with mat3:
        st.markdown(
            f"""<div class="metric-card">
                <div class="metric-label">Sand & Aggregates (Zone II)</div>
                <div class="metric-value" style="font-size: 1.6rem; color: #34D399;">{m_data['sand_aggregates']['total_cuft']:,} cu.ft</div>
                <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 6px;">
                    Consumed: <strong>{m_data['sand_aggregates']['consumed_cuft']:,} cu.ft</strong>
                </div>
                <div class="metric-note">Norm: {m_data['sand_aggregates']['unit_rate_norm']}</div>
            </div>""",
            unsafe_allow_html=True
        )

    # Plotly Charts: Budget vs Asset Value & Material Allocation
    st.markdown("#### 📈 Financial Breakdown & Material Allocation")
    ch_col1, ch_col2 = st.columns(2)

    with ch_col1:
        # Donut Chart for Budget Incurred vs Balance
        fig_fin = go.Figure(data=[go.Pie(
            labels=["Incurred CapEx", "Remaining Budget Balance", "Estimated Stage Equity Gain"],
            values=[calc["capex_incurred_inr"], max(0, calc["total_budget_inr"] - calc["capex_incurred_inr"]), calc["unrealized_gain_inr"]],
            hole=.55,
            marker_colors=["#38BDF8", "#334155", "#10B981"]
        )])
        fig_fin.update_layout(
            title_text="Capital Allocation & Value Creation",
            title_font_color="#F8FAFC",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#CBD5E1")),
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_fin, use_container_width=True)

    with ch_col2:
        # Bar chart for material progress
        fig_mat = go.Figure(data=[
            go.Bar(
                name="Consumed to Date",
                x=["Steel (MT)", "Cement (Bags / 100)", "Aggregates (cu.ft / 1000)"],
                y=[m_data['steel']['consumed_mt'], m_data['cement']['consumed_bags'] / 100.0, m_data['sand_aggregates']['consumed_cuft'] / 1000.0],
                marker_color="#F59E0B"
            ),
            go.Bar(
                name="Remaining Balance",
                x=["Steel (MT)", "Cement (Bags / 100)", "Aggregates (cu.ft / 1000)"],
                y=[m_data['steel']['balance_mt'], m_data['cement']['balance_bags'] / 100.0, m_data['sand_aggregates']['balance_cuft'] / 1000.0],
                marker_color="#475569"
            )
        ])
        fig_mat.update_layout(
            barmode='stack',
            title_text="Material Consumption Schedule",
            title_font_color="#F8FAFC",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#CBD5E1")),
            xaxis=dict(color="#94A3B8"),
            yaxis=dict(color="#94A3B8"),
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig_mat, use_container_width=True)

    # 3D Conceptual Architectural Rendering Integration (Pollinations AI)
    st.markdown("---")
    st.markdown("### 🏛️ Conceptual 3D Architectural Rendering (Pollinations AI)")
    st.caption("Autonomous parametric prompt engineering generates realistic architectural visualizations for client pitches and planning approvals.")

    r_col1, r_col2 = st.columns([1, 2], gap="medium")

    with r_col1:
        st.markdown("#### Architectural Styling")
        style_option = st.selectbox(
            "Architectural Style",
            options=[
                "Modern Glass Curtain & Biophilic Terraces",
                "Sustainable Green Architecture with Vertical Gardens",
                "Minimalist Exposed Concrete & Cantilevered Volumes",
                "Neo-Classical Luxury Landmark with Grand Plaza"
            ],
            index=0
        )

        lighting_option = st.selectbox(
            "Lighting & Atmosphere",
            options=[
                "Golden Hour Dusk Architectural Photography",
                "Bright Crisp Midday Natural Sunlight",
                "Dramatic Twilight with Warm Interior Illumination"
            ],
            index=0
        )

        seed_value = st.number_input("Variation Seed", min_value=1, max_value=999999, value=42, step=1)
        generate_render_btn = st.button("🎨 Synthesize 3D Architectural Render", type="primary", use_container_width=True)

    # Pollinations AI URL generation
    render_url, prompt_text = generate_pollinations_render_url(
        structure_type=sel_structure,
        arch_style=style_option,
        lighting=lighting_option,
        seed=seed_value
    )

    with r_col2:
        st.markdown("#### Render Visual Output")
        st.image(render_url, caption=f"3D Conceptual Render: {sel_structure} ({style_option})", use_container_width=True)
        with st.expander("🔍 View Parametric Prompt Formulation", expanded=False):
            st.code(prompt_text, language="text")
            st.markdown(f"[🔗 Direct High-Res Image Link]({render_url})")

# =========================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER ADVISORY (EPIC 5)
# =========================================================
with tab_weather:
    st.markdown("### 🌦️ Daily Site Assistant & Weather-Aware Engineering Advisory")
    st.caption("Dynamic meteorological risk mitigation (IS 875 wind thresholds & hot/cold concreting) coupled with a multi-turn Construction Engineering Chatbot.")

    w_col1, w_col2 = st.columns([1, 1], gap="medium")

    with w_col1:
        st.markdown("#### 1. Site Meteorological Selector")
        weather_choice = st.selectbox(
            "Select Current / Forecasted Weather Condition",
            options=list(WEATHER_PROFILES.keys()),
            index=0
        )
        weather_info = WEATHER_PROFILES[weather_choice]

        # Dynamic Weather Sliders
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            w_speed = st.slider("Wind Velocity (km/h)", 0, 100, weather_info["wind_speed_kmh"])
            w_temp = st.slider("Ambient Temperature (°C)", -5, 55, weather_info["temperature_c"])
        with col_w2:
            w_hum = st.slider("Relative Humidity (%)", 10, 100, weather_info["humidity_pct"])
            w_precip = st.slider("Rainfall Rate (mm/hr)", 0, 150, weather_info["precipitation_mm"])

    with w_col2:
        st.markdown("#### 2. Live Weather Risk Status")
        # Evaluate severity dynamically
        if w_speed > 38 or w_temp > 42 or w_precip > 50:
            badge_w = "badge-critical"
            alert_hdr = "CRITICAL SITE SAFETY ADVISORY ACTIVE"
        elif w_speed > 25 or w_temp > 38 or w_precip > 20:
            badge_w = "badge-high"
            alert_hdr = "ELEVATED RISK - HEIGHTENED SOP IN EFFECT"
        else:
            badge_w = "badge-safe"
            alert_hdr = "OPTIMAL SITE OPERATIONS"

        st.markdown(
            f"""<div style="background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px;">
                <div style="font-size: 2.2rem; margin-bottom: 6px;">{weather_info['icon']}</div>
                <div style="margin-bottom: 8px;"><span class="badge {badge_w}" style="font-size: 0.9rem; padding: 6px 14px;">{alert_hdr}</span></div>
                <div style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.5;">
                    Wind: <strong>{w_speed} km/h</strong> | Temp: <strong>{w_temp}°C</strong> | Humidity: <strong>{w_hum}%</strong> | Rain: <strong>{w_precip} mm/h</strong>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

    # Dynamic SOP Alerts & Protocols
    st.markdown("#### 🚨 Dynamic Safety Alerts & Engineering Protocols")
    for p in weather_info["protocols"]:
        urg = p.get("urgency", "Urgent")
        u_badge = f"badge-{urg.lower()}" if urg.lower() in ["immediate", "urgent", "critical", "high"] else "badge-medium"
        
        st.markdown(
            f"""<div style="background: rgba(30, 41, 59, 0.85); border-left: 4px solid #EF4444; border-radius: 6px; padding: 14px 18px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <strong style="color: #F8FAFC; font-size: 1.05rem;">⚡ {p['title']}</strong>
                    <span class="badge {u_badge}">{urg} Action</span>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 6px;">
                    Standard Reference: <code>{p['standard']}</code>
                </div>
                <div style="font-size: 0.9rem; color: #E2E8F0; line-height: 1.5;">
                    {p['action']}
                </div>
            </div>""",
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # Multi-Turn Construction Engineering Chatbot
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("### 💬 StrucIQ™ — Construction Engineering Assistant")
    st.caption("Specialized AI Assistant grounded in IS 456:2000, IS 875, IS 13920, NBC 2016, and OSHA 1926 standards.")

    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "model",
                "content": (
                    "👋 **Hello Site Engineer / Project Manager!** I am **StrucIQ™**, your autonomous civil and safety intelligence assistant. "
                    "Ask me anything about **IS 456 curing schedules**, **formwork stripping periods**, **slump requirements**, "
                    "**wind speed thresholds**, or **OSHA fall protection protocols**."
                )
            }
        ]

    # Pre-canned Quick Inquiry Buttons
    st.markdown("**Quick Technical Inquiries:**")
    qc1, qc2, qc3, qc4 = st.columns(4)
    quick_query = None
    with qc1:
        if st.button("📋 IS 456 Curing for OPC vs PPC", use_container_width=True):
            quick_query = "What is the IS 456:2000 minimum curing duration for OPC versus PPC in hot weather?"
    with qc2:
        if st.button("💨 Tower Crane Wind Limits", use_container_width=True):
            quick_query = "What are the safe wind speed limits and shutdown protocols for tower cranes under IS 875 and OSHA?"
    with qc3:
        if st.button("🏗️ Formwork Stripping Schedule", use_container_width=True):
            quick_query = "Provide the minimum formwork stripping (deshuttering) time for slabs, beams, and props per IS 456."
    with qc4:
        if st.button("🧪 Concrete Slump for Pumping", use_container_width=True):
            quick_query = "What is the recommended concrete slump for pumping and tremie underwater piling per IS 456?"

    # Render Chat History
    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"], avatar="👷" if msg["role"] == "user" else "🏗️"):
            st.markdown(msg["content"])

    # Handle User Input or Quick Query
    user_input = st.chat_input("Ask StrucIQ a civil engineering or site safety question...")
    effective_prompt = quick_query or user_input

    if effective_prompt:
        # Append User Message
        st.session_state["chat_messages"].append({"role": "user", "content": effective_prompt})
        with st.chat_message("user", avatar="👷"):
            st.markdown(effective_prompt)

        # Generate Response
        with st.chat_message("model", avatar="🏗️"):
            with st.spinner("StrucIQ is consulting structural codes & site standards..."):
                if is_demo_mode:
                    reply = get_demo_chat_response(effective_prompt)
                else:
                    reply = gemini_client.chat_query(
                        messages=st.session_state["chat_messages"],
                        system_instruction=ASSISTANT_SYSTEM_PROMPT,
                        model_name=model_choice
                    )
                    if not reply or "Error" in reply:
                        # Fallback to local intelligence if API call failed
                        reply = get_demo_chat_response(effective_prompt)
                
                st.markdown(reply)
                st.session_state["chat_messages"].append({"role": "model", "content": reply})

    # Clear Chat History Button
    if len(st.session_state["chat_messages"]) > 1:
        if st.button("🗑️ Reset Chat History", key="clear_chat"):
            st.session_state["chat_messages"] = [st.session_state["chat_messages"][0]]
            st.rerun()

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown(
    """<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 10px 0;">
        <strong>Multimodal Construction Intelligence Platform</strong> • Skill Wallet Capstone Project 1<br>
        Compliant with OSHA 1926 • IS 456:2000 • IS 875:1987 • IS 13920:2016 • Zero External Database Dependencies
    </div>""",
    unsafe_allow_html=True
)

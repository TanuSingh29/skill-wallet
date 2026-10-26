"""
Module for Tab 4: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Provides dynamic weather risk matrix, civil engineering SOP alerts,
and a multi-turn Construction Engineering Chatbot with IS & OSHA grounding.
"""

from typing import Dict, Any, List

WEATHER_PROFILES = {
    "High Wind (Gale Warning)": {
        "wind_speed_kmh": 45,
        "temperature_c": 28,
        "humidity_pct": 55,
        "precipitation_mm": 0,
        "icon": "💨",
        "alert_level": "CRITICAL STOP-WORK ADVISORY",
        "alert_color": "#EF4444",
        "protocols": [
            {
                "title": "Immediate Tower Crane & Hoist Shutdown",
                "standard": "IS 875 (Part 3) & OSHA 1926.1431",
                "action": "Wind speeds exceed 38 km/h (20 knots). Immediately suspend all tower crane hook lifting, luffing, and passenger hoist operations. Weather-vane (release slewing brake) tower crane jibs to allow free rotation with prevailing wind.",
                "urgency": "Immediate"
            },
            {
                "title": "Suspended & Perimeter Scaffolding Evacuation",
                "standard": "IS 3696 (Part 1) & OSHA 1926.451",
                "action": "Evacuate workers from suspended cradles, mast climbers, and perimeter scaffolding above Level 3. Secure loose formwork sheets, tin roofing sheets, and tarp covers using ballast and steel tie-wires.",
                "urgency": "Urgent"
            },
            {
                "title": "Glazing & External Cladding Suspension",
                "standard": "NBC 2016 Part 6 Sec 6",
                "action": "Halt vacuum-suction glass lifters and curtain-wall panel installations. Secure facade brackets and tie back temporary netting.",
                "urgency": "High"
            }
        ]
    },
    "Heavy Rain & Monsoon Ingress": {
        "wind_speed_kmh": 22,
        "temperature_c": 26,
        "humidity_pct": 92,
        "precipitation_mm": 65,
        "icon": "🌧️",
        "alert_level": "HIGH WATER INGRESS & ELECTRICAL HAZARD",
        "alert_color": "#F59E0B",
        "protocols": [
            {
                "title": "Deep Excavation & Foundation Pit Dewatering",
                "standard": "IS 3764 (Safety in Excavation) & OSHA 1926.651",
                "action": "Activate submersible slurry sump pumps across foundation raft and lift pits. Inspect earth retaining berms and shoring sheet-piles for signs of slope slippage or piping failure.",
                "urgency": "Immediate"
            },
            {
                "title": "Site Electrical Power Isolation & ELCB Verification",
                "standard": "IS 732 & OSHA 1926.404 Ground-Fault Protection",
                "action": "De-energize non-essential surface feeder cables and distribution boards exposed to standing water. Test all 30mA Earth Leakage Circuit Breakers (ELCBs/RCCBs).",
                "urgency": "Critical"
            },
            {
                "title": "Fresh Concrete Pour Protection & Slump Guard",
                "standard": "IS 456:2000 Cl. 13.3",
                "action": "Do NOT pour unprotected slab concrete during torrential rain. Rainwater addition alters water-cement ratio, drastically reducing compressive strength. Cover green concrete with 250-micron poly-sheeting.",
                "urgency": "High"
            }
        ]
    },
    "Extreme Heat Wave (Heat Index > 42°C)": {
        "wind_speed_kmh": 12,
        "temperature_c": 43,
        "humidity_pct": 48,
        "precipitation_mm": 0,
        "icon": "🔥",
        "alert_level": "HEAT STRESS & CONCRETE DESICCATION WARNING",
        "alert_color": "#EA580C",
        "protocols": [
            {
                "title": "Hot-Weather Concreting & Chilled Water Protocol",
                "standard": "IS 7861 (Part 1) & ACI 305R",
                "action": "Concrete placement temperature must NOT exceed 32°C. Replace mixing water with flake ice up to 50%. Pre-wet aggregate stockpiles and schedule high-volume pours exclusively during night shift (7 PM - 5 AM).",
                "urgency": "High"
            },
            {
                "title": "Continuous Evaporation Curing & Burlap Ponding",
                "standard": "IS 456:2000 Cl. 13.5",
                "action": "Apply aluminized resin-based curing compound within 15 minutes of finishing. Extend wet Hessian burlap wrapping for minimum 14 days to prevent plastic shrinkage cracking.",
                "urgency": "Urgent"
            },
            {
                "title": "Worker Heat Stroke Prevention & Mandatory Rest Cycles",
                "standard": "OSHA Safety and Health Bulletin (Heat Illness) & DGFASLI",
                "action": "Implement OSHA Work/Rest schedule: 15-minute shaded rest per hour. Provide chilled potable drinking water infused with electrolyte ORS at every floor level.",
                "urgency": "High"
            }
        ]
    },
    "Normal Fair Weather (Optimal Site Conditions)": {
        "wind_speed_kmh": 14,
        "temperature_c": 29,
        "humidity_pct": 52,
        "precipitation_mm": 0,
        "icon": "☀️",
        "alert_level": "OPTIMAL WORKING CONDITIONS - NORMAL SOP ACTIVE",
        "alert_color": "#10B981",
        "protocols": [
            {
                "title": "Standard Superstructure Pouring & Lifting Operations",
                "standard": "IS 456:2000 & OSHA 1926 Subpart Q",
                "action": "Weather parameters optimal for standard concrete placing, rebar tying, and tower crane operations. Maintain routine 7-day ponding curing on completed slabs.",
                "urgency": "Routine"
            },
            {
                "title": "Pre-pour Quality Assurance Checklist",
                "standard": "IS 456 Cl. 10 & IS 1199",
                "action": "Verify clear cover blocks (25mm slab, 40mm beam, 40-50mm column). Confirm slump tolerance (100-120mm for pumped concrete) via site slump cone test before discharge.",
                "urgency": "Routine"
            }
        ]
    }
}

ASSISTANT_SYSTEM_PROMPT = """
You are "StrucIQ", a Senior Principal Construction & Structural Engineering Assistant specialized in:
- Indian Standard Codes: IS 456:2000 (RCC Design & Execution), IS 875 Parts 1-5 (Design Loads & Wind/Earthquake), IS 1893 (Earthquake Resisting Structures), IS 13920:2016 (Ductile Detailing), IS 7861 (Hot/Cold Concreting), IS 3696 (Scaffolding Safety), NBC 2016.
- International & OSHA Standards: OSHA 1926 (Construction Safety Regulations), ACI 318, ACI 224 (Cracking), Eurocode 2.
- Practical Construction Site Execution: Formwork striking periods, slump values, batching tolerances, pre-pour checklists, curing durations, bar bending schedules (BBS), and non-destructive testing (UPV, Rebound Hammer).

Provide authoritative, technically rigorous, and actionable advice. Reference the exact standard clauses and formulas where applicable. Format responses with clear headings, bullet points, and engineering formulas.
"""

def get_demo_chat_response(prompt: str) -> str:
    """Provides high-quality offline engineering responses for demo mode."""
    p_lower = prompt.lower()
    
    if "curing" in p_lower or "opc" in p_lower or "ppc" in p_lower:
        return """### 📋 IS 456:2000 Curing Requirements (Clause 13.5)

Under **IS 456:2000, Clause 13.5 (Curing)**, the minimum curing duration depends strictly on the cement type and ambient weather conditions:

1. **Ordinary Portland Cement (OPC - 33, 43, 53 Grade per IS 269 / IS 8112 / IS 12269):**
   - **Normal / Moist Weather:** Minimum **7 days** of continuous moist curing.
   - **Hot / Dry Weather (Temperature >35°C or RH <50%):** Minimum **10 days** of moist curing.

2. **Mineral Admixtures / Blended Cements (PPC - Fly Ash based per IS 1489, or PSC - Slag based per IS 455):**
   - **Normal Weather:** Minimum **10 days** of continuous moist curing.
   - **Hot / Dry Weather:** Minimum **14 days** of continuous moist curing.
   - *Technical Reason:* Pozzolanic reaction of secondary hydrated calcium silicate (C-S-H gel) is significantly slower and requires prolonged moisture availability.

3. **Approved Curing Methods:**
   - **Ponding:** Best for horizontal grade and floor slabs (25mm water depth).
   - **Wet Burlap / Hessian Cloth:** Best for vertical columns and beam sides (wrapped and kept continuously soaked).
   - **Membrane Curing Compounds:** Conforming to ASTM C309, applied immediately after surface sheen disappears.
"""
    elif "wind" in p_lower or "crane" in p_lower or "speed" in p_lower:
        return """### 💨 Wind Speed Thresholds & Crane Safety (IS 875 Part 3 & OSHA 1926.1431)

Standard international and Indian safety guidelines specify strict operational wind speed limits for construction lifting:

| Operation Type | Max Permissible Wind Speed | SOP Action / Protocol |
| :--- | :--- | :--- |
| **Normal Tower Crane Operations** | **38 km/h (20 knots / 10.5 m/s)** | Maximum safe limit for standard container/bucket hoisting. |
| **Large Surface Panels / Glazing / Formwork** | **28 km/h (15 knots / 7.8 m/s)** | Sail effect can induce uncommanded slewing torque. Stop large panel hoisting. |
| **Complete Crane Shutdown & Weather-Vaning** | **> 50 km/h (27 knots / 14 m/s)** | Lower hook block to highest limit, release slew brake so jib rotates freely with the wind to avoid overturning torque. |
| **Personnel Man-Basket Hoisting** | **25 km/h (14 knots / 7.0 m/s)** | Zero tolerance per OSHA 1926.1431. |

> [!CAUTION]
> Never lock the swing brake of a tower crane in gale conditions; a locked jib acts like a rigid lever arm and can buckle the tower mast.
"""
    elif "stripping" in p_lower or "formwork" in p_lower or "deshuttering" in p_lower or "prop" in p_lower:
        return """### 🏗️ Formwork Stripping (Deshuttering) Periods (IS 456:2000 Clause 11.3)

Unless specified otherwise by the Structural Engineer of Record (SEOR) using cube strength verification, formwork stripping periods for OPC concrete are:

| Structural Element | Minimum Period before Striking |
| :--- | :--- |
| **Vertical formwork to columns, walls, beams** | **16 - 24 hours** |
| **Soffit formwork to slabs** *(props to be refixed immediately)* | **3 days** |
| **Soffit formwork to beams** *(props to be refixed immediately)* | **7 days** |
| **Props to slabs:** | |
| • Spanning up to 4.5 meters | **7 days** |
| • Spanning over 4.5 meters | **14 days** |
| **Props to beams and arches:** | |
| • Spanning up to 6 meters | **14 days** |
| • Spanning over 6 meters | **21 days** |

> [!NOTE]
> When using PPC (Fly Ash) or GGBS blended concrete, strip times must be extended by **25% - 40%** unless test cubes crushed at the site lab achieve at least **67% of characteristic compressive strength ($f_{ck}$)**.
"""
    elif "slump" in p_lower or "tremie" in p_lower or "pump" in p_lower:
        return """### 🧪 Concrete Slump Recommendations (IS 456:2000 Clause 7.1 & IS 1199)

Recommended slump ranges measured at point of discharge:

1. **Tremie Concrete (Piling & Diaphragm Walls under Bentonite Slurry):**
   - **150 mm to 200 mm** (Self-compacting, highly cohesive, non-segregating).
   - High slump is essential to displace drilling bentonite without requiring mechanical vibration.

2. **Pumped Concrete (Slabs, Beams, High-Rise Columns):**
   - **100 mm to 130 mm** using superplasticizer admixtures (IS 9103).

3. **Heavily Reinforced Concrete Sections (Deep Transfer Girders, Column Jams):**
   - **75 mm to 100 mm**.

4. **Mass Concrete & Shallow Foundations:**
   - **25 mm to 75 mm** (Lower slump minimizes hydration heat and shrinkage).
"""
    else:
        return f"""### 👷 Civil & Structural Engineering Technical Advisory

**Topic Query:** *"{prompt}"*

Based on **IS 456:2000, IS 875, IS 1893:2016, and OSHA 1926 standards**, here is the recommended site protocol:

1. **Quality & Standard Compliance:**
   - Verify material compliance against relevant Indian Standard specifications (e.g., IS 1786 for Fe 500D TMT reinforcement, IS 8112 for 43-Grade OPC).
   - Maintain structural tolerances specified in IS 456 Clause 12.3 (e.g., cross-sectional dimensions of beams/columns within $+12\\text{ mm}$ to $-6\\text{ mm}$).

2. **Site Safety Protocol (OSHA 1926 / IS 3696):**
   - Ensure edge protection (standard 1.05m high top rail and intermediate mid-rail) on all open floor levels above 1.8 meters.
   - Enforce mandatory Tool Box Talks (TBT) before every shift with specialized hazard identification for heavy equipment.

3. **Environmental Considerations:**
   - Check ambient weather variables (wind speed, wet bulb temperature) before releasing critical work permits for elevated lifting or large concrete placements.

*Note: In live mode with a Gemini API key connected, this assistant dynamically queries multimodal models with live engineering reasoning.*
"""

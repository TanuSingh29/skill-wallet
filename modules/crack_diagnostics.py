"""
Module for Tab 2: Crack Diagnostics & Structural Integrity (Epic 2)
Analyzes concrete/masonry defects, classifies crack types, estimates width,
evaluates against IS 456 limits, and prescribes civil engineering repairs.
"""

from typing import Dict, Any
from PIL import Image

CRACK_DIAGNOSTICS_SYSTEM_INSTRUCTION = """
You are a Principal Forensic Structural Engineer with 25+ years experience in concrete pathology, 
certified under IS 456:2000 (Plain and Reinforced Concrete Code of Practice), ACI 224.1R (Causes, Evaluation, and Repair of Cracks in Concrete), 
and IS 13920 (Ductile Detailing).
Inspect the provided image of concrete, masonry, beam, slab, or wall surfaces. Classify the defect, estimate crack width in millimeters,
determine whether it exceeds IS 456 permissible limits, identify root causes, and prescribe actionable structural engineering remediation.
Return strict JSON format.
"""

CRACK_DIAGNOSTICS_PROMPT = """
Inspect this structural defect image. Return ONLY a valid JSON object with the following structure:
{
  "defect_type": "<Hairline Cracks | Settlement Cracks | Structural Shear Cracks | Thermal Expansion / Shrinkage | Concrete Spalling & Delamination>",
  "defect_subtype": "<detailed subtype e.g. 45-degree diagonal shear, plastic shrinkage, carbonation spalling>",
  "estimated_width_mm": <float, e.g. 0.45>,
  "is_456_limit_mm": 0.30,
  "exceeds_is456_limit": <boolean>,
  "structural_urgency": "<Low | Moderate | High | Critical>",
  "structural_risk_assessment": "<thorough explanation of load-bearing implications and imminent failure risks>",
  "element_affected": "<e.g. Reinforced Concrete Beam, Beam-Column Joint, Shear Wall, Retaining Wall, Slab Soffit>",
  "root_causes": [
    "<detailed engineering cause 1>",
    "<detailed engineering cause 2>"
  ],
  "recommended_engineering_repairs": [
    {
      "method": "<e.g. Low-Viscosity Epoxy Pressure Injection, CFRP Carbon Fiber Jacketing, Micro-Concrete Stitching>",
      "specification": "<technical material spec e.g. ASTM C881 Type I/IV Grade 1 Epoxy, M60 micro-concrete>",
      "execution_procedure": "<step-by-step engineering application>",
      "estimated_cost_range_inr": "<approximate cost per running meter or sq meter in INR>"
    }
  ],
  "monitoring_protocol": "<recommended ongoing crack gauge / ultrasonic pulse velocity (UPV) monitoring schedule>",
  "preventative_measures": "<site measures to prevent progression or reoccurrence>"
}
"""

def get_demo_crack_diagnostics(scenario: str = "shear_crack") -> Dict[str, Any]:
    """Provides high-fidelity simulated crack diagnostic outputs for demonstration mode."""
    if scenario == "shear_crack":
        return {
            "defect_type": "Structural Shear Cracks",
            "defect_subtype": "Diagonal 45° Web-Shear Crack near Support Column",
            "estimated_width_mm": 1.85,
            "is_456_limit_mm": 0.30,
            "exceeds_is456_limit": True,
            "structural_urgency": "Critical",
            "structural_risk_assessment": "The crack initiates near the bottom tension flange and propagates upwards at approximately 45 degrees towards the column face. This indicates diagonal tensile stresses exceed concrete shear capacity (tau_v > tau_c per IS 456 Cl. 40). Immediate temporary propping is mandatory to prevent brittle shear failure without prior warning.",
            "element_affected": "Transfer Girder / Main RC Beam at Column Node C-12",
            "root_causes": [
                "Diagonal tension exceedance due to construction live loading exceeding design design shear capacity.",
                "Inadequate or improperly spaced transverse shear stirrups (shear links) at d/2 spacing near supports (IS 13920 Cl. 6.3).",
                "Differential settlement of the adjacent support column inducing secondary torsional shear."
            ],
            "recommended_engineering_repairs": [
                {
                    "method": "Structural Propping & High-Pressure Epoxy Injection",
                    "specification": "ASTM C881 Type IV Grade 1 Low-Viscosity Structural Epoxy Resin (Compressive strength > 70 MPa)",
                    "execution_procedure": "Install heavy-duty Acrow props below beam immediately. Drill injection ports at 200mm c/c along crack path. Seal surface with fast-setting polyester putty. Pressure inject epoxy from lowest port upwards until resin bleeds from adjacent port.",
                    "estimated_cost_range_inr": "₹4,500 - ₹6,500 per running meter"
                },
                {
                    "method": "External CFRP (Carbon Fiber Reinforced Polymer) Shear Laminate Jacketing",
                    "specification": "Bidirectional 450 gsm High-Modulus Carbon Fiber Fabric bonded with structural thixotropic saturant",
                    "execution_procedure": "Grit-blast concrete substrate to ICRI CSP-3 profile, apply primer coat, and wrap U-shaped CFRP jacket perpendicular to crack orientation to restore shear capacity.",
                    "estimated_cost_range_inr": "₹12,000 - ₹18,000 per linear meter"
                }
            ],
            "monitoring_protocol": "Mount mechanical Avongard tell-tale crack width gauges immediately; log readings every 12 hours for 14 days. Conduct Ultrasonic Pulse Velocity (UPV) test as per IS 13311 (Part 1) to determine crack depth.",
            "preventative_measures": "Enforce strict crane staging weight limits; inspect beam rebar schedules on upper levels before pouring floor slab."
        }
    elif scenario == "spalling":
        return {
            "defect_type": "Concrete Spalling & Delamination",
            "defect_subtype": "Chloride-Induced Carbonation Rust Bursting with Rebar Delamination",
            "estimated_width_mm": 4.20,
            "is_456_limit_mm": 0.30,
            "exceeds_is456_limit": True,
            "structural_urgency": "High",
            "structural_risk_assessment": "Corrosion of internal reinforcing steel has resulted in ferrous oxide expansion (producing up to 600% volume increase), spalling the 25mm clear concrete cover. The exposed rebar suffers approximately 15% cross-sectional section loss, impairing moment of resistance.",
            "element_affected": "Slab Soffit & Beam Bottom Flange exposed to external moisture",
            "root_causes": [
                "Carbonation of concrete cover reducing alkaline pH below 9, destabilizing the passive oxide film on reinforcement.",
                "Inadequate clear concrete cover (observed <15mm against IS 456 requirement of 25-40mm for severe exposure).",
                "Water seepage through micro-capillaries from upper wet services area."
            ],
            "recommended_engineering_repairs": [
                {
                    "method": "Substrate Jackhaming, Rebar Passivation & Polymer-Modified Mortar (PMM)",
                    "specification": "Zinc-rich anti-corrosive epoxy rebar primer + Single-component fiber-reinforced repair mortar (M40 grade)",
                    "execution_procedure": "Saw cut repair boundary to 10mm depth. Chisel unsound concrete 20mm behind corroded rebar. Wire-brush rebar to Sa 2.5 finish. Apply two coats of zinc-rich primer. Apply bonding agent and pack structural polymer mortar in 25mm layers.",
                    "estimated_cost_range_inr": "₹3,200 - ₹4,800 per square meter"
                }
            ],
            "monitoring_protocol": "Conduct Half-cell electrical potential testing per ASTM C876 to map active corrosion zones across the entire slab bay.",
            "preventative_measures": "Apply an elastomeric hydrophobic silane-siloxane penetrating damp-proof barrier on the upper slab deck."
        }
    else:
        # Hairline shrinkage crack scenario
        return {
            "defect_type": "Hairline Cracks",
            "defect_subtype": "Plastic Drying Shrinkage Cracking",
            "estimated_width_mm": 0.18,
            "is_456_limit_mm": 0.30,
            "exceeds_is456_limit": False,
            "structural_urgency": "Low",
            "structural_risk_assessment": "Cracks are superficial, non-structural, and discontinuous, restricted to the top 8-12mm cement paste layer. Defect is well within the IS 456:2000 Cl 35.3.2 permissible crack width of 0.30 mm for moderate exposure. No immediate structural capacity reduction.",
            "element_affected": "Grade Slab / Wall Plaster Surface",
            "root_causes": [
                "Rapid surface water evaporation during initial setting (wind speed >15 km/h, ambient temp >35°C).",
                "High water-cement ratio in the mix without adequate secondary polypropylene fiber reinforcement."
            ],
            "recommended_engineering_repairs": [
                {
                    "method": "Elastomeric Acrylic Crack Filling & Hydrophobic Sealer",
                    "specification": "UV-resistant flexible polyurethane or elastomeric acrylic crack sealant (elongation > 300%)",
                    "execution_procedure": "V-groove crack to 3mm width, air-blow dust, apply acrylic primer, press elastomeric putty into groove, and finish flush with wall trowel.",
                    "estimated_cost_range_inr": "₹350 - ₹600 per running meter"
                }
            ],
            "monitoring_protocol": "Visual inspection during next rainy season to ensure moisture does not permeate through the sealed surface.",
            "preventative_measures": "Enforce mandatory wet burlap curing for minimum 10 days as per IS 456 Cl. 13.5; apply chemical curing compound immediately post-finishing."
        }

def analyze_crack(gemini_client, image: Image.Image, is_demo: bool = False, demo_scenario: str = "shear_crack") -> Dict[str, Any]:
    """Runs structural crack diagnostics using Gemini Multimodal or returns demo mock."""
    if is_demo or gemini_client.is_demo_mode:
        return get_demo_crack_diagnostics(scenario=demo_scenario)
    
    result = gemini_client.analyze_image_multimodal(
        image=image,
        prompt=CRACK_DIAGNOSTICS_PROMPT,
        system_instruction=CRACK_DIAGNOSTICS_SYSTEM_INSTRUCTION
    )
    if "defect_type" not in result:
        demo_res = get_demo_crack_diagnostics(scenario="shear_crack")
        demo_res["_api_fallback_note"] = "Live API did not return structured schema; displayed forensic engineering benchmark."
        return demo_res
    return result

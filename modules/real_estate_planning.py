"""
Module for Tab 3: Planning & Real Estate Valuation (Epic 3)
Calculates project budget, incurred CapEx, market asset valuation in INR,
empirical steel/cement requirements, milestone tracking, and 3D architectural rendering via Pollinations AI.
"""

import urllib.parse
from typing import Dict, Any, Tuple

# Base Construction Cost per sq ft (INR) for Tier 1 cities
BASE_CONSTRUCTION_COSTS = {
    "Residential High-Rise (G+25)": 3200,
    "Commercial Grade-A Tech Park": 3800,
    "Industrial Logistics Warehouse": 2100,
    "Luxury Villa Community": 4200,
    "Infrastructure Flyover / Elevated Viaduct": 5600
}

# Base Selling / Asset Market Value per sq ft (INR) for Tier 1 cities
BASE_MARKET_VALUES = {
    "Residential High-Rise (G+25)": 14500,
    "Commercial Grade-A Tech Park": 16500,
    "Industrial Logistics Warehouse": 6200,
    "Luxury Villa Community": 18500,
    "Infrastructure Flyover / Elevated Viaduct": 9800
}

# City Tier Multipliers
TIER_MULTIPLIERS = {
    "Tier 1 (Mumbai MMR, Delhi NCR, Bengaluru, Hyderabad)": {"cost": 1.0, "value": 1.0, "label": "Tier 1"},
    "Tier 2 (Pune, Ahmedabad, Kolkata, Kochi, Jaipur)": {"cost": 0.85, "value": 0.65, "label": "Tier 2"},
    "Tier 3 (Indore, Lucknow, Coimbatore, Bhubaneswar)": {"cost": 0.72, "value": 0.45, "label": "Tier 3"}
}

# Empirical Material Consumption Factors per sq ft (CPWD & IS Norms)
MATERIAL_NORMS = {
    "Residential High-Rise (G+25)": {"steel_kg_per_sqft": 4.8, "cement_bags_per_sqft": 0.42, "sand_cuft_per_sqft": 1.8},
    "Commercial Grade-A Tech Park": {"steel_kg_per_sqft": 5.2, "cement_bags_per_sqft": 0.45, "sand_cuft_per_sqft": 1.9},
    "Industrial Logistics Warehouse": {"steel_kg_per_sqft": 3.4, "cement_bags_per_sqft": 0.32, "sand_cuft_per_sqft": 1.4},
    "Luxury Villa Community": {"steel_kg_per_sqft": 4.0, "cement_bags_per_sqft": 0.44, "sand_cuft_per_sqft": 1.85},
    "Infrastructure Flyover / Elevated Viaduct": {"steel_kg_per_sqft": 7.5, "cement_bags_per_sqft": 0.58, "sand_cuft_per_sqft": 2.2}
}

MILESTONES = [
    {"range": (0, 15), "phase": "Site Preparation, Piling & Foundation Raft", "status": "Substructure Level"},
    {"range": (15, 35), "phase": "Basement Retaining Walls & Podium Slabs", "status": "Plinth to Podium"},
    {"range": (35, 70), "phase": "Superstructure RCC Framing & Slabs Casting", "status": "Structural Framing"},
    {"range": (70, 85), "phase": "Block Masonry, MEP Infrastructure & Façade", "status": "Building Enclosure"},
    {"range": (85, 98), "phase": "Internal Architectural Finishes, Lifts & Landscaping", "status": "Fit-out & Finishes"},
    {"range": (98, 100), "phase": "Statutory Testing, Commissioning & Occupancy Certificate", "status": "Handover Ready"}
]

def format_inr(amount: float) -> str:
    """Formats an amount in INR to Lakhs or Crores."""
    if amount >= 10000000:
        return f"₹{amount / 10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount / 100000:.2f} L"
    else:
        return f"₹{amount:,.0f}"

def calculate_valuation_and_materials(
    structure_type: str,
    built_up_sqft: float,
    tier_name: str,
    completion_pct: float
) -> Dict[str, Any]:
    """Computes all budgetary, valuation, and material estimations."""
    tier_info = TIER_MULTIPLIERS.get(tier_name, {"cost": 1.0, "value": 1.0, "label": "Tier 1"})
    
    base_cost_per_sqft = BASE_CONSTRUCTION_COSTS.get(structure_type, 3200) * tier_info["cost"]
    base_val_per_sqft = BASE_MARKET_VALUES.get(structure_type, 14000) * tier_info["value"]
    
    # Financial metrics
    total_budget_inr = built_up_sqft * base_cost_per_sqft
    capex_incurred_inr = total_budget_inr * (completion_pct / 100.0)
    
    # Valuation considers land share (approx 35% of finished value) plus incurred progress + stage risk premium
    finished_market_value_inr = built_up_sqft * base_val_per_sqft
    land_equity_component = finished_market_value_inr * 0.35
    construction_value_add = (finished_market_value_inr - land_equity_component) * (completion_pct / 100.0)
    # Risk discount reduces as project approaches 100%
    completion_factor = completion_pct / 100.0
    current_asset_valuation_inr = land_equity_component + construction_value_add * (0.85 + 0.15 * completion_factor)
    
    # Materials requirement based on CPWD / IS standards
    norms = MATERIAL_NORMS.get(structure_type, {"steel_kg_per_sqft": 4.5, "cement_bags_per_sqft": 0.42, "sand_cuft_per_sqft": 1.8})
    total_steel_kg = built_up_sqft * norms["steel_kg_per_sqft"]
    total_steel_mt = total_steel_kg / 1000.0
    steel_consumed_mt = total_steel_mt * (completion_pct / 100.0)
    
    total_cement_bags = built_up_sqft * norms["cement_bags_per_sqft"]
    total_cement_mt = (total_cement_bags * 50) / 1000.0
    cement_consumed_bags = total_cement_bags * (completion_pct / 100.0)
    
    total_sand_cuft = built_up_sqft * norms["sand_cuft_per_sqft"]
    sand_consumed_cuft = total_sand_cuft * (completion_pct / 100.0)
    
    # Determine current milestone
    current_phase = "Preliminary Groundwork"
    phase_status = "Pre-Construction"
    for m in MILESTONES:
        if m["range"][0] <= completion_pct <= m["range"][1]:
            current_phase = m["phase"]
            phase_status = m["status"]
            break

    return {
        "structure_type": structure_type,
        "built_up_sqft": built_up_sqft,
        "tier": tier_info["label"],
        "completion_pct": completion_pct,
        "current_phase": current_phase,
        "phase_status": phase_status,
        "cost_per_sqft": base_cost_per_sqft,
        "val_per_sqft": base_val_per_sqft,
        "total_budget_inr": total_budget_inr,
        "total_budget_formatted": format_inr(total_budget_inr),
        "capex_incurred_inr": capex_incurred_inr,
        "capex_incurred_formatted": format_inr(capex_incurred_inr),
        "finished_market_value_inr": finished_market_value_inr,
        "finished_market_value_formatted": format_inr(finished_market_value_inr),
        "current_asset_valuation_inr": current_asset_valuation_inr,
        "current_asset_valuation_formatted": format_inr(current_asset_valuation_inr),
        "unrealized_gain_inr": max(0, current_asset_valuation_inr - capex_incurred_inr),
        "unrealized_gain_formatted": format_inr(max(0, current_asset_valuation_inr - capex_incurred_inr)),
        "materials": {
            "steel": {
                "total_mt": round(total_steel_mt, 1),
                "consumed_mt": round(steel_consumed_mt, 1),
                "balance_mt": round(total_steel_mt - steel_consumed_mt, 1),
                "unit_rate_norm": f"{norms['steel_kg_per_sqft']} kg/sq.ft (IS 1786 Fe500D TMT)"
            },
            "cement": {
                "total_bags": int(total_cement_bags),
                "consumed_bags": int(cement_consumed_bags),
                "total_mt": round(total_cement_mt, 1),
                "balance_bags": int(total_cement_bags - cement_consumed_bags),
                "unit_rate_norm": f"{norms['cement_bags_per_sqft']} bags/sq.ft (IS 8112 OPC 43/53)"
            },
            "sand_aggregates": {
                "total_cuft": int(total_sand_cuft),
                "consumed_cuft": int(sand_consumed_cuft),
                "balance_cuft": int(total_sand_cuft - sand_consumed_cuft),
                "unit_rate_norm": f"{norms['sand_cuft_per_sqft']} cu.ft/sq.ft (Zone II M-Sand / River Sand)"
            }
        }
    }

def generate_pollinations_render_url(
    structure_type: str,
    arch_style: str = "Modern Glass Curtain & Biophilic Terraces",
    lighting: str = "Golden Hour Dusk Architectural Photography",
    seed: int = 42
) -> Tuple[str, str]:
    """
    Generates a high-resolution conceptual 3D architectural rendering URL via Pollinations AI.
    Returns (image_url, prompt_text).
    """
    prompt = (
        f"Award-winning 3D architectural photorealistic rendering of a {structure_type}, "
        f"designed in {arch_style} style, featuring sleek exterior cantilever terraces, reflective energy-efficient glass facade, "
        f"luxurious landscape plaza with water features and mature trees, {lighting}, hyper-detailed 8k resolution, "
        f"architectural digest exterior elevation, Octane render, unreal engine 5 archviz."
    )
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=750&seed={seed}&nologo=true&model=flux"
    return url, prompt

"""
Automated unit verification test for Multimodal Construction Intelligence Platform.
Tests all modules, calculations, demo payloads, and JSON schemas.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image

def test_imports():
    print("Testing imports...")
    import streamlit
    import google.genai
    import plotly
    import pandas
    from modules.gemini_client import GeminiPlatformClient
    from modules.ppe_audit import analyze_ppe, get_demo_ppe_audit
    from modules.crack_diagnostics import analyze_crack, get_demo_crack_diagnostics
    from modules.real_estate_planning import calculate_valuation_and_materials, generate_pollinations_render_url
    from modules.weather_assistant import WEATHER_PROFILES, get_demo_chat_response
    from sample_data.sample_images import generate_sample_ppe_image, generate_sample_crack_image
    print("All module imports passed!")

def test_ppe_audit():
    print("Testing PPE Audit module...")
    from modules.gemini_client import GeminiPlatformClient
    from modules.ppe_audit import analyze_ppe
    from sample_data.sample_images import generate_sample_ppe_image
    
    client = GeminiPlatformClient(api_key="")
    assert client.is_demo_mode is True, "Client should be in demo mode"
    
    img = generate_sample_ppe_image(scenario="compliant")
    assert isinstance(img, Image.Image), "Should generate PIL Image"
    
    res = analyze_ppe(client, img, is_demo=True, demo_scenario="default")
    assert "safety_score" in res, "Result must contain safety_score"
    assert "ppe_detection" in res, "Result must contain ppe_detection"
    assert "site_hazards" in res, "Result must contain site_hazards"
    print(f"PPE Audit test passed! Safety score: {res['safety_score']}")

def test_crack_diagnostics():
    print("Testing Crack Diagnostics module...")
    from modules.gemini_client import GeminiPlatformClient
    from modules.crack_diagnostics import analyze_crack
    from sample_data.sample_images import generate_sample_crack_image
    
    client = GeminiPlatformClient(api_key="")
    img = generate_sample_crack_image(crack_type="shear")
    res = analyze_crack(client, img, is_demo=True, demo_scenario="shear_crack")
    assert "defect_type" in res, "Result must contain defect_type"
    assert "estimated_width_mm" in res, "Result must contain estimated_width_mm"
    assert "recommended_engineering_repairs" in res, "Result must contain repairs"
    print(f"Crack Diagnostics test passed! Defect: {res['defect_type']}, Width: {res['estimated_width_mm']} mm")

def test_real_estate_and_materials():
    print("Testing Real Estate Valuation & Material Engine...")
    from modules.real_estate_planning import calculate_valuation_and_materials, generate_pollinations_render_url
    
    res = calculate_valuation_and_materials(
        structure_type="Residential High-Rise (G+25)",
        built_up_sqft=100000,
        tier_name="Tier 1 (Mumbai MMR, Delhi NCR, Bengaluru, Hyderabad)",
        completion_pct=50
    )
    assert res["total_budget_inr"] > 0, "Budget must be positive"
    assert res["capex_incurred_inr"] == res["total_budget_inr"] * 0.5, "CapEx at 50% must be half total budget"
    assert "materials" in res, "Materials dict required"
    assert res["materials"]["steel"]["total_mt"] > 0, "Steel MT must be positive"
    
    url, prompt = generate_pollinations_render_url(structure_type="Residential High-Rise (G+25)")
    assert url.startswith("https://image.pollinations.ai"), "URL must point to pollinations.ai"
    print(f"Planning Engine test passed! Budget: {res['total_budget_formatted']}, Steel: {res['materials']['steel']['total_mt']} MT")

def test_weather_and_chat():
    print("Testing Weather SOP and Chatbot...")
    from modules.weather_assistant import WEATHER_PROFILES, get_demo_chat_response
    assert "High Wind (Gale Warning)" in WEATHER_PROFILES
    
    reply = get_demo_chat_response("What is the curing time for OPC?")
    assert "IS 456" in reply, "Response must cite IS 456"
    print("Weather & Chatbot tests passed!")

if __name__ == "__main__":
    test_imports()
    test_ppe_audit()
    test_crack_diagnostics()
    test_real_estate_and_materials()
    test_weather_and_chat()
    print("\n🎉 ALL PLATFORM UNIT TESTS PASSED WITH 100% SUCCESS!")

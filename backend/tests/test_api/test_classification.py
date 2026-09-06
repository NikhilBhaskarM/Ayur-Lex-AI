import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_classification_classical_medicine(client: AsyncClient, auth_headers: dict):
    headers = {"Authorization": auth_headers["Authorization"]}
    payload = {
        "formulation_name": "Triphala Churna",
        "description": "Authentic classical rasayana from Charaka Samhita",
        "ingredients": ["Terminalia chebula (Haritaki)", "Terminalia bellirica (Bibhitaki)", "Phyllanthus emblica (Amalaki)"],
        "intended_use": "Digestion and antioxidant rasayana",
        "is_classical_text_based": True,
        "has_been_modified": False,
        "marketed_as": "Medicine",
        "jurisdiction": "India",
        "biological_resources_involved": True
    }
    response = await client.post("/api/v1/classification", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "Classical" in data["classification"]
    assert "Form 25-D" in " ".join(data["regulatory_implications"])
    assert "Section 3(p)" in " ".join(data["ip_implications"])
    assert data["confidence"]["level"] == "HIGH"
    assert "disclaimer" in data

@pytest.mark.asyncio
async def test_classification_ayurveda_aahara(client: AsyncClient, auth_headers: dict):
    headers = {"Authorization": auth_headers["Authorization"]}
    payload = {
        "formulation_name": "Herbal Wellness Tea",
        "description": "Daily herbal infusion drink",
        "ingredients": ["Ocimum sanctum (Tulsi)", "Zingiber officinale (Shunthi)", "Cinnamomum verum (Dalchini)"],
        "intended_use": "Daily nutritional wellness beverage",
        "is_classical_text_based": True,
        "has_been_modified": True,
        "marketed_as": "Ayurveda-Aahar",
        "jurisdiction": "India",
        "biological_resources_involved": True
    }
    response = await client.post("/api/v1/classification", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "Ayurveda Aahara" in data["classification"]
    assert "FSSAI" in " ".join(data["regulatory_implications"])

@pytest.mark.asyncio
async def test_classification_cosmetic(client: AsyncClient, auth_headers: dict):
    headers = {"Authorization": auth_headers["Authorization"]}
    payload = {
        "formulation_name": "Kumkumadi Face Glow Oil",
        "description": "Herbal facial oil for skin illumination",
        "ingredients": ["Crocus sativus (Kumkuma)", "Santalum album (Chandana)", "Rubia cordifolia (Manjistha)"],
        "intended_use": "Skin radiance and cosmetic hydration",
        "is_classical_text_based": True,
        "has_been_modified": True,
        "marketed_as": "Cosmetic",
        "jurisdiction": "India",
        "biological_resources_involved": True
    }
    response = await client.post("/api/v1/classification", json=payload, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "Cosmetic" in data["classification"]
    assert "Cosmetics Rules" in " ".join(data["regulatory_implications"])

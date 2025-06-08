import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_humanize_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/humanize", json={
            "text": "Climate change impacts are becoming more evident.",
            "mode": "balanced"
        })
        assert response.status_code == 200
        result = response.json()
        assert result["ai_detection_estimate"] < 50
        assert result["humanized"] != result["original"]

@pytest.mark.asyncio
async def test_batch_processing():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/batch", json={
            "texts": [
                "Companies are facing challenges.",
                "Research suggests new findings."
            ],
            "mode": "fast"
        })
        assert response.status_code == 200
        result = response.json()
        assert len(result["results"]) == 2

@pytest.mark.asyncio
async def test_modes():
    test_text = "The effectiveness of AI is evident."
    async with AsyncClient(app=app, base_url="http://test") as client:
        for mode in ["fast", "balanced", "aggressive"]:
            response = await client.post("/humanize", json={
                "text": test_text,
                "mode": mode
            })
            assert response.status_code == 200
            result = response.json()
            print(f"{mode}: {result['processing_time_ms']}ms, detection: {result['ai_detection_estimate']}%")

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "healthy"

@pytest.mark.asyncio
async def test_analyze_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/analyze", params={
            "text": "The research demonstrates significant findings."
        })
        assert response.status_code == 200
        result = response.json()
        assert "ai_detection_estimate" in result
        assert "needs_enhancement" in result 
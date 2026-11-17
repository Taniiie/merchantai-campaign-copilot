import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db


def test_full_campaign_workflow():
    """End-to-end integration test of the agentic campaign copilot flow."""
    init_db()

    async def _run():
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as c:
            # 1. Health check
            r = await c.get("/health")
            assert r.status_code == 200
            assert r.json() == {"status": "healthy"}

            # 2. Root endpoint
            r = await c.get("/")
            assert r.status_code == 200
            data = r.json()
            assert data["status"] == "running"
            assert data["ai_provider"] == "demo"

            # 3. Create merchant
            merchant_payload = {
                "business_name": "Test Boutique",
                "business_type": "Fashion/Apparel",
                "location": "Mumbai",
                "product_service": "Women ethnic wear",
                "target_customers": "Women 22-40",
                "marketing_goal": "Increase Diwali sales",
                "campaign_budget": 15000,
                "preferred_platform": "Instagram"
            }
            r = await c.post("/api/merchants/", json=merchant_payload)
            assert r.status_code == 200
            merchant = r.json()
            mid = merchant["id"]
            assert merchant["business_name"] == "Test Boutique"

            # 4. Get merchant
            r = await c.get(f"/api/merchants/{mid}")
            assert r.status_code == 200
            assert r.json()["id"] == mid

            # 5. Validate onboarding
            r = await c.post(f"/api/merchants/{mid}/validate-onboarding")
            assert r.status_code == 200
            val = r.json()
            assert val["is_complete"] is True
            assert val["completion_percentage"] == 100

            # 6. Plan campaign
            r = await c.post("/api/campaigns/plan", json={"merchant_id": mid})
            assert r.status_code == 200
            plan = r.json()
            assert plan["objective"] != ""
            assert plan["target_audience"] != ""

            # 7. Get created campaign
            r = await c.get("/api/campaigns/1")
            assert r.status_code == 200
            cid = r.json()["id"]

            # 8. Generate ad copy
            r = await c.post(f"/api/campaigns/{cid}/generate-ad-copy")
            assert r.status_code == 200
            ad_copy = r.json()
            assert ad_copy["headline"] != ""
            assert ad_copy["primary_copy"] != ""

            # 9. Generate creative brief
            r = await c.post(f"/api/campaigns/{cid}/generate-creative-brief")
            assert r.status_code == 200
            brief = r.json()
            assert brief["visual_concept"] != ""

            # 10. Check campaign readiness
            r = await c.post(f"/api/campaigns/{cid}/check-readiness")
            assert r.status_code == 200
            readiness = r.json()
            assert readiness["validation"]["is_ready"] is True

    asyncio.run(_run())


if __name__ == "__main__":
    test_full_campaign_workflow()
    print("All backend tests passed successfully!")

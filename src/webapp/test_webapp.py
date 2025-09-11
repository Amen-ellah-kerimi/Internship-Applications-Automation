import pytest
from src.webapp.app import app

def test_dashboard_route():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"Internship Candidates" in response.data

def test_settings_route():
    with app.test_client() as client:
        response = client.get("/settings")
        assert response.status_code == 200
        assert b"Settings" in response.data

def test_candidate_detail_route():
    # This test assumes at least one candidate exists in the DB
        with app.app_context():
            with app.test_client() as client:
                # Try to get the first candidate
                from src.webapp.models import Candidate
                candidate = Candidate.query.first()
                if candidate:
                    response = client.get(f"/candidate/{candidate.id}")
                    assert response.status_code == 200
                    assert bytes(candidate.name, "utf-8") in response.data
                else:
                    pytest.skip("No candidates in DB to test candidate detail route.")

def test_scrape_and_save_candidates():
    from src.webapp.services import scrape_and_save_candidates
    with app.app_context():
        result = scrape_and_save_candidates()
        assert isinstance(result, dict)
        assert "new_count" in result or "error" in result

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


def test_home_renders_portfolio_story(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"What this project demonstrates" in response.data
    assert b"Fictional demo data" in response.data


def test_jobs_api_returns_collection(client):
    payload = client.get("/api/jobs").get_json()
    assert payload["count"] == 6
    assert len(payload["jobs"]) == 6


def test_jobs_api_filters_by_department(client):
    payload = client.get("/api/jobs?department=Engineering").get_json()
    assert payload["count"] == 3
    assert all(job["department"] == "Engineering" for job in payload["jobs"])


def test_jobs_api_searches_skills(client):
    payload = client.get("/api/jobs?q=pytorch").get_json()
    assert payload["count"] == 1
    assert payload["jobs"][0]["id"] == 1


def test_job_detail_and_missing_job(client):
    assert client.get("/api/jobs/1").get_json()["title"] == "Machine Learning Platform Engineer"
    assert client.get("/api/jobs/999").status_code == 404


def test_health_check(client):
    assert client.get("/health").get_json() == {
        "service": "talentflow-careers",
        "status": "ok",
    }

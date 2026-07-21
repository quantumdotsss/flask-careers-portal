"""TalentFlow careers portal.

A small Flask application that demonstrates server-rendered UI composition
and a filterable JSON API. All job listings are fictional demo data.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime

from flask import Flask, abort, jsonify, render_template, request


JOBS = (
    {
        "id": 1,
        "title": "Machine Learning Platform Engineer",
        "department": "Engineering",
        "location": "San Francisco, CA · Hybrid",
        "employment_type": "Full-time",
        "salary": "$165K–$210K",
        "summary": "Build reliable training and inference infrastructure for applied AI teams.",
        "skills": ["Python", "PyTorch", "Kubernetes"],
    },
    {
        "id": 2,
        "title": "Applied AI Product Engineer",
        "department": "Product Engineering",
        "location": "Remote · United States",
        "employment_type": "Full-time",
        "salary": "$150K–$195K",
        "summary": "Turn language-model prototypes into secure, measurable product workflows.",
        "skills": ["LLMs", "Flask", "Evaluation"],
    },
    {
        "id": 3,
        "title": "Data Scientist",
        "department": "Data",
        "location": "Irvine, CA · Hybrid",
        "employment_type": "Full-time",
        "salary": "$140K–$180K",
        "summary": "Design experiments and decision systems from product and operational data.",
        "skills": ["Python", "SQL", "Experimentation"],
    },
    {
        "id": 4,
        "title": "Frontend Engineer",
        "department": "Engineering",
        "location": "Remote · Americas",
        "employment_type": "Full-time",
        "salary": "$135K–$175K",
        "summary": "Create accessible interfaces for complex data and AI-assisted experiences.",
        "skills": ["TypeScript", "Accessibility", "Design Systems"],
    },
    {
        "id": 5,
        "title": "Technical Program Manager",
        "department": "Operations",
        "location": "Seattle, WA · Hybrid",
        "employment_type": "Full-time",
        "salary": "$145K–$185K",
        "summary": "Coordinate cross-functional delivery across platform, product, and research.",
        "skills": ["Program Strategy", "Risk", "Communication"],
    },
    {
        "id": 6,
        "title": "Software Engineering Intern",
        "department": "Engineering",
        "location": "San Francisco, CA · On-site",
        "employment_type": "Internship",
        "salary": "$42–$52 / hour",
        "summary": "Ship a scoped product feature with mentorship from an experienced engineer.",
        "skills": ["Python", "Web APIs", "Testing"],
    },
)


def _matches(value: str, query: str) -> bool:
    return query.casefold() in value.casefold()


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def home():
        return render_template(
            "home.html",
            jobs=JOBS,
            departments=sorted({job["department"] for job in JOBS}),
            current_year=datetime.now(UTC).year,
        )

    @app.get("/api/jobs")
    def list_jobs():
        department = request.args.get("department", "").strip()
        location = request.args.get("location", "").strip()
        query = request.args.get("q", "").strip()

        jobs = list(JOBS)
        if department:
            jobs = [job for job in jobs if job["department"].casefold() == department.casefold()]
        if location:
            jobs = [job for job in jobs if _matches(job["location"], location)]
        if query:
            searchable_fields = ("title", "department", "location", "summary")
            jobs = [
                job
                for job in jobs
                if any(_matches(str(job[field]), query) for field in searchable_fields)
                or any(_matches(skill, query) for skill in job["skills"])
            ]

        return jsonify({"count": len(jobs), "jobs": jobs})

    @app.get("/api/jobs/<int:job_id>")
    def job_detail(job_id: int):
        job = next((job for job in JOBS if job["id"] == job_id), None)
        if job is None:
            abort(404, description="Job not found")
        return jsonify(job)

    @app.get("/health")
    def health():
        return jsonify({"service": "talentflow-careers", "status": "ok"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )

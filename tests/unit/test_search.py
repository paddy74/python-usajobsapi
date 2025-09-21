import pytest

from usajobsapi.endpoints.search import HiringPath, SearchEndpoint


class TestSearchEndpointParams:
    def test_to_params_serialization(self):
        data = {
            "keyword": "developer",
            "location_names": ["City, ST", "Town, ST2"],
            "radius": 25,
            "relocation": True,
            "job_category_codes": ["001", "002"],
            "hiring_paths": [HiringPath.PUBLIC, HiringPath.VET],
        }
        params = SearchEndpoint.Params.model_validate(data)
        assert params.to_params() == {
            "Keyword": "developer",
            "LocationName": "City, ST;Town, ST2",
            "Radius": "25",
            "RelocationIndicator": "True",
            "JobCategoryCode": "001;002",
            "HiringPath": "public;vet",
        }

    def test_radius_requires_location(self):
        with pytest.raises(ValueError):
            SearchEndpoint.Params.model_validate({"radius": 10})

    def test_remuneration_max_less_than_min(self):
        with pytest.raises(ValueError):
            SearchEndpoint.Params.model_validate(
                {"remuneration_min": 100, "remuneration_max": 50}
            )


class TestSearchEndpointResponses:
    def test_job_summary_parses_nested_fields(self, job_summary_payload):
        summary = SearchEndpoint.JobSummary.model_validate(job_summary_payload)

        assert summary.position_id == "24-123456"
        assert summary.position_uri == "https://example.com/job/1"
        assert summary.apply_uri == ["https://example.com/apply/1"]
        assert (
            summary.department_name == "National Aeronautics and Space Administration"
        )
        assert summary.locations_display == "Houston, TX"

        assert len(summary.locations) == 1
        location = summary.locations[0]
        assert location.city_name == "Houston"
        assert location.state_code == "TX"
        assert location.latitude == pytest.approx(29.7604)
        assert location.longitude == pytest.approx(-95.3698)

        assert summary.job_categories[0].code == "0801"
        assert summary.job_grades[0].current_grade == "12"
        assert summary.position_schedules[0].name == "Full-time"
        assert summary.position_offerings[0].code == "15317"

        assert summary.salary_range() == (50000.0, 100000.0)
        assert summary.hiring_paths() == ["public", "vet"]
        assert summary.summary() == "Design and build spacecraft components."

        assert summary.user_area
        assert summary.user_area.details
        assert summary.user_area.details.who_may_apply
        assert summary.user_area.details.who_may_apply.name == "Open to the public"

    def test_search_result_jobs_parsing(self, search_result_item):
        items = [
            search_result_item,
            {"MatchedObjectId": "2", "PositionTitle": "Analyst"},
            {"MatchedObjectDescriptor": {"MatchedObjectId": "3"}},  # invalid
        ]
        search_result = SearchEndpoint.SearchResult.model_validate(
            {
                "SearchResultCount": 3,
                "SearchResultCountAll": 3,
                "SearchResultItems": items,
            }
        )
        jobs = search_result.jobs()
        assert len(jobs) == 2
        assert jobs[0].id == "1"
        assert jobs[1].id == "2"

    def test_response_model_parsing(self, search_result_item):
        response = SearchEndpoint.Response.model_validate(
            {
                "LanguageCode": "EN",
                "SearchParameters": {
                    "keyword": "python",
                    "location_names": ["Anywhere"],
                },
                "SearchResult": {
                    "SearchResultCount": 1,
                    "SearchResultCountAll": 1,
                    "SearchResultItems": [search_result_item],
                },
            }
        )
        assert response.language == "EN"
        assert response.params is not None
        assert response.params.keyword == "python"
        assert response.search_result is not None
        jobs = response.search_result.jobs()
        assert jobs[0].id == "1"

    def test_response_jobs_helper(self, search_result_item):
        response = SearchEndpoint.Response.model_validate(
            {
                "SearchResult": {
                    "SearchResultCount": 1,
                    "SearchResultCountAll": 1,
                    "SearchResultItems": [search_result_item],
                }
            }
        )
        jobs = response.jobs()
        assert len(jobs) == 1
        assert jobs[0].id == "1"

        empty_response = SearchEndpoint.Response.model_validate({})
        assert empty_response.jobs() == []

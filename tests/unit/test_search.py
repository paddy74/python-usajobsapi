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

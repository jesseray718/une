"""Pytest fixtures + mocking examples."""
import json, pytest
from unittest.mock import mock_open

@pytest.fixture
def sample_result():
    return {"eta": 33.3, "volume_m3": 55, "person_hours": 1.2}

@pytest.fixture
def mock_file(mocker, sample_result):
    fake_json = json.dumps(sample_result)
    return mocker.patch("builtins.open", mock_open(read_data=fake_json))

def test_load_result_with_fixture(mock_file, sample_result):
    with open("fake.json") as f:
        data = json.load(f)
    assert data["eta"] == sample_result["eta"]
    mock_file.assert_called_once()

def test_save_result(mocker, sample_result):
    mocked_open = mocker.patch("builtins.open", mock_open())
    with open("out.json", "w") as f:
        json.dump(sample_result, f)
    mocked_open.assert_called_once_with("out.json", "w")

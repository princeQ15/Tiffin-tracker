import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
from surprise_travel.main import run, train, SurpriseTravel

def test_surprise_travel_init():
    """Test initialization of SurpriseTravel class."""
    planner = SurpriseTravel()
    assert isinstance(planner.preferences, dict)
    assert isinstance(planner.destinations, list)

def test_set_preferences():
    """Test setting travel preferences."""
    planner = SurpriseTravel()
    test_prefs = {"climate": "warm", "budget": "medium"}
    planner.set_preferences(**test_prefs)
    assert planner.preferences == test_prefs

def test_load_destinations(tmp_path):
    """Test loading destinations from a JSON file."""
    # Create a temporary directory and file
    test_data = [
        {"name": "Test Destination", "climate": "test", "budget": "test"}
    ]
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    data_file = data_dir / "destinations.json"
    data_file.write_text(json.dumps(test_data), encoding='utf-8')
    
    # Create a mock for Path
    with patch('surprise_travel.main.Path') as mock_path:
        # Set up the mock to return our test file path
        mock_path.return_value.parent = tmp_path
        mock_path.return_value.__truediv__.side_effect = lambda x: tmp_path / x
        
        planner = SurpriseTravel()
        assert len(planner.destinations) == 1
        assert planner.destinations[0]["name"] == "Test Destination"

def test_get_suggestions():
    """Test getting travel suggestions."""
    planner = SurpriseTravel()
    planner.destinations = [
        {"name": "Test1", "climate": "warm", "budget": "medium"},
        {"name": "Test2", "climate": "cold", "budget": "high"}
    ]
    
    # Test with matching preferences
    planner.set_preferences(climate="warm")
    suggestions = planner.get_suggestions()
    assert len(suggestions) == 1
    assert suggestions[0]["name"] == "Test1"
    
    # Test with no matches
    planner.set_preferences(climate="arctic")
    suggestions = planner.get_suggestions()
    assert len(suggestions) == 0

def test_run(capsys):
    """Test the run function."""
    with patch('surprise_travel.main.SurpriseTravel') as mock_planner:
        mock_instance = mock_planner.return_value
        mock_instance.get_suggestions.return_value = [
            {"name": "Test", "climate": "test", "budget": "test", "activities": ["test"]}
        ]
        run()
        captured = capsys.readouterr()
        assert "Welcome to Surprise Travel! 🚀" in captured.out
        assert "Here are some travel suggestions" in captured.out

def test_train(capsys, tmp_path):
    """Test the train function."""
    # Create a mock for Path
    with patch('surprise_travel.main.Path') as mock_path:
        # Setup mock for data directory
        mock_path.return_value.parent = tmp_path
        mock_path.return_value.__truediv__.side_effect = lambda x: tmp_path / x
        
        # Call the train function
        train()
        
        # Verify output
        captured = capsys.readouterr()
        assert "Training the surprise travel model" in captured.out
        
        # Verify file was created
        data_file = tmp_path / "data" / "destinations.json"
        assert data_file.exists()
        
        # Verify file content
        with open(data_file, 'r', encoding='utf-8') as f:
            destinations = json.load(f)
            assert len(destinations) > 0
            assert "name" in destinations[0]
            assert "climate" in destinations[0]

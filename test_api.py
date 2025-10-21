from fastapi.testclient import TestClient
from main import app
from fastapi import status
import pytest


client= TestClient(app=app)


def test_getdata():
    response = client.get("/data")
    assert response.status_code==status.HTTP_200_OK
    
def test_get_posts_is_list():
    response = client.get("/data")
    assert isinstance(response.json(), list) 

def test_post_response_structure():
    response = client.get("/data")
    data = response.json()

    if data:
        post = data[0]
        print("Returned keys:", post.keys())
        expected_keys = {"id", "datetime", "open", "high", "low", "close", "volume"}
        assert set(post.keys()) == expected_keys

        # field type
        assert isinstance(post["id"], int)
        assert isinstance(post["datetime"], str)
        
        # casting string to float 
        for key in ["open", "high", "low", "close"]:
            try:
                value = float(post[key])
            except ValueError:
                pytest.fail(f"Field {key} is not a number: {post[key]}")
        
        assert isinstance(post["volume"], int)
    else:
        pytest.skip("No data returned from API — skipping structure test")


def test_create_post():
    payload = {
        "open": 221.0,
        "high": 226.05,
        "low": 221.0,
        "close": 223.5,
        "volume": 5074920
    }

    response = client.post("/data", json=payload)
    assert response.status_code == 201

    data = response.json()

    # response keys
    expected_keys = {"id", "datetime", "open", "high", "low", "close", "volume"}
    assert set(data.keys()) == expected_keys

    #type check
    assert isinstance(data["id"], int)
    assert isinstance(data["datetime"], str)  # ISO datetime string

    for key in ["open", "high", "low", "close"]:
        assert isinstance(data[key], float)

    assert isinstance(data["volume"], int)

    #value checks
    assert data["open"] == 221.0
    assert data["high"] == 226.05
    assert data["low"] == 221.0
    assert data["close"] == 223.5
    assert data["volume"] == 5074920

    # datetime format 
    from datetime import datetime
    datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))  # should not raise error



        
def test_strategy_performance_structure():
    response = client.get("/strategy/performance")
    assert response.status_code == 200
    
    data = response.json()
    
    # keys
    assert "strategy" in data
    assert "performance" in data
    
    # name
    assert data["strategy"] == "Moving Average Crossover"
    
    #performance structure
    performance = data["performance"]
    expected_keys = {"cumulative_return", "total_trades", "win_rate"}
    assert set(performance.keys()) == expected_keys
    
    # types
    assert isinstance(performance["cumulative_return"], (float, int))
    assert isinstance(performance["total_trades"], int)
    assert isinstance(performance["win_rate"], (float, int))
    
    #values are reasonable
    assert -200 <= performance["cumulative_return"] <= 10000  # arbitrary sanity check
    assert performance["total_trades"] >= 0
    assert 0 <= performance["win_rate"] <= 100

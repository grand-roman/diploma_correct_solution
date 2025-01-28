import unittest
import pytest


@pytest.mark.parametrize("user_data", [{"name": "test", "api_key": "test"}, {"name": "test2", "api_key": "test2"}])
def test_1_add_users(client, user_data):
    response = client.post("/users/add", json=user_data)
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_2_get_current_user(client):
    response = client.get("/api/users/me", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_3_get_user_by_id(client):
    response = client.get("/api/users/2", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_4_follow(client):
    response = client.post("/api/users/2/follow", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_5_get_current_user_with_following(client):
    response = client.get("/api/users/me", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True
    assert len(json.get('user').get('following')) is 1


def test_6_remove_follow(client):
    response = client.delete("/api/users/2/follow", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_7_get_current_user_with_following(client):
    response = client.get("/api/users/me", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True
    assert len(json.get('user').get('following')) is 0


def test_8_add_tweet(client):
    tweet_data = {"tweet_data": "data", "tweet_media_ids": []}
    response = client.post("/api/tweets", json=tweet_data, headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_9_get_tweets(client):
    response = client.get("/api/tweets", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True
    assert len(json.get('tweets')) is 1


def test_10_add_like(client):
    response = client.post("/api/tweets/1/likes", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_11_remove_like(client):
    response = client.delete("/api/tweets/1/likes", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


def test_12_remove_tweet(client):
    response = client.delete("/api/tweets/1", headers={"Api-Key": "test"})
    json = response.json()

    assert response.status_code == 200
    assert json.get('result') is True


if __name__ == '__main__':
    unittest.main()

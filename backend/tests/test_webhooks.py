def test_webhook_post_and_get(client, db_session):
    # Send webhook
    payload = {"tracking_id": "TEST123", "status": "in_transit", "location": "Lagos"}
    response = client.post("/webhooks/sendbox", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["tracking_id"] == "TEST123"

    # Fetch webhook events
    response = client.get("/webhooks/TEST123")
    assert response.status_code == 200
    events = response.json()
    assert len(events) > 0
    assert events[0]["tracking_id"] == "TEST123"

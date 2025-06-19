from unittest.mock import patch
import pytest
from fastapi import status
from urllib.parse import unquote
import re

import httpx

BASE_URL = "/api/v1/oauth"

fake_user_data = dict(
    email="johndoe@helloworld.com",
    username="johndoe",
    last_name="doe",
    first_name="john",
    password="string123",
)

login_data = dict(email="johndoe@helloworld.com", password="string123")


# Test successful user signup and email verification flow
@patch("app.auth.service.send_email.delay")
@pytest.mark.asyncio
async def test_signup(mock_send_email, async_client):
    # Mock the email sending function to prevent actual emails from being sent
    mock_send_email.return_value = None

    # Step 1: Test user signup endpoint
    # Send POST request to signup endpoint with fake user data
    response = await async_client.post(f"{BASE_URL}/signup", json=fake_user_data)

    # Verify signup was successful
    assert response.status_code == 201
    assert (
        response.json().get("message")
        == "Account created! Check email to verify your email"
    )

    # Step 2: Extract verification email content from the mock
    # Get the HTML content that would have been sent in the verification email
    html_content = mock_send_email.call_args[0][2]

    # Step 3: Extract verification token from the email content
    # Use regex to find the verification token in the email's verification link
    match = re.search(r'href="[^"]+/verify/([^"]+)"', html_content)
    token = match.group(1)
    assert token is not None

    # Step 4: Test email verification endpoint
    # Call the verification endpoint with the extracted token
    verify_response = await async_client.get(f"{BASE_URL}/verify/{token}")
    assert verify_response.status_code == 200
    assert verify_response.json()["message"] == "Account verified successfully"


# @patch("app.main.auth.user_service")
@pytest.mark.asyncio
async def test_login_and_get_me(async_client):
    response = await async_client.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("token_type") == "bearer"

    access_token = response.json().get("access_token")

    response = await async_client.get(
        f"{BASE_URL}/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == status.HTTP_200_OK

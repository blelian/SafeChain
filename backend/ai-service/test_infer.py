# backend/ai-service/test_infer.py
import requests

API_BASE = "http://localhost:8000/api"
EMAIL = "testuser@example.com"   # Change if you want a different test user
PASSWORD = "Password123"         # Change if needed

def get_token(email: str, password: str) -> str:
    """Try login, if fails then register, then login again."""
    # Attempt login
    login_resp = requests.post(f"{API_BASE}/auth/login", json={"email": email, "password": password})
    if login_resp.ok:
        return login_resp.json()["access_token"]

    # If login failed, attempt registration
    print("Login failed, trying to register user...")
    reg_resp = requests.post(f"{API_BASE}/auth/register", json={"email": email, "password": password})
    if not reg_resp.ok:
        raise RuntimeError(f"Failed to register user: {reg_resp.text}")

    # Login after registration
    login_resp = requests.post(f"{API_BASE}/auth/login", json={"email": email, "password": password})
    if not login_resp.ok:
        raise RuntimeError(f"Login failed after registration: {login_resp.text}")

    return login_resp.json()["access_token"]

def run_inference(token: str, input_list: list[float]):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"input": input_list}
    resp = requests.post(f"{API_BASE}/infer/", json=payload, headers=headers)  # note the trailing '/'
    if resp.ok:
        print("✅ Inference result:", resp.json())
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    token = get_token(EMAIL, PASSWORD)
    print("✅ Token acquired!")

    # Example input for inference
    test_input = [1.0, 2.0, 3.0]
    run_inference(token, test_input)

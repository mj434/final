"""This test the homepage"""

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200

def set_admin(client):
    response = client.post("/register", data={"email": "mj434@njit.edu", "password": "12345678", "confirm": "12345678"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    response = client.get("/confirm/1")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    response = client.post("/login", data={"email": "mj434@njit.edu", "password": "12345678"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]

def test_register(client):
    assert client.get("/register").status_code == 200
    response = client.post("/register", data={"email": "test@example.com", "password": "abcdef", "confirm": "abcdef"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_login_without_confirm(client):
    assert client.get("/login").status_code == 200
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_login_bad_username(client):
    response = client.post("/login", data={"email": "test1@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_login_bad_password(client):
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdefgh"})
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]


def test_confirm(client):
    response = client.get("/confirm/2")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_login(client):
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]

def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_new_user_not_admin(client):
    client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b'User Management' not in response.data
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_user_admin(client):
    response = client.post("/login", data={"email": "mj434@njit.edu", "password": "12345678"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert b'User Management' in response.data
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]


def test_edit_user_admin(client):
    response = client.post("/login", data={"email": "mj434@njit.edu", "password": "12345678"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/users/2/edit")
    assert response.status_code == 200
    response = client.post("/users/2/edit", data={"about":"test user about edit"})
    assert response.status_code == 302
    assert "/users" == response.headers["Location"]
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_view_user_admin(client):
    response = client.post("/login", data={"email": "mj434@njit.edu", "password": "12345678"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/users/2")
    assert response.status_code == 200
    assert b'test user about edit' in response.data
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_make_admin(client):
    response = client.post("/login", data={"email": "mj434@njit.edu", "password": "12345678"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/users/2/edit")
    assert response.status_code == 200
    response = client.post("/users/2/edit", data={"is_admin": True})
    assert response.status_code == 302
    assert "/users" == response.headers["Location"]
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]


def test_manage_profile(client):
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/profile")
    assert response.status_code == 200
    assert b'test user about edit' in response.data
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]


def test_manage_account(client):
    response = client.post("/login", data={"email": "test@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/account")
    assert response.status_code == 200
    assert b'Manage Account' in response.data
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]

def test_add_new_user(client):
    response = client.post("/login", data={"email": "mj434@njit.edu", "password": "12345678"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/users/new")
    assert response.status_code == 200
    response = client.post("/users/new", data={"email": "test01@example.com", "password": "abcdef", "confirm": "abcdef"})
    assert response.status_code == 302
    assert "/users" == response.headers["Location"]
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    response = client.get("/confirm/3")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
    response = client.post("/login", data={"email": "test01@example.com", "password": "abcdef"})
    assert response.status_code == 302
    assert "/dashboard" == response.headers["Location"]
    response = client.get("/logout")
    assert response.status_code == 302
    assert "/login" == response.headers["Location"]
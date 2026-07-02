from auth import get_current_user, login_user, logout_user


def test_login_and_logout_flow():
    logout_user()
    login_user("Alice")
    assert get_current_user() == "Alice"
    logout_user()
    assert get_current_user() is None

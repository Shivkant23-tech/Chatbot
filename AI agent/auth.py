from flask import session


def login_user(username: str) -> None:
    session["username"] = username.strip()


def logout_user() -> None:
    session.pop("username", None)


def get_current_user() -> str | None:
    return session.get("username")

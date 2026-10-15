from sqlalchemy import select

from app.db import SessionLocal
from app.models import User
from app.security import hash_password


def main():
    db = SessionLocal()
    try:
        defaults = [
            ("viewer", "viewer123", "viewer"),
            ("operator", "operator123", "operator"),
            ("admin", "admin123", "admin"),
        ]
        for username, password, role in defaults:
            if db.scalar(select(User).where(User.username == username)) is None:
                db.add(User(username=username, hashed_password=hash_password(password), role=role))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()

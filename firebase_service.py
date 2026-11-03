import os
from pathlib import Path

from app_config import DEFAULT_CREDENTIALS_FILE


def connect_firebase():
    """Initialize Firebase Admin and return a Firestore client and module."""
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as error:
        raise RuntimeError(
            "Firebase support is not installed. Run "
            "pip install -r requirements.txt and try again."
        ) from error

    credentials_file = Path(
        os.environ.get("FIREBASE_CREDENTIALS", DEFAULT_CREDENTIALS_FILE)
    )
    if not credentials_file.exists():
        raise FileNotFoundError(
            "Firebase service-account credentials were not found. "
            f"Add {DEFAULT_CREDENTIALS_FILE.name} beside this app or set "
            "the FIREBASE_CREDENTIALS environment variable."
        )
    if not firebase_admin._apps:
        firebase_admin.initialize_app(credentials.Certificate(str(credentials_file)))
    return firestore.client(), firestore

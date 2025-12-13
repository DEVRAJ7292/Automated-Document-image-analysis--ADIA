from adia.core.config import get_settings
from adia.core.config import Settings


def get_app_settings() -> Settings:
    """
    Dependency that provides application settings.

    This allows:
    - Easy overrides in tests
    - Clean separation from global state
    """
    return get_settings()

from uuid import uuid4


def get_identifier() -> str:
    """Get a unique identifier.

    Returns:
        str: The unique identifier.

    """
    return str(uuid4()).replace("-", "")

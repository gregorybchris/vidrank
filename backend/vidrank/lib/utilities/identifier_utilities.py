from uuid import uuid4


def get_identifier() -> str:
    return str(uuid4()).replace("-", "")

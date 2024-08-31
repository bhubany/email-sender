import os


def get_environment_variable_or_default(key: str, default=None):
    if key in os.environ:
        return os.environ[key]
    else:
        return default

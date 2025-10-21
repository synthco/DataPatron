
class LoadpipeError(Exception):
    """Базовий виняток пакета."""

class AuthError(LoadpipeError):
    pass

class ConfigError(LoadpipeError):
    pass

class RateLimitError(LoadpipeError):
    pass

class ResumeMismatchError(LoadpipeError):
    pass

class IntegrityError(LoadpipeError):
    pass

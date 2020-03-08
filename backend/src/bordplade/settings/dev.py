from ._base import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
def _load_secret_key() -> str:
    import warnings

    try:
        secret_key = os.environ['DJANGO_SECRET_KEY']
    except KeyError:
        warnings.warn("DJANGO_SECRET_KEY not set in environment. Please make sure to provide a secret key!")
        secret_key = ""

    if secret_key:
        return secret_key
    else:
        from random import choice
        from string import ascii_letters
        secret_key = "".join(choice(ascii_letters) for __ in range(32))
        warnings.warn(f"Generated temporary secret key: '{secret_key}'."
                      f" Please make sure to persist it if you want to continue using security-sensitive data.")
        return secret_key

SECRET_KEY = _load_secret_key()

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

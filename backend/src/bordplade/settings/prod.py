from ._base import *

def _load_secret_key() -> str:
    key_file: Path = (
        SRC_PATH
            .parent  # backend directory
            .parent  # repository root directory
    ) / ".django_secret"
    key_text = key_file.read_text(encoding="utf-8").strip()

    if key_text == "":
        raise ValueError(f"The secret key file <{key_file}> does not contain a valid key."
                         f" Please make sure that the file exists and contains a key!")
    return key_text

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

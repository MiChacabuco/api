from django.core.exceptions import ValidationError
from django.core.files import File


def validate_file_size_limit(mb_limit: int):
    def validate(file: File):
        mb_size = file.size / 1024 / 1024  # Convert to megabytes
        if mb_size > mb_limit:
            raise ValidationError(f"El archivo no debe pesar más de {mb_limit} MB")

    return validate

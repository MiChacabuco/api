from django.core.files import File


def validate_image_size(mb_limit: int):
    mb_limit = 5  # 5MB
    mb_size = file.size / 1024 / 1024  # Convert to megabytes
    if mb_size > mb_limit:
        raise ValidationError(f"El archivo no debe pesar más de {mb_limit} MB")

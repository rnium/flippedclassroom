from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from PIL import Image
from io import BytesIO
def compress_image(image):
    image_validator = FileExtensionValidator(allowed_extensions=settings.ALLOWED_IMAGE_EXTENSIONS)
    try:
        image_validator(image)
    except ValidationError:
        raise ValidationError("File Extension Not Allowed")
    img = Image.open(image)
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=50)
    img_file = ContentFile(img_io.getvalue())

    if hasattr(image, 'name') and image.name:
        img_file.name = image.name

    if hasattr(image, 'content_type') and image.content_type:
        img_file.content_type = image.content_type

    if hasattr(image, 'size') and image.size:
        img_file.size = image.size

    if hasattr(image, 'charset') and image.charset:
        img_file.charset = image.charset

    if hasattr(image, '_committed') and image._committed:
        img_file._committed = image._committed

    return img_file
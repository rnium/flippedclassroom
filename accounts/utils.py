from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from pathlib import Path
from PIL import Image
from io import BytesIO

def validate_image_extension(value):
    valid_extensions = settings.ALLOWED_IMAGE_EXTENSIONS
    ext = Path(value.name).suffix
    if not ext.lower() in valid_extensions:
        raise ValidationError('Invalid file type. Allowed file types are: {}'.format(', '.join(valid_extensions)))

# this utility will check mendatory User object filed
def check_user_data(user_data:dict):
    try:
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        username = user_data['username']
        email = user_data['email']
    except:
        raise ValidationError('Some user info not provided')
    len_truths = [bool(len(info)) for info in [first_name, last_name, username, email]]
    if not all(len_truths):
        raise ValidationError('Some user fields left empty')

# this utility will check mendatory Account object filed
def check_account_data(ac_data:dict, request=None):
    checking_fields = []
    try:
        institution = ac_data['institution']
        checking_fields.append(institution)
        if request:
            if request.user.account.is_student:
                institutional_id = ac_data['institutional_id']
                checking_fields.append(institutional_id)
    except:
        raise ValidationError('Some account info not provided')
    len_truths = [bool(len(info)) for info in checking_fields]
    if not all(len_truths):
        raise ValidationError('Some account fields left empty')

def compress_image(image):
    try:
        validate_image_extension(image)
    except ValidationError:
        raise ValidationError("Invalid image file")
    img = Image.open(image)
    img_format = img.format.lower()
    img_io = BytesIO()
    img.save(img_io, format=img_format, quality=50)
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
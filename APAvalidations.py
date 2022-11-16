"""
validationg models fiels
"""

from django.core.exceptions import ValidationError
import re


def validate_name(Name):
    if not re.match("[\u0600-\u06FF\uFB8A\u067E\u0686\u06AF\u200C\u200F ]{3,70}", Name):
        raise ValidationError("فقط حروف فارسی وارد کنید")


def validate_filesize(file):
    file_size = file.file.size
    limit_mb = 10
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("حداکثر حجم {}"
                              "MB می باشد".format(limit_mb))

def validate_image(ImageField):
    file_size = ImageField.file.size
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("حداکثر حجم عکس {}"
                              "MB می باشد".format(limit_mb))


def validate_file(FileField):
    file_size = FileField.file.size
    limit_mb = 20
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("حداکثر حجم فایل {}"
                              "MB می باشد".format(limit_mb))


def validate_date(DateField):
    if not re.match("([1][234]\d{2}/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01]))", str(DateField)):
        raise ValidationError("تاریخ معتبر وارد کنید")


def is_valid_iran_code(nationalCode):
    nationalCode = str(nationalCode)
    if not re.search(r'^\d{10}$', nationalCode):
        raise ValidationError("تعداد ارقام کد ملی 10 عدد می باشد")
    check = int(nationalCode[9])
    s = sum(int(nationalCode[x]) * (10 - x) for x in range(9)) % 11
    if s < 2:
        if not check == s:
            raise ValidationError("کد ملی معتبر وارد کنید")
    else:
        if not check + s == 11:
            raise ValidationError("کد ملی معتبر وارد کنید")
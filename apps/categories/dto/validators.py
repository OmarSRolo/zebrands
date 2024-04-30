import string

from django.core.validators import RegexValidator

NoSpecialCharacter = RegexValidator(r'[' + string.punctuation + ']', "Your string contains no valid character.")

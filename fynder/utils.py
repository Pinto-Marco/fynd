import random
import string
from django.conf import settings



def generate_unique_code():
    """Genera un codice a 6 cifre che non è già presente nel database."""
    from .models import TemporaryCode
    while True:
        code = "".join(random.choices(string.digits, k=6))
        if not TemporaryCode.objects.filter(code=code).exists():
            return code
        
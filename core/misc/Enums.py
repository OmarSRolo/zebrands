from django.db import models
from django.utils.translation import gettext_lazy as _


# REQUESTS

class REQUESTS_STATUS(models.TextChoices):
    PREPAGO = 'prepago', _('prepago')
    BORRADOR = 'borrador', _('borrador')
    SOLICITADO = 'solicitado', _('solicitado')
    CERRADO = 'cerrado', _('cerrado')
    CANCELADO = 'cancelado', _('cancelado')
    INVALIDADO = 'invalidado', _('invalidado')
    TERMINADO = 'terminado', _('terminado')

"""
ASGI config for leaky_ledger_bank_and_company project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "leaky_ledger_bank_and_company.settings"
)

application = get_asgi_application()

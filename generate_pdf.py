from chrome import Chrome
import os
from django.conf import settings
import django


BASE_DIR = os.path.abspath("")

SETTINGS = {
    "BASE_DIR": BASE_DIR,
    "MEDIA_ROOT": f"{BASE_DIR}/static",
    "STATIC_ROOT": f"{BASE_DIR}/static",
    "STATIC_URL":  "/static/compiled/",
    "CHROME_BINARY": "chromium-browser", # chromium binary path
    "TEMPLATES": [
        {
            "DIRS": [os.path.join(BASE_DIR, "templates"),],
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        }
    ],
}

context = {
    "assets": {
        "count": 5,
    },
    "company": {
        "name": "Flughafen Bern AG",
    },
    "assembly": {
        "name": "Generalversammlung der Flughafen Bern AG",
        "date": "4 Aug 2020",
        "address": "GV Flughafen Bern AG"
    },
    "shareholder": {
        "get_full_name": "Rudy Fasel Sarl",
        "get_stacked_address": "Rue Pontmurre 14",
    },
    "coupon_count": 15
}

settings.configure(**SETTINGS)

django.setup()

p = Chrome()

pdf = p.render_template("admission_card.pdf.html", context)

pdf_file = open("admission_card.pdf", 'wb')

pdf_file.write(pdf)
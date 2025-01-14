#!/bin/bash
OIDC_RSA_PRIVATE_KEY=$(<oidc.key)
export OIDC_RSA_PRIVATE_KEY

concurrently \
    --names "django,vite,tailwindcss" \
    --prefix-colors "green.bold,yellow.bold,blue.bold" \
    --kill-others \
    "python manage.py runserver_plus --cert-file cert.crt" \
    "(cd vite && npm run build -- --watch)" \
    "npx tailwindcss -i ./accounts/static/css/input.css -o ./accounts/static/css/output.css --watch"

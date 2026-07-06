#!/usr/bin/env bash
# Helper: generate JWT secret and Fernet key for Replit Secrets
echo "JWT_SECRET=$(python3 -c "import secrets;print(secrets.token_urlsafe(48))")"
echo "ENCRYPTION_KEY=$(python3 -c "from cryptography.fernet import Fernet;print(Fernet.generate_key().decode())")"

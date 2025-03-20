#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p app/static/images/equipment app/static/images/qrcodes

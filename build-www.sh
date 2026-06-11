#!/bin/bash
# Build the www/ directory for Tauri frontendDist
set -e
cd "$(dirname "$0")"

# Clean and recreate www/
rm -rf www
mkdir -p www/js/vendor www/css

# Copy frontend assets
cp index.html www/
cp -r js/*.js www/js/
cp -r js/vendor/*.js www/js/vendor/
cp -r css/*.css www/css/

# Generate data bundle
python3 bundle_data.py

echo "www/ ready"

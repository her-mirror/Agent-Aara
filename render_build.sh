#!/bin/bash

set -e  # Exit on any error

echo "🔧 Render Build Script for Ara Health Agent"
echo "==========================================="

# Update system packages
echo "📦 Updating system packages..."
apt-get update

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get install -y build-essential curl

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "✅ Build completed successfully!" 
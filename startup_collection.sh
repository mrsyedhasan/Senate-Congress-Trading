#!/bin/bash

# Startup data collection script
# Run this when your computer starts to collect any missed data

SCRIPT_DIR="/Users/syed/Home App/Senate-Congress-Trading/backend"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"
COLLECTION_SCRIPT="$SCRIPT_DIR/scheduled_collection.py"

echo "🔄 Running startup data collection..."
echo "Checking for missed data since last collection..."

# Run the collection script
cd "$SCRIPT_DIR"
source venv/bin/activate
python scheduled_collection.py

echo "✅ Startup collection completed"
echo "📊 Your dashboard now has the latest data"

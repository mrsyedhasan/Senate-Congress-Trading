#!/bin/bash

# Setup cron job for automatic data collection
# This script sets up a cron job to collect data daily

SCRIPT_DIR="/Users/syed/Home App/Senate-Congress-Trading/backend"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"
COLLECTION_SCRIPT="$SCRIPT_DIR/scheduled_collection.py"

echo "Setting up automatic data collection..."
echo "Script directory: $SCRIPT_DIR"
echo "Python path: $PYTHON_PATH"
echo "Collection script: $COLLECTION_SCRIPT"

# Create cron job entry (runs daily at 6 AM)
CRON_ENTRY="0 6 * * * cd $SCRIPT_DIR && $PYTHON_PATH $COLLECTION_SCRIPT >> $SCRIPT_DIR/data_collection.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

echo "Cron job added successfully!"
echo "Data will be collected daily at 6:00 AM"
echo "Logs will be saved to: $SCRIPT_DIR/data_collection.log"

# Show current crontab
echo "Current crontab:"
crontab -l

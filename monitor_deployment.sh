#!/bin/bash

# Resumaker Deployment Monitor
# Continuously checks backend health and reports status

BACKEND_URL="https://resumaker-backend-production.up.railway.app"
MAX_ATTEMPTS=60
SLEEP_INTERVAL=10

echo "=========================================="
echo "🔍 RESUMAKER DEPLOYMENT MONITOR"
echo "=========================================="
echo "Backend URL: $BACKEND_URL"
echo "Max attempts: $MAX_ATTEMPTS"
echo "Check interval: ${SLEEP_INTERVAL}s"
echo ""

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
    attempt=$((attempt + 1))
    echo "[$attempt/$MAX_ATTEMPTS] Testing backend..."

    # Try health endpoint
    response=$(curl -s --connect-timeout 5 --max-time 10 "$BACKEND_URL/health" 2>&1)

    if echo "$response" | grep -q "healthy\|status"; then
        echo "✅ SUCCESS! Backend is responding!"
        echo ""
        echo "Response:"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
        echo ""
        echo "=========================================="
        echo "🎉 DEPLOYMENT SUCCESSFUL!"
        echo "=========================================="
        echo "Backend URL: $BACKEND_URL"
        echo "Health Check: $BACKEND_URL/health"
        echo "API Docs: $BACKEND_URL/docs"
        exit 0
    else
        echo "⏳ Not ready yet..."
        if [ $attempt -lt $MAX_ATTEMPTS ]; then
            sleep $SLEEP_INTERVAL
        fi
    fi
done

echo ""
echo "=========================================="
echo "❌ DEPLOYMENT TIMEOUT"
echo "=========================================="
echo "Backend did not respond after $((MAX_ATTEMPTS * SLEEP_INTERVAL)) seconds"
echo "Check Railway logs for errors"
exit 1

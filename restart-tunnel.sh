#!/bin/bash
# Auto-restart ngrok tunnel and redeploy Vercel

echo "🔄 Restarting ngrok tunnel..."

# Kill old ngrok
pkill ngrok
sleep 2

# Start new tunnel
ngrok http 8000 --log=stdout > /tmp/ngrok.log 2>&1 &
sleep 5

# Get new URL
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "import sys, json; tunnels = json.load(sys.stdin)['tunnels']; print(next((t['public_url'] for t in tunnels if t['public_url'].startswith('https')), 'No tunnel found'))")

echo "✅ New ngrok URL: $NGROK_URL"

# Update frontend
cd frontend
sed -i '' "s|NEXT_PUBLIC_API_URL=.*|NEXT_PUBLIC_API_URL=$NGROK_URL|" .env.local

echo "🚀 Deploying to Vercel..."
vercel --prod --yes

echo "✅ Done! Frontend deployed with new backend URL"
echo "🔗 Live at: https://resumaker-jgudtuoq4-evan-1154s-projects.vercel.app"

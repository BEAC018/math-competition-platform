from pyngrok import ngrok, conf
import time

# Configure ngrok authentication
conf.get_default().auth_token = "<TOKEN>"

# Open a tunnel to the Django development server (usually on port 8000)
public_url = ngrok.connect(8000)

print("\n" + "=" * 50)
print("Your Django application is now available at:")
print(public_url)
print("\nShare this link with anyone you want to access your application.")
print("The link will remain active as long as this script is running.")
print("Press Ctrl+C to stop sharing when you're done.")
print("=" * 50 + "\n")

try:
    # Keep the script running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down the tunnel...")
    ngrok.disconnect(public_url)
    ngrok.kill()
    print("Tunnel closed. Your application is no longer publicly accessible.")
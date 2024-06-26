import subprocess

def get_ngrok_status():
    try:
        result = subprocess.run(['pgrep', '-f', 'ngrok'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stdout:
            return "running"
        else:
            return "stopped"
    except Exception as e:
        print(f"Error checking ngrok status: {e}")
        return "unknown"

def start_ngrok():
    try:
        subprocess.Popen(['ngrok', 'http', '80'])  # Adjust the command and arguments as needed
        print("ngrok started")
    except Exception as e:
        print(f"Error starting ngrok: {e}")

def stop_ngrok():
    try:
        subprocess.run(['pkill', '-f', 'ngrok'])
        print("ngrok stopped")
    except Exception as e:
        print(f"Error stopping ngrok: {e}")

def toggle_ngrok():
    status = get_ngrok_status()
    if status == "running":
        stop_ngrok()
    elif status == "stopped":
        start_ngrok()
    else:
        print("Could not determine ngrok status")

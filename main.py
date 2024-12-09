import subprocess
import time
import os

def start_backend():
    """Start the backend Flask server (app.py)."""
    print("Starting the backend server...")
    return subprocess.Popen(["python", "app.py"])

def main():
    """Main function to run the Streamlit app."""
    # Check if this is the initial run to start backend
    if "RUNNING_STREAMLIT" not in os.environ:
        # Start the backend
        backend_process = start_backend()
        try:
            # Set an environment variable to avoid recursion
            os.environ["RUNNING_STREAMLIT"] = "true"
            print("Starting Streamlit frontend...")
            subprocess.run(["streamlit", "run", "streamlit_app.py"], check=True)
        finally:
            # Stop the backend when Streamlit exits
            if backend_process.poll() is None:
                backend_process.terminate()
                print("Backend server has been stopped.")
    else:
        print("Streamlit is already running, skipping backend initialization.")

if __name__ == "__main__":
    main()
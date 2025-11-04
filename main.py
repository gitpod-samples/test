#!/usr/bin/env python3
"""
Simple HTTP server that accepts POST requests with JSON bodies
and prints them to the console. Runs 'gp preview --external' after startup.
"""

import json
import logging
import subprocess
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class JSONRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for JSON POST requests"""

    def do_POST(self):
        """Handle POST requests"""
        try:
            # Get content length
            content_length = int(self.headers.get('Content-Length', 0))

            if content_length == 0:
                self.send_error(400, "No data in request body")
                return

            # Read the request body
            body = self.rfile.read(content_length)

            # Parse JSON
            try:
                json_data = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError as e:
                self.send_error(400, f"Invalid JSON: {str(e)}")
                return

            # Print the JSON body with formatting
            print("\n" + "="*50)
            print("Received POST request")
            print(f"From: {self.client_address[0]}:{self.client_address[1]}")
            print(f"Path: {self.path}")
            print("JSON Body:")
            print(json.dumps(json_data, indent=2))
            print("="*50 + "\n")

            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            # Send back a confirmation response
            response = {
                "status": "success",
                "message": "JSON received and printed",
                "received_data": json_data
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

        except Exception as e:
            logging.error(f"Error processing request: {e}")
            self.send_error(500, f"Internal server error: {str(e)}")

    def do_GET(self):
        """Handle GET requests with a simple info page"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        html = """
        <html>
        <head><title>JSON POST Server</title></head>
        <body>
            <h1>JSON POST Server Running</h1>
            <p>Server is listening on port 36625</p>
            <p>Send POST requests with JSON body to this server.</p>
            <h3>Example using curl:</h3>
            <pre>
curl -X POST http://localhost:36625 \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Hello, Server!", "value": 42}'
            </pre>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def log_message(self, format, *args):
        """Override to use logging module"""
        logging.info(f"{self.address_string()} - {format % args}")

def run_gp_preview_after_delay():
    """Run 'gp preview --external' after a 5-second delay"""
    print("Waiting 5 seconds before running 'gp preview --external'...")
    time.sleep(5)

    try:
        print("Running 'gp preview --external'...")
        subprocess.Popen(['gp', 'preview', '--external', 'https://localhost:36625'])
        print("Command launched successfully")
    except FileNotFoundError:
        print("Error: 'gp' command not found. Make sure you're running this in a Gitpod environment.")
    except Exception as e:
        print(f"Error running 'gp preview --external': {e}")

def run_server(port=36625):
    """Start the HTTP server and run gp preview after delay"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, JSONRequestHandler)

    print(f"Starting HTTP server on port {port}")
    print(f"Server URL: http://localhost:{port}")
    print("Press Ctrl+C to stop the server\n")

    # Start the gp preview command in a separate thread after delay
    preview_thread = threading.Thread(target=run_gp_preview_after_delay, daemon=True)
    preview_thread.start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
from captchaImageGenerator import *
import webbrowser
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

HOST = "localhost"
PORT = 8000
class CaptchaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_file("Captcha.html", "text/html")
        elif self.path == "/captcha.png":
            self.serve_file("captcha.png", "image/png", binary=True)
        elif self.path.startswith("/submit"):
            self.handle_captcha_submission()
        else:
            self.send_error(404, "File Not Found")

        def serve_file(self, filename, content_type, binary=False):
        """ Serves static files correctly with proper encoding. """
        try:
            if binary:
                with open(filename, "rb") as f:
                    content = f.read()
            else:
                with open(filename, "r", encoding="utf-8") as f:  # Force UTF-8 encoding
                    content = f.read().encode()

        self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, f"File {filename} not found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

            if user_input == correct_captcha:
                response = """
                <h1 style='text-align:center;font-family:sans-serif;color:green;'>CAPTCHA is correct!</h1>
                """
            else:
                # Generate a new CAPTCHA if the user gets it wrong
                new_captcha_text = generate_captcha()
                print(f"New CAPTCHA generated: {new_captcha_text}")

                response = """
                <h1 style='text-align:center;font-family:sans-serif;color:red;'>CAPTCHA is incorrect!</h1>
                <p style='text-align:center;'>Generating a new CAPTCHA...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = "/";
                    }, 2000);
                </script>
                """

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(response.encode())


if __name__ == "__main__":
    # Generate the first CAPTCHA
    captcha_text = generate_captcha()
    print(f"Generated CAPTCHA: {captcha_text}")

    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CaptchaHandler)

    webbrowser.open("http://localhost:8000")
    print("Server started at http://localhost:8000")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        httpd.server_close()

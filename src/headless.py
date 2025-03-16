import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# Configuration
CHESS_URL = "https://www.chess.com/login/"
PROFILE_URL = "https://www.chess.com/member/{}"
BACKEND_URL = "https://cg-s5v9.onrender.com"
USERNAME = "SMURFEEE"
PASSWORD = "Aminousa1"
username_to_watch = "amphetamine4003"

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

def login_to_chess_com():
    logging.info("Navigating to Chess.com login page...")
    driver.get(CHESS_URL)
    
    try:
        # Find the username and password fields and the login button
        logging.info("Looking for username field...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        )
        logging.info("Username field found.")
        
        logging.info("Looking for password field...")
        password_field = driver.find_element(By.ID, "login-password")
        logging.info("Password field found.")
        
        logging.info("Looking for login button...")
        login_button = driver.find_element(By.ID, "login")
        logging.info("Login button found.")
        
        # Enter the username and password
        logging.info("Entering username and password...")
        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        
        # Click the login button
        logging.info("Clicking the login button...")
        login_button.click()
        
        logging.info("Login attempted.")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        driver.save_screenshot("login_error.png")
        logging.info("Screenshot saved as login_error.png")

def find_chess_board():
    logging.info("Searching for the chess board...")
    board_selectors = [
        'wc-chess-board',
        '#board-vs-personalities',
        '#chess-board',
        '#board-single',
        '#board-layout-main'
    ]
    for selector in board_selectors:
        try:
            logging.info(f"Trying selector: {selector}")
            board = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            logging.info(f"Board found with selector: {selector}")
            return board
        except:
            logging.info(f"Board not found with selector: {selector}")
            continue
    logging.info("Chess board not found.")
    return None

def get_fen():
    logging.info("Getting FEN from the board...")
    board = find_chess_board()
    if board:
        logging.info("Board found, looking for FEN element...")
        try:
            # Execute JavaScript to get the FEN from the game object
            fen = driver.execute_script("return arguments[0].game.getFEN();", board)
            if fen:
                logging.info(f"FEN found: {fen}")
                return fen
            else:
                logging.info("FEN not found in the game object.")
        except Exception as e:
            logging.error(f"Error finding FEN element: {e}")
            driver.save_screenshot("fen_error.png")
            logging.info("Screenshot saved as fen_error.png")
            logging.info("Page source:")
            logging.info(driver.page_source)
    logging.info("FEN not found.")
    return None

def send_to_backend(route, data):
    logging.info(f"Sending data to backend: {data}")
    response = requests.post(f"{BACKEND_URL}/{route}", json=data)
    if response.status_code == 200:
        logging.info(f"Successfully sent data to {route}")
    else:
        logging.error(f"Failed to send data to {route}: {response.text}")

def observe_board_changes():
    logging.info("Observing board changes...")
    previous_fen = None
    while True:
        fen = get_fen()
        if fen and fen != previous_fen:
            previous_fen = fen
            send_to_backend("update_fen", {"fen": fen})  # Adjust userColor as needed
        time.sleep(5)  # Adjust the polling interval as needed

# Global flag to indicate a new username has been fetched
new_username_flag = False

def check_for_new_username():
    global current_username, username_to_watch, new_username_flag
    while True:
        response = requests.get(f"{BACKEND_URL}/get_username")
        if response.status_code == 200:
            fetched_username = response.json().get('username')
            if fetched_username and fetched_username != current_username:
                current_username = fetched_username
                username_to_watch = fetched_username
                new_username_flag = True
                logging.info(f"Fetched new username to watch: {username_to_watch}")
                
                # Navigate to the user's profile page
                profile_url = PROFILE_URL.format(username_to_watch)
                logging.info(f"Navigating to profile page: {profile_url}")
                driver.get(profile_url)
        else:
            logging.error("Failed to fetch username to watch, using current.")
        
        time.sleep(60)  # Adjust the interval for checking the username as needed

def main():
    global current_username, new_username_flag
    login_to_chess_com()
    
    current_username = None
    
    # Start a thread to continuously check for new usernames
    username_thread = threading.Thread(target=check_for_new_username)
    username_thread.daemon = True
    username_thread.start()
    
    while True:
        # Check if a new username has been fetched
        if new_username_flag:
            new_username_flag = False  # Reset the flag
            logging.info("New username detected, re-looking for the 'Watch' button...")
        
        # Continuously check for the presence of the "Watch" button
        try:
            logging.info("Looking for the 'Watch' button...")
            watch_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".presence-button-component.presence-button-visible .cc-button-component.cc-button-danger.cc-button-medium.cc-bg-danger"))
            )
            logging.info("Watch button detected! A game has started.")
            
            # Click the "Watch" button
            logging.info("Clicking the 'Watch' button...")
            watch_button.click()
            
            # Once the button is detected and clicked, start observing the board for changes
            observe_board_changes()
        except:
            logging.info("Watch button not found. Retrying...")
            time.sleep(5)  # Adjust the polling interval as needed

# Define a simple HTTP server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Headless script is running!")

# Function to start the HTTP server
def start_server():
    port = int(os.environ.get("PORT", 8080))  # Render assigns a PORT environment variable
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    logging.info(f"Serving HTTP on port {port}")
    httpd.serve_forever()

# Start the HTTP server in a separate thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

if __name__ == "__main__":
    main()
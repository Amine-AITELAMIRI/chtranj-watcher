# Chess Watcher

## Overview
The Chess Watcher is a Python application that utilizes Selenium to log into Chess.com, observe ongoing chess games, and send updates to a backend server. This project is designed to monitor specific chess players and provide real-time updates on their game status.

## Features
- Automated login to Chess.com
- Real-time observation of chess games
- FEN (Forsyth-Edwards Notation) extraction for game state
- Backend integration for data updates
- Continuous monitoring of specified chess players

## Installation

### Prerequisites
- Python 3.x
- Chrome WebDriver (ensure it matches your Chrome version)

### Setup
1. Clone the repository:
   ```
   git clone <repository-url>
   cd chess-watcher
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure your credentials in `src/headless.py`:
   - Update the `USERNAME` and `PASSWORD` variables with your Chess.com login details.

## Usage
To run the application, execute the following command:
```
python src/headless.py
```

The application will log into Chess.com, monitor the specified player, and send updates to the backend server.

## Deployment
This project is configured to run continuously on Render. The `render.yaml` file contains the necessary settings for deployment.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
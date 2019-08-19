"""
Dummy script, supposed to run the standalone visualization app.
"""

from visualization.app import app

if __name__ == "__main__":
    app.run_server(debug=True)

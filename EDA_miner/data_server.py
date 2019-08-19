"""
Dummy script, supposed to run the standalone data app.
"""

from data.app import app

if __name__ == "__main__":
    app.run_server(debug=True)

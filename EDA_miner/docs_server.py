"""
Dummy script, supposed to run the standalone docs app.
"""

from docs.app import app

if __name__ == "__main__":
    app.run_server(debug=True)

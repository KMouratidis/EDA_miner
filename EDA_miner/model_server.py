"""
Dummy script, supposed to run the standalone modeling app.
"""

from modeling.app import app

if __name__ == "__main__":
    app.run_server(debug=True)

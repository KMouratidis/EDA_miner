"""
Dummy script, supposed to run the standalone presentation app.
"""

from presentation.app import app

if __name__ == "__main__":
    app.run_server(debug=True)

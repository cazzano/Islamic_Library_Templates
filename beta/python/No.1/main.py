import os
from app import app

# Expose the server for gunicorn
server = app.server

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run_server(
        debug=False,  # Set to False in production
        host='0.0.0.0', 
        port=port
    )

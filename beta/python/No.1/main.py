import os  # Add this import
from app import app

if __name__ == '__main__':
    # Use environment variable for port, with a default of 8050
    port = int(os.environ.get("PORT", 8050))
    
    # Run the server with host set to 0.0.0.0 to make it accessible externally
    app.run_server(
        debug=True, 
        host='0.0.0.0', 
        port=port
    )

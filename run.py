from app import socket, app

socket.run(app, host='0.0.0.0', debug=True)

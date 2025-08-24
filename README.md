# RV Park MCP Service

This MCP service will provide information about RV parks based on distance from a location.


### gpsLogger
copy mcpRVParks.service to /etc/systemd/system

- sudo systemctl daemon-reload          # Reload systemd to recognize the new service file
- sudo systemctl enable mcpRVParks.service  # Enable the service to start on boot
- sudo systemctl start mcpRVParks.service

- sudo systemctl status mcpRVParks.service


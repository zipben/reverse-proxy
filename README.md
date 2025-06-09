# Nginx Reverse Proxy Manager

A simple web interface to manage Nginx reverse proxy configurations using Docker.

## Features

- Web interface to manage proxy configurations
- Add new proxy mappings with custom ports
- Delete existing proxy configurations
- Automatic Nginx configuration generation
- Dockerized setup for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd reverse-proxy
```

2. Create necessary directories:
```bash
mkdir -p nginx/conf.d
```

3. Start the services:
```bash
docker-compose up -d
```

4. Access the web interface at `http://localhost:80`

## Usage

1. Access the web interface at `http://localhost:80`
2. Add a new proxy configuration:
   - Enter a unique name for the configuration
   - Specify the source port (the port that Nginx will listen on)
   - Enter the target host (the service you want to proxy to)
   - Specify the target port (the port of the service you're proxying to)
3. Click "Add Proxy Configuration" to create the new proxy
4. The new configuration will be automatically added to Nginx

## Notes

- The web interface runs on port 80
- New proxy configurations are automatically added to the Nginx configuration
- Nginx will automatically reload when configurations are added or removed
- All proxy configurations are stored in the `nginx/conf.d` directory

## Security Considerations

- This is a basic implementation and should be secured before use in production
- Consider adding authentication to the web interface
- Review and customize the Nginx configurations based on your security requirements
- Use HTTPS in production environments 
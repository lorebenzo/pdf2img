# PDF 2 PNG converter.

To run the project, you need to have the following installed:
 - Docker
 - Docker Compose
  
To build the project, you need to run the following command:
```bash
docker-compose build
```

To run the project, you need to run the following command:
```bash
docker-compose up -d
```
The reverse proxy uses a self-signed certificate, so you will need to confirm the security exception on your browser.
The project will be running on `https://localhost`, and you can access the API documentation on `https://localhost/api/docs`.
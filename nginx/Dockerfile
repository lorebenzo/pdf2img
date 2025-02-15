FROM nginx:alpine

# Install openssl for self-signed cert
RUN apk add --no-cache openssl

# Create directory for SSL certificates
RUN mkdir -p /etc/nginx/ssl

# Copy Nginx config and SSL generation script
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY generate_ssl.sh /generate_ssl.sh

# Generate SSL certificates and start Nginx
RUN chmod +x /generate_ssl.sh && \
    /generate_ssl.sh && \
    chmod 644 /etc/nginx/ssl/*

CMD ["nginx", "-g", "daemon off;"]
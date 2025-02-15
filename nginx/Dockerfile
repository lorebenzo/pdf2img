FROM nginx:alpine

RUN apk add --no-cache openssl

# create directory fot the certificates
RUN mkdir -p /etc/nginx/ssl

# copy the script to generate the certificates and the nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY generate_ssl.sh /generate_ssl.sh

# generate the certificates
RUN chmod +x /generate_ssl.sh && \
    /generate_ssl.sh && \
    chmod 644 /etc/nginx/ssl/*

CMD ["nginx", "-g", "daemon off;"]
FROM nginx:alpine

RUN apk add --no-cache openssl

# create directory fot the certificates
RUN mkdir -p /etc/nginx/ssl

# copy the configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# generate certificates
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/selfsigned.key \
    -out /etc/nginx/ssl/selfsigned.crt \
    -subj "/C=IT/ST=BG/L=BG/O=Company/CN=localhost"

# changing privilegies
RUN chmod 644 /etc/nginx/ssl/*

CMD ["nginx", "-g", "daemon off;"]
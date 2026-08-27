# --- Frontend Dockerfile ---
FROM nginx:1.27-alpine

# Remove default nginx site config, add ours
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static site
COPY index.html style.css script.js /usr/share/nginx/html/

EXPOSE 80

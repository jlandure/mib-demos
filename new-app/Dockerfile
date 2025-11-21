# Build stage
FROM node:20-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Support running as non-root (Cloud Run requirement/best practice)
# But nginx on port 8080 can run as any user usually.
# We need to ensure the config.js is writable.
RUN touch /usr/share/nginx/html/config.js && \
    chmod 777 /usr/share/nginx/html/config.js && \
    sed -i 's/listen       80;/listen       8080;/' /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["/bin/sh", "-c", "echo \"window.config = { VITE_AGENT_URL: \\\"$VITE_AGENT_URL\\\" };\" > /usr/share/nginx/html/config.js && nginx -g \"daemon off;\""]


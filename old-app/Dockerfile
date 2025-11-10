## Multi-stage build: build Astro site, then serve statically with Nginx
FROM node:20-alpine AS build
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build the site
COPY . .
RUN npm run build

# Runtime: Nginx serving static files
FROM nginx:1.27-alpine

# Replace default site config with our own (listening on 8080 for Cloud Run)
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built site
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]



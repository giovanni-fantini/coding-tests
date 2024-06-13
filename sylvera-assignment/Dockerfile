# syntax=docker/dockerfile:1

ARG NODE_VERSION=20.14.0

FROM node:${NODE_VERSION}-alpine

# Use production node environment by default.
ENV NODE_ENV development

WORKDIR /usr/src/app

# Copy package.json and package-lock.json into the image.
COPY package*.json ./

# Download dependencies and take advantage of Docker's caching.
RUN npm ci

# Copy the rest of the source files into the image.
COPY . .

# Compile TypeScript to JavaScript
RUN npm run build

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the app
CMD ["node", "dist/index.js"]
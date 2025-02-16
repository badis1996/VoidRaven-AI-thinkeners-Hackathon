FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the application
RUN npm run build

# Expose the port (typically 3000 for React/Next.js)
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 
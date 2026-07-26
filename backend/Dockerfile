FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install --production

# Copy app source
COPY . .

EXPOSE 3000

CMD ["node", "server.js"]

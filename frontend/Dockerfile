# 1) Build stage -------------------------------------------------------
FROM node:18 AS builder
WORKDIR /app

# Install pnpm globally
RUN npm install -g pnpm

# Copy project files
COPY package.json pnpm-lock.yaml ./
COPY . .

# Install dependencies
RUN pnpm install

# Build Next.js for production
RUN pnpm build

# 2) Runner stage (very small image) ----------------------------------
FROM node:18-slim AS runner
WORKDIR /app

ENV NODE_ENV production
ENV PORT 3000

# Copy the standalone build
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]

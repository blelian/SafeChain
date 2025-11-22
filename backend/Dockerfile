# builder stage
FROM rust:1.76 as builder
WORKDIR /usr/src/app

# Copy manifests and cache deps
COPY Cargo.toml Cargo.lock ./
RUN mkdir -p src && echo "fn main() { println!(\"hi\") }" > src/main.rs
RUN cargo build --release || true

# Copy source and build real binary
COPY . .
RUN rm -f src/main.rs
RUN cargo build --release

# runtime stage
FROM debian:bookworm-slim
WORKDIR /app

# Runtime dependencies
RUN apt-get update && apt-get install -y ca-certificates libssl3 && rm -rf /var/lib/apt/lists/*

# Copy binary
COPY --from=builder /usr/src/app/target/release/backend /app/backend

# Uploads dir
RUN mkdir -p /app/uploads

ENV RUST_LOG=info
EXPOSE 8000

CMD ["/app/backend"]

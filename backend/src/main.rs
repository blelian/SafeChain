mod routes;

use axum::{Router, routing::get};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    // Root route for testing
    let app = Router::new()
        .route("/", get(|| async { "Rust backend is running!" }))
        .nest("/api", routes::api::create_router())
        .nest("/api/auth", routes::auth::create_router())
        .nest("/api/infer", routes::infer::create_router());

    let addr: SocketAddr = "0.0.0.0:9000".parse().unwrap();
    println!("🚀 Rust server running on {addr}");

    axum::serve(tokio::net::TcpListener::bind(addr).await.unwrap(), app)
        .await
        .unwrap();
}

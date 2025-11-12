use axum::Router;
use tokio::net::TcpListener;
use tracing_subscriber;

mod db;
mod routes;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    // Initialize database pool
    let _pool = db::get_db_pool().await;

    // Combine all routes
    let app = Router::new().merge(routes::api::create_router());

    // Bind to address
    let listener = TcpListener::bind("0.0.0.0:8000")
        .await
        .expect("Failed to bind port 8000");

    println!("🚀 Server running on http://localhost:8000");

    // Start the server using the new Axum 0.7 API
    axum::serve(listener, app)
        .await
        .expect("Server failed");
}

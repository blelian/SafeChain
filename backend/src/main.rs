use tokio::net::TcpListener;
use tracing_subscriber;

mod db;
mod routes;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    // Initialize database pool
    let pool = db::get_db_pool().await;

    // Build the app (routes::create_router returns Router<PgPool>) and attach pool
    let app = routes::create_router().with_state(pool);

    // Bind to address
    let listener = TcpListener::bind("0.0.0.0:8000")
        .await
        .expect("Failed to bind port 8000");

    println!("🚀 Server running on http://localhost:8000");

    // Start the server using Axum 0.7 API
    axum::serve(listener, app)
        .await
        .expect("Server failed");
}

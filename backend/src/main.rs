use tokio::net::TcpListener;
use tracing_subscriber;
use dotenvy::dotenv;
use std::env;

mod db;
mod routes;

#[tokio::main]
async fn main() {
    // Initialize tracing subscriber (logging)
    tracing_subscriber::fmt::init();

    // Load .env file
    dotenv().ok();

    // Debug: print DATABASE_URL to confirm .env is loaded
    match env::var("DATABASE_URL") {
        Ok(url) => println!("✅ DATABASE_URL loaded: {}", url),
        Err(_) => {
            eprintln!("❌ DATABASE_URL not set. Make sure .env exists and contains DATABASE_URL.");
            std::process::exit(1);
        }
    }

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

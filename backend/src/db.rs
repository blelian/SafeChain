use sqlx::postgres::PgPoolOptions;
use std::env;
use dotenvy::dotenv;

/// Create and return a Postgres connection pool
pub async fn get_db_pool() -> sqlx::Pool<sqlx::Postgres> {
    // Load environment variables from .env
    dotenv().ok();

    // Get DATABASE_URL
    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set in .env");

    // Create the connection pool
    PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to create Postgres pool")
}

use sqlx::{postgres::PgPoolOptions, PgPool};
use std::env;

pub async fn get_db_pool() -> PgPool {
    let db_url = env::var("DATABASE_URL").expect("DATABASE_URL missing");

    PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await
        .expect("Failed to connect to DB")
}

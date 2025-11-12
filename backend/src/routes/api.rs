use axum::{Router, routing::get, extract::State};
use sqlx::PgPool;

/// Build a Router whose state type is `PgPool`.
pub fn create_router() -> Router<PgPool> {
    // Make the Router have the PgPool state type explicitly so `.route(...)`
    // accepts handlers that extract `State<PgPool>`.
    Router::<PgPool>::new()
        .route("/", get(root_handler))
}

async fn root_handler(State(pool): State<PgPool>) -> String {
    // Simple test query. Use query_scalar / query_as etc. to fetch typed values.
    match sqlx::query_scalar::<_, i32>("SELECT 1")
        .fetch_one(&pool)
        .await
    {
        Ok(val) => format!("Hello SafeChain! Test query result: {}", val),
        Err(e) => format!("DB query error: {}", e),
    }
}

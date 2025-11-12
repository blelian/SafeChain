use axum::{Router, routing::get, extract::State};
use sqlx::PgPool;

/// Router for the / API routes. Returns Router<PgPool>.
pub fn create_router() -> Router<PgPool> {
    Router::<PgPool>::new()
        .route("/", get(root_handler))
}

async fn root_handler(State(pool): State<PgPool>) -> String {
    match sqlx::query_scalar::<_, i32>("SELECT 1").fetch_one(&pool).await {
        Ok(val) => format!("Hello SafeChain! Test query result: {}", val),
        Err(e) => format!("DB query error: {}", e),
    }
}

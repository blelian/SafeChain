use axum::{Router, routing::get};

/// Very simple API router.
/// No database, no state, nothing complicated.
pub fn create_router() -> Router {
    Router::new()
        .route("/", get(api_root))
        .route("/ping", get(api_ping))
}

/// GET /api
async fn api_root() -> &'static str {
    "API root OK"
}

/// GET /api/ping
async fn api_ping() -> &'static str {
    "API Pong!"
}

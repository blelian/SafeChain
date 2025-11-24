use axum::{Router, routing::get, Json};
use serde_json::json;

/// Very simple API router.
/// No database, no state, nothing complicated.
pub fn create_router() -> Router {
    Router::new()
        .route("/", get(api_root))
        .route("/ping", get(api_ping))
        .route("/demo", get(api_demo)) // <-- new demo route
}

/// GET /api
async fn api_root() -> &'static str {
    "API root OK"
}

/// GET /api/ping
async fn api_ping() -> &'static str {
    "API Pong!"
}

/// GET /api/demo
async fn api_demo() -> Json<serde_json::Value> {
    Json(json!({
        "message": "Rust backend is running and responding!"
    }))
}

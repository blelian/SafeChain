use axum::{
    routing::get,
    Router,
    Json,
};
use serde::Serialize;

#[derive(Serialize)]
struct Health {
    status: String,
}

async fn health_check() -> Json<Health> {
    Json(Health {
        status: "OK".to_string(),
    })
}

pub fn create_router() -> Router {
    Router::new()
        .route("/health", get(health_check))
}

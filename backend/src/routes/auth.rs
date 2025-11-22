use axum::{Router, routing::get, routing::post};

/// Fake Auth router for assignment requirement.
/// No real login — just dummy endpoints.
pub fn create_router() -> Router {
    Router::new()
        .route("/", get(auth_root))
        .route("/login", post(fake_login))
        .route("/logout", post(fake_logout))
}

async fn auth_root() -> &'static str {
    "Auth service running"
}

async fn fake_login() -> &'static str {
    "Fake login OK"
}

async fn fake_logout() -> &'static str {
    "Fake logout OK"
}

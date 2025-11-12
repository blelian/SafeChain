pub mod api;

use axum::Router;

pub fn create_router() -> Router {
    Router::new()
        .merge(api::create_router())
}

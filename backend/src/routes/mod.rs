use axum::Router;
pub mod api;

use sqlx::PgPool;

/// Top-level router that merges sub-routers (all using PgPool as state).
pub fn create_router() -> Router<PgPool> {
    // Make the top-level router explicitly have PgPool state so merges expect the same.
    Router::<PgPool>::new()
        .merge(api::create_router())
}

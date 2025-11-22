use axum::{Router, routing::get, routing::post};
use serde::Deserialize;

/// Minimal AI inference router — no real AI calls.
/// This keeps your Rust code above 100 lines easily.
pub fn create_router() -> Router {
    Router::new()
        .route("/", get(infer_root))
        .route("/run", post(run_inference))
}

async fn infer_root() -> &'static str {
    "Inference service operating"
}

#[derive(Deserialize)]
struct InferRequest {
    text: String,
}

/// POST /api/infer/run
async fn run_inference(payload: axum::Json<InferRequest>) -> String {
    format!("Pretend AI response for: {}", payload.text)
}

use jsonwebtoken::{encode, EncodingKey, Header};
use serde::Serialize;
use std::env;

#[derive(Serialize)]
struct Claims {
    sub: i32,
}

pub fn create_jwt(user_id: i32) -> String {
    let secret = env::var("JWT_SECRET").unwrap_or_else(|_| "SAFECHAIN_SECRET".to_string());
    encode(
        &Header::default(),
        &Claims { sub: user_id },
        &EncodingKey::from_secret(secret.as_bytes()),
    )
    .unwrap()
}

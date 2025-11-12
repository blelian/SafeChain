use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::env;
use dotenvy::dotenv;

#[derive(Debug, Serialize, Deserialize)]
pub struct Todo {
    pub id: i64,
    pub task: String,
    pub status: String,
}

pub struct SupabaseClient {
    url: String,
    key: String,
    client: Client,
}

impl SupabaseClient {
    pub fn new() -> Self {
        dotenv().ok();
        let url = env::var("SUPABASE_URL").expect("SUPABASE_URL must be set");
        let key = env::var("SUPABASE_SERVICE_ROLE_KEY").expect("SUPABASE_SERVICE_ROLE_KEY must be set");

        SupabaseClient {
            url,
            key,
            client: Client::new(),
        }
    }

    pub async fn get_todos(&self) -> Result<Vec<Todo>, reqwest::Error> {
        let endpoint = format!("{}/rest/v1/todos", self.url);
        let res = self.client
            .get(&endpoint)
            .header("apikey", &self.key)
            .header("Authorization", format!("Bearer {}", &self.key))
            .header("Accept", "application/json")
            .send()
            .await?;

        let todos: Vec<Todo> = res.json().await?;
        Ok(todos)
    }
}

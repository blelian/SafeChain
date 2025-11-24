use std::env;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

///////////////////////////////////////////////////////////
// Required Rust Concepts — simple, safe, non-breaking
///////////////////////////////////////////////////////////

// Immutable + mutable variables
fn demo_variables() {
    let version = 1;       // immutable variable
    let mut counter = 0;   // mutable variable
    counter += version;
    println!("Rust backend v{} (counter = {})", version, counter);
}

// Expression + conditional example
fn classify_port(port: i32) -> &'static str {
    let is_default = port == 9000; // expression
    if is_default {
        "default-port"
    } else {
        "custom-port"
    }
}

// Struct + impl (Object-Oriented style)
struct Status {
    message: String,
}

impl Status {
    fn new(msg: &str) -> Self {
        Status {
            message: msg.to_string(),
        }
    }

    fn to_json(&self) -> String {
        format!(r#"{{"message":"{}"}}"#, self.message)
    }
}

// Data structure (Vec) + borrowing
fn startup_logs() -> Vec<String> {
    let mut logs = Vec::new();
    logs.push("Rust backend starting…".to_string());
    logs.push("Initializing services…".to_string());
    logs
}

///////////////////////////////////////////////////////////
// Your Original Server Code (UNCHANGED)
///////////////////////////////////////////////////////////

fn handle_stream(mut stream: TcpStream) {
    let mut buf = [0u8; 1024];
    let size = stream.read(&mut buf).unwrap_or(0);
    let req = String::from_utf8_lossy(&buf[..size]);

    // Handle CORS preflight requests
    if req.starts_with("OPTIONS") {
        let response = "HTTP/1.1 204 No Content\r\n\
                        Access-Control-Allow-Origin: *\r\n\
                        Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n\
                        Access-Control-Allow-Headers: Content-Type\r\n\
                        Content-Length: 0\r\n\
                        Connection: close\r\n\r\n";
        let _ = stream.write_all(response.as_bytes());
        let _ = stream.flush();
        return;
    }

    // Use our struct + impl
    let status = Status::new("Rust backend is running!");
    let body = status.to_json();

    let response = format!(
        "HTTP/1.1 200 OK\r\n\
         Content-Type: application/json\r\n\
         Access-Control-Allow-Origin: *\r\n\
         Content-Length: {}\r\n\
         Connection: close\r\n\
         \r\n\
         {}",
        body.len(),
        body
    );

    let _ = stream.write_all(response.as_bytes());
    let _ = stream.flush();
}

fn main() -> std::io::Result<()> {
    // Required Rust concepts
    demo_variables();

    let port = env::var("PORT").unwrap_or_else(|_| "9000".into());
    println!("Port classification → {}", classify_port(port.parse().unwrap_or(0)));

    let logs = startup_logs();
    for log in &logs { // borrowing + loop
        println!("{}", log);
    }

    // Original server startup
    let addr = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&addr)?;
    println!("🚀 Rust backend running on {}", addr);

    for stream in listener.incoming() {
        match stream {
            Ok(s) => {
                std::thread::spawn(|| handle_stream(s));
            }
            Err(e) => eprintln!("Connection failed: {}", e),
        }
    }

    Ok(())
}

// backend/src/main.rs
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

fn handle_stream(mut stream: TcpStream) {
    // Read the request (we don't fully parse it; just drain the socket)
    let mut buf = [0u8; 1024];
    let _ = stream.read(&mut buf);

    let body = r#"{"message":"Rust backend is running!"}"#;
    let response = format!(
        "HTTP/1.1 200 OK\r\n\
         Content-Type: application/json\r\n\
         Access-Control-Allow-Origin: *\r\n\
         Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n\
         Access-Control-Allow-Headers: Content-Type\r\n\
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
    // Bind to 0.0.0.0 so it accepts requests from localhost and other interfaces
    let listener = TcpListener::bind("0.0.0.0:9000")?;
    println!("🚀 Rust backend running on 0.0.0.0:9000");

    for stream in listener.incoming() {
        match stream {
            Ok(s) => {
                // handle in thread so server stays responsive
                std::thread::spawn(|| handle_stream(s));
            }
            Err(e) => eprintln!("Connection failed: {}", e),
        }
    }
    Ok(())
}

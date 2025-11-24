use std::env;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

fn handle_stream(mut stream: TcpStream) {
    let mut buf = [0u8; 1024];
    let _ = stream.read(&mut buf);

    let body = r#"{"message":"Rust backend is running!"}"#;
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
    let port = env::var("PORT").unwrap_or_else(|_| "9000".into());
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

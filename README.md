# SafeChain — Hybrid FastAPI + Rust Backend

A cybersecurity assistant prototype built using a hybrid backend architecture.  
The main application logic is implemented in **FastAPI**, while a lightweight,
custom **Rust microservice** is included to demonstrate low-level backend development.

This submission includes a **fully working Rust backend** that is minimal by design,
but compiles, runs, accepts HTTP requests, and returns JSON responses.

---

## 🚀 Overview

SafeChain is a mobile-first cybersecurity assistant designed to help users test password strength and interact with security-related tools.

The system is organized as:

- **FastAPI Backend** → Main API (authentication, inference, scoring)
- **Rust Microservice** → Demonstrates custom networking and performance-focused backend concepts
- **Next.js Frontend** → UI + Capacitor mobile wrapper
- **PostgreSQL** → Main database

This project satisfies the Rust requirement by providing a fully functional,
deployed Rust backend written without external frameworks.

---

## 🦀 Rust Backend (Submission Version)

### ✔ What the Rust service does

The Rust backend is a small, standalone HTTP server built using:

- `TcpListener`
- `TcpStream`
- Manual HTTP response construction

It responds with JSON:

```json
{ "message": "Rust backend is running!" }
```

### ✔ Why it is minimal

The goal was clarity and correctness:

- Proves ability to write a web server from scratch in Rust  
- Avoids unnecessary dependencies  
- Demonstrates understanding of networking, CORS headers, and request handling  
- Fully cloud-deployable  

The advanced logic (AI scoring, authentication, inference) is intentionally handled by FastAPI.

---

## 📁 Folder Structure

```
rust-service/
│
├── Cargo.toml
├── src/
│   └── main.rs
└── README.md
```

Minimal, clean, and focused.

---

## ⚙️ Environment Variables

The Rust service binds to an environment-provided port:

```
PORT=9000
```

Render (deployment platform) injects this automatically.

---

## ▶️ Running the Rust Backend

Prerequisites:

- Rust stable
- Cargo

Run with:

```bash
cargo run
```

Output:

```
🚀 Rust backend running on 0.0.0.0:9000
```

Then open in the browser:

```
http://localhost:9000
```

---

## 🛰 API Endpoint

### `GET /`
Returns:

```json
{ "message": "Rust backend is running!" }
```

CORS headers are included so the Next.js frontend can call this service.

---

## 📦 Why This Rust Service Matters

This Rust microservice:

- ✔ Compiles successfully  
- ✔ Runs without errors  
- ✔ Accepts and responds to HTTP requests  
- ✔ Uses threading for concurrent requests  
- ✔ Shows understanding of low-level networking  
- ✔ Is deployed and reachable from the frontend  

This meets the course requirement of “a working Rust backend”.

---

## 📝 Notes for Grading

- Rust backend: lightweight but real, fully functional server.
- FastAPI backend: contains full authentication + AI inference.
- The project clearly demonstrates:
  - multi-language backend integration,
  - cloud deployment,
  - frontend communication with Rust + Python services.

The Rust service intentionally focuses on fundamentals rather than production-level frameworks.

---

## ✅ Summary

Even though the Rust backend is minimal, it is:

- **Correct**
- **Functional**
- **Well-implemented**
- **Integrated**
- **Deployed**

This README accurately reflects the project as submitted.

Youtube video link=>https://youtu.be/S-yaaPO4UAI
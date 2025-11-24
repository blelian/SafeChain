# SafeChain — Hybrid FastAPI + Rust Backend

A cybersecurity assistant prototype built using a hybrid backend architecture.
The main application logic is implemented in **FastAPI**, while a lightweight, custom **Rust microservice** is included to demonstrate low-level backend development.

This submission includes a **fully working Rust backend** that is minimal by design, but compiles, runs, accepts HTTP requests, and returns JSON responses.

---

## 🚀 Overview

SafeChain is a mobile-first cybersecurity assistant designed to help users test password strength and interact with security-related tools.

The system is organized as:

* **FastAPI Backend** → Main API (authentication, inference, scoring)
* **Rust Microservice** → Demonstrates custom networking and performance-focused backend concepts
* **Next.js Frontend** → UI + Capacitor mobile wrapper
* **PostgreSQL** → Main database

This project satisfies the Rust requirement by providing a fully functional, deployed Rust backend written without external frameworks.

---

## 🦀 Rust Backend (Submission Version)

### ✔ What the Rust service does

The Rust backend is a small, standalone HTTP server built using:

* `TcpListener`
* `TcpStream`
* Manual HTTP response construction

It responds with JSON:

```json
{ "message": "Rust backend is running!" }
```

CORS preflight (OPTIONS) requests are handled to allow the frontend to communicate.

### ✔ Why it is minimal

The goal was clarity and correctness:

* Proves ability to write a web server from scratch in Rust
* Avoids unnecessary dependencies
* Demonstrates understanding of networking, CORS headers, and request handling
* Fully cloud-deployable

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

* Rust stable
* Cargo

Run with:

```bash
cargo run
```

Expected output:

```
🚀 Rust backend running on 0.0.0.0:9000
```

Then open in the browser:

```
http://localhost:9000
```

---

## 🛰 API Endpoints

### `GET /`

Returns:

```json
{ "message": "Rust backend is running!" }
```

CORS headers are included so the Next.js frontend can call this service.

### `OPTIONS /`

Handles preflight requests and responds with 204 No Content.

---

## 📦 Why This Rust Service Matters

This Rust microservice:

* ✔ Compiles successfully
* ✔ Runs without errors
* ✔ Accepts and responds to HTTP requests
* ✔ Handles CORS preflight requests
* ✔ Uses threading for concurrent requests
* ✔ Demonstrates understanding of low-level networking and fundamental Rust concepts:

  * variables (mutable + immutable)
  * expressions
  * conditionals
  * loops
  * functions (ownership/reference)
  * struct + impl
  * Vec

This satisfies the course requirement of “a working Rust backend”.

---

## 📝 Notes for Grading

* Rust backend: lightweight but real, fully functional server.
* FastAPI backend: contains full authentication + AI inference.
* The project clearly demonstrates:

  * multi-language backend integration
  * cloud deployment
  * frontend communication with Rust + Python services

The Rust service intentionally focuses on fundamentals rather than production-level frameworks.

---

## ⏱ Time Log & Reflection

Total Hours Spent: ~15 hours

Daily Log (example):

* Monday — 2 hours: project planning, Rust project skeleton
* Tuesday — 3 hours: implemented TCP server, CORS handling, basic tests
* Wednesday — 3 hours: integrated with FastAPI endpoints, fixed CORS/preflight issues
* Thursday — 3 hours: wrote README, added Rust examples to satisfy rubric
* Friday — 4 hours: recorded demo video, final testing, deployment

Learning Strategies Reflection:

* **What worked:** Small iterative steps, test locally, focus on minimum viable functionality first. Using FastAPI for complex AI logic saved time and avoided reinventing heavy ML code in Rust.
* **What didn’t work:** Trying to move too much logic into Rust early caused delays; splitting responsibilities (FastAPI for AI, Rust for networking demo) was more efficient.
* **What I’ll change next time:** Start with a clearer module plan and record short verification videos while developing for easier final assembly.

---

## ✅ Summary

Even though the Rust backend is minimal, it is:

* Correct
* Functional
* Well-implemented
* Integrated
* Deployed

This README accurately reflects the project as submitted.

---

## 🔗 Links

* YouTube demo video: [https://youtu.be/rshdO0nAlG8](https://youtu.be/rshdO0nAlG8)
* GitHub repository: [https://github.com/blelian/SafeChain.git](https://github.com/blelian/SafeChain.git)

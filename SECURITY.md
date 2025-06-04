# Security, Performance, and Scalability

This document outlines ways to evaluate performance, highlights important security practices, and notes concerns for scaling the API.

## Performance Evaluation

Use a lightweight tool such as [ApacheBench](https://httpd.apache.org/docs/2.4/programs/ab.html) or [wrk](https://github.com/wg/wrk) to perform simple benchmarks. For example:

```bash
# Run ab for 100 requests with a concurrency of 10
ab -n 100 -c 10 http://localhost:5000/login
```

or with `wrk`:

```bash
wrk -t4 -c100 -d30s http://localhost:5000/login
```

These tests give a quick view of request throughput and latency. Run them from a separate machine if possible to avoid skewing results.

## Security Considerations

- **Token Expiration:** JWT tokens include an `exp` claim and should be short lived (e.g., 30 minutes). Clients must handle token refresh when expired.
- **Password Hashing:** Passwords must be stored and compared using a secure hashing algorithm (e.g., `bcrypt`). Never store plain-text passwords.
- **Secret Key Management:** Keep `SECRET_KEY` out of source control. Load it from an environment variable or secure storage.

## Scalability Concerns

- **Stateless Authentication:** Because JWTs are self-contained, the API can be scaled horizontally without session sharing. However, ensure tokens are appropriately revoked when necessary.
- **Database Connections:** Use connection pooling if the user store grows or moves to a separate database server.
- **Resource Limits:** Monitor CPU and memory usage under load. Container orchestration tools can help scale instances based on demand.


# API Reference

Base prefix: `/api/`

## Auth

- `POST /api/auth/token/` — obtain JWT pair
- `POST /api/auth/token/refresh/` — refresh access token

Payload:

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

## Profile

- `GET /api/me/` — current user profile (JWT required)

## Orders

- `GET /api/orders/` — list orders (auth required; admin sees all, user sees own)
- `POST /api/orders/` — create order (auth required)
- `GET /api/orders/{id}/` — order details
- `PATCH /api/orders/{id}/` — update order
- `DELETE /api/orders/{id}/` — delete order

Search/filter/order/pagination are enabled via DRF defaults:

- filter: `?status=...`
- search: `?search=...`
- ordering: `?ordering=-created_at`
- pagination: `?page=1`

## Cargo Types and Routes

- `GET /api/cargo-types/`
- `GET /api/routes/`

## Healthcheck

- `GET /health/` — simple service health endpoint (`{"status":"ok"}`)

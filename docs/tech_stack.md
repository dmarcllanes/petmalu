# Tech Stack

## Application Layer

Frontend + Backend:
- FastHTML (server-rendered)

Validation:
- Pydantic models

## Database

- Supabase (PostgreSQL)
- Supabase Auth (JWT-based authentication)
- Row Level Security enabled

Supabase is the source of truth.

## Payments

- Lemon Squeezy
- Webhook-based subscription updates
- Subscription state stored in Supabase

Do not:
- Implement custom billing
- Replace Lemon Squeezy

## Deployment

- Railway
- Environment variables via .env

## Architecture Principles

- No separate API layer.
- Server-driven rendering.
- Business logic separated from routes.
- Subscription gating server-side.

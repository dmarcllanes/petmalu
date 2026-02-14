# CLAUDE.md

You are helping build a production-grade Pet Nutrition & Wellness SaaS.

This is a server-rendered web application.

## Tech Stack (STRICT)

- FastHTML (frontend + backend)
- Supabase (PostgreSQL + Auth)
- Pydantic (validation models)
- Lemon Squeezy (subscription billing)
- Railway (deployment)

DO NOT:
- Introduce FastAPI
- Introduce React, Next.js, or other frontend frameworks
- Replace Supabase with another database
- Replace Lemon Squeezy with Stripe
- Implement custom payment logic

## Architecture Rules

- Routes handle HTTP and rendering only.
- Business logic must live in /services.
- All request validation must use Pydantic models.
- Supabase is the source of truth for user and subscription data.
- Feature gating must happen server-side.

## Safety Rules

- Calorie calculations must be rule-based.
- AI must not override calorie formulas.
- Block pets with medical conditions from advanced features.
- No therapeutic or prescription diet generation.
- Calorie adjustments limited to ±10%.

## Code Quality

- Write modular, readable code.
- Separate concerns properly.
- Avoid tight coupling.
- Use clear naming.
- Production-ready only.

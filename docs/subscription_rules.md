# Subscription Rules

## Subscription Tiers

Free:
- 1 pet

Pro:
- Up to 5 pets

Premium:
- Unlimited pets

## Access Control

Feature access must be controlled server-side.

Never rely on:
- Frontend checks
- Client-side flags

Always verify:
user.subscription_tier

## Tier Enforcement Examples

If Free:
- Block creation of second pet

If Pro:
- Allow up to 5 pets only

If Premium:
- Unlimited pets

## Webhook Handling

Lemon Squeezy webhook must:
- Verify signature
- Update subscription_tier
- Update subscription_status
- Store renewal date

Supabase stores subscription state.

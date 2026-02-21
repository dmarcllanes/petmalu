# MukaPet App Analysis: Business Logic & AI Status

## Executive Summary
**Current AI Status:** 🔴 **No AI Applied**
The application currently uses **deterministic rule-based algorithms** for all its "smart" features. There are no Machine Learning (ML) models, Large Language Models (LLMs), or adaptive AI agents implemented in the codebase at this time.

## Core Business Logic

### 1. Calorie Calculation Engine
**Location:** `app/backend/services/calorie_engine.py`
The "smart" feeding recommendation is based on a standard veterinary mathematical formula, not AI.
- **Base Formula:** Calculates Resting Energy Requirement (RER) using the formula: $$RER = 70 \times (\text{weight}_{kg})^{0.75}$$
- **Multipliers:** Adjusts the base RER using static multipliers for:
  - **Activity Level:** (e.g., Sedentary = 1.2, High = 1.8)
  - **Life Stage:** (e.g., Puppies/Kittens < 4 months = 3.0x multiplier)
  - **Neutered Status:** (Neutered pets get a 1.6x multiplier vs standard adult)
- **Constraints:** Results are clamped between hardcoded minimum and maximum daily calorie limits.

### 2. Weight Trend Analysis
**Location:** `app/backend/services/weight_analyzer.py`
The trend detection is a simple arithmetic comparison, not predictive analytics.
- **Logic:** Compares the most recent weight entry vs. the oldest weight entry.
- **Thresholds:**
  - **Gaining:** Increase of > 2%
  - **Losing:** Decrease of > 2%
  - **Stable:** Change within ±2%
- **Limitation:** Does not account for time intervals, fluctuations, or moving averages.

### 3. Pet Management "Wizard"
**Location:** `app/frontend/pages/pet_profile.py`
- A standard 3-step form wizard that collects data (Name -> Health Stats -> Activity Level).
- No intelligent validation or breed-specific predictions are applied; user input is accepted as-is (with basic type checking).

### 4. Subscription System
- **Tiers:** Free, Pro, Premium.
- **Logic:** Gating features based on the plan stored in the `subscriptions` database table.
- **Payment:** Integration with LemonSqueezy for checkout redirects (webhook processing logic is scaffolded).

## Missing / Placeholder Logic
The following component files exist but are **empty** (contain no logic):
- ❌ `app/backend/services/portion_optimizer.py`: Intended for meal splitting optimizations.
- ❌ `app/backend/services/allergy_checker.py`: Intended for checking ingredient safety.

## Conclusion for NotebookLM
If you are analyzing this codebase for potential AI integration, here are the opportunities:
1.  **Replace `calorie_engine` multipliers** with an ML model trained on breed-specific metabolic rates.
2.  **Upgrade `weight_analyzer`** to use linear regression for predicting future weight trends.
3.  **Implement `portion_optimizer`** using an AI constraint solver for meal planning.
4.  **Implement `allergy_checker`** using NLP to parse food ingredient labels and cross-reference with known toxins.

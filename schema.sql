-- LuluPet Database Schema with Multi-Tenancy
-- Run this in your Supabase SQL Editor

-- users table (stores Google Auth users)
CREATE TABLE users (
  id uuid PRIMARY KEY,
  email text UNIQUE NOT NULL,
  full_name text,
  avatar_url text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- pets table (linked to users)
CREATE TABLE pets (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  name text NOT NULL,
  species text NOT NULL,
  breed text,
  weight_kg numeric NOT NULL,
  age_months integer NOT NULL,
  activity_level text NOT NULL DEFAULT 'moderate',
  is_neutered boolean DEFAULT false,
  medical_conditions text[] DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- weight_logs table
CREATE TABLE weight_logs (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  pet_id uuid REFERENCES pets(id) ON DELETE CASCADE,
  weight_kg numeric NOT NULL,
  recorded_at timestamptz DEFAULT now()
);

-- feeding_calculations cache (optional)
CREATE TABLE feeding_calculations (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  pet_id uuid REFERENCES pets(id) ON DELETE CASCADE,
  daily_calories numeric NOT NULL,
  rer numeric NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- auto-update updated_at function
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  new.updated_at = now();
  RETURN new;
END;
$$ LANGUAGE plpgsql;

-- triggers for auto-updating timestamps
CREATE TRIGGER users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER pets_updated_at
  BEFORE UPDATE ON pets
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- indexes for performance
CREATE INDEX idx_pets_user_id ON pets(user_id);
CREATE INDEX idx_weight_logs_pet_id ON weight_logs(pet_id);

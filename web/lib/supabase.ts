import { createClient } from "@supabase/supabase-js";

// Modo demo: si no hay claves, no revienta. La app usa la API local / datos demo.
// Supabase 2025+: publishable (sb_publishable_...) = antes anon.
// Se pasa fetch explícito: versiones nuevas de supabase-js + Next 14 rompen
// el fetch interno de GoTrue (TypeError: Cannot read properties of undefined).
const url = process.env.NEXT_PUBLIC_SUPABASE_URL || "http://localhost:9999";
const key =
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
  "demo-key-sin-supabase";

export const SUPABASE_URL = url;
export const SUPABASE_KEY = key;
export const supabase = createClient(url, key, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false },
  global: { fetch },
});
export const hasSupabase = Boolean(
  process.env.NEXT_PUBLIC_SUPABASE_URL &&
  (process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ||
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY)
);

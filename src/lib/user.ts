/** Display helpers for the anonymous-default profile (handle, avatar). */

/** Lowercase, alphanumeric slug from a display name. */
export function slugify(name: string): string {
  return name.trim().toLowerCase().replace(/[^a-z0-9]+/g, '').slice(0, 20);
}

/** A usable @handle: stored handle, else a slug of the name, else a fallback. */
export function displayHandle(name: string, handle: string): string {
  return handle.trim() || slugify(name) || 'you';
}

/** Avatar initial from the name (falls back to a neutral glyph). */
export function initialOf(name: string): string {
  const t = name.trim();
  return t ? t[0].toUpperCase() : '·';
}

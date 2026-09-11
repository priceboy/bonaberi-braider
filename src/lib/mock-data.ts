import type { Hairstyle } from "@/lib/types";

const image = (id: string) => `https://images.unsplash.com/${id}?auto=format&fit=crop&w=1400&q=85`;

export const mockHairstyles: Hairstyle[] = [
  { id: "1", title: "Sculpted Knotless Braids", slug: "sculpted-knotless-braids", category: "Braids", caption: "Lightweight, precise and effortlessly elegant.", image_url: image("photo-1522337360788-8b13dee7a37e"), published: true, featured: true, created_at: "2026-09-06" },
  { id: "2", title: "Soft Glam Waves", slug: "soft-glam-waves", category: "Wigs", caption: "A polished finish with movement.", image_url: image("photo-1512496015851-a90fb38ba796"), published: true, featured: true, created_at: "2026-09-04" },
  { id: "3", title: "Crown Loc Style", slug: "crown-loc-style", category: "Locs", caption: "Defined texture, finished with care.", image_url: image("photo-1549236177-f9b00317542b"), published: true, featured: true, created_at: "2026-08-31" },
  { id: "4", title: "Defined Natural Curls", slug: "defined-natural-curls", category: "Natural Hair", caption: "Healthy hair, elevated texture.", image_url: image("photo-1525507119028-ed4c629a60a3"), published: true, featured: false, created_at: "2026-08-26" },
  { id: "5", title: "Signature Senegalese Twists", slug: "signature-senegalese-twists", category: "Twists", caption: "A timeless protective style.", image_url: image("photo-1508182311256-e3f7d0e5f1e2"), published: true, featured: false, created_at: "2026-08-22" },
  { id: "6", title: "Editorial Updo", slug: "editorial-updo", category: "Other", caption: "For the moments that deserve drama.", image_url: image("photo-1487412720507-e7ab37603c6f"), published: true, featured: false, created_at: "2026-08-16" },
];

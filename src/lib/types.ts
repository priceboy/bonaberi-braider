export type Category = "Braids" | "Locs" | "Twists" | "Wigs" | "Natural Hair" | "Other";

export type Hairstyle = {
  id: string;
  title: string;
  slug: string;
  category: Category;
  caption?: string;
  image_url: string;
  published: boolean;
  featured: boolean;
  created_at: string;
};

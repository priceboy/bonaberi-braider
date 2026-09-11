import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = { title: "Phanie Magic Touch | Hair artistry", description: "Luxury hair artistry in Douala, Cameroon." };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }

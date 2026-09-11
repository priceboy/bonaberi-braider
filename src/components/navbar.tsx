import Link from "next/link";
import { Menu } from "lucide-react";
import { business } from "@/lib/config";

export function Navbar() {
  return <header className="nav"><Link href="/" className="wordmark">{business.name}</Link><nav><a href="#work">Work</a><a href="#gallery">Gallery</a><a href="#visit">Visit us</a><a className="nav-cta" href="#visit">Book now</a></nav><button className="menu" aria-label="Open menu"><Menu /></button></header>;
}

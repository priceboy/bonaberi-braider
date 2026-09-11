"use client";
import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { categories } from "@/lib/config";
import type { Hairstyle } from "@/lib/types";

export function Gallery({ styles }: { styles: Hairstyle[] }) {
  const [category, setCategory] = useState<(typeof categories)[number]>("All");
  const filtered = category === "All" ? styles : styles.filter((style) => style.category === category);
  return <section id="gallery" className="gallery section"><div className="section-head"><div><p className="eyebrow">The portfolio</p><h2>Made for your<br /><em>main character</em> moment.</h2></div><p className="section-copy">Every appointment is a collaboration between your mood, your hair, and our attention to detail.</p></div><div className="filters" aria-label="Filter styles">{categories.map((item) => <button key={item} className={item === category ? "selected" : ""} onClick={() => setCategory(item)}>{item}</button>)}</div><div className="masonry">{filtered.map((style, index) => <Link className={`gallery-item item-${index % 5}`} href={`/style/${style.slug}`} key={style.id}><Image src={style.image_url} alt={style.title} fill sizes="(max-width: 700px) 50vw, 33vw" /><div><p>{style.category}</p><h3>{style.title}</h3></div></Link>)}</div></section>;
}

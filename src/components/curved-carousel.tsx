"use client";
import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import type { Hairstyle } from "@/lib/types";

export function CurvedCarousel({ styles }: { styles: Hairstyle[] }) {
  const [active, setActive] = useState(0);
  const visible = styles.slice(0, 5);
  return <section id="work" className="work section"><div className="eyebrow">Latest work</div><div className="carousel" aria-roledescription="carousel">{visible.map((style, index) => {
    const offset = index - active;
    const pos = ((offset % visible.length) + visible.length) % visible.length;
    const displayOffset = pos > Math.floor(visible.length / 2) ? pos - visible.length : pos;
    return <button key={style.id} className="carousel-card" style={{ "--x": displayOffset, "--abs": Math.abs(displayOffset) } as React.CSSProperties} onClick={() => setActive(index)} aria-label={`Show ${style.title}`} aria-current={index === active}>
      <Image src={style.image_url} alt={style.title} fill sizes="(max-width: 700px) 70vw, 31vw" />
    </button>;
  })}</div><div className="carousel-caption"><p>{visible[active]?.category}</p><h2>{visible[active]?.title}</h2><Link href={`/style/${visible[active]?.slug}`}>View this style <span>↗</span></Link></div><div className="carousel-controls">{visible.map((s, index) => <button key={s.id} onClick={() => setActive(index)} className={index === active ? "active" : ""} aria-label={`Show slide ${index + 1}`} />)}</div></section>;
}

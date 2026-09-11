import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { ArrowLeft, ArrowUpRight } from "lucide-react";
import { mockHairstyles } from "@/lib/mock-data";
import { whatsappUrl } from "@/lib/whatsapp";

export function generateStaticParams() { return mockHairstyles.map(({ slug }) => ({ slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> { const { slug } = await params; const style = mockHairstyles.find((item) => item.slug === slug); return { title: style ? `${style.title} | Phanie Magic Touch` : "Style | Phanie Magic Touch", description: style?.caption, openGraph: style ? { images: [style.image_url] } : undefined }; }
export default async function StylePage({ params }: { params: Promise<{ slug: string }> }) { const { slug } = await params; const style = mockHairstyles.find((item) => item.slug === slug); if (!style) return <main className="not-found"><h1>Style not found.</h1><Link href="/">Return home</Link></main>; return <main className="style-page"><Link href="/#gallery" className="back"><ArrowLeft size={17} /> Back to portfolio</Link><div className="style-image"><Image src={style.image_url} alt={style.title} fill priority sizes="(max-width: 800px) 100vw, 60vw" /></div><article><p className="eyebrow">{style.category}</p><h1>{style.title}</h1><p>{style.caption}</p><a className="button" href={whatsappUrl(`Hi, I'd like to book the ${style.title} hairstyle.`)} target="_blank" rel="noreferrer">Book this style <ArrowUpRight size={18} /></a></article></main>; }

import Image from "next/image";
import Link from "next/link";
import { ArrowDownRight, MapPin } from "lucide-react";
import { Navbar } from "@/components/navbar";
import { CurvedCarousel } from "@/components/curved-carousel";
import { Gallery } from "@/components/gallery";
import { WhatsAppButton } from "@/components/whatsapp-button";
import { business } from "@/lib/config";
import { mockHairstyles } from "@/lib/mock-data";
import { whatsappUrl } from "@/lib/whatsapp";

export default function Home() { const styles = mockHairstyles; return <main><div className="hero-wrap"><Navbar /><section className="hero"><div className="hero-copy"><p className="eyebrow">Douala · Cameroon</p><h1>{business.heroTitle}<br /><em>Made to be remembered.</em></h1><p className="hero-text">{business.heroText}</p><a href="#gallery" className="button">Explore our work <ArrowDownRight size={18} /></a></div><div className="hero-image"><Image src={styles[0].image_url} alt="A featured hairstyle by Phanie Magic Touch" fill priority sizes="(max-width: 800px) 100vw, 50vw" /><div className="hero-stamp">EST.<br />2026</div></div><p className="hero-note">Scroll to discover<br />our signature work <span>↓</span></p></section></div><CurvedCarousel styles={styles} /><Gallery styles={styles} /><section id="visit" className="visit section"><div><p className="eyebrow">Visit the studio</p><h2>Beauty, with<br /><em>intention.</em></h2><p className="section-copy">A calm, considered space to reset, be cared for, and leave feeling unmistakably like yourself.</p></div><div className="visit-card"><MapPin size={22} /><p>{business.address}</p><div className="hours">{business.hours.map((hour) => <span key={hour}>{hour}</span>)}</div><a className="text-link" href={business.directionsUrl} target="_blank" rel="noreferrer">Get directions <span>↗</span></a></div></section><section className="book"><p className="eyebrow">Your hair deserves the moment</p><h2>Let’s create<br /><em>something beautiful.</em></h2><a className="button light" href={whatsappUrl()} target="_blank" rel="noreferrer">Book an appointment <ArrowDownRight size={18} /></a></section><footer><Link href="/" className="wordmark">{business.name}</Link><p>Hair artistry for every version of you.</p><a href={business.instagramUrl} target="_blank" rel="noreferrer">Instagram ↗</a><Link href="/admin">Studio login</Link></footer><WhatsAppButton /></main>; }

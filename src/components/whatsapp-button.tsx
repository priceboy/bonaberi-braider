import { MessageCircle } from "lucide-react";
import { whatsappUrl } from "@/lib/whatsapp";

export function WhatsAppButton() {
  return <a className="whatsapp" href={whatsappUrl()} target="_blank" rel="noreferrer" aria-label="Chat with us on WhatsApp"><MessageCircle size={20} /><span>Chat with us</span></a>;
}

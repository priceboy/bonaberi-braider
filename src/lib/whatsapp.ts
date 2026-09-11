import { business } from "@/lib/config";

export function whatsappUrl(message = "Hi, I'd like to book an appointment.") {
  return `https://wa.me/${business.whatsappNumber.replace(/\D/g, "")}?text=${encodeURIComponent(message)}`;
}

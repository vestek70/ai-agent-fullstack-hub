import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI Agent Fullstack Hub | DeepSeek V4 + Next.js + Python",
  description: "Agente Autônomo de IA com Tool Calling (SQL e APIs externas) desenvolvido em Next.js 16, Python FastAPI, DeepSeek V4 e Nous Hermes com UI em Tailwind CSS.",
  keywords: ["AI Agent", "DeepSeek V4", "Next.js", "Python", "FastAPI", "Hermes", "Tool Calling", "Tailwind CSS", "Portfólio"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR" className={`${geistSans.variable} ${geistMono.variable} dark`}>
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}

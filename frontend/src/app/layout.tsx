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
  title: "AI Agent Fullstack Hub | Next.js + Python + Tailwind",
  description: "Autonomous AI Agent with Tool Calling (SQL & External APIs) built on Next.js, Python FastAPI, Gemini & Hermes.",
  keywords: ["AI Agent", "Next.js", "Python", "FastAPI", "Gemini", "Hermes", "Tool Calling", "Tailwind CSS"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru" className={`${geistSans.variable} ${geistMono.variable} dark`}>
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased selection:bg-cyan-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}

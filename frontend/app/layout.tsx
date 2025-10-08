import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Resumaker - AI-Powered Resume Builder",
  description: "Build truthful, ATS-optimized resumes with AI assistance",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

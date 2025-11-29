import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RBT166 Travel Booking",
  description: "Travel booking platform powered by Amadeus API",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}

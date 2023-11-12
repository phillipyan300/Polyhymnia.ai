import React from 'react';
import { getServerSession } from "next-auth";
import { authOptions } from "./api/auth/[...nextauth]/route";

export default function Home() {
  const session = getServerSession(authOptions);
  return (
    <main className="flex flex-col items-center justify-center min-h-screen py-12 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-3">Learn, Play, and Improve with Polyhymnia.ai</h1>
      <p className="text-xl mb-6">Discover and develop your skills with your favorite instrument with us!</p>
      {/* Additional content can be added here */}
      <img src = "/IMG_2337.png" alt ="App Logo"></img>
    </main>
  );
}

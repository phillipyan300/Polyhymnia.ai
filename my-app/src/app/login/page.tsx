"use client";
import React, { useEffect, useState } from "react";
import Link from "next/link";
import { signIn, useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

const Login = () => {
  const router = useRouter();
  const [error, setError] = useState("");
  const { data: session, status: sessionStatus } = useSession();
  

  useEffect(() => {
    if (sessionStatus === "authenticated") {
      router.replace("/dashboard");
    }
  }, [sessionStatus, router]);

  const isValidEmail = (email: string) => {
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    return emailRegex.test(email);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    const email = e.target[0].value;
    const password = e.target[1].value;

    if (!isValidEmail(email)) {
      setError("Email is invalid");
      return;
    }

    if (!password || password.length < 8) {
      setError("Password is invalid");
      return;
    }

    const res = await signIn("credentials", {
      redirect: false,
      email,
      password,
    });

    if (res?.error) {
      setError("Invalid email or password");
      if (res?.url) router.replace("/dashboard");
    } else {
      setError("");
    }
  };

  if (sessionStatus === "loading") {
    return <h1>Loading...</h1>;
  }

  
  return (
    sessionStatus !== "authenticated" && (
      <div className="flex min-h-screen flex-col items-center justify-center bg-white">
        <div className="absolute top-4 left-4 flex items-center">
          {/* Icon and Text - Adjust as needed */}
        </div>
        <div className="p-8 rounded-lg shadow-md w-full max-w-md">
          <h1 className="text-black text-5xl text-center font-semibold mb-8">Login</h1>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              className="w-full border border-black bg-white text-black rounded px-3 py-2 focus:outline-none focus:border-blue-400"
              placeholder="Email"
              required
            />
            <input
              type="password"
              className="w-full border border-black bg-white text-black rounded px-3 py-2 focus:outline-none focus:border-blue-400"
              placeholder="Password"
              required
            />
            <button
              type="submit"
              className="w-full bg-white text-black py-2 rounded hover:bg-gray-800 hover:text-white"
            >
              Sign In
            </button>
            <p className="text-white text-lg text-center">{error && error}</p>
          </form>
          <div className="text-center text-gray-500 mt-4">- OR -</div>
          <Link legacyBehavior href="/register">
            <a className="block text-center text-blue-500 hover:underline mt-2">
              Register Here
            </a>
          </Link>
        </div>
      </div>
    )
  );
};

export default Login;

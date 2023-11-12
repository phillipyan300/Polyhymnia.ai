"use client";
import React from "react";
import Link from "next/link";
import { signOut, useSession } from "next-auth/react";
import { useRouter } from 'next/router';





const Navbar = () => {


  
  const { data: session } = useSession();


  const sendProficiencyScore = async () => {
    // Check if there's a session and a proficiencyScore
    console.log(session.user?.proficiencyScore?.toFixed(2))
    if (session && session.user && session.user.proficiencyScore) {
      try {
        // Make a POST request to your Flask endpoint
        const response = await fetch('YOUR_FLASK_ENDPOINT', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          // Make sure to stringify your payload
          body: JSON.stringify({
            proficiencyScore: session.user?.proficiencyScore?.toFixed(2)
          }),
        });

        // Handle response from Flask
        if (response.ok) {
          console.log('Score sent successfully');
          // You can add more logic here, such as redirecting or showing a message
        } else {
          // Handle any errors if the server doesn't respond with a success
          throw new Error('Failed to send score');
        }
      } catch (error) {
        // Handle any exceptions during fetch
        console.error('Error sending score:', error);
      }
    }
  };

  return (
    <div>
      <ul className="flex justify-between m-10 item-center">
        <div>
          <Link href="/">
            <li>Home</li>
          </Link>
        </div>
        <div className="flex gap-10">
          <Link href="/dashboard">
           <li>Dashboard</li>
          </Link>
          {!session ? (
            <>
              <Link href="/login">
                <li>Login</li>
              </Link>
              <Link href="/register">
                <li>Register</li>
              </Link>
            </>
          ) : (
            <>
              <span>{session.user?.email} (Score: {session.user?.proficiencyScore?.toFixed(2)})</span>
                <li>
                  <Link href="/train">
                    <li
                      onClick={sendProficiencyScore}
                    >Train</li>
                  </Link>
                <button
                  onClick={() => signOut()}
                  className="p-2 px-5 -mt-1 bg-blue-800 rounded-full"
                >
                  Logout
                </button>
              </li>
            </>
          )}
        </div>
      </ul>
    </div>
  );
};

export default Navbar;

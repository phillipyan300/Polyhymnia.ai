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
        const response = await fetch('http://127.0.0.1:5000/generate-image', {
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
          <div className="bg-gray-800 text-white shadow-lg">
<ul className="flex justify-between items-center py-4 px-10">
          <div>
          <Link href="/">
            <li className="text-xl font-semibold hover:text-blue-300">Home</li>
          </Link>
        </div>
        <div className="flex items-center gap-8">
          {!session ? (
            <>
              <Link 
              href="/login">
                <li               className="hover:text-blue-300"
>Login</li>
              </Link>
              <Link 
              
              href="/register">
                <li className="hover:text-blue-300">Register</li>
              </Link>
            </>
          ) : (
            <>
              <span>{session.user?.email}</span>
                <li>
                  <Link href="/train">
                    <li className="ver:text-blue-300"
                      onClick={sendProficiencyScore}
                    >Train
                    </li>
                  </Link>
                  </li>
                  <li>
                <button
                  onClick={() => signOut()}
                  className="text-sm p-2 bg-blue-600 hover:bg-blue-700 rounded-full transition duration-300"
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
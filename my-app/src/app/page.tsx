import { getServerSession } from "next-auth";
import { authOptions } from "./api/auth/[...nextauth]/route";
export default function Home() {
  const session = getServerSession(authOptions);
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Home Page</h1>
    </main>
  );
}



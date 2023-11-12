import NextAuth, { Account, NextAuthOptions, User as NextAuthUser, Profile } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";
import User from "@/models/User";
import connect from "@/utils/db";
import { JWT } from "next-auth/jwt";

export const authOptions: NextAuthOptions= {
  providers: [
    CredentialsProvider({
      id: "credentials",
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials: any) {
        await connect();
        try {
          const user = await User.findOne({ email: credentials.email });
          if (user) {
            const isPasswordCorrect = await bcrypt.compare(
              credentials.password,
              user.password
            );
            if (isPasswordCorrect) {
              return user;
            }
          }
        } catch (err: any) {
          throw new Error(err);
        }
      },
    }),
    // ...add more providers here
  ],
  callbacks: {
    // Add callbacks if needed
    jwt: async ({ token, user, account, profile }:{token: JWT, user: NextAuthUser, account?: (Account | null) , profile?: Profile}) => {
      console.log(token, user, account)
      try {
        const user_ = await User.findOne({ email: token.email });
        token.proficiencyScore= user_.proficiencyScore
      } catch (err) {
        throw new Error(err as any);
      }
      return token
    },
    async session({ session, user, token }) {
      // @ts-ignore
      session.user.proficiencyScore = token.proficiencyScore
      return session
    },
  },
};

export const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };

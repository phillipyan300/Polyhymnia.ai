import { getSession } from "next-auth/react";
import User from "@/models/User";
import connect from "@/utils/db";

export default async function handler(req: any, res: any) {
  // Check for user session
  const session = await getSession({ req });
  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  // Handle POST request
  if (req.method === 'POST') {
    const { score } = req.body; // 'score' is a decimal value
    console.log(score);
    await connect();

    try {
      const email = session.user?.email;
      const user = await User.findOne({ email });

      // Calculate new proficiencyScore
      let newScore = user.proficiencyScore + (score-0.5 * 0.05) * (1-user.proficiencyScore);
      console.log(newScore);

      // Update user's proficiency score
      const updatedUser = await User.findOneAndUpdate(
        { email },
        { $set: { proficiencyScore: newScore }},
        { new: true }
      );

      return res.status(200).json({ message: 'Proficiency score updated', user: updatedUser });
    } catch (error) {
      return res.status(500).json({ error: 'Error connecting to database' });
    }
  } else {
    // Handle other methods as not allowed
    return res.status(405).json({ error: 'Method not allowed' });
  }
}

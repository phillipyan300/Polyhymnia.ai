import { getSession } from "next-auth/react";
import User from "@/models/User";
import connect from "@/utils/db";

export default async (req : any, res : any) => {
  const session = await getSession({ req });

  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (req.method === 'POST') {
    const { change } = req.body; // change is a decimal value
    await connect();

    try {
      const email = session.user?.email;
      const user = await User.findOne({ email: email });

      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

        // Calculate new proficiencyScore
        // let curr = 0.05

      let newScore = user.proficiencyScore + (change * 0.05) * (1-user.proficiencyScore);

      const updatedUser = await User.findOneAndUpdate(
        { email: email },
        { $set: { proficiencyScore: newScore }},
        { new: true }
      );

      return res.status(200).json({ message: 'Proficiency score updated', user: updatedUser });
    } catch (error) {
      return res.status(500).json({ error: 'Error connecting to email' });
    }
  } else {
    return res.status(405).json({ error: 'Method not allowed' });
  }
};

import mongoose from "mongoose";

const { Schema } = mongoose;

const userSchema = new Schema(
  {
    email: {
      type: String,
      unique: true,
      required: true,
    },
    password: {
      type: String,
      required: false,
    },
    proficiencyScore: {
      type: Number,
      default: 0.5,
    },
  }
);

export default mongoose.models.User || mongoose.model("User", userSchema);

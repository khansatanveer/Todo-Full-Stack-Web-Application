import { betterAuth } from "better-auth";

const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  database: {
    provider: "sqlite",
    url: process.env.DATABASE_URL || "./auth.db",
  },
  emailAndPassword: {
    enabled: true,
  },
  user: {
    additionalFields: {
      name: {
        type: "string",
        required: false,
      }
    }
  },
});

export { auth };
export default auth;
import { betterAuth } from "better-auth";

const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "fallback-secret-for-development",
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || 'postgresql://neondb_owner:npg_Fyh73cvSPZgJ@ep-restless-forest-ah925lio-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
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
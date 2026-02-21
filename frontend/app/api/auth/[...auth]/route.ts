import { auth } from "@/app/lib/better-auth";

// This API route handles all Better Auth requests
export const GET = auth.handler;
export const POST = auth.handler;
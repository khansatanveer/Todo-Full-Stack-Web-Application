import { auth } from "../../../lib/better-auth";
import { toNextJsHandler } from "better-auth/next-js";

// This API route handles all Better Auth requests
export const { GET, POST } = toNextJsHandler(auth);
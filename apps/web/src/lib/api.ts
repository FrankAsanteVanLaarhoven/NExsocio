import type {
  ApiResponse,
  ConnectionsListResponse,
  CreatePostRequest,
  FeedResponse,
  FeedType,
  ModeSelectRequest,
  ModeSelectResponse,
  Post,
  ProfessionalDashboard,
  ProfessionalProfile,
  PublicUser,
  RegisterRequest,
  RegisterResponse,
  UpdateProfileRequest,
  UserMode,
  UserProfile,
  ViewContext,
  ZKPAgeProof,
} from "@nexus/types";

const IDENTITY_URL = process.env.NEXT_PUBLIC_IDENTITY_URL || "http://localhost:8001";
const SOCIAL_URL = process.env.NEXT_PUBLIC_SOCIAL_URL || "http://localhost:8002";
const CONTENT_URL = process.env.NEXT_PUBLIC_CONTENT_URL || "http://localhost:8003";
const PROFESSIONAL_URL = process.env.NEXT_PUBLIC_PROFESSIONAL_URL || "http://localhost:8004";

async function request<T>(
  baseUrl: string,
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const res = await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const text = await res.text();
  let json: unknown;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    throw new Error(text || `Request failed: ${res.status}`);
  }

  if (!res.ok) {
    const body = json as { detail?: string | { msg: string }[]; error?: string };
    const detail = body.detail;
    const message =
      typeof detail === "string"
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join(", ")
          : body.error || `Request failed: ${res.status}`;
    throw new Error(message);
  }

  const response = json as ApiResponse<T>;
  if (!response.success) {
    throw new Error(response.error || `Request failed: ${res.status}`);
  }

  if (response.data === null) {
    throw new Error("Empty response data");
  }

  return response.data;
}

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}` };
}

export async function generateStubProof(isAdult = true): Promise<ZKPAgeProof> {
  return request<ZKPAgeProof>(IDENTITY_URL, `/api/v1/zkp/stub-proof?is_adult=${isAdult}`, {
    method: "POST",
  });
}

export async function register(data: RegisterRequest): Promise<RegisterResponse> {
  return request<RegisterResponse>(IDENTITY_URL, "/api/v1/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function selectMode(token: string, mode: UserMode): Promise<ModeSelectResponse> {
  const body: ModeSelectRequest = { mode };
  return request<ModeSelectResponse>(IDENTITY_URL, "/api/v1/auth/mode", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(body),
  });
}

export async function getMe(token: string): Promise<UserProfile> {
  return request<UserProfile>(IDENTITY_URL, "/api/v1/users/me", {
    headers: authHeaders(token),
  });
}

export async function updateProfile(
  token: string,
  data: UpdateProfileRequest
): Promise<UserProfile> {
  return request<UserProfile>(IDENTITY_URL, "/api/v1/users/me", {
    method: "PUT",
    headers: authHeaders(token),
    body: JSON.stringify(data),
  });
}

export async function searchUsers(query: string): Promise<PublicUser[]> {
  return request<PublicUser[]>(
    IDENTITY_URL,
    `/api/v1/users/search?q=${encodeURIComponent(query)}`
  );
}

export async function createPost(token: string, data: CreatePostRequest): Promise<Post> {
  return request<Post>(CONTENT_URL, "/api/v1/posts", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(data),
  });
}

export async function getFeed(
  token: string,
  opts: {
    feedType?: FeedType;
    context?: ViewContext;
    mode?: UserMode;
  } = {}
): Promise<FeedResponse> {
  const params = new URLSearchParams();
  if (opts.feedType) params.set("feed_type", opts.feedType);
  if (opts.context) params.set("context", opts.context);
  if (opts.mode) params.set("mode", opts.mode);
  const qs = params.toString() ? `?${params}` : "";
  return request<FeedResponse>(CONTENT_URL, `/api/v1/feed${qs}`, {
    headers: authHeaders(token),
  });
}

export async function getConnections(token: string): Promise<ConnectionsListResponse> {
  return request<ConnectionsListResponse>(SOCIAL_URL, "/api/v1/connections", {
    headers: authHeaders(token),
  });
}

export async function requestConnection(
  token: string,
  recipientId: string
): Promise<void> {
  await request(SOCIAL_URL, "/api/v1/connections", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify({ recipient_id: recipientId }),
  });
}

export async function acceptConnection(token: string, connectionId: string): Promise<void> {
  await request(SOCIAL_URL, `/api/v1/connections/${connectionId}/accept`, {
    method: "POST",
    headers: authHeaders(token),
  });
}

export async function getProfessionalProfile(token: string): Promise<ProfessionalProfile> {
  return request<ProfessionalProfile>(PROFESSIONAL_URL, "/api/v1/profile", {
    headers: authHeaders(token),
  });
}

export async function getProfessionalDashboard(token: string): Promise<ProfessionalDashboard> {
  return request<ProfessionalDashboard>(PROFESSIONAL_URL, "/api/v1/dashboard", {
    headers: authHeaders(token),
  });
}
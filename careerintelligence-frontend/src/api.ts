import type { UserRole } from "./auth/AuthContext";

const API_URL = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8001/api/"
).replace(/\/?$/, "/");

export interface ApiUser {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  phone_number: string | null;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface AuthResponse {
  message: string;
  user: ApiUser;
  tokens: AuthTokens;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

function getErrorMessage(data: unknown): string {
  if (typeof data === "string") return data;

  if (Array.isArray(data)) {
    return data.map(getErrorMessage).join(" ");
  }

  if (data && typeof data === "object") {
    const record = data as Record<string, unknown>;

    if (typeof record.detail === "string") return record.detail;
    if (typeof record.message === "string") return record.message;

    return Object.entries(record)
      .map(([key, value]) => `${key}: ${getErrorMessage(value)}`)
      .join(" | ");
  }

  return "Something went wrong. Please try again.";
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  } catch {
    throw new Error(
      "Cannot connect to the backend. Make sure the Django server is running on port 8001.",
    );
  }

  const data: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(getErrorMessage(data) || `Request failed (${response.status}).`);
  }

  return data as T;
}

export function registerAccount(
  payload: Record<string, string>,
): Promise<AuthResponse> {
  return request<AuthResponse>("auth/register/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function loginAccount(
  username: string,
  password: string,
): Promise<LoginResponse> {
  return request<LoginResponse>("auth/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export function getCurrentUser(accessToken: string): Promise<ApiUser> {
  return request<ApiUser>("auth/me/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export const api = {
  async getStatus() {
    return request<Record<string, unknown>>("");
  },
};

export interface StudentProfileData {
  id: number;
  university: number | null;
  programme: string;
  education_level: string;
  graduation_year: number | null;
  experience_years: string | null;
  interests: string[];
  location: string;
  bio: string;
}

export interface StudentProfileUpdateResponse {
  message: string;
  profile: StudentProfileData;
}

export function getStudentProfile(
  accessToken: string,
): Promise<StudentProfileData> {
  return request<StudentProfileData>("student/profile/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export function updateStudentProfile(
  accessToken: string,
  payload: Partial<Omit<StudentProfileData, "id">>,
): Promise<StudentProfileUpdateResponse> {
  return request<StudentProfileUpdateResponse>("student/profile/", {
    method: "PATCH",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify(payload),
  });
}

export interface StudentDocument {
  id: number;
  document_type: "cv" | "transcript" | "certificate" | "other";
  original_filename: string;
  mime_type: string;
  size_bytes: number | null;
  extraction_status: "pending" | "processing" | "completed" | "failed";
  review_status: "pending" | "reviewed" | "verified" | "rejected";
  uploaded_at: string;
}

export interface StudentDocumentUploadResponse {
  message: string;
  document: StudentDocument;
}

async function documentRequest<T>(
  endpoint: string,
  accessToken: string,
  options: RequestInit = {},
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${accessToken}`,
        ...options.headers,
      },
    });
  } catch {
    throw new Error(
      "Cannot connect to Django. Make sure the backend is running on port 8001.",
    );
  }

  const data: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      getErrorMessage(data) || `Document request failed (${response.status}).`,
    );
  }

  return data as T;
}

export function getStudentDocuments(
  accessToken: string,
): Promise<StudentDocument[]> {
  return documentRequest<StudentDocument[]>(
    "student/documents/",
    accessToken,
  );
}

export function uploadStudentDocument(
  accessToken: string,
  file: File,
  documentType: StudentDocument["document_type"],
): Promise<StudentDocumentUploadResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("document_type", documentType);

  return documentRequest<StudentDocumentUploadResponse>(
    "student/documents/",
    accessToken,
    {
      method: "POST",
      body: formData,
    },
  );
}

// ==========================================
// STUDENT SKILLS API
// ==========================================

export interface SkillCatalogueItem {
  id: number;
  name: string;
  category: string;
  description: string;
}

export interface StudentSkillRecord {
  id: number;
  skill: number;
  level: number | null;
  verified: boolean;
  source: string;
  evidence_description: string;
  created_at: string;
  updated_at: string;
}

export function getSkillCatalogue(
  accessToken: string,
): Promise<SkillCatalogueItem[]> {
  return request<SkillCatalogueItem[]>("skills/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export function getStudentSkills(
  accessToken: string,
): Promise<StudentSkillRecord[]> {
  return request<StudentSkillRecord[]>("student/skills/", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
}

export interface AddStudentSkillPayload {
  skill: number;
  level: number | null;
  evidence_description: string;
}

export interface AddStudentSkillResponse {
  message: string;
  skill: StudentSkillRecord;
}

export function addStudentSkill(
  accessToken: string,
  payload: AddStudentSkillPayload,
): Promise<AddStudentSkillResponse> {
  return request<AddStudentSkillResponse>("student/skills/", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}
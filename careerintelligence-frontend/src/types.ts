export interface Career {
  id: string;
  title: string;
  description: string;
  compatibility: number;
  demand: "High" | "Growing" | "Stable";
  skills: string[];
}

export interface Skill {
  name: string;
  level: number;
  target: number;
  evidence: string;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  match: number;
  skills: string[];
}

export interface StudentProfile {
  name: string;
  programme: string;
  university: string;
  targetCareer: string;
}
import type { Career, Job, Skill, StudentProfile } from "../types";

export const studentProfile: StudentProfile = {
  name: "Alex Student",
  programme: "BSc Information Technology",
  university: "University Student",
  targetCareer: "Data Analyst"
};

export const careers: Career[] = [
  {
    id: "data-analyst",
    title: "Data Analyst",
    description: "Analyze data, identify patterns and communicate evidence-based insights.",
    compatibility: 78,
    demand: "High",
    skills: ["SQL", "Excel", "Power BI", "Statistics", "Data Visualization"]
  },
  {
    id: "software-developer",
    title: "Software Developer",
    description: "Design, build, test and maintain software applications.",
    compatibility: 72,
    demand: "High",
    skills: ["Python", "JavaScript", "Git", "APIs", "Databases"]
  },
  {
    id: "cybersecurity-analyst",
    title: "Cybersecurity Analyst",
    description: "Monitor systems, investigate threats and improve information security.",
    compatibility: 64,
    demand: "Growing",
    skills: ["Networking", "Linux", "Security", "Risk Analysis", "Incident Response"]
  }
];

export const skills: Skill[] = [
  { name: "Excel", level: 82, target: 80, evidence: "Academic coursework" },
  { name: "SQL", level: 65, target: 85, evidence: "Practical project" },
  { name: "Power BI", level: 42, target: 80, evidence: "Self-reported" },
  { name: "Statistics", level: 70, target: 75, evidence: "Academic coursework" },
  { name: "Data Visualization", level: 55, target: 80, evidence: "Project evidence" }
];

export const jobs: Job[] = [
  {
    id: "job-1",
    title: "Junior Data Analyst",
    company: "Example Analytics Ltd",
    location: "Nairobi, Kenya",
    match: 82,
    skills: ["Excel", "SQL", "Power BI"]
  },
  {
    id: "job-2",
    title: "Graduate Data Associate",
    company: "Example Digital",
    location: "Nairobi, Kenya",
    match: 76,
    skills: ["Statistics", "SQL", "Data Visualization"]
  },
  {
    id: "job-3",
    title: "Business Intelligence Intern",
    company: "Example Technologies",
    location: "Hybrid",
    match: 71,
    skills: ["Power BI", "Excel", "Reporting"]
  }
];
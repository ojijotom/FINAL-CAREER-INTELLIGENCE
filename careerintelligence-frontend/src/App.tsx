import { Navigate, Route, Routes } from "react-router-dom";
import AuthLayout from "./layouts/AuthLayout";
import StudentLayout from "./layouts/StudentLayout";
import EmployerLayout from "./layouts/EmployerLayout";
import UniversityLayout from "./layouts/UniversityLayout";
import ProtectedRoute from "./auth/ProtectedRoute";
import LandingPage from "./pages/LandingPage";
import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

import Dashboard from "./pages/student/Dashboard";
import Careers from "./pages/student/Careers";
import CareerDetail from "./pages/student/CareerDetail";
import Skills from "./pages/student/Skills";
import SkillGap from "./pages/student/SkillGap";
import Jobs from "./pages/student/Jobs";
import JobDetail from "./pages/student/JobDetail";
import Profile from "./pages/student/Profile";
import Settings from "./pages/student/Settings";

import EmployerDashboard from "./pages/employer/EmployerDashboard";
import CompanyProfile from "./pages/employer/CompanyProfile";
import PostJob from "./pages/employer/PostJob";
import MyJobs from "./pages/employer/MyJobs";
import Candidates from "./pages/employer/Candidates";
import Applications from "./pages/employer/Applications";
import TalentSearch from "./pages/employer/TalentSearch";
import CandidateProfile from "./pages/employer/CandidateProfile";
import EmployerSettings from "./pages/employer/EmployerSettings";
import Evidence from "./pages/student/Evidence";
import CVUpload from "./pages/student/CVUpload";
import TranscriptUpload from "./pages/student/TranscriptUpload";

import UniversityDashboard from "./pages/university/Dashboard";
import { useEffect, useState } from "react";
import { api } from "./api";

export default function App() {
  const [status, setStatus] = useState("Connecting");

  useEffect(() => {
    api.getStatus()
      .then(data => setStatus(data.message))
      .catch(error => setStatus(error.message));
  }, []);
  
  return (
    <div>
      <h1>Career Intelligence</h1>
      <p>{status}</p>
    </div>
  );

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />

      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Route>

      <Route element={<ProtectedRoute allowedRole="student" />}>
        <Route path="/student" element={<StudentLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="careers" element={<Careers />} />
          <Route path="careers/:careerId" element={<CareerDetail />} />
          <Route path="skills" element={<Skills />} />
           <Route path="evidence" element={<Evidence />} />
          <Route path="cv-upload" element={<CVUpload />} />
          <Route path="transcript-upload" element={<TranscriptUpload />} />
          <Route path="skill-gap" element={<SkillGap />} />
          <Route path="jobs" element={<Jobs />} />
          <Route path="jobs/:jobId" element={<JobDetail />} />
          <Route path="profile" element={<Profile />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Route>

      <Route element={<ProtectedRoute allowedRole="employer" />}>
        <Route path="/employer" element={<EmployerLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<EmployerDashboard />} />
          <Route path="company" element={<CompanyProfile />} />
          <Route path="post-job" element={<PostJob />} />
          <Route path="jobs" element={<MyJobs />} />
          <Route path="candidates" element={<Candidates />} />
          <Route path="applications" element={<Applications />} />
          <Route path="talent-search" element={<TalentSearch />} />
          <Route path="candidate/:candidateId" element={<CandidateProfile />} />
          <Route path="settings" element={<EmployerSettings />} />
        </Route>
      </Route>

      <Route element={<ProtectedRoute allowedRole="university" />}>
        <Route path="/university" element={<UniversityLayout />}>
          <Route index element={<Navigate to="dashboard" replace />} />
          <Route path="dashboard" element={<UniversityDashboard />} />
        </Route>
      </Route>

      <Route path="/dashboard" element={<Navigate to="/student/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}






import { Link } from "react-router-dom";

export default function Evidence() {
  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-6xl">

        {/* Header */}
        <div className="mb-8">
          <p className="text-sm font-semibold uppercase tracking-wider text-blue-600">
            Student Profile
          </p>

          <h1 className="mt-2 text-3xl font-bold text-slate-900">
            My Evidence
          </h1>

          <p className="mt-2 max-w-2xl text-slate-600">
            Upload and manage the academic, professional and project evidence
            that helps Career Intelligence understand your skills.
          </p>
        </div>

        {/* Progress */}
        <div className="mb-8 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-semibold text-slate-900">
                Profile evidence
              </h2>
              <p className="mt-1 text-sm text-slate-500">
                Complete your evidence profile to improve your recommendations.
              </p>
            </div>

            <span className="text-lg font-bold text-blue-600">
              20%
            </span>
          </div>

          <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-200">
            <div
              className="h-full rounded-full bg-blue-600"
              style={{ width: "20%" }}
            />
          </div>
        </div>

        {/* Evidence cards */}
        <div className="grid gap-6 md:grid-cols-2">

          {/* CV */}
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <div className="mb-4 flex items-start justify-between">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-2xl">
                📄
              </div>

              <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">
                Not uploaded
              </span>
            </div>

            <h2 className="text-xl font-bold text-slate-900">
              CV / Resume
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              Upload your latest CV so the system can identify your education,
              experience, projects and skills.
            </p>

            <Link
              to="/cv-upload"
              className="mt-5 inline-flex rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-blue-700"
            >
              Upload CV
            </Link>
          </div>

          {/* Transcript */}
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <div className="mb-4 flex items-start justify-between">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-purple-100 text-2xl">
                🎓
              </div>

              <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-700">
                Not uploaded
              </span>
            </div>

            <h2 className="text-xl font-bold text-slate-900">
              Academic Transcript
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              Upload your transcript so courses and academic performance can
              later be mapped to relevant skills.
            </p>

            <Link
              to="/transcript-upload"
              className="mt-5 inline-flex rounded-xl bg-purple-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-purple-700"
            >
              Upload Transcript
            </Link>
          </div>

          {/* Certificates */}
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-100 text-2xl">
              🏆
            </div>

            <h2 className="text-xl font-bold text-slate-900">
              Certificates
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              Add professional certificates and training records that provide
              additional evidence of your skills.
            </p>

            <button
              disabled
              className="mt-5 cursor-not-allowed rounded-xl bg-slate-200 px-5 py-3 text-sm font-semibold text-slate-500"
            >
              Coming soon
            </button>
          </div>

          {/* Projects */}
          <div className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-orange-100 text-2xl">
              💼
            </div>

            <h2 className="text-xl font-bold text-slate-900">
              Projects & Experience
            </h2>

            <p className="mt-2 text-sm leading-6 text-slate-600">
              Add projects, internships and work experience to provide
              practical evidence of your capabilities.
            </p>

            <button
              disabled
              className="mt-5 cursor-not-allowed rounded-xl bg-slate-200 px-5 py-3 text-sm font-semibold text-slate-500"
            >
              Coming soon
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
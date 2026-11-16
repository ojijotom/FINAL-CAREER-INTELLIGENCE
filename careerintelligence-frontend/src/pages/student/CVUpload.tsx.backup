import { useState } from "react";
import { Link } from "react-router-dom";

export default function CVUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];

    if (!allowedTypes.includes(selectedFile.type)) {
      setFile(null);
      setMessage("Please select a PDF, DOC or DOCX file.");
      return;
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setFile(null);
      setMessage("The file must be smaller than 5 MB.");
      return;
    }

    setFile(selectedFile);
    setMessage("");
  };

  const handleUpload = () => {
    if (!file) {
      setMessage("Please select your CV first.");
      return;
    }

    setMessage(
      "CV selected successfully. Permanent upload will be connected to the backend later."
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-3xl">

        <Link
          to="/evidence"
          className="text-sm font-semibold text-blue-600 hover:text-blue-700"
        >
          ← Back to My Evidence
        </Link>

        <div className="mt-6 rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">

          <div className="text-center">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-blue-100 text-3xl">
              📄
            </div>

            <h1 className="mt-5 text-3xl font-bold text-slate-900">
              Upload your CV
            </h1>

            <p className="mx-auto mt-3 max-w-xl text-slate-600">
              Your CV can help us understand your education, experience,
              projects and existing skills.
            </p>
          </div>

          <label className="mt-8 flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 p-10 text-center transition hover:border-blue-400 hover:bg-blue-50">

            <span className="text-4xl">⬆️</span>

            <span className="mt-4 text-lg font-semibold text-slate-800">
              Choose your CV
            </span>

            <span className="mt-2 text-sm text-slate-500">
              PDF, DOC or DOCX · Maximum 5 MB
            </span>

            <input
              type="file"
              accept=".pdf,.doc,.docx"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          {file && (
            <div className="mt-6 rounded-xl bg-blue-50 p-4">
              <p className="font-semibold text-slate-900">
                Selected file
              </p>

              <p className="mt-1 text-sm text-slate-600">
                {file.name}
              </p>

              <p className="mt-1 text-xs text-slate-500">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          )}

          {message && (
            <div className="mt-5 rounded-xl bg-slate-100 p-4 text-sm text-slate-700">
              {message}
            </div>
          )}

          <button
            onClick={handleUpload}
            className="mt-6 w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700"
          >
            Upload CV
          </button>

          <p className="mt-5 text-center text-xs leading-5 text-slate-500">
            In the backend phase, uploaded documents will be validated,
            securely stored and processed according to the system's privacy
            requirements.
          </p>

        </div>
      </div>
    </div>
  );
}
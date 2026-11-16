import { useState, type ChangeEvent } from "react";
import { Link } from "react-router-dom";
import { uploadStudentDocument } from "../../api";
import { useAuth } from "../../auth/AuthContext";

export default function CVUpload() {
  const { accessToken } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (!selectedFile) return;

    const extension = selectedFile.name.split(".").pop()?.toLowerCase();

    if (!["pdf", "docx"].includes(extension || "")) {
      setFile(null);
      setMessage("Only PDF and DOCX files are accepted.");
      return;
    }

    if (selectedFile.size === 0 || selectedFile.size > 5 * 1024 * 1024) {
      setFile(null);
      setMessage("Choose a non-empty file no larger than 5 MB.");
      return;
    }

    setFile(selectedFile);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select your CV first.");
      return;
    }

    if (!accessToken) {
      setMessage("Your session has expired. Please log in again.");
      return;
    }

    setUploading(true);
    setMessage("");

    try {
      const result = await uploadStudentDocument(accessToken, file, "cv");
      setMessage(`Success: ${result.document.original_filename} was uploaded. Review status: ${result.document.review_status}.`);
      setFile(null);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "CV upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-6">
      <div className="mx-auto max-w-3xl">
        <Link to="/evidence" className="text-sm font-semibold text-blue-600 hover:text-blue-700">
          &larr; Back to My Evidence
        </Link>

        <div className="mt-8 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
          <h1 className="text-2xl font-bold text-slate-900">Upload your CV / Resume</h1>
          <p className="mt-2 text-sm text-slate-600">
            Select your latest CV. Accepted formats: PDF and DOCX. Maximum size: 5 MB.
          </p>

          <label className="mt-6 flex cursor-pointer flex-col items-center rounded-xl border-2 border-dashed border-slate-300 p-8 text-center hover:border-blue-500">
            <span className="text-lg font-semibold text-slate-800">Choose your CV</span>
            <span className="mt-2 text-sm text-slate-500">PDF or DOCX · Maximum 5 MB</span>
            <input
              type="file"
              accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              onChange={handleFileChange}
              className="hidden"
            />
          </label>

          {file && (
            <div className="mt-6 rounded-xl bg-blue-50 p-4">
              <p className="font-semibold text-slate-900">Selected file</p>
              <p className="mt-1 text-sm text-slate-600">{file.name}</p>
              <p className="mt-1 text-xs text-slate-500">
                {(file.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          )}

          {message && (
            <div className="mt-5 rounded-xl bg-slate-100 p-4 text-sm text-slate-700" role="status">
              {message}
            </div>
          )}

          <button
            type="button"
            onClick={handleUpload}
            disabled={uploading || !file}
            className="mt-6 w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {uploading ? "Uploading CV..." : "Upload CV"}
          </button>

          <p className="mt-5 text-center text-xs leading-5 text-slate-500">
            Your document is stored in your student account. Its extraction and review statuses are tracked separately.
          </p>
        </div>
      </div>
    </div>
  );
}

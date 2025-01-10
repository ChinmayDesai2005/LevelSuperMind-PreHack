import React, { useState } from "react";
import { Check, ChevronDown, Loader2 } from "lucide-react";
import axios from "axios";
import "./AnalyticsPanel.css";

const AnalyticsPanel = () => {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [postType, setPostType] = useState("");
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      setFileUploaded(true);
      setPostType("");
      setInsights([]);
      setError("");
    }
  };

  const handleAnalyze = async () => {
    setInsights([]);
    if (!postType) {
      setError("Please select a post type");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post(
        "http://localhost:5000/api/analyze",
        { postType },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = response.data;

      if (data.success) {
        // Split insights into array assuming they're newline separated
        setInsights(
          data.insights.split("\n").filter((insight) => insight.trim())
        );
      } else {
        setError(data.error || "Failed to analyze data");
      }
    } catch (err) {
      setError("Failed to connect to server");
    } finally {
      setLoading(false);
    }
  };

  const handlePostChange = (e) => {
    setInsights([]);
    setPostType(e.target.value);
  };

  return (
    <div className="panel-wrapper">
      <div className=" panel-container rounded-xl border border-gray-700 text-white shadow w-full">
        <div className="flex flex-col space-y-1.5 p-6">
          <h3 className="font-semibold leading-none tracking-tight">
            Social Media Analytics
          </h3>
        </div>
        <div className="p-6 pt-0">
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Upload File</label>
              <input
                type="file"
                onChange={handleFileChange}
                className="block w-full text-sm text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
            </div>

            {fileUploaded && (
              <>
                <div className="space-y-2">
                  <label className="text-sm font-medium">
                    Select Post Type
                  </label>
                  <div className="relative">
                    <select
                      value={postType}
                      onChange={handlePostChange}
                      className="flex h-9 w-full items-center justify-between rounded-md border border-gray-700 bg-gray-800 px-2 py-2 text-sm text-white shadow-sm ring-offset-background placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-600 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      <option value="" disabled>
                        Choose post type...
                      </option>
                      <option value="Text">Text Post</option>
                      <option value="Image">Image Post</option>
                      <option value="Video">Video Post</option>
                      <option value="Link">Link</option>
                      <option value="Poll">Poll</option>
                      <option value="Short Video">Short Video</option>
                    </select>
                    {/* <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 opacity-50" /> */}
                  </div>
                </div>

                <button
                  onClick={handleAnalyze}
                  disabled={loading || !postType}
                  className="inline-flex items-center justify-center w-full h-9 px-4 py-2 mt-4 text-sm font-medium text-white transition-colors bg-blue-600 rounded-md shadow hover:bg-blue-500 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    "Analyze Data"
                  )}
                </button>
              </>
            )}

            {error && <div className="text-red-500 text-sm">{error}</div>}

            {insights.length > 0 && (
              <div className="mt-6 space-y-2">
                <h3 className="font-medium mb-3">Insights</h3>
                {insights.map((insight, index) => (
                  <div key={index} className="p-3 bg-gray-700 rounded-lg">
                    {insight}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPanel;

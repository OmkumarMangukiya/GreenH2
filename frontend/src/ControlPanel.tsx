import React, { useState } from "react";

// Define the form data type
interface FormData {
  region: string;
  maxLcoh: number;
  minProduction: number;
  proximityToGrid: boolean;
}

// Define the GeoJSON type
interface GeoJSON {
  type: string;
  features: any[];
  metadata?: any;
}

interface ControlPanelProps {
  onRunOptimization: (formData: FormData) => void;
  loading: boolean;
  error: string | null;
  results: GeoJSON | null;
}

const ControlPanel: React.FC<ControlPanelProps> = ({
  onRunOptimization,
  loading,
  error,
  results,
}) => {
  const [formData, setFormData] = useState({
    region: "",
    maxLcoh: 5.0,
    minProduction: 1000,
    proximityToGrid: true,
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox" ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: checked,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onRunOptimization(formData);
  };

  return (
    <div className="bg-gray-100 p-4 h-screen overflow-y-auto">
      <h2 className="text-xl font-bold text-gray-800 mb-4">GreenH2 Controls</h2>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Region Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Region
          </label>
          <select
            name="region"
            value={formData.region}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">Select a region</option>
            <option value="gujarat">Gujarat, India</option>
            <option value="rajasthan">Rajasthan, India</option>
            <option value="maharashtra">Maharashtra, India</option>
            <option value="karnataka">Karnataka, India</option>
            <option value="tamil_nadu">Tamil Nadu, India</option>
            <option value="andhra_pradesh">Andhra Pradesh, India</option>
            <option value="india">India (All States)</option>
            <option value="namibia">Namibia</option>
            <option value="chile">Chile</option>
            <option value="australia">Australia</option>
          </select>
        </div>

        {/* Max LCOH Target */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Max LCOH Target ($/kg): {formData.maxLcoh}
          </label>
          <input
            type="range"
            name="maxLcoh"
            min="1"
            max="10"
            step="0.1"
            value={formData.maxLcoh}
            onChange={handleInputChange}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>$1.0</span>
            <span>$10.0</span>
          </div>
        </div>

        {/* Production Capacity */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Minimum Production (t/year)
          </label>
          <input
            type="number"
            name="minProduction"
            min="100"
            step="100"
            value={formData.minProduction}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
        </div>

        {/* Grid Proximity */}
        <div>
          <label className="flex items-center">
            <input
              type="checkbox"
              name="proximityToGrid"
              checked={formData.proximityToGrid}
              onChange={handleCheckboxChange}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="ml-2 text-sm text-gray-700">
              Proximity to Grid
            </span>
          </label>
        </div>

        {/* Run Optimization Button */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 px-4 rounded-md focus:ring-2 focus:ring-offset-2 transition-colors ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700 focus:ring-blue-500"
          } text-white`}
        >
          {loading ? "Running Optimization..." : "Run Optimization"}
        </button>
      </form>

      {/* Error Display */}
      {error && (
        <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-md">
          <p className="text-sm font-medium">Error: {error}</p>
        </div>
      )}

      {/* Results Section */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Results</h3>
        <div className="bg-white p-3 rounded-md border border-gray-200">
          {results ? (
            <div className="space-y-2">
              <p className="text-sm text-gray-600">
                Found {results.features.length} optimal sites:
              </p>
              <div className="space-y-1">
                {results.features.slice(0, 3).map((feature, index) => (
                  <div key={index} className="text-xs text-gray-700">
                    <span className="font-medium">
                      #{feature.properties.rank}
                    </span>{" "}
                    {feature.properties.site_name} - ${feature.properties.lcoh}
                    /kg
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <p className="text-sm text-gray-600">
              Click "Run Optimization" to find optimal hydrogen production
              sites.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ControlPanel;

import { useState } from "react";
import ControlPanel from "./ControlPanel";
import Map from "./components/Map";
import MapView from "./components/MapView";
import "./App.css";

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

function App() {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<GeoJSON | null>(null);

  const handleRunOptimization = async (formData: FormData) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://localhost:8000/api/optimize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
      console.log("Optimization results:", data);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "An unknown error occurred";
      setError(errorMessage);
      console.error("Optimization failed:", errorMessage);
    } finally {
      setLoading(false);
    }
  };

  // Determine map center and zoom based on results
  const getMapSettings = () => {
    if (results && results.metadata && results.metadata.optimization_criteria) {
      const region =
        results.metadata.optimization_criteria.region?.toLowerCase();

      if (region?.includes("gujarat")) {
        return { center: [22.2587, 71.1924] as [number, number], zoom: 7 };
      } else if (region?.includes("rajasthan")) {
        return { center: [27.0238, 74.2179] as [number, number], zoom: 6 };
      } else if (region?.includes("maharashtra")) {
        return { center: [19.7515, 75.7139] as [number, number], zoom: 6 };
      } else if (region?.includes("karnataka")) {
        return { center: [15.3173, 75.7139] as [number, number], zoom: 6 };
      } else if (region?.includes("tamil")) {
        return { center: [11.1271, 78.6569] as [number, number], zoom: 6 };
      } else if (region?.includes("andhra")) {
        return { center: [15.9129, 79.74] as [number, number], zoom: 6 };
      } else if (region?.includes("india")) {
        return { center: [20.5937, 78.9629] as [number, number], zoom: 5 };
      }
    }

    // Default settings
    return { center: [20.5937, 78.9629] as [number, number], zoom: 4 };
  };

  const mapSettings = getMapSettings();

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left Column - Control Panel Sidebar */}
      <div className="w-1/5 bg-white shadow-lg">
        <ControlPanel
          onRunOptimization={handleRunOptimization}
          loading={loading}
          error={error}
          results={results}
        />
      </div>

      {/* Right Column - Map Area */}
      <div className="w-4/5">
        <Map center={mapSettings.center} zoom={mapSettings.zoom}>
          <MapView results={results} />
        </Map>
      </div>
    </div>
  );
}

export default App;

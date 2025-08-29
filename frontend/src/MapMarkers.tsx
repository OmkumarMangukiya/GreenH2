import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";

// Define the GeoJSON feature type
interface GeoJSONFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: [number, number]; // [longitude, latitude]
  };
  properties: {
    site_name: string;
    lcoh: number;
    production_cost: number;
    transport_cost: number;
    region: string;
    rank: number;
  };
}

// Define the GeoJSON type
interface GeoJSON {
  type: string;
  features: GeoJSONFeature[];
  metadata?: any;
}

interface MapMarkersProps {
  results: GeoJSON | null;
}

const MapMarkers: React.FC<MapMarkersProps> = ({ results }) => {
  if (!results || !results.features || results.features.length === 0) {
    return null;
  }

  return (
    <>
      {results.features.map((feature, index) => {
        const { coordinates } = feature.geometry;
        const { site_name, lcoh, production_cost, transport_cost, rank } = feature.properties;

        return (
          <Marker
            key={`${site_name}-${index}`}
            position={[coordinates[1], coordinates[0]]} // Leaflet expects [lat, lng]
            icon={L.divIcon({
              className: "custom-marker",
              html: `<div class="marker-content">
                <span class="marker-rank">${rank}</span>
                <span class="marker-lcoh">$${lcoh}</span>
              </div>`,
              iconSize: [40, 40],
              iconAnchor: [20, 40],
            })}
          >
            <Popup>
              <div className="p-2">
                <h3 className="font-bold text-lg mb-2">{site_name}</h3>
                <div className="space-y-1 text-sm">
                  <p><strong>Rank:</strong> #{rank}</p>
                  <p><strong>LCOH:</strong> ${lcoh}/kg</p>
                  <p><strong>Production Cost:</strong> ${production_cost}/kg</p>
                  <p><strong>Transport Cost:</strong> ${transport_cost}/kg</p>
                </div>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </>
  );
};

export default MapMarkers;

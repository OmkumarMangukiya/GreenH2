import React from "react";
import { Marker, Popup } from "react-leaflet";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

interface GeoJSONFeature {
  geometry: {
    coordinates: [number, number];
  };
  properties: {
    site_name: string;
    lcoh: number;
  };
}

interface MapViewProps {
  results: {
    features?: GeoJSONFeature[];
  } | null;
}

const MapView: React.FC<MapViewProps> = ({ results }) => {
  if (!results || !results.features) return null;

  return (
    <>
      {results.features.map((feature, idx) => (
        <Marker
          key={idx}
          position={[
            feature.geometry.coordinates[1],
            feature.geometry.coordinates[0],
          ]}
        >
          <Popup>
            <div>
              <strong>{feature.properties.site_name}</strong>
              <br />
              LCOH: {feature.properties.lcoh}
            </div>
          </Popup>
        </Marker>
      ))}
    </>
  );
};

export default MapView;

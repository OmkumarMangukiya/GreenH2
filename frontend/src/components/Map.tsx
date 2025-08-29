import React from "react";
import { MapContainer, TileLayer } from "react-leaflet";

type MapProps = {
  children: React.ReactNode;
  center?: [number, number];
  zoom?: number;
};

const Map: React.FC<MapProps> = ({ children, center, zoom }) => {
  // Default center and zoom
  const defaultCenter: [number, number] = center || [22.2587, 71.1924]; // Center of Gujarat
  const defaultZoom: number = zoom || 7;

  return (
    <MapContainer
      className="h-full w-full"
      center={defaultCenter}
      zoom={defaultZoom}
      scrollWheelZoom={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
      />
      {children}
    </MapContainer>
  );
};

export default Map;

import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

// Define the GeoJSON feature type
interface GeoJSONFeature {
  type: string;
  geometry: {
    type: string;
    coordinates: [number, number];
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

interface DashboardProps {
  selectedSite: GeoJSONFeature | null;
}

const Dashboard: React.FC<DashboardProps> = ({ selectedSite }) => {
  const chartRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!selectedSite || !chartRef.current) return;

    // Clear previous chart
    d3.select(chartRef.current).selectAll("*").remove();

    // Prepare data for the chart
    const data = [
      { name: "Production Cost", value: selectedSite.properties.production_cost },
      { name: "Transport Cost", value: selectedSite.properties.transport_cost },
    ];

    // Chart dimensions
    const margin = { top: 20, right: 20, bottom: 40, left: 60 };
    const width = 300 - margin.left - margin.right;
    const height = 200 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3
      .select(chartRef.current)
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // X scale
    const x = d3
      .scaleBand()
      .range([0, width])
      .domain(data.map((d) => d.name))
      .padding(0.2);

    // Y scale
    const y = d3
      .scaleLinear()
      .domain([0, d3.max(data, (d) => d.value) || 0])
      .range([height, 0]);

    // Add X axis
    svg
      .append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .style("text-anchor", "middle")
      .style("font-size", "12px");

    // Add Y axis
    svg
      .append("g")
      .call(d3.axisLeft(y).tickFormat((d) => `$${d}`))
      .style("font-size", "12px");

    // Add bars
    svg
      .selectAll("rect")
      .data(data)
      .enter()
      .append("rect")
      .attr("x", (d) => x(d.name) || 0)
      .attr("y", (d) => y(d.value))
      .attr("width", x.bandwidth())
      .attr("height", (d) => height - y(d.value))
      .attr("fill", (d, i) => (i === 0 ? "#3b82f6" : "#10b981"))
      .attr("rx", 3)
      .attr("ry", 3);

    // Add value labels on bars
    svg
      .selectAll(".bar-label")
      .data(data)
      .enter()
      .append("text")
      .attr("class", "bar-label")
      .attr("x", (d) => (x(d.name) || 0) + x.bandwidth() / 2)
      .attr("y", (d) => y(d.value) - 5)
      .attr("text-anchor", "middle")
      .style("font-size", "11px")
      .style("font-weight", "bold")
      .style("fill", "white")
      .text((d) => `$${d.value.toFixed(2)}`);

    // Add chart title
    svg
      .append("text")
      .attr("x", width / 2)
      .attr("y", -5)
      .attr("text-anchor", "middle")
      .style("font-size", "14px")
      .style("font-weight", "bold")
      .text("Cost Breakdown");

  }, [selectedSite]);

  if (!selectedSite) {
    return (
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">Site Dashboard</h3>
        <p className="text-sm text-gray-600">
          Click on a marker on the map to view detailed cost analysis.
        </p>
      </div>
    );
  }

  const { site_name, lcoh, production_cost, transport_cost, rank } = selectedSite.properties;

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Site Dashboard</h3>
      
      {/* Site Information */}
      <div className="mb-4">
        <h4 className="font-medium text-gray-700 mb-2">{site_name}</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-gray-600">Rank:</span>
            <span className="ml-1 font-medium">#{rank}</span>
          </div>
          <div>
            <span className="text-gray-600">Total LCOH:</span>
            <span className="ml-1 font-medium text-green-600">${lcoh}/kg</span>
          </div>
        </div>
      </div>

      {/* Cost Breakdown Chart */}
      <div className="mb-4">
        <svg ref={chartRef} className="w-full"></svg>
      </div>

      {/* Cost Details */}
      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-600">Production Cost:</span>
          <span className="font-medium text-blue-600">${production_cost}/kg</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-600">Transport Cost:</span>
          <span className="font-medium text-green-600">${transport_cost}/kg</span>
        </div>
        <div className="border-t pt-2 flex justify-between font-medium">
          <span>Total LCOH:</span>
          <span className="text-green-600">${lcoh}/kg</span>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

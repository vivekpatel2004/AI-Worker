import React, { useEffect, useState } from "react";
import api from "../api/api";

const Dashboard = () => {
  const [workers, setWorkers] = useState([]);
  const [stations, setStations] = useState([]);
  const [factory, setFactory] = useState(null);
  const [selectedWorker, setSelectedWorker] = useState("All");
  const [minConfidence, setMinConfidence] = useState(0);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, [minConfidence]);

  const fetchData = async () => {
    try {
      setLoading(true);

      const workerRes = await api.get(
        `/metrics/workers?min_confidence=${Number(minConfidence)}`
      );

      const stationRes = await api.get("/metrics/workstations");
      const factoryRes = await api.get("/metrics/factory");

      setWorkers(workerRes.data || []);
      setStations(stationRes.data || []);
      setFactory(factoryRes.data || null);
    } catch (error) {
      console.error("Error fetching metrics:", error);
    } finally {
      setLoading(false);
    }
  };

  const seedDatabase = async () => {
    try {
      setLoading(true);
      await api.post("/seed/data");
      await fetchData(); // refresh data after seeding
    } catch (error) {
      console.error("Error seeding database:", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredWorkers =
    selectedWorker === "All"
      ? workers
      : workers.filter((w) => w.worker_id === selectedWorker);

  return (
    <div className="p-8 bg-gray-50 min-h-screen text-gray-800">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-blue-700">
          AI Worker Productivity Dashboard
        </h1>

        <button
          onClick={seedDatabase}
          className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
        >
          Seed Data
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium">Select Worker</label>
          <select
            className="mt-1 p-2 border rounded"
            value={selectedWorker}
            onChange={(e) => setSelectedWorker(e.target.value)}
          >
            <option value="All">All</option>
            {workers.map((w) => (
              <option key={w.worker_id} value={w.worker_id}>
                {w.worker_id}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium">
            Minimum Confidence
          </label>
          <input
            type="number"
            step="0.1"
            min="0"
            max="1"
            value={minConfidence}
            onChange={(e) => setMinConfidence(Number(e.target.value))}
            className="mt-1 p-2 border rounded"
          />
        </div>
      </div>

      {loading && <p className="mb-4">Loading...</p>}

      {/* Factory Summary */}
      {factory && (
        <div className="grid md:grid-cols-3 gap-6 mb-10">
          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="text-sm text-gray-500">Total Production</h2>
            <p className="text-3xl font-bold mt-2">
              {factory.total_production_units}
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="text-sm text-gray-500">Total Active Minutes</h2>
            <p className="text-3xl font-bold mt-2">
              {factory.total_active_minutes}
            </p>
          </div>

          <div className="bg-white p-6 rounded-xl shadow">
            <h2 className="text-sm text-gray-500">Avg Production / Hour</h2>
            <p className="text-3xl font-bold mt-2">
              {factory.average_production_rate_per_hour}
            </p>
          </div>
        </div>
      )}

      {/* Worker Metrics */}
      <h2 className="text-2xl font-semibold mb-3">Worker Metrics</h2>
      <div className="overflow-x-auto bg-white rounded-xl shadow mb-10">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
            <tr>
              <th className="p-3 text-left">Worker</th>
              <th className="p-3 text-left">Active</th>
              <th className="p-3 text-left">Idle</th>
              <th className="p-3 text-left">Util %</th>
              <th className="p-3 text-left">Units</th>
              <th className="p-3 text-left">Units/hr</th>
            </tr>
          </thead>
          <tbody>
            {filteredWorkers.length > 0 ? (
              filteredWorkers.map((w) => (
                <tr key={w.worker_id} className="border-t hover:bg-gray-50">
                  <td className="p-3 font-medium">{w.worker_id}</td>
                  <td className="p-3">{w.active_minutes}</td>
                  <td className="p-3">{w.idle_minutes}</td>
                  <td className="p-3">{w.utilization_percent}%</td>
                  <td className="p-3">{w.total_units}</td>
                  <td className="p-3">{w.units_per_hour}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="p-4 text-center text-gray-500">
                  No worker data available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Workstation Metrics */}
      <h2 className="text-2xl font-semibold mb-3">Workstation Metrics</h2>
      <div className="overflow-x-auto bg-white rounded-xl shadow">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
            <tr>
              <th className="p-3 text-left">Station</th>
              <th className="p-3 text-left">Occupancy</th>
              <th className="p-3 text-left">Units</th>
              <th className="p-3 text-left">Throughput/hr</th>
            </tr>
          </thead>
          <tbody>
            {stations.length > 0 ? (
              stations.map((s) => (
                <tr key={s.station_id} className="border-t hover:bg-gray-50">
                  <td className="p-3 font-medium">{s.station_id}</td>
                  <td className="p-3">{s.occupancy_minutes}</td>
                  <td className="p-3">{s.total_units}</td>
                  <td className="p-3">{s.throughput_per_hour}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="p-4 text-center text-gray-500">
                  No workstation data available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
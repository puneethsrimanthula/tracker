import { useEffect, useState } from "react";

const API = "http://localhost:8000";

export default function App() {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const load = () =>
      fetch(`${API}/locations`)
        .then((r) => r.json())
        .then((d) => { setData(d); setError(null); })
        .catch(() => setError("Cannot reach backend"));

    load();                                   // load once immediately
    const id = setInterval(load, 5000);       // then every 5 seconds
    return () => clearInterval(id);           // cleanup when page closes
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Device Tracker Dashboard</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Device</th><th>Latitude</th><th>Longitude</th>
            <th>Time</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((d, i) => (
            <tr key={i}>
              <td>{d.device_id}</td>
              <td>{d.latitude}</td>
              <td>{d.longitude}</td>
              <td>{d.timestamp}</td>
              <td>{d.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
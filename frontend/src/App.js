import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css"; // we'll create this

function App() {
  const [indicators, setIndicators] = useState([]);
  const [form, setForm] = useState({
    value: "",
    source: "manual",
    threat_level: "low",
  });

  // Fetch indicators from backend
  const fetchIndicators = () => {
    axios
      .get("http://localhost:8000/api/indicators/")
      .then((res) => setIndicators(res.data))
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchIndicators();
  }, []);

  // Handle input change
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Handle form submit
  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post("http://localhost:8000/api/indicators/", form)
      .then(() => {
        setForm({ value: "", source: "manual", threat_level: "low" });
        fetchIndicators();
      })
      .catch((err) => console.error(err));
  };

  return (
    <div className="container">
      <h1>Threat Intelligence Dashboard</h1>

      <div className="form-container">
        <h2>Add New Indicator</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="value"
            placeholder="Value (IP, domain, hash)"
            value={form.value}
            onChange={handleChange}
            required
          />
          <select name="source" value={form.source} onChange={handleChange}>
            <option value="manual">Manual</option>
            <option value="OTX">OTX</option>
            <option value="AbuseIPDB">AbuseIPDB</option>
          </select>
          <select
            name="threat_level"
            value={form.threat_level}
            onChange={handleChange}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
          <button type="submit">Add Indicator</button>
        </form>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Value</th>
              <th>Source</th>
              <th>Threat Level</th>
            </tr>
          </thead>
          <tbody>
            {indicators.map((i) => (
              <tr key={i.id}>
                <td>{i.id}</td>
                <td>{i.value}</td>
                <td>{i.source}</td>
                <td>{i.threat_level}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;

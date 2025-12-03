import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [indicators, setIndicators] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/indicators/")
      .then(res => setIndicators(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Threat Intelligence Dashboard</h1>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>ID</th>
            <th>Value</th>
            <th>Source</th>
            <th>Threat Level</th>
          </tr>
        </thead>
        <tbody>
          {indicators.map(i => (
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
  );
}

export default App;

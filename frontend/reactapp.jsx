import React, { useState, useEffect } from "react";

function App() {
  const API_BASE = process.env.REACT_APP_API_BASE;
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [name, setName] = useState("");
  const [path, setPath] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/all`)
      .then(res => res.json())
      .then(setItems);
  }, [API_BASE]);

  const handleSearch = async () => {
    const res = await fetch(`${API_BASE}/search/${encodeURIComponent(search)}`);
    const data = await res.json();
    alert(data.message);
  };

  const handleNew = async () => {
    await fetch(`${API_BASE}/new-item`, {
      method: "POST", 
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify({ name, path })
    });
    alert("New item added!");
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>Flask / FastAPI UI Demo (React)</h2>

      <h3>Items:</h3>
      <ul>
        {items.map(i => (
          <li key={i.id}><i>{i.name}</i> can be found here: {i.path}</li>
        ))}
      </ul>

      <h3>Search</h3>
      <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Enter search..." />
      <button onClick={handleSearch}>Search</button>

      <h3>Add New Item</h3>
      <input value={name} onChange={e => setName(e.target.value)} placeholder="name" />
      <input value={path} onChange={e => setPath(e.target.value)} placeholder="path/to/resource" />
      <button onClick={handleNew}>Add</button>
    </div>
  );
}

export default App;

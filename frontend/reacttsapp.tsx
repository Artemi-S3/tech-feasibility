import { useState, useEffect, ChangeEvent } from "react";

interface Item {
  id: number;
  name: string;
  path: string;
}

interface APIResponse<T> {
  data?: T;
  error?: string;
}

const API_BASE = process.env.REACT_APP_API_BASE;

const fetchItems = async (): Promise<APIResponse<Item[]>> => {
  try {
    const res = await fetch(`${API_BASE}/all`);
    if (!res.ok) throw new Error("Failed to fetch items");
    const data: Item[] = await res.json();
    return { data };
  } catch (err: any) {
    return { error: err.message };
  }
};

const searchItem = async (query: string): Promise<APIResponse<string>> => {
  try {
    const res = await fetch(`${API_BASE}/search/${encodeURIComponent(query)}`);
    const data = await res.json();
    return { data: data.message };
  } catch (err: any) {
    return { error: err.message };
  }
};

const addItem = async (item: Omit<Item, "id">): Promise<APIResponse<Item>> => {
  try {
    const res = await fetch(`${API_BASE}/new-item`, {
      method: "POST", 
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify(item)
    });
    if (!res.ok) throw new Error("Failed to add new item");
    const data: Item = await res.json();
    return { data };
  } catch (err: any) {
    return { error: err.message };
  }
};

const App = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [search, setSearch] = useState<string>("");
  const [name, setName] = useState<string>("");
  const [path, setPath] = useState<string>("");

  useEffect(() => {
    (async () => {
      const res = await fetchItems();
      if (res.data) setItems(res.data ?? []);
    })();
  }, []);

  const handleSearch = async (): Promise<void> => {
    const res = await searchItem(search);
    alert(res.data ?? `Error: ${res.error}`);
  };

  const handleNew = async (): Promise<void> => {
    const res = await addItem({ name, path });
    if (res.data) {
      setItems(prev => [...prev, res.data!]);
      alert(`Added: ${res.data.name}`);
    } else {
      alert(`Error: ${res.error}`);
    }
  };

  const handleChange = (setter: React.Dispatch<React.SetStateAction<string>>) => (e: ChangeEvent<HTMLInputElement>): void => setter(e.target.value);

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>Flask / FastAPI UI Demov (React + TypeScript)</h2>

      <h3>Items:</h3>
      <ul>
        {items.map(i => (
          <li key={i.id}><i>{i.name}</i> can be found here: {i.path}</li>
        ))}
      </ul>

      <h3>Search</h3>
      <input value={search} onChange={handleChange(setSearch)} placeholder="Enter search..." />
      <button onClick={handleSearch}>Search</button>

      <h3>Add New Item</h3>
      <input value={name} onChange={handleChange(setName)} placeholder="name" />
      <input value={path} onChange={handleChange(setPath)} placeholder="path/to/resource" />
      <button onClick={handleNew}>Add</button>
    </div>
  );
};

export default App;

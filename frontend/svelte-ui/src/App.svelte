<script>
  import { onMount } from "svelte";

  const API_BASE = "http://127.0.0.1:5000";

  let items = [];
  let query = "";
  let name = "";
  let path = "";

  async function loadAll() {
    try {
      const res = await fetch(`${API_BASE}/all`);
      if (!res.ok) throw new Error("Failed to fetch items");
      items = await res.json();
    } catch {
      items = [];
    }
  }

  async function doSearch() {
    const res = await fetch(`${API_BASE}/search/${encodeURIComponent(query)}`);
    const data = await res.json();
    alert(data && data.message ? data.message : "No result");
  }

  async function addItem() {
    const res = await fetch(`${API_BASE}/new-item`, {
      method: "POST", 
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify({ name, path })
    });
    const item = await res.json().catch(() => null);
    if (item) items = [...items, item];
  }

  onMount(loadAll);
</script>

<main style="font-family: sans-serif; padding: 16px;">
  <h2>Svelte UI Test</h2>

  <h3>Items</h3>
  <ul>
    {#each items as i (i.id)}
      <li><strong>{i.name}</strong> — <em>{i.path}</em></li>
    {/each}
  </ul>

  <h3>Search</h3>
  <input bind:value={query} placeholder="Search term" />
  <button on:click={doSearch}>Search</button>

  <h3>Add</h3>
  <input bind:value={name} placeholder="name" />
  <input bind:value={path} placeholder="path/to/resource" />
  <button on:click={addItem}>Add</button>
</main>

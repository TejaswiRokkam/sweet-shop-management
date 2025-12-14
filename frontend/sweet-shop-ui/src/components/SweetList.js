import { apiRequest } from "../api/api";
import { useEffect, useState } from "react";
import SweetCard from "./SweetCard";

export default function SweetList({ isAdmin }) {
  const [sweets, setSweets] = useState([]);
  const [form, setForm] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
  });

  const [filters, setFilters] = useState({
    name: "",
    category: "",
    min_price: "",
    max_price: "",
  });

  const loadSweets = async () => {
    const query = new URLSearchParams(
      Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== "")
      )
    ).toString();

    const url = query ? `/sweets/search?${query}` : "/sweets";

    try {
      const data = await apiRequest(url);
      setSweets(data);
    } catch (err) {
      alert(err.message);
    }
  };

  useEffect(() => {
    loadSweets();
  }, []);

  const addSweet = async () => {
    try {
      await apiRequest("/sweets", "POST", {
        name: form.name,
        category: form.category,
        price: Number(form.price),
        quantity: Number(form.quantity),
      });

      setForm({ name: "", category: "", price: "", quantity: "" });
      loadSweets();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
  <div>
    <h2 className="text-2xl font-semibold mb-4 text-gray-800">
      Sweets
    </h2>

    {/* SEARCH & FILTER */}
    <div className="bg-white rounded-xl shadow p-4 mb-6">
      <h4 className="font-semibold mb-3 text-gray-700">
        Search & Filter
      </h4>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <input
          className="border p-2 rounded"
          placeholder="Name"
          value={filters.name}
          onChange={(e) =>
            setFilters({ ...filters, name: e.target.value })
          }
        />

        <input
          className="border p-2 rounded"
          placeholder="Category"
          value={filters.category}
          onChange={(e) =>
            setFilters({ ...filters, category: e.target.value })
          }
        />

        <input
          className="border p-2 rounded"
          type="number"
          placeholder="Min Price"
          value={filters.min_price}
          onChange={(e) =>
            setFilters({ ...filters, min_price: e.target.value })
          }
        />

        <input
          className="border p-2 rounded"
          type="number"
          placeholder="Max Price"
          value={filters.max_price}
          onChange={(e) =>
            setFilters({ ...filters, max_price: e.target.value })
          }
        />
      </div>

      <button
        onClick={loadSweets}
        className="mt-4 px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 transition"
      >
        Apply Filters
      </button>
    </div>

    {/* ADMIN ADD SWEET */}
    {isAdmin && (
      <div className="bg-blue-50 rounded-xl shadow p-4 mb-6">
        <h3 className="font-semibold mb-3 text-gray-700">
          Admin – Add Sweet
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
          <input
            className="border p-2 rounded"
            placeholder="Name"
            value={form.name}
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
          />

          <input
            className="border p-2 rounded"
            placeholder="Category"
            value={form.category}
            onChange={(e) =>
              setForm({ ...form, category: e.target.value })
            }
          />

          <input
            className="border p-2 rounded"
            type="number"
            placeholder="Price"
            value={form.price}
            onChange={(e) =>
              setForm({ ...form, price: e.target.value })
            }
          />

          <input
            className="border p-2 rounded"
            type="number"
            placeholder="Quantity"
            value={form.quantity}
            onChange={(e) =>
              setForm({ ...form, quantity: e.target.value })
            }
          />
        </div>

        <button
          onClick={addSweet}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Add Sweet
        </button>
      </div>
    )}

    {/* SWEETS LIST */}
    {sweets.length === 0 ? (
      <p className="text-gray-500 text-center mt-8">
        No sweets available
      </p>
    ) : (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sweets.map((s) => (
          <SweetCard
            key={s.id}
            sweet={s}
            isAdmin={isAdmin}
            onUpdate={loadSweets}
          />
        ))}
      </div>
    )}
  </div>
  );

}

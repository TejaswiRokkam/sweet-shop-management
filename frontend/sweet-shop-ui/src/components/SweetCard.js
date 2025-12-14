import { apiRequest } from "../api/api";
import { useState } from "react";

export default function SweetCard({ sweet, isAdmin, onUpdate }) {
  const [restockQty, setRestockQty] = useState("");

  const purchase = async () => {
    try {
      await apiRequest(`/sweets/${sweet.id}/purchase`, "POST");
      onUpdate();
    } catch (err) {
      alert(err.message);
    }
  };

  const deleteSweet = async () => {
    try {
      await apiRequest(`/sweets/${sweet.id}`, "DELETE");
      onUpdate();
    } catch (err) {
      alert(err.message);
    }
  };

  const restock = async () => {
    if (!restockQty || Number(restockQty) <= 0) {
      alert("Enter valid quantity");
      return;
    }

    try {
      await apiRequest(`/sweets/${sweet.id}/restock`, "POST", {
        quantity: Number(restockQty),
      });
      setRestockQty("");
      onUpdate();
    } catch (err) {
      alert(err.message);
    }
  };

  return (
  <div className="bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition">
    <h3 className="text-lg font-semibold text-gray-800 mb-1">
      {sweet.name}
    </h3>

    <p className="text-sm text-gray-600">Category: {sweet.category}</p>
    <p className="text-sm text-gray-600">Price: ₹{sweet.price}</p>
    <p className="text-sm text-gray-600 mb-3">
      Available: {sweet.quantity}
    </p>

    <div className="flex flex-wrap gap-2">
      <button
        disabled={sweet.quantity === 0}
        onClick={purchase}
        className={`px-3 py-1 rounded text-white transition ${
          sweet.quantity === 0
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-green-500 hover:bg-green-600"
        }`}
      >
        Purchase
      </button>

      {isAdmin && (
        <button
          onClick={deleteSweet}
          className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition"
        >
          Delete
        </button>
      )}
    </div>

    {isAdmin && (
      <div className="mt-3 flex items-center gap-2">
        <input
          type="number"
          placeholder="Restock"
          value={restockQty}
          onChange={(e) => setRestockQty(e.target.value)}
          className="border border-gray-300 p-1 rounded w-24"
        />
        <button
          onClick={restock}
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          Restock
        </button>
      </div>
    )}
  </div>
  );

}

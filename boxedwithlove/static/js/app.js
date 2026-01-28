const toastRoot = document.getElementById("toast-root");

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `card px-4 py-3 text-sm ${
    type === "error" ? "border-red-400 text-red-700" : "border-brand-soft text-brand-text"
  }`;
  toast.textContent = message;
  toastRoot.appendChild(toast);
  setTimeout(() => {
    toast.classList.add("opacity-0");
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

async function apiRequest(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (response.status === 204) {
    return { data: null };
  }
  const payload = await response.json();
  if (!response.ok) {
    const message = payload?.error?.message || "Something went wrong.";
    throw new Error(message);
  }
  return payload;
}

window.BoxedWithLove = { showToast, apiRequest };

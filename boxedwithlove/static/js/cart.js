const { apiRequest, showToast } = window.BoxedWithLove;

async function handleAddToCart(button) {
  const productId = button.dataset.productId;
  const quantityInput = document.getElementById("quantity");
  const quantity = quantityInput ? Number(quantityInput.value || 1) : 1;
  button.disabled = true;
  try {
    await apiRequest("/api/cart/items", {
      method: "POST",
      body: JSON.stringify({ product_id: productId, quantity }),
    });
    showToast(`${button.dataset.productName} added to cart.`);
  } catch (error) {
    showToast(error.message, "error");
  } finally {
    button.disabled = false;
  }
}

async function updateQuantity(itemId, newQty) {
  try {
    await apiRequest(`/api/cart/items/${itemId}`, {
      method: "PATCH",
      body: JSON.stringify({ quantity: newQty }),
    });
    window.location.reload();
  } catch (error) {
    showToast(error.message, "error");
  }
}

async function removeItem(itemId) {
  try {
    await apiRequest(`/api/cart/items/${itemId}`, { method: "DELETE" });
    window.location.reload();
  } catch (error) {
    showToast(error.message, "error");
  }
}

document.querySelectorAll(".add-to-cart").forEach((button) => {
  button.addEventListener("click", () => handleAddToCart(button));
});

document.querySelectorAll(".qty-decrease").forEach((button) => {
  button.addEventListener("click", () => {
    const itemId = button.dataset.itemId;
    const qtyEl = document.querySelector(`[data-qty='${itemId}']`);
    const current = Number(qtyEl.textContent || 1);
    if (current > 1) {
      updateQuantity(itemId, current - 1);
    }
  });
});

document.querySelectorAll(".qty-increase").forEach((button) => {
  button.addEventListener("click", () => {
    const itemId = button.dataset.itemId;
    const qtyEl = document.querySelector(`[data-qty='${itemId}']`);
    const current = Number(qtyEl.textContent || 1);
    updateQuantity(itemId, current + 1);
  });
});

document.querySelectorAll(".remove-item").forEach((button) => {
  button.addEventListener("click", () => removeItem(button.dataset.itemId));
});

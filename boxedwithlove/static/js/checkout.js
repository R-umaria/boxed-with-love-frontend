const { apiRequest, showToast } = window.BoxedWithLove;

const toggleButton = document.getElementById("toggle-payment-form");
const paymentForm = document.getElementById("payment-form");
const savePaymentButton = document.getElementById("save-payment");
const placeOrderButton = document.getElementById("place-order");

if (toggleButton && paymentForm) {
  toggleButton.addEventListener("click", () => {
    paymentForm.classList.toggle("hidden");
  });
}

if (savePaymentButton) {
  savePaymentButton.addEventListener("click", async () => {
    const brand = paymentForm.querySelector("input[name='brand']").value;
    const last4 = paymentForm.querySelector("input[name='last4']").value;
    const expiry = paymentForm.querySelector("input[name='expiry']").value;
    savePaymentButton.disabled = true;
    try {
      await apiRequest("/api/payment-methods", {
        method: "POST",
        body: JSON.stringify({ brand, last4, expiry }),
      });
      showToast("Payment method added.");
      window.location.reload();
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      savePaymentButton.disabled = false;
    }
  });
}

if (placeOrderButton) {
  placeOrderButton.addEventListener("click", async () => {
    if (placeOrderButton.dataset.hasItems === "false") {
      showToast("Your cart is empty.", "error");
      return;
    }
    placeOrderButton.disabled = true;
    const shipping = {
      first_name: document.querySelector("input[name='first_name']")?.value || "",
      last_name: document.querySelector("input[name='last_name']")?.value || "",
      address: document.querySelector("input[name='address']")?.value || "",
      city: document.querySelector("input[name='city']")?.value || "",
      postal: document.querySelector("input[name='postal']")?.value || "",
    };
    try {
      const response = await apiRequest("/api/orders", {
        method: "POST",
        body: JSON.stringify({ shipping }),
      });
      const orderId = response.data.id;
      showToast("Order placed successfully.");
      window.location.href = `/orders/${orderId}/confirmation`;
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      placeOrderButton.disabled = false;
    }
  });
}

const removeButtons = document.querySelectorAll(".remove-payment");
removeButtons.forEach((button) => {
  button.addEventListener("click", async () => {
    button.disabled = true;
    try {
      await apiRequest(`/api/payment-methods/${button.dataset.methodId}`, { method: "DELETE" });
      showToast("Payment method removed.");
      window.location.reload();
    } catch (error) {
      showToast(error.message, "error");
    } finally {
      button.disabled = false;
    }
  });
});

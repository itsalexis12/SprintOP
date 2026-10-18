const form = document.getElementById("restaurant-form");

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = Object.fromEntries(new FormData(form));
    formData.price = Number(formData.price);

    const response = await fetch("/api/v1/restaurants", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    const message = document.getElementById("message");

    if (response.ok) {
      message.textContent = "Restaurante creado correctamente";
      form.reset();
    } else {
      const error = await response.json();
      message.textContent = error.detail || "Error al guardar";
    }
  });
}
document.addEventListener("DOMContentLoaded", () => {
  // 1. Manejo del Formulario (Crear y Editar)
  const form = document.getElementById("restaurant-form");
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const message = document.getElementById("message");
      const restaurantId = form.dataset.id;
      
      const formData = Object.fromEntries(new FormData(form));
      formData.price = Number(formData.price);
      if (!formData.photoUrl) delete formData.photoUrl;

      const isEdit = Boolean(restaurantId);
      const url = isEdit ? `/api/v1/restaurants/${restaurantId}` : "/api/v1/restaurants";
      const method = isEdit ? "PATCH" : "POST";

      try {
        const response = await fetch(url, {
          method: method,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        if (response.ok) {
          message.style.color = "green";
          message.textContent = isEdit ? "Restaurante actualizado con éxito." : "Restaurante creado con éxito.";
          setTimeout(() => {
            window.location.href = isEdit ? `/restaurants/${restaurantId}` : "/";
          }, 1000);
        } else {
          const error = await response.json();
          message.style.color = "red";
          message.textContent = error.detail || "Error al procesar la solicitud.";
        }
      } catch (err) {
        message.style.color = "red";
        message.textContent = "Error de conexión con el servidor.";
      }
    });
  }

  // 2. Manejo de la Eliminación desde el Detalle
  const deleteBtn = document.getElementById("delete-btn");
  if (deleteBtn) {
    deleteBtn.addEventListener("click", async () => {
      const restaurantId = deleteBtn.dataset.id;
      if (confirm("¿Estás seguro de que deseas eliminar este restaurante?")) {
        try {
          const response = await fetch(`/api/v1/restaurants/${restaurantId}`, {
            method: "DELETE"
          });

          if (response.ok) {
            alert("Restaurante eliminado correctamente.");
            window.location.href = "/";
          } else {
            alert("Error al eliminar el restaurante.");
          }
        } catch (err) {
          alert("Error de conexión con el servidor.");
        }
      }
    });
  }
});
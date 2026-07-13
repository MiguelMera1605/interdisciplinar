const API_BASE = "/api";

const elements = {
  nav: document.getElementById("mainNav"),
  navToggle: document.getElementById("navToggle"),
  themeToggle: document.getElementById("themeToggle"),
  materialFilter: document.getElementById("materialFilter"),
  materialsGrid: document.getElementById("materialsGrid"),
  materialsLoading: document.getElementById("materialsLoading"),
  materialsError: document.getElementById("materialsError"),
  feedbackForm: document.getElementById("feedbackForm"),
  formMessage: document.getElementById("formMessage"),
  galleryImage: document.getElementById("galleryImage"),
  galleryPrev: document.getElementById("galleryPrev"),
  galleryNext: document.getElementById("galleryNext"),
  galleryThumbs: document.getElementById("galleryThumbs"),
};

let materialsData = [];
let galleryIndex = 0;
const galleryImages = [
  "assets/images/gallery1.svg",
  "assets/images/gallery2.svg",
  "assets/images/gallery3.svg",
  "assets/images/gallery4.svg",
];

function toggleMenu() {
  elements.nav.classList.toggle("active");
}

function setTheme(isDark) {
  if (isDark) {
    document.documentElement.style.setProperty("--bg", "#ffffff");
    document.documentElement.style.setProperty("--surface", "#f4f7fb");
    document.documentElement.style.setProperty("--surface-alt", "#e6ebf3");
    document.documentElement.style.setProperty("--text", "#091421");
    document.documentElement.style.setProperty("--muted", "#425563");
    document.documentElement.style.setProperty("--primary", "#2d7dff");
    elements.themeToggle.textContent = "Modo claro";
  } else {
    document.documentElement.style.removeProperty("--bg");
    document.documentElement.style.removeProperty("--surface");
    document.documentElement.style.removeProperty("--surface-alt");
    document.documentElement.style.removeProperty("--text");
    document.documentElement.style.removeProperty("--muted");
    document.documentElement.style.removeProperty("--primary");
    elements.themeToggle.textContent = "Modo oscuro";
  }
}

function showMessage(element, text, type = "success") {
  element.textContent = text;
  element.classList.remove("hidden", "message-error");
  if (type === "error") {
    element.classList.add("message-error");
  }
}

function clearMessage(element) {
  element.textContent = "";
  element.classList.add("hidden");
  element.classList.remove("message-error");
}

function renderMaterials(items) {
  elements.materialsGrid.innerHTML = "";
  if (!items.length) {
    elements.materialsGrid.innerHTML = "<p>No se encontraron materiales con ese criterio.</p>";
    return;
  }

  const cards = items.map((item) => {
    const card = document.createElement("article");
    card.className = "card";
    card.innerHTML = `
      <h3>${item.nombre}</h3>
      <p>${item.descripcion || "Descripción no disponible."}</p>
      <p><strong>Cantidad:</strong> ${item.cantidad || "n/a"}</p>
      <p><strong>Uso:</strong> ${item.uso || "General"}</p>
    `;
    return card;
  });

  cards.forEach((card) => elements.materialsGrid.appendChild(card));
}

async function fetchMaterials() {
  elements.materialsLoading.classList.remove("hidden");
  elements.materialsError.classList.add("hidden");
  try {
    const response = await fetch(`${API_BASE}/materiales`);
    if (!response.ok) {
      throw new Error(`Error ${response.status}`);
    }
    const data = await response.json();
    materialsData = Array.isArray(data) ? data : [];
    renderMaterials(materialsData);
  } catch (error) {
    elements.materialsError.textContent = "No se pudieron cargar los materiales. Verifica el backend.";
    elements.materialsError.classList.remove("hidden");
    console.error(error);
  } finally {
    elements.materialsLoading.classList.add("hidden");
  }
}

function filterMaterials() {
  const query = elements.materialFilter.value.trim().toLowerCase();
  const filtered = materialsData.filter((item) => {
    return item.nombre.toLowerCase().includes(query) || (item.descripcion || "").toLowerCase().includes(query) || (item.uso || "").toLowerCase().includes(query);
  });
  renderMaterials(filtered);
}

function setupGallery() {
  elements.galleryThumbs.innerHTML = "";
  galleryImages.forEach((src, index) => {
    const thumb = document.createElement("button");
    thumb.className = "gallery-thumb";
    thumb.type = "button";
    thumb.innerHTML = `<img src="${src}" alt="Miniatura ${index + 1}" />`;
    thumb.addEventListener("click", () => {
      galleryIndex = index;
      updateGallery();
    });
    elements.galleryThumbs.appendChild(thumb);
  });
  elements.galleryPrev.addEventListener("click", () => {
    galleryIndex = (galleryIndex - 1 + galleryImages.length) % galleryImages.length;
    updateGallery();
  });
  elements.galleryNext.addEventListener("click", () => {
    galleryIndex = (galleryIndex + 1) % galleryImages.length;
    updateGallery();
  });
  updateGallery();
}

function updateGallery() {
  elements.galleryImage.src = galleryImages[galleryIndex];
  elements.galleryThumbs.querySelectorAll(".gallery-thumb").forEach((btn, index) => {
    btn.classList.toggle("active", index === galleryIndex);
  });
}

function validateForm(formData) {
  const errors = [];
  if (!formData.get("name").trim()) {
    errors.push("El nombre es obligatorio.");
  }
  const email = formData.get("email").trim();
  if (!email) {
    errors.push("El email es obligatorio.");
  } else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    errors.push("El email no es válido.");
  }
  if (!formData.get("feeling")) {
    errors.push("Selecciona si te genera placer o felicidad.");
  }
  if (!formData.get("comments").trim()) {
    errors.push("El comentario es obligatorio.");
  }
  return errors;
}

async function handleFormSubmit(event) {
  event.preventDefault();
  clearMessage(elements.formMessage);
  const formData = new FormData(elements.feedbackForm);
  const errors = validateForm(formData);
  if (errors.length) {
    showMessage(elements.formMessage, errors.join(" "), "error");
    return;
  }

  const payload = {
    nombre: formData.get("name").trim(),
    email: formData.get("email").trim(),
    sensacion: formData.get("feeling"),
    comentario: formData.get("comments").trim(),
    fecha: new Date().toISOString(),
  };

  try {
    const response = await fetch(`${API_BASE}/comentarios`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error(`Error ${response.status}`);
    }
    elements.feedbackForm.reset();
    showMessage(elements.formMessage, "¡Gracias! Tu opinión se guardó correctamente.");
  } catch (error) {
    showMessage(elements.formMessage, "No se pudo enviar el formulario. Intenta más tarde.", "error");
    console.error(error);
  }
}

function init() {
  elements.navToggle.addEventListener("click", toggleMenu);
  elements.themeToggle.addEventListener("click", () => {
    const isDark = elements.themeToggle.textContent.includes("Claro");
    setTheme(isDark);
  });
  elements.materialFilter.addEventListener("input", filterMaterials);
  elements.feedbackForm.addEventListener("submit", handleFormSubmit);
  fetchMaterials();
  setupGallery();
}

document.addEventListener("DOMContentLoaded", init);

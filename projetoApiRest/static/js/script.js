const statusElement = document.getElementById("api-status");

async function verificarAPI() {
  try {
    const response = await fetch("/api/status/");

    if (!response.ok) {
      throw new Error("API offline");
    }

    const data = await response.json();

    statusElement.textContent =
      data.status === "online" ? "API online" : "API respondendo";
  } catch (error) {
    statusElement.textContent = "API offline";

    const badge = statusElement.closest(".status-badge");

    if (badge) {
      badge.style.borderColor = "rgba(239, 68, 68, 0.2)";
      badge.style.background = "rgba(239, 68, 68, 0.06)";
    }

    const dot = badge?.querySelector(".status-dot");

    if (dot) {
      dot.style.background = "#ef4444";
      dot.style.boxShadow = "0 0 10px rgba(239, 68, 68, 0.7)";
    }
  }
}

verificarAPI();

// Atualiza o status a cada 30 segundos

setInterval(verificarAPI, 30000);

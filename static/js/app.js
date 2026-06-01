const form = document.getElementById("classify-form");
const textarea = document.getElementById("email-text");
const charCount = document.getElementById("char-count");
const clearBtn = document.getElementById("clear-btn");
const submitBtn = document.getElementById("submit-btn");
const resultSection = document.getElementById("result-section");
const resultContent = document.getElementById("result-content");
const exampleBtns = document.querySelectorAll(".example-btn");

function updateCharCount() {
  charCount.textContent = `${textarea.value.length} / 5000`;
}

function setLoading(loading) {
  submitBtn.disabled = loading;
  submitBtn.querySelector(".btn-text").classList.toggle("hidden", loading);
  submitBtn.querySelector(".spinner").classList.toggle("hidden", !loading);
}

function renderResult(data) {
  const isSpam = data.label === "spam";
  const badgeClass = isSpam ? "spam" : "ham";
  const icon = isSpam ? "⚠" : "✓";

  const bars = Object.entries(data.probabilities)
    .map(([label, value]) => `
      <div class="prob-row">
        <div class="prob-header">
          <span class="prob-label">${label}</span>
          <span class="prob-value">${value}%</span>
        </div>
        <div class="prob-track">
          <div class="prob-fill ${label}" style="width: ${value}%"></div>
        </div>
      </div>
    `)
    .join("");

  resultContent.innerHTML = `
    <div class="result-badge ${badgeClass}">${icon} ${data.label}</div>
    <div class="confidence">${data.confidence}%</div>
    <div class="confidence-label">Confidence score</div>
    <div class="probability-bars">${bars}</div>
  `;

  resultSection.classList.remove("hidden");
  resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function showError(message) {
  resultContent.innerHTML = `<div class="error-message">${message}</div>`;
  resultSection.classList.remove("hidden");
}

textarea.addEventListener("input", updateCharCount);

clearBtn.addEventListener("click", () => {
  textarea.value = "";
  updateCharCount();
  resultSection.classList.add("hidden");
  textarea.focus();
});

exampleBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    textarea.value = btn.dataset.text;
    updateCharCount();
    form.requestSubmit();
  });
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = textarea.value.trim();

  if (!text) {
    showError("Please enter email content to classify.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch("/api/classify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Classification failed. Please try again.");
      return;
    }

    renderResult(data);
  } catch {
    showError("Unable to reach the server. Make sure the app is running.");
  } finally {
    setLoading(false);
  }
});

updateCharCount();

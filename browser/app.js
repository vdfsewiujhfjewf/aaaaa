const DEFAULT_URL = "https://example.com/";
const SEARCH_ENGINE_URL = "https://duckduckgo.com/";

const viewer = document.getElementById("viewer");
const urlInput = document.getElementById("url-input");
const statusMessage = document.getElementById("status-message");
const errorTemplate = document.getElementById("error-template");
const searchInput = document.getElementById("search-input");

const backButton = document.getElementById("back");
const forwardButton = document.getElementById("forward");
const reloadButton = document.getElementById("reload");
const goButton = document.getElementById("go");
const searchButton = document.getElementById("search");

const historyStack = [];
let historyIndex = -1;

function normaliseUrl(raw) {
  const trimmed = raw.trim();
  if (!trimmed) {
    throw new Error("URL が空です");
  }

  try {
    return new URL(trimmed).toString();
  } catch (err) {
    try {
      return new URL(`https://${trimmed}`).toString();
    } catch (error) {
      throw new Error("URL の形式が正しくありません");
    }
  }
}

function setStatus(text) {
  statusMessage.textContent = text;
}

function updateNavigationButtons() {
  backButton.disabled = historyIndex <= 0;
  forwardButton.disabled = historyIndex === -1 || historyIndex >= historyStack.length - 1;
  reloadButton.disabled = historyIndex === -1;
}

function showErrorPage(url, message) {
  const template = errorTemplate.content.cloneNode(true);
  template.getElementById("error-url").textContent = url;
  viewer.srcdoc = template.firstElementChild.outerHTML;
  setStatus(message);
}

function loadUrl(rawUrl, { addToHistory = true } = {}) {
  let targetUrl;
  try {
    targetUrl = normaliseUrl(rawUrl);
  } catch (error) {
    showErrorPage(rawUrl || "", error.message);
    return;
  }

  if (addToHistory) {
    historyStack.splice(historyIndex + 1);
    historyStack.push(targetUrl);
    historyIndex = historyStack.length - 1;
  }

  urlInput.value = targetUrl;
  viewer.removeAttribute("srcdoc");
  viewer.src = targetUrl;
  viewer.dataset.url = targetUrl;
  setStatus(`読み込み中: ${targetUrl}`);
  updateNavigationButtons();
}

function buildSearchUrl(query) {
  const trimmed = query.trim();
  if (!trimmed) {
    throw new Error("検索キーワードを入力してください");
  }

  const searchUrl = new URL(SEARCH_ENGINE_URL);
  searchUrl.searchParams.set("q", trimmed);
  return searchUrl.toString();
}

function performSearch(query) {
  let searchUrl;
  try {
    searchUrl = buildSearchUrl(query);
  } catch (error) {
    setStatus(error.message);
    return;
  }

  searchInput.value = query.trim();
  loadUrl(searchUrl);
}

function navigateBack() {
  if (historyIndex > 0) {
    historyIndex -= 1;
    const targetUrl = historyStack[historyIndex];
    loadUrl(targetUrl, { addToHistory: false });
  }
}

function navigateForward() {
  if (historyIndex < historyStack.length - 1) {
    historyIndex += 1;
    const targetUrl = historyStack[historyIndex];
    loadUrl(targetUrl, { addToHistory: false });
  }
}

function reloadCurrent() {
  if (historyIndex >= 0) {
    const current = historyStack[historyIndex];
    loadUrl(current, { addToHistory: false });
  }
}

viewer.addEventListener("load", () => {
  const currentUrl = viewer.dataset.url || viewer.src;
  urlInput.value = currentUrl;
  setStatus(`表示中: ${currentUrl}`);
});

viewer.addEventListener("error", () => {
  const failedUrl = viewer.dataset.url || urlInput.value;
  showErrorPage(failedUrl, "ページを読み込めませんでした");
});

backButton.addEventListener("click", navigateBack);
forwardButton.addEventListener("click", navigateForward);
reloadButton.addEventListener("click", reloadCurrent);

goButton.addEventListener("click", () => {
  loadUrl(urlInput.value);
});

urlInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    loadUrl(urlInput.value);
  }
});

searchButton.addEventListener("click", () => {
  performSearch(searchInput.value);
});

searchInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    performSearch(searchInput.value);
  }
});

window.addEventListener("DOMContentLoaded", () => {
  urlInput.value = DEFAULT_URL;
  loadUrl(DEFAULT_URL);
  updateNavigationButtons();
});

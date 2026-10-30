// First Farmer Agriculture System - Client-side Interactive Modules

document.addEventListener("DOMContentLoaded", () => {
  initMobileDrawer();
  initBookmarkButtons();
  initTabs();
  initConfirmationModals();
  initChatbot();
});

// 1. Mobile Drawer Navigation
function initMobileDrawer() {
  const toggleBtn = document.getElementById("mobile-menu-btn");
  const sidebar = document.getElementById("app-sidebar");
  const backdrop = document.getElementById("sidebar-backdrop");

  if (!toggleBtn || !sidebar) return;

  function toggle() {
    const isOpen = sidebar.classList.toggle("open");
    if (backdrop) backdrop.classList.toggle("active", isOpen);
    toggleBtn.setAttribute("aria-expanded", isOpen ? "true" : "false");
  }

  function close() {
    sidebar.classList.remove("open");
    if (backdrop) backdrop.classList.remove("active");
    toggleBtn.setAttribute("aria-expanded", "false");
  }

  toggleBtn.addEventListener("click", toggle);
  if (backdrop) backdrop.addEventListener("click", close);

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && sidebar.classList.contains("open")) {
      close();
    }
  });
}

// 2. Bookmark Toggle via Fetch with Form Fallback
function initBookmarkButtons() {
  const forms = document.querySelectorAll(".bookmark-form");
  forms.forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector(".bookmark-btn");
      const url = form.action;
      const csrfInput = form.querySelector('input[name="csrf_token"]');
      const csrfToken = csrfInput ? csrfInput.value : "";

      try {
        if (btn) btn.disabled = true;
        const resp = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken,
          },
        });

        if (resp.redirected) {
          window.location.href = resp.url;
          return;
        }

        const data = await resp.json();
        if (data.success && btn) {
          if (data.bookmarked) {
            btn.classList.add("active");
            btn.setAttribute("aria-pressed", "true");
            const label = btn.querySelector(".btn-label");
            if (label) label.textContent = "Saved";
          } else {
            btn.classList.remove("active");
            btn.setAttribute("aria-pressed", "false");
            const label = btn.querySelector(".btn-label");
            if (label) label.textContent = "Bookmark";
          }
        }
      } catch (err) {
        // On network/script error, submit standard form
        form.submit();
      } finally {
        if (btn) btn.disabled = false;
      }
    });
  });
}

// 3. Tab Navigation
function initTabs() {
  const tabContainers = document.querySelectorAll("[data-tabs]");
  tabContainers.forEach((container) => {
    const buttons = container.querySelectorAll(".tab-btn");
    const contents = container.querySelectorAll(".tab-content");

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-tab-target");

        buttons.forEach((b) => b.classList.remove("active"));
        contents.forEach((c) => (c.style.display = "none"));

        btn.classList.add("active");
        const activeContent = document.getElementById(targetId);
        if (activeContent) activeContent.style.display = "block";
      });
    });
  });
}

// 4. Accessible Confirmation Dialogs
function initConfirmationModals() {
  const confirmButtons = document.querySelectorAll("[data-confirm]");
  confirmButtons.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const message = btn.getAttribute("data-confirm") || "Are you sure you want to proceed with this destructive action?";
      if (!window.confirm(message)) {
        e.preventDefault();
      }
    });
  });
}

// 5. Interactive Chatbot
function initChatbot() {
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");
  const messagesBox = document.getElementById("chat-messages");
  const sendBtn = document.getElementById("chat-send-btn");

  if (!chatForm || !chatInput || !messagesBox) return;

  // Scroll to bottom
  messagesBox.scrollTop = messagesBox.scrollHeight;

  // Suggested question buttons
  const promptButtons = document.querySelectorAll(".suggested-prompt-btn");
  promptButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      chatInput.value = btn.textContent.trim();
      chatInput.focus();
    });
  });

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = chatInput.value.trim();
    if (!query) return;

    // Append user message to UI
    appendMessage(query, "user");
    chatInput.value = "";
    if (sendBtn) sendBtn.disabled = true;

    // Append loading bubble
    const loadingElem = appendLoadingBubble();
    messagesBox.scrollTop = messagesBox.scrollHeight;

    const csrfToken = document.querySelector('input[name="csrf_token"]')?.value || "";

    try {
      const resp = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ message: query }),
      });

      const data = await resp.json();
      loadingElem.remove();

      if (data.answer) {
        appendMessage(data.answer, "assistant", data.link_url, data.link_text);
      } else {
        appendMessage("Sorry, I could not process your request at this time.", "assistant");
      }
    } catch (err) {
      loadingElem.remove();
      appendMessage("An error occurred connecting to the service. Please try again.", "assistant");
    } finally {
      if (sendBtn) sendBtn.disabled = false;
      messagesBox.scrollTop = messagesBox.scrollHeight;
    }
  });

  function appendMessage(text, role, linkUrl, linkText) {
    const bubble = document.createElement("div");
    bubble.className = `chat-bubble ${role}`;
    
    // Parse line breaks and simple markdown
    let html = escapeHtml(text).replace(/\n/g, "<br>");
    html = html.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    if (linkUrl && linkText) {
      html += `<div style="margin-top: 8px;"><a href="${linkUrl}" class="btn btn-secondary btn-sm" style="display:inline-block;">${escapeHtml(linkText)} &rarr;</a></div>`;
    }

    bubble.innerHTML = html;
    messagesBox.appendChild(bubble);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }

  function appendLoadingBubble() {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble assistant";
    bubble.innerHTML = "<em>Consulting agricultural database...</em>";
    messagesBox.appendChild(bubble);
    return bubble;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
}


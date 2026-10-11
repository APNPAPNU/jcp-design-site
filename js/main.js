/* JCP Graphic Design: site behavior (vanilla JS, no dependencies) */
(function () {
  "use strict";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Footer year ---------- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ---------- Sticky nav border + mobile menu ---------- */
  var nav = document.querySelector(".nav");
  var toggle = document.querySelector(".nav__toggle");
  var menu = document.getElementById("nav-menu");

  function onScroll() { if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  function setMenu(open, returnFocus) {
    if (!toggle || !menu) return;
    toggle.setAttribute("aria-expanded", String(open));
    menu.classList.toggle("is-open", open);
    if (!open && returnFocus) toggle.focus();
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") !== "true";
      setMenu(open);
      if (open) { var first = menu.querySelector("a"); if (first) first.focus(); }
    });
    menu.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setMenu(false, true);
    });
    document.addEventListener("click", function (e) {
      if (toggle.getAttribute("aria-expanded") === "true" && !e.target.closest(".nav")) setMenu(false);
    });
    window.matchMedia("(min-width: 761px)").addEventListener("change", function (m) { if (m.matches) setMenu(false); });
  }

  /* ---------- Portfolio grid ---------- */
  var items = Array.isArray(window.PORTFOLIO) ? window.PORTFOLIO : [];
  var gallery = document.getElementById("gallery");
  var BASE = "images/portfolio/";

  if (gallery) {
    var frag = document.createDocumentFragment();
    items.forEach(function (item, i) {
      var li = document.createElement("li");
      li.className = "gallery__item reveal";
      li.style.setProperty("--d", (i % 3) * 0.08 + "s");

      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "gallery__btn";
      btn.setAttribute("aria-label", "View larger: " + item.title + " (" + item.category + ")");
      btn.dataset.index = String(i);

      var img = document.createElement("img");
      img.src = BASE + item.file;
      img.alt = item.alt || item.title;
      img.width = item.width || 1600;
      img.height = item.height || 1200;
      img.loading = "lazy";
      img.decoding = "async";

      var meta = document.createElement("span");
      meta.className = "gallery__meta";
      meta.setAttribute("aria-hidden", "true");
      meta.innerHTML = '<span class="gallery__cat"></span><span class="gallery__title"></span>';
      meta.firstChild.textContent = item.category;
      meta.lastChild.textContent = item.title;

      btn.appendChild(img);
      btn.appendChild(meta);
      li.appendChild(btn);
      frag.appendChild(li);
    });
    gallery.appendChild(frag);
  }

  /* ---------- Lightbox (Esc closes, arrows navigate, focus trapped) ---------- */
  var lb = document.getElementById("lightbox");
  var lbImg = document.getElementById("lightbox-img");
  var lbCap = document.getElementById("lightbox-caption");
  var current = 0, lastFocus = null;

  function show(i) {
    if (!items.length) return;
    current = (i + items.length) % items.length;
    var it = items[current];
    lbImg.src = BASE + it.file;
    lbImg.alt = it.alt || it.title;
    lbImg.width = it.width || 1600;
    lbImg.height = it.height || 1200;
    lbCap.innerHTML = "<strong></strong> &middot; <span></span> <span class='sr-only'></span>";
    lbCap.children[0].textContent = it.title;
    lbCap.children[1].textContent = it.category;
    lbCap.children[2].textContent = "(" + (current + 1) + " of " + items.length + ")";
  }
  function openLb(i) {
    if (!lb || typeof lb.showModal !== "function") {
      window.open(BASE + items[i].file, "_blank", "noopener"); return;
    }
    lastFocus = document.activeElement;
    show(i);
    lb.showModal();
    document.body.classList.add("lb-open");
    lb.querySelector(".lightbox__close").focus();
  }
  function closeLb() { if (lb && lb.open) lb.close(); }

  if (lb) {
    lb.addEventListener("close", function () {
      document.body.classList.remove("lb-open");
      if (lastFocus) lastFocus.focus();
    });
    lb.querySelector(".lightbox__close").addEventListener("click", closeLb);
    lb.querySelector(".lightbox__prev").addEventListener("click", function () { show(current - 1); });
    lb.querySelector(".lightbox__next").addEventListener("click", function () { show(current + 1); });
    // Click outside the image/buttons closes
    lb.addEventListener("click", function (e) {
      if (e.target === lb || e.target.classList.contains("lightbox__inner") || e.target.classList.contains("lightbox__figure")) closeLb();
    });
    lb.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); show(current + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); show(current - 1); }
      else if (e.key === "Tab") {
        var f = Array.prototype.slice.call(lb.querySelectorAll("button"));
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
  if (gallery) {
    gallery.addEventListener("click", function (e) {
      var b = e.target.closest(".gallery__btn");
      if (b) openLb(parseInt(b.dataset.index, 10));
    });
  }

  /* ---------- Scroll reveal ---------- */
  var reveals = document.querySelectorAll(".reveal, .step");
  if (!reduceMotion && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ---------- "Start with a free mockup" links preselect the service ---------- */
  var serviceSelect = document.getElementById("f-service");
  document.querySelectorAll("[data-service]").forEach(function (a) {
    a.addEventListener("click", function () {
      if (serviceSelect) serviceSelect.value = a.dataset.service;
    });
  });

  /* ---------- Contact form (AJAX with graceful fallback) ---------- */
  var form = document.getElementById("contact-form");
  var statusEl = document.getElementById("form-status");
  if (form && window.fetch && window.FormData) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      statusEl.className = "form__status";
      statusEl.textContent = "";

      // Honeypot: silently "succeed" for bots
      if (form.elements._honey && form.elements._honey.value) { form.reset(); return; }

      // Validate required fields
      var bad = null;
      ["name", "email", "message"].forEach(function (n) {
        var el = form.elements[n];
        var ok = el.value.trim() !== "" && (n !== "email" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value.trim()));
        el.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok && !bad) bad = el;
      });
      if (bad) {
        statusEl.classList.add("is-error");
        statusEl.textContent = "Please fill in your name, a valid email and a short message.";
        bad.focus();
        return;
      }

      var action = form.getAttribute("action");
      var data = new FormData(form);
      var isWeb3 = action.indexOf("web3forms.com") !== -1;
      if (isWeb3) {
        data.delete("_honey"); data.delete("_next"); data.delete("_template"); data.delete("_subject");
        data.append("subject", "New free mockup request from your website");
        data.append("from_name", "JCP Graphic Design website");
      } else {
        data.delete("access_key");
        data.delete("_next");
        // FormSubmit AJAX endpoint returns JSON instead of redirecting
        action = action.replace("formsubmit.co/", "formsubmit.co/ajax/");
      }

      var btn = form.querySelector('button[type="submit"]');
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = "Sending...";

      fetch(action, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          var ok = res.ok && (res.j.success === true || res.j.success === "true");
          if (!ok) throw new Error(res.j.message || "Request failed");
          form.reset();
          form.querySelectorAll("[aria-invalid]").forEach(function (el) { el.removeAttribute("aria-invalid"); });
          statusEl.classList.add("is-success");
          statusEl.textContent = "Thanks! Your message is on its way. I'll get back to you soon.";
        })
        .catch(function () {
          statusEl.classList.add("is-error");
          statusEl.innerHTML = 'Sorry, something went wrong. Please email me at <a href="mailto:jcpgraphicdesign@gmail.com">jcpgraphicdesign@gmail.com</a> or call <a href="tel:+18653865356">(865) 386-5356</a>.';
        })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  }
})();

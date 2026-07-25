/* ClearCents — main.js */
(function () {
  'use strict';

  /* ---------- Sticky header ---------- */
  const header = document.getElementById('siteHeader');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Mobile nav ---------- */
  const toggle = document.getElementById('navToggle');
  const menu   = document.getElementById('mobileMenu');
  if (toggle && menu) {
    toggle.addEventListener('click', () => {
      const open = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.innerHTML = open ? '&#10005;' : '&#9776;';
    });
    document.addEventListener('click', (e) => {
      if (!toggle.contains(e.target) && !menu.contains(e.target)) {
        menu.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '&#9776;';
      }
    });
  }

  /* ---------- Reading progress bar ---------- */
  const bar     = document.getElementById('progressBar');
  const content = document.getElementById('postContent');
  if (bar && content) {
    const update = () => {
      const rect    = content.getBoundingClientRect();
      const total   = content.offsetHeight;
      const scrolled = Math.max(0, -rect.top);
      const pct    = Math.min(100, Math.round((scrolled / total) * 100));
      bar.style.width = pct + '%';
      bar.setAttribute('aria-valuenow', pct);
    };
    window.addEventListener('scroll', update, { passive: true });
  }

  /* ---------- Scroll-to-top button ---------- */
  const scrollBtn = document.getElementById('scrollTop');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('show', window.scrollY > 400);
    }, { passive: true });
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Fade-in on scroll (IntersectionObserver) ---------- */
  const fadeEls = document.querySelectorAll('.fade-in');
  if (fadeEls.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    fadeEls.forEach((el) => io.observe(el));
  } else {
    fadeEls.forEach((el) => el.classList.add('visible'));
  }

  /* ---------- 3D card tilt on desktop ---------- */
  if (window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.post-card, .post-featured').forEach((card) => {
      card.addEventListener('mousemove', (e) => {
        const rect  = card.getBoundingClientRect();
        const cx    = rect.left + rect.width  / 2;
        const cy    = rect.top  + rect.height / 2;
        const dx    = (e.clientX - cx) / (rect.width  / 2);
        const dy    = (e.clientY - cy) / (rect.height / 2);
        const rotY  = dx * 4;
        const rotX  = -dy * 3;
        card.style.transform =
          `perspective(900px) rotateY(${rotY}deg) rotateX(${rotX}deg) translateY(-6px)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  /* ---------- Copy link button ---------- */
  const copyBtn = document.getElementById('copyLink');
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        const orig = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        setTimeout(() => { copyBtn.textContent = orig; }, 2000);
      } catch (_) {
        /* fallback: select URL from address bar */
      }
    });
  }

  /* ---------- Lazy image fade-in ---------- */
  document.querySelectorAll('img[loading="lazy"]').forEach((img) => {
    img.style.opacity = '0';
    img.style.transition = 'opacity 0.4s ease';
    if (img.complete) {
      img.style.opacity = '1';
    } else {
      img.addEventListener('load', () => { img.style.opacity = '1'; });
    }
  });

  /* ---------- Newsletter form — async POST to Google Apps Script ---------- */
  const nlForm = document.getElementById('nlForm');
  if (nlForm) {
    const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbxFaLYjkSvY7O6crghxGAY_d9lAzHymOd6TuB2CA8HDn11mS6diEaYGTSTxLR7Kb81D/exec';
    nlForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('nlEmail').value.trim();
      if (!email || !SCRIPT_URL.startsWith('https://')) return;
      const btn = nlForm.querySelector('.nl-btn');
      btn.textContent = 'Sending…';
      btn.disabled = true;
      fetch(`${SCRIPT_URL}?email=${encodeURIComponent(email)}`, { mode: 'no-cors' })
        .then(() => {
          nlForm.style.display = 'none';
          const ok = document.getElementById('nlSuccess');
          if (ok) ok.style.display = 'block';
        })
        .catch(() => {
          btn.textContent = 'Subscribe free →';
          btn.disabled = false;
        });
    });
  }

})();

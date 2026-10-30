// Cobb Refrigerated Freight — site behavior
(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');

  // Mobile menu
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Header shadow once the page scrolls
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Reveal-on-scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -60px 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Quote form: only shown once a delivery endpoint is configured in data-endpoint
  // (e.g. https://formsubmit.co/ajax/you@example.com). Until then, visitors see the call card.
  var form = document.querySelector('[data-quote-form]');
  if (form) {
    var endpoint = form.getAttribute('data-endpoint');
    var fallback = document.querySelector('[data-quote-fallback]');
    if (endpoint) {
      form.hidden = false;
      if (fallback) fallback.hidden = true;
      var status = form.querySelector('.form-status');
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (form.querySelector('.hp input').value) return;
        var btn = form.querySelector('button[type="submit"]');
        btn.disabled = true;
        status.className = 'form-status';
        status.textContent = 'Sending…';
        var data = Object.fromEntries(new FormData(form).entries());
        delete data._hp;
        data._subject = 'New quote request — cobb website';
        fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify(data)
        }).then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.reset();
          status.className = 'form-status ok';
          status.textContent = 'Thank you — your request was sent. We will be in touch shortly.';
        }).catch(function () {
          status.className = 'form-status err';
          status.textContent = 'Sorry, that did not go through. Please call (209) 576-0327.';
        }).finally(function () { btn.disabled = false; });
      });
    }
  }
})();

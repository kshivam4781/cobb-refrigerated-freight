// Cobb Refrigerated Freight: site behavior
(function () {
  var doc = document;
  var body = doc.body;
  var header = doc.querySelector('.site-header');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- Header: transparent over the hero, solid once scrolled ----------
  var alwaysSolid = body.getAttribute('data-header') === 'solid';
  var callBar = doc.querySelector('.call-bar');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('solid', alwaysSolid || y > 40);
    if (callBar) callBar.classList.toggle('show', y > 520);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ---------- Mobile menu ----------
  var toggle = doc.querySelector('.menu-toggle');
  var nav = doc.getElementById('site-nav');
  function setMenu(open) {
    nav.classList.toggle('open', open);
    body.classList.toggle('menu-open', open);
    body.classList.toggle('lock', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    toggle.querySelector('use').setAttribute('href', open ? '#i-x' : '#i-menu');
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setMenu(!nav.classList.contains('open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  }

  // ---------- Services dropdown (click/keyboard; hover handled in CSS) ----------
  doc.querySelectorAll('.nav-item > button').forEach(function (btn) {
    var item = btn.parentElement;
    btn.addEventListener('click', function () {
      var open = !item.classList.contains('open');
      item.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget) && window.innerWidth > 1024) {
        item.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  });

  doc.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    if (nav && nav.classList.contains('open')) { setMenu(false); toggle.focus(); }
    doc.querySelectorAll('.nav-item.open').forEach(function (i) {
      i.classList.remove('open');
      i.querySelector('button').setAttribute('aria-expanded', 'false');
    });
  });

  // ---------- Quote dialog ----------
  var dialog = doc.getElementById('quote-dialog');
  function openQuote(service) {
    if (!dialog) return;
    if (nav && nav.classList.contains('open')) setMenu(false);
    var wrap = dialog.querySelector('[data-form-wrap]');
    wrap.classList.remove('sent');
    var sel = dialog.querySelector('select[name="service"]');
    if (service && sel) {
      sel.value = service;
      sel.dispatchEvent(new Event('change', { bubbles: true }));
    }
    if (typeof dialog.showModal === 'function') {
      dialog.showModal();
      body.classList.add('lock');
    } else {
      window.location.href = 'contact.html#quote';
    }
  }
  doc.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-open-quote]');
    if (opener) { e.preventDefault(); openQuote(opener.getAttribute('data-service')); }
    if (e.target.closest('[data-close-quote]')) dialog.close();
  });
  if (dialog) {
    dialog.addEventListener('close', function () { body.classList.remove('lock'); });
    dialog.addEventListener('click', function (e) { if (e.target === dialog) dialog.close(); });
  }

  // ---------- Quote forms -> email ----------
  // Tries Web3Forms (if an access key is configured), then FormSubmit. Only a confirmed
  // success shows the thank-you state; otherwise the visitor is asked to call.
  function postJSON(url, payload) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok || String(j.success) !== 'true') throw new Error(j.message || 'send failed');
        return j;
      });
    });
  }

  function sendQuote(form, data) {
    var subject = 'Website quote request: ' + (data.service || 'General') + ' from ' + (data.name || 'website visitor');
    var senders = [];
    var key = form.getAttribute('data-w3f-key');
    var email = form.getAttribute('data-fs-email');
    if (key) {
      senders.push(function () {
        return postJSON('https://api.web3forms.com/submit', Object.assign({
          access_key: key, subject: subject, from_name: 'Cobb Refrigerated Freight website'
        }, data));
      });
    }
    if (email) {
      senders.push(function () {
        return postJSON('https://formsubmit.co/ajax/' + email, Object.assign({
          _subject: subject, _template: 'table', _captcha: 'false'
        }, data));
      });
    }
    return senders.reduce(function (chain, send) {
      return chain.catch(function () { return send(); });
    }, Promise.reject(new Error('no sender')));
  }

  // Show only the fields that fit the chosen service. Hidden rows are disabled so they
  // are neither validated nor sent. The hero card also swaps its title, icon, and button.
  function applyService(form, animate) {
    var radio = form.querySelector('input[name="service"]:checked');
    var sel = form.querySelector('select[name="service"]');
    var value = radio ? radio.value : (sel ? sel.value : '');
    form.querySelectorAll('[data-when]').forEach(function (row) {
      var on = row.getAttribute('data-when').split('|').indexOf(value) > -1;
      var was = !row.hidden;
      row.hidden = !on;
      row.querySelectorAll('input, select, textarea').forEach(function (el) { el.disabled = !on; });
      if (on && !was && animate && !reduceMotion) {
        row.classList.remove('swap-in'); void row.offsetWidth; row.classList.add('swap-in');
      }
    });
    if (!radio) return;
    var seg = radio.closest('.seg');
    if (seg) seg.style.setProperty('--i', radio.getAttribute('data-i'));
    var card = form.closest('.quote-card');
    var cta = form.querySelector('span[data-cta]');
    if (cta) cta.textContent = radio.getAttribute('data-cta');
    if (!card) return;
    var title = card.querySelector('[data-qc-title]');
    var sub = card.querySelector('[data-qc-sub]');
    var icon = card.querySelector('[data-qc-icon]');
    if (title) title.innerHTML = radio.getAttribute('data-title');
    if (sub) sub.innerHTML = radio.getAttribute('data-sub');
    if (icon) icon.setAttribute('href', '#' + radio.getAttribute('data-icon'));
    if (animate && !reduceMotion) {
      var head = card.querySelector('.qc-head');
      head.classList.remove('swap-in'); void head.offsetWidth; head.classList.add('swap-in');
    }
  }

  doc.querySelectorAll('form[data-quote]').forEach(function (form) {
    applyService(form, false);
    form.addEventListener('change', function (e) {
      if (e.target.name === 'service') applyService(form, true);
    });
    form.addEventListener('reset', function () { setTimeout(function () { applyService(form, false); }, 0); });
  });

  doc.querySelectorAll('form[data-quote]').forEach(function (form) {
    var wrap = form.closest('[data-form-wrap]');
    var errorBox = form.querySelector('.form-error');
    var submit = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errorBox.classList.remove('show');
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var data = {};
      new FormData(form).forEach(function (value, key) { if (String(value).trim()) data[key] = String(value).trim(); });
      if (data.botcheck) { wrap.classList.add('sent'); return; }
      data.submitted_from = window.location.href;

      submit.setAttribute('aria-busy', 'true');
      sendQuote(form, data)
        .then(function () { form.reset(); wrap.classList.add('sent'); })
        .catch(function () { errorBox.classList.add('show'); })
        .finally(function () { submit.removeAttribute('aria-busy'); });
    });
  });
  doc.querySelectorAll('[data-reset-form]').forEach(function (btn) {
    btn.addEventListener('click', function () { btn.closest('[data-form-wrap]').classList.remove('sent'); });
  });

  // ---------- Services showcase tabs ----------
  doc.querySelectorAll('[data-tabs]').forEach(function (root) {
    var tabs = root.querySelectorAll('[role="tab"]');
    var panels = root.querySelectorAll('[role="tabpanel"]');
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        panels[j].classList.toggle('active', on);
        panels[j].hidden = false;
        panels[j].setAttribute('aria-hidden', String(!on));
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(i); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    select(0);
  });

  // ---------- Count-up numbers ----------
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count'));
    if (reduceMotion) { el.textContent = end.toLocaleString(); return; }
    var start = performance.now(), dur = 1600;
    (function tick(now) {
      var p = Math.min((now - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(end * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(tick);
    })(start);
  }

  // ---------- Scroll-triggered effects ----------
  var watched = doc.querySelectorAll('.reveal, [data-count], .lanes-map, .steps li');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        // Also reveal anything already scrolled past (fast scrolls, anchor jumps).
        if (!entry.isIntersecting && entry.boundingClientRect.top > 0) return;
        var el = entry.target;
        el.classList.add('in');
        if (el.hasAttribute('data-count')) countUp(el);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.12 });
    watched.forEach(function (el) { io.observe(el); });
  } else {
    watched.forEach(function (el) { el.classList.add('in'); });
  }

  // ---------- Service page sub-nav highlighting ----------
  var subLinks = doc.querySelectorAll('.subnav a');
  if (subLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    subLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        subLinks.forEach(function (a) { a.classList.remove('active'); });
        var link = map[entry.target.id];
        if (link) {
          link.classList.add('active');
          var bar = link.parentElement;
          bar.scrollTo({ left: link.offsetLeft - (bar.clientWidth - link.offsetWidth) / 2, behavior: reduceMotion ? 'auto' : 'smooth' });
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { var s = doc.getElementById(id); if (s) so.observe(s); });
  }

  // ---------- Cookie choice & consent-gated embeds ----------
  // The only thing stored is the visitor's choice, in localStorage under "cobb_consent"
  // ("all" or "essential"). Google Maps embeds load only with "all" or a click on "Load map".
  var CONSENT_KEY = 'cobb_consent';
  var banner = doc.getElementById('consent');
  function readConsent() {
    try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; }
  }
  function writeConsent(v) {
    try { localStorage.setItem(CONSENT_KEY, v); } catch (e) { /* storage blocked: choice lasts for this page */ }
  }
  function loadMap(box) {
    if (!box || box.querySelector('iframe')) return;
    var f = doc.createElement('iframe');
    f.src = box.getAttribute('data-map');
    f.title = box.getAttribute('data-map-title') || 'Map';
    f.loading = 'lazy';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    box.innerHTML = '';
    box.appendChild(f);
  }
  function applyConsent(v) {
    if (v === 'all') doc.querySelectorAll('[data-map]').forEach(loadMap);
  }
  function showBanner(show) {
    if (!banner) return;
    banner.hidden = !show;
    body.classList.toggle('consent-open', show);
    if (show) requestAnimationFrame(function () { banner.classList.add('in'); });
    else banner.classList.remove('in');
  }
  var privacySignal = navigator.globalPrivacyControl === true || navigator.doNotTrack === '1' || window.doNotTrack === '1';
  var consent = readConsent();
  if (!consent && privacySignal) { consent = 'essential'; writeConsent(consent); }
  applyConsent(consent);
  if (!consent) setTimeout(function () { showBanner(true); }, 700);

  doc.addEventListener('click', function (e) {
    var choice = e.target.closest('[data-consent]');
    if (choice) {
      var v = choice.getAttribute('data-consent');
      var mapsLoaded = doc.querySelector('[data-map] iframe');
      writeConsent(v);
      showBanner(false);
      if (v === 'essential' && mapsLoaded) window.location.reload();
      else applyConsent(v);
    }
    if (e.target.closest('[data-consent-open]')) { e.preventDefault(); showBanner(true); }
    var load = e.target.closest('[data-load-map]');
    if (load) loadMap(load.closest('[data-map]'));
  });

  // ---------- Footer year ----------
  doc.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();

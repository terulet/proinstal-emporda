(function () {
  'use strict';

  var consentKey = 'proinstal_analytics_consent';
  var measurementId = String(window.PROINSTAL_GA4_ID || '');
  var analyticsReady = false;

  function validMeasurementId() {
    return /^G-[A-Z0-9]{6,}$/.test(measurementId);
  }

  function loadAnalytics() {
    if (analyticsReady || !validMeasurementId()) return;
    analyticsReady = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(measurementId);
    document.head.appendChild(script);
  }

  window.proinstalTrack = function (eventName, parameters) {
    if (!analyticsReady || typeof window.gtag !== 'function') return;
    window.gtag('event', eventName, parameters || {});
  };

  function setConsent(value) {
    localStorage.setItem(consentKey, value);
    var banner = document.getElementById('analytics-consent');
    if (banner) banner.remove();
    if (value === 'accepted') loadAnalytics();
  }

  function showConsentBanner() {
    if (!validMeasurementId() || localStorage.getItem(consentKey)) return;
    var banner = document.createElement('aside');
    banner.id = 'analytics-consent';
    banner.className = 'consent-banner';
    banner.setAttribute('aria-label', 'Preferències d’analítica');
    banner.innerHTML = '<p><strong>Analítica opcional</strong><br>Amb el teu permís, mesurem visites i contactes per millorar la web. No enviem a Google el nom, telèfon ni el text del formulari. <a href="/privacitat.html">Més informació</a>.</p><div><button type="button" data-consent="rejected">Rebutjar</button><button type="button" class="accept" data-consent="accepted">Acceptar</button></div>';
    banner.addEventListener('click', function (event) {
      var button = event.target.closest('[data-consent]');
      if (button) setConsent(button.getAttribute('data-consent'));
    });
    document.body.appendChild(banner);
  }

  function bindContactEvents() {
    document.addEventListener('click', function (event) {
      var link = event.target.closest('a[href]');
      if (!link) return;
      var href = link.getAttribute('href') || '';
      var method = '';
      if (href.indexOf('wa.me/') !== -1) method = 'whatsapp';
      else if (href.indexOf('tel:') === 0) method = 'phone';
      else if (href.indexOf('mailto:') === 0) method = 'email';
      else if (href.indexOf('instagram.com/') !== -1) method = 'instagram';
      if (method) window.proinstalTrack(method === 'instagram' ? 'outbound_click' : 'generate_lead', { method: method });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindContactEvents();
    if (localStorage.getItem(consentKey) === 'accepted') loadAnalytics();
    else showConsentBanner();
  });
}());

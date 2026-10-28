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
    var language = (document.documentElement.lang || 'ca').toLowerCase().split('-')[0];
    var messages = {
      ca: {
        label: 'Preferències d’analítica', title: 'Analítica opcional',
        description: 'Amb el teu permís, mesurem visites i clics als canals de contacte per millorar la web. No enviem a Google el nom, telèfon ni el text del formulari.',
        more: 'Més informació', reject: 'Rebutjar', accept: 'Acceptar'
      },
      es: {
        label: 'Preferencias de analítica', title: 'Analítica opcional',
        description: 'Con tu permiso, medimos visitas y clics en los canales de contacto para mejorar la web. No enviamos a Google el nombre, el teléfono ni el texto del formulario.',
        more: 'Más información', reject: 'Rechazar', accept: 'Aceptar'
      },
      fr: {
        label: 'Préférences de mesure d’audience', title: 'Mesure d’audience facultative',
        description: 'Avec votre accord, nous mesurons les visites et les clics vers les moyens de contact pour améliorer le site. Nous ne transmettons pas à Google le nom, le numéro de téléphone ni le texte du formulaire.',
        more: 'Plus d’informations', reject: 'Refuser', accept: 'Accepter'
      }
    };
    var message = messages[language] || messages.ca;
    var banner = document.createElement('aside');
    banner.id = 'analytics-consent';
    banner.className = 'consent-banner';
    banner.setAttribute('aria-label', message.label);
    banner.innerHTML = '<p><strong>' + message.title + '</strong><br>' + message.description + ' <a href="/privacitat.html">' + message.more + '</a>.</p><div><button type="button" data-consent="rejected">' + message.reject + '</button><button type="button" class="accept" data-consent="accepted">' + message.accept + '</button></div>';
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
      if (method) window.proinstalTrack(method === 'instagram' ? 'outbound_click' : 'contact_click', { method: method });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    bindContactEvents();
    if (localStorage.getItem(consentKey) === 'accepted') loadAnalytics();
    else showConsentBanner();
  });
}());

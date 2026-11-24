(function () {
  'use strict';

  var phones = document.querySelectorAll('[data-call-choice]');
  if (!phones.length) return;

  var selected = Math.random() < 0.5 ? 0 : 1;
  var storageKey = 'proinstal_call_destination';

  try {
    var saved = sessionStorage.getItem(storageKey);
    if (saved === '0' || saved === '1') selected = Number(saved);
    else sessionStorage.setItem(storageKey, String(selected));
  } catch (error) {
    // The call links also work when browser storage is unavailable.
  }

  var destination = phones[selected].getAttribute('href');
  document.querySelectorAll('[data-call-default]').forEach(function (link) {
    link.setAttribute('href', destination);
    var number = link.querySelector('[data-call-number]');
    if (number) number.textContent = phones[selected].textContent.trim();
  });

  if (selected === 1) {
    document.querySelectorAll('[data-call-list]').forEach(function (list) {
      var links = list.querySelectorAll('[data-call-choice]');
      list.insertBefore(links[1], links[0]);
    });
  }
}());

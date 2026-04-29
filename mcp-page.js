(function () {
  /* Only run on the AI/MCP page */
  function onMcpPage() {
    return location.pathname.includes('ai-mcp');
  }

  /* ── Copy buttons ── */
  function initCopyBtns() {
    document.querySelectorAll('.mcp-tc-copy[data-copy]').forEach(function (btn) {
      if (btn._mcpReady) return;
      btn._mcpReady = true;
      btn.addEventListener('click', function () {
        navigator.clipboard.writeText(btn.getAttribute('data-copy')).then(function () {
          var orig = btn.textContent;
          btn.textContent = '✓ Copied';
          btn.style.color = '#28c840';
          btn.style.background = 'rgba(40,200,64,0.1)';
          btn.style.borderColor = 'rgba(40,200,64,0.25)';
          setTimeout(function () {
            btn.textContent = orig;
            btn.style.color = '';
            btn.style.background = '';
            btn.style.borderColor = '';
          }, 2000);
        });
      });
    });
  }

  /* ── Stagger entrance via IntersectionObserver ── */
  function initAnimations() {
    var heading = document.querySelector('.mcp-tools-heading');
    var cards = document.querySelectorAll('.mcp-tc-card');
    if (!cards.length) return;

    if (!('IntersectionObserver' in window)) {
      if (heading) heading.classList.add('mcp-heading-visible');
      cards.forEach(function (c) { c.classList.add('mcp-card-visible'); });
      return;
    }

    var hObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('mcp-heading-visible');
          hObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });
    if (heading) hObs.observe(heading);

    var cObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          var idx = Array.prototype.indexOf.call(cards, e.target);
          setTimeout(function () {
            e.target.classList.add('mcp-card-visible');
          }, idx * 130);
          cObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.08 });
    cards.forEach(function (c) { cObs.observe(c); });
  }

  /* ── Force dark mode ── */
  function applyDark() {
    try { localStorage.setItem('theme', 'dark'); } catch (e) {}
    document.documentElement.setAttribute('data-theme', 'dark');
    document.documentElement.classList.add('dark');
    document.documentElement.classList.remove('light');
  }

  function applyDarkIfOnPage() {
    if (onMcpPage()) applyDark();
  }

  /* ── CLI Chat Animation ── */
  function initChatDemo() {
    if (window._mcpChatStop) { try { window._mcpChatStop(); } catch (e) {} }

    window._mcpChatSeq = (window._mcpChatSeq || 0) + 1;
    var mySeq = window._mcpChatSeq;
    function alive() { return mySeq === window._mcpChatSeq; }

    function g(id) { return document.getElementById(id); }
    function show(id) { var e = g(id); if (e) e.classList.add('mcp-show'); }
    function hide(id) { var e = g(id); if (e) e.classList.remove('mcp-show'); }

    if (!g('mcp-chat-demo')) return;

    var tids = [];
    function later(fn, ms) {
      tids.push(setTimeout(function () { if (alive()) fn(); }, ms));
    }

    window._mcpChatStop = function () { tids.forEach(clearTimeout); window._mcpChatSeq++; };

    var MSG = 'Build a scrollable community feed';
    var RESP = [
      { t: "Here's your feed setup:", c: 'mcp-ans-prose' },
      { t: '', c: 'mcp-ans-blank' },
      { t: 'const { data, loadMore } = useFeed({', c: 'mcp-ans-code' },
      { t: '  feedType: "globalFeed",', c: 'mcp-ans-code' },
      { t: '  pageSize: 20', c: 'mcp-ans-code' },
      { t: '});', c: 'mcp-ans-code' },
      { t: '', c: 'mcp-ans-blank' },
      { t: 'loadMore() fetches next page ✓', c: 'mcp-ans-note' }
    ];

    function typeMsg(text, done) {
      var i = 0;
      var buf = '';
      function tick() {
        if (!alive()) return;
        var el = g('mcp-typed');
        if (!el) return;
        if (i < text.length) {
          buf += text[i++];
          el.textContent = buf;
          setTimeout(tick, 38 + Math.random() * 32);
        } else { done && done(); }
      }
      tick();
    }

    function streamResp(done) {
      var i = 0;
      function next() {
        if (!alive()) return;
        var el = g('mcp-ans-body');
        if (i >= RESP.length) { done && done(); return; }
        if (el) {
          var d = document.createElement('div');
          d.className = 'mcp-ans-line ' + RESP[i].c;
          d.textContent = RESP[i].t;
          el.appendChild(d);
        }
        i++;
        setTimeout(next, 155);
      }
      next();
    }

    function reset() {
      var typedEl = g('mcp-typed'); if (typedEl) typedEl.textContent = '';
      var ansBody = g('mcp-ans-body'); if (ansBody) ansBody.innerHTML = '';
      var curEl = g('mcp-cur'); if (curEl) curEl.classList.remove('mcp-cur-off');
      var demo = g('mcp-chat-demo'); if (demo) { demo.style.transition = ''; demo.style.opacity = '1'; }
      ['mcp-think', 'mcp-tool1', 'mcp-res1', 'mcp-tool2', 'mcp-res2', 'mcp-ans'].forEach(hide);
    }

    function run() {
      if (!alive()) return;
      reset();
      later(function () {
        typeMsg(MSG, function () {
          later(function () {
            var curEl = g('mcp-cur'); if (curEl) curEl.classList.add('mcp-cur-off');
            show('mcp-think');
          }, 380);
          later(function () { show('mcp-tool1'); }, 2600);
          later(function () { show('mcp-res1'); }, 3020);
          later(function () { show('mcp-tool2'); }, 3440);
          later(function () { show('mcp-res2'); }, 3860);
          later(function () {
            hide('mcp-think');
            show('mcp-ans');
            streamResp(function () {
              later(function () {
                var demo = g('mcp-chat-demo');
                if (demo) { demo.style.transition = 'opacity 0.55s'; demo.style.opacity = '0'; }
                later(function () { run(); }, 620);
              }, 3200);
            });
          }, 4280);
        });
      }, 250);
    }

    run();
  }

  function boot() {
    if (!onMcpPage()) return;
    applyDark();
    setTimeout(applyDarkIfOnPage, 50);
    setTimeout(applyDarkIfOnPage, 300);
    setTimeout(applyDarkIfOnPage, 800);
    initCopyBtns();
    initAnimations();
    initChatDemo();
  }

  /* Patch history to restore theme when leaving the MCP page */
  if (!history._mcpPatched) {
    history._mcpPatched = true;
    var _origPush = history.pushState;
    history.pushState = function () {
      _origPush.apply(this, arguments);
      if (!location.pathname.includes('ai-mcp')) {
        try { localStorage.removeItem('theme'); } catch (e) {}
      } else {
        /* Navigated TO the MCP page — boot after a tick for React to render */
        setTimeout(boot, 100);
        setTimeout(boot, 800);
      }
    };
  }

  /* Initial load */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
    setTimeout(boot, 800);
  }
})();

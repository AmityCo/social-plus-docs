// ---------------------------------------------------------------------------
// Demo iframe theme sync — mirrors Mintlify's dark/light mode into the iframe
// ---------------------------------------------------------------------------
(function () {
  function getIframe() {
    return document.getElementById('demo-iframe');
  }

  function getCurrentTheme() {
    return document.documentElement.classList.contains('dark') ||
      document.documentElement.getAttribute('data-theme') === 'dark'
      ? 'dark'
      : 'light';
  }

  function syncTheme() {
    var iframe = getIframe();
    if (!iframe || !iframe.contentWindow) return;
    var theme = getCurrentTheme();
    iframe.contentWindow.postMessage({ type: 'SET_DEMO_THEME', theme: theme }, '*');
    console.log('[scrollbar.js] Synced theme to iframe:', theme);
  }

  // Watch for Mintlify theme class changes on <html>
  var observer = new MutationObserver(function () {
    syncTheme();
  });
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class', 'data-theme'],
  });

  // Also sync when iframe loads or page navigates
  document.addEventListener('DOMContentLoaded', function () {
    var iframe = getIframe();
    if (iframe) {
      iframe.addEventListener('load', function () {
        setTimeout(syncTheme, 300);
      });
    }
    setTimeout(syncTheme, 1000);
  });

  // Sync immediately in case DOMContentLoaded already fired
  if (document.readyState !== 'loading') {
    setTimeout(syncTheme, 1000);
  }
})();

// ---------------------------------------------------------------------------
// Auto-show scrollbar functionality
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function() {
  let scrollTimer = null;
  
  function showScrollbar() {
    document.documentElement.classList.add('scrolling');
    document.documentElement.style.setProperty('--scrollbar-opacity', '1');
    
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => {
      document.documentElement.classList.remove('scrolling');
      document.documentElement.style.setProperty('--scrollbar-opacity', '0');
    }, 1500); // Hide after 1.5 seconds of no scrolling
  }
  
  // Show scrollbar on scroll
  window.addEventListener('scroll', showScrollbar);
  
  // Show scrollbar on mouse wheel
  document.addEventListener('wheel', showScrollbar);
  
  // Show scrollbar on touch scroll (mobile)
  document.addEventListener('touchstart', showScrollbar);
  document.addEventListener('touchmove', showScrollbar);
  
  // Show scrollbar on hover over scrollable areas
  document.addEventListener('mouseenter', function(e) {
    if (e.target.scrollHeight > e.target.clientHeight) {
      showScrollbar();
    }
  }, true);
});

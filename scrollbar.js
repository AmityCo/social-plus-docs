// Auto-show scrollbar functionality
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

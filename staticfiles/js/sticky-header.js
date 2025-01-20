

window.addEventListener('scroll', function() {
    const headerLogo = document.getElementById('header-logo');
    const stickyHeader = document.getElementById('sticky-header');
    
    if (window.scrollY > 0 && stickyHeader.classList.contains('sticky')) {
        headerLogo.src = '/static/img/logo1.png'; // sticky durum için logo
    } else {
        headerLogo.src = 'static/img/logo1.jpg'; // normal durum için logo
    }
});
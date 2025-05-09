/* JavaScript to prevent right-click and content copying */
document.addEventListener('contextmenu', function(e) {
  e.preventDefault();
  alert('حقوق الملكية محفوظة لشركة إطلاق المتميزة المحدودة. غير مسموح بنسخ المحتوى أو الصور.');
});

document.addEventListener('keydown', function(e) {
  // Prevent Ctrl+S, Ctrl+U, Ctrl+P, Ctrl+C
  if (
    (e.ctrlKey && (e.key === 's' || e.key === 'u' || e.key === 'p' || e.key === 'c')) ||
    // Prevent F12 key
    (e.key === 'F12')
  ) {
    e.preventDefault();
    alert('حقوق الملكية محفوظة لشركة إطلاق المتميزة المحدودة. غير مسموح بنسخ المحتوى أو الصور.');
  }
});

// Prevent text selection
document.addEventListener('selectstart', function(e) {
  e.preventDefault();
});

// Prevent drag and drop of images
document.addEventListener('dragstart', function(e) {
  e.preventDefault();
});

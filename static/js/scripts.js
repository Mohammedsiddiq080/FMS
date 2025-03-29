document.addEventListener('DOMContentLoaded', function () {

    // Form Validation for All Pages
    const forms = document.querySelectorAll('form');
  
    forms.forEach(form => {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        const inputs = form.querySelectorAll('input');
        let isValid = true;
  
        inputs.forEach(input => {
          if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
          } else {
            input.classList.remove('error');
          }
        });
  
        if (isValid) {
          fetch(form.action, {
            method: form.method,
            body: new FormData(form)
          })
          .then(response => response.json())
          .then(data => alert(data.message || data.error))
          .catch(error => console.error('Error:', error));
        } else {
          alert('Please fill in all fields.');
        }
      });
    });
  
    // Smooth Scroll for Internal Links
    const links = document.querySelectorAll('a[href^="#"]');
  
    links.forEach(link => {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          window.scrollTo({
            top: target.offsetTop,
            behavior: 'smooth'
          });
        }
      });
    });
  
    // Button Animation
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
      button.addEventListener('mouseenter', function () {
        this.style.transform = 'scale(1.05)';
      });
  
      button.addEventListener('mouseleave', function () {
        this.style.transform = 'scale(1)';
      });
    });
  
    // Error Handling for Inputs
    document.querySelectorAll('input').forEach(input => {
      input.addEventListener('input', () => {
        if (input.value.trim()) {
          input.classList.remove('error');
        }
      });
    });
  });
  
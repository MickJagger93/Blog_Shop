document.addEventListener("DOMContentLoaded", function() {
    
    const passwordFields = document.querySelectorAll('input[type="password"]');
    
    passwordFields.forEach(field => {
        
        const wrapper = document.createElement('div');
        wrapper.style.position = 'relative';
        wrapper.style.display = 'flex';
        wrapper.style.alignItems = 'center';
        
        field.parentNode.insertBefore(wrapper, field);
        wrapper.appendChild(field);
        
        const toggleBtn = document.createElement('span');
        toggleBtn.innerHTML = '👁️';
        toggleBtn.style.cursor = 'pointer';
        toggleBtn.style.position = 'absolute';
        toggleBtn.style.right = '10px';
        toggleBtn.style.userSelect = 'none';
        
        wrapper.appendChild(toggleBtn);
        
        toggleBtn.addEventListener('click', function() {
            if (field.type === 'password') {
                field.type = 'text';
                this.innerHTML = '🔒'; // Cambia el icono
            } else {
                field.type = 'password';
                this.innerHTML = '👁️';
            }
        });
    });
});

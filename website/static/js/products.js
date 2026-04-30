document.addEventListener('DOMContentLoaded', () => {
   
   const searchInput = document.getElementById('search-input');
   const productContainer = document.getElementById('product-container');

   let searchTimeout = null;

   if (searchInput && productContainer) {
      
      searchInput.addEventListener('keyup', (e) => {
         clearTimeout(searchTimeout); 

         searchTimeout = setTimeout(() => {
            const query = e.target.value.trim();
            
            // CAMBIO 1: Si se borra todo (query vacío), permitimos el fetch para resetear la lista
            if (query.length === 1) return; 

            const url = `?q=${query}&ajax=1`;

            fetch(url)
               .then(response => response.text())
               .then(html => {
                  productContainer.innerHTML = html;

                  const newItems = productContainer.querySelectorAll('.product-item');
                  newItems.forEach(item => {
                     // CAMBIO 2: Si el IntersectionObserver existe, lo vinculamos de nuevo
                     if (typeof observer !== 'undefined') {
                        // Reseteamos el estilo inicial para que la animación se dispare
                        item.style.opacity = "0"; 
                        observer.observe(item);
                     } else {
                        // Si no hay observer, forzamos que se vea
                        item.style.opacity = "1";
                     }
                  });
               })
               .catch(error => console.error('Error en búsqueda:', error));
         }, 350); 
      });
   }
});

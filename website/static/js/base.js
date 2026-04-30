document.addEventListener('DOMContentLoaded', () => {
    
    // --- Utilidades ---
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

    const closeAllModals = () => {
        document.querySelectorAll('.modal').forEach(m => {
            m.style.display = 'none';
            m.setAttribute('aria-hidden', 'true');
        });
    };

    // --- Listeners Globales (Delegación de eventos) ---
    document.addEventListener('click', (e) => {
        
        // 1. Cerrar Modales
        if (e.target.classList.contains('close-btn') || e.target.classList.contains('close-button') || e.target.classList.contains('modal')) {
            closeAllModals();
        }

        // 2. Abrir Modal de Producto (Vista Rápida)
                
        const btnView = e.target.closest('.btn-view');
        if (btnView) {
            const item = btnView.closest('.product-item');
            const productModal = document.getElementById('productModal');
            
            if (productModal && item) {
                const nombreParaRegistrar = item.dataset.name; // Usamos dataset porque SI existe en tu HTML
                console.log("Registrando:", nombreParaRegistrar);

                fetch('/dashboard/register_clic/', { // <--- Asegúrate que el nombre de la función en la URL sea 'register_clic' como en tu urls.py
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ 'producto': nombreParaRegistrar })
                })
                .then(res => res.json())
                .then(data => console.log("Servidor dice:", data))
                .catch(err => console.log("Error en fetch:", err));
                
                const stock = parseInt(item.dataset.quantity) || 0;
                const addToCartBtn = document.getElementById('add-to-cart');
                const qtyControl = document.querySelector('.quantity-control');

                // SEGUNDO: Llenamos los datos básicos
                document.getElementById('modal-img').src = item.dataset.image;
                document.getElementById('modal-name').textContent = item.dataset.name;
                document.getElementById('modal-name').dataset.productId = item.dataset.id;
                document.getElementById('modal-price').textContent = item.dataset.price;
                document.getElementById('modal-description').textContent = item.dataset.description;
                document.getElementById('modal-quantity').textContent = stock;
                document.getElementById('quantity-input').value = 1;

                // TERCERO: Lógica de bloqueo según el stock
                if (stock <= 0) {
                    addToCartBtn.disabled = true;
                    addToCartBtn.textContent = "Sin Stock / Pausado";
                    if (qtyControl) qtyControl.style.display = 'none'; // Ocultamos el selector de cantidad
                } else {
                    addToCartBtn.disabled = false;
                    addToCartBtn.textContent = "Add to cart";
                    if (qtyControl) qtyControl.style.display = 'flex'; // Mostramos el selector
                }

                productModal.style.display = 'flex';
                productModal.setAttribute('aria-hidden', 'false');
            }
        }


        // 3. Botón Agregar al Carrito (LA SOLUCIÓN)
        const addToCartBtn = e.target.closest('#add-to-cart');
        if (addToCartBtn) {
            if (typeof isAuthenticated !== 'undefined' && !isAuthenticated) {
                return alert('Por favor, inicia sesión.');
            }
            
            const qtyInput = document.getElementById('quantity-input');
            const productId = document.getElementById('modal-name').dataset.productId;
            const qty = parseInt(qtyInput.value);

            if (!productId) return alert('Error: No existe el ID del producto.');

            fetch('/cart/add_to_cart/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `product_id=${encodeURIComponent(productId)}&quantity=${qty}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    // Actualizar contador global
                    const counter = document.getElementById('cart-counter');
                    if (counter) counter.textContent = data.total_items;
                    
                    closeAllModals();

                    // Abrir Side Cart automáticamente
                    const cartIcon = document.getElementById('cart-icon');
                    if (cartIcon) cartIcon.click(); 
                } else {
                    alert('Error: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(() => alert('Error de conexión'));
        }

        // 4. Modal de Blog/Posts
        const postCard = e.target.closest('.post-card');
        if (postCard) {
            const blogModal = document.getElementById('post-modal');
            if (blogModal) {
                document.getElementById('modal-title').textContent = postCard.dataset.title;
                document.getElementById('modal-author').textContent = postCard.dataset.author;
                document.getElementById('modal-date').textContent = postCard.dataset.date;
                document.getElementById('modal-content').innerHTML = postCard.querySelector('.post-full-content').innerHTML;
                blogModal.style.display = 'block';
            }
        }
    });

    // --- Lógica del Side Cart ---
    const sideCart = document.getElementById('side-cart');
    const cartOverlay = document.getElementById('cart-overlay');
    const cartIcon = document.getElementById('cart-icon'); 
    const closeCart = document.getElementById('close-cart'); 

    if (cartIcon) {
        cartIcon.addEventListener('click', (e) => {
            e.preventDefault();
            if (sideCart && cartOverlay) {
                sideCart.classList.add('open');
                cartOverlay.classList.add('active');
                
                fetch('/cart/side_cart/') 
                    .then(res => res.text())
                    .then(html => {
                        const itemsContainer = document.getElementById('side-cart-items');
                        itemsContainer.innerHTML = html;
                        const newTotal = document.getElementById('hidden-total')?.value || "0.00";
                        document.getElementById('side-cart-total').textContent = `$${newTotal}`;
                    });
            }
        });
    }

    const hideSideCart = () => {
        if (sideCart && cartOverlay) {
            sideCart.classList.remove('open');
            cartOverlay.classList.remove('active');
        }
    };

    if (closeCart) closeCart.addEventListener('click', hideSideCart);
    if (cartOverlay) cartOverlay.addEventListener('click', hideSideCart);

    // --- Control de Cantidades en el Modal ---
    const quantityInput = document.getElementById('quantity-input');
    const modalQuantityMax = document.getElementById('modal-quantity');

    document.addEventListener('click', (e) => {
        if (e.target.id === 'quantity-increase') {
            let current = parseInt(quantityInput.value);
            let max = parseInt(modalQuantityMax.textContent) || 1;
            if (current < max) quantityInput.value = current + 1;
        }
        if (e.target.id === 'quantity-decrease') {
            let current = parseInt(quantityInput.value);
            if (current > 1) quantityInput.value = current - 1;
        }
    });

    // --- Observer para Animaciones ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal', 'active');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    const observeElements = () => {
        document.querySelectorAll('section, .product-item, .post-card, .category-card, .sub-title, .blog-section, .shop-section, .author-container, .register-wrapper, .login_wrapper')
        .forEach((el) => {
            if (!el.classList.contains('reveal')) el.style.opacity = "0"; 
            observer.observe(el);
        });
    };

    observeElements();
});




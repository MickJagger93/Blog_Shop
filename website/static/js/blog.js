// Función para obtener el CSRF (fuera de todo)
function getCookie(name) {
    
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', () => {
    
    const modal = document.getElementById('post-modal');
    const closeButton = document.querySelector('.close-button');
    const modalTitle = document.getElementById('modal-title');
    const modalAuthor = document.getElementById('modal-author');
    const modalDate = document.getElementById('modal-date');
    const modalContent = document.getElementById('modal-content');

    // Seleccionamos todas las tarjetas
    const cards = document.querySelectorAll('.post-card');
    console.log("Tarjetas encontradas:", cards.length); // Debe decir 9 o más

    cards.forEach(card => {
        card.addEventListener('click', function() {
            const postId = this.dataset.postId;
            console.log("Clic en post ID:", postId);

            // 1. Llenar y mostrar modal
            modalTitle.textContent = this.dataset.title;
            modalAuthor.textContent = this.dataset.author;
            modalDate.textContent = this.dataset.date;
            const fullContent = this.querySelector('.post-full-content').innerHTML;
            modalContent.innerHTML = fullContent;
            modal.style.display = 'flex';

            // 2. Enviar vista a Django
            fetch(`/post/hit-view/${postId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            })
            .then(response => {
                if(response.ok) console.log("Vista registrada en el servidor");
            })
            .catch(err => console.error("Error en fetch:", err));
        });
    });

    // Cerrar modal
    if(closeButton) {
        closeButton.onclick = () => modal.style.display = 'none';
    }

    window.onclick = (event) => {
        if (event.target === modal) modal.style.display = 'none';
    };
});

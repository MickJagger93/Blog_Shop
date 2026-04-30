document.addEventListener('DOMContentLoaded', function() {
  
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

    var stripe = Stripe(window.STRIPE_PUBLIC_KEY);
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');

    var form = document.getElementById('payment-form');
    var submitButton = document.getElementById('payment-submit');

    if(!form) {
        return;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        document.getElementById('error-message').textContent = '';
        submitButton.disabled = true; 
        
        stripe.createToken(card).then(function(result) {
        if (result.error) {
            document.getElementById('error-message').textContent = result.error.message;
            submitButton.disabled = false;
        } else {
            fetch('/orders/create_payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),  
            },
            body: 'stripeToken=' + encodeURIComponent(result.token.id)
            })
            .then(response => response.json())
            .then(json => {
            if(json.status === 'success') {
                window.location.href = '/orders/order_success/';  
            } else {
                document.getElementById('error-message').textContent = json.message || 'Error en el pago.';
                submitButton.disabled = false;
            }
            })
            .catch(() => {
            document.getElementById('error-message').textContent = 'Error en la conexión.';
            submitButton.disabled = false;
            });
        }
        });
    });
});
document.addEventListener('DOMContentLoaded', function() {
    
    // Cellar Detail Page
    
    const editBtns = document.querySelectorAll('.js-edit-btn');
    if (editBtns.length > 0) {
        editBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const card = this.closest('.js-bottle-card');
                card.classList.add('is-editing');
            });
        });
    }

    const minusBtns = document.querySelectorAll('.qty-minus');
    const plusBtns = document.querySelectorAll('.qty-plus');

    if (minusBtns.length > 0) {
        minusBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const input = this.nextElementSibling;
                let val = parseInt(input.value);
                if (val > 1) input.value = val - 1;
            });
        });

        plusBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const input = this.previousElementSibling;
                let val = parseInt(input.value);
                input.value = val + 1;
            });
        });
    }

    // Catalog Page
    
    const modal = document.getElementById('add-to-cellar-modal');
    if (modal) {
        const addBtns = document.querySelectorAll('.btn-add');
        const closeBtn = document.querySelector('.js-close-modal');
        const form = document.getElementById('catalog-add-form');
        const modalSkuInput = document.getElementById('js-modal-product-sku');
        
        const cellarCount = window.CELLAR_CONFIG ? window.CELLAR_CONFIG.cellarCount : 0;
        const createUrl = window.CELLAR_CONFIG ? window.CELLAR_CONFIG.createUrl : '/cellars/create/';

        addBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const sku = this.dataset.productSku; 
                const productName = this.dataset.productName;

                if (cellarCount === 0) {
                    window.location.href = createUrl;
                } else if (cellarCount >= 2) {
                    modalSkuInput.value = sku;
                    document.getElementById('js-modal-product-name').textContent = productName;
                    modal.style.display = 'flex';
                } else {
                    const cellarId = document.querySelector('input[name="cellar_id"]').value;
                    form.action = `/cellars/${cellarId}/bottles/add/${sku}/`;
                    form.submit();
                }
            });
        });

        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const checkedCellar = document.querySelector('input[name="cellar_id"]:checked');
                const cellarId = checkedCellar ? checkedCellar.value : '';
                const sku = modalSkuInput.value;

                if (cellarId && sku) {
                    this.action = `/cellars/${cellarId}/bottles/add/${sku}/`;
                    this.submit();
                }
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', () => modal.style.display = 'none');
        }
    }
});
document.addEventListener('DOMContentLoaded', function() {

    // =================================================================
    // 1. Global UI & Navigation
    // =================================================================
    
    // Mobile Menu Toggle
    const toggleBtns = document.querySelectorAll('.js-toggle-mobile-menu');
    const mobileMenu = document.getElementById('mobile-menu');

    toggleBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            mobileMenu.classList.toggle('is-open');
        });
    });

    // Mobile Auth Drawer Toggle
    const authToggleBtn = document.querySelector('.js-toggle-auth-drawer');
    const authContent = document.querySelector('.mobile-auth-drawer-content');
    const authIcon = document.querySelector('.auth-toggle-icon');

    if (authToggleBtn && authContent) {
        authToggleBtn.addEventListener('click', function() {
            if (authContent.style.display === 'none' || authContent.style.display === '') {
                authContent.style.display = 'block';
                authIcon.textContent = '-';
            } else {
                authContent.style.display = 'none';
                authIcon.textContent = '+';
            }
        });
    }

    // =================================================================
    // 2. Cellar Management Modals (Edit & Delete)
    // =================================================================
    
    const editModal = document.getElementById('edit-cellar-modal');
    const deleteModal = document.getElementById('delete-cellar-modal');
    
    if (editModal && deleteModal) {
        const editForm = document.getElementById('edit-cellar-form');
        const deleteForm = document.getElementById('delete-cellar-form');
        const editNextInput = document.getElementById('edit-cellar-next');
        const openEditBtns = document.querySelectorAll('.js-open-edit-cellar');
        
        let tempDeleteUrl = '';
        let tempCellarName = '';
        let tempBottleCount = '';

        openEditBtns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                
                tempCellarName = this.dataset.cellarName;
                tempBottleCount = this.dataset.bottleCount;
                tempDeleteUrl = this.dataset.deleteUrl;

                document.getElementById('display-cellar-name-title').textContent = tempCellarName;
                document.getElementById('edit-cellar-name').value = tempCellarName;
                document.getElementById('edit-cellar-desc').value = this.dataset.cellarDesc;
                editForm.action = this.dataset.updateUrl;
                
                if (editNextInput) {
                    editNextInput.value = this.dataset.nextUrl;
                }

                editModal.style.display = 'flex';
            });
        });

        const openDeleteBtn = document.querySelector('.js-open-delete-modal');
        if (openDeleteBtn) {
            openDeleteBtn.addEventListener('click', function() {
                editModal.style.display = 'none';
                
                document.getElementById('delete-display-name').textContent = tempCellarName;
                document.getElementById('delete-display-count').textContent = tempBottleCount;
                deleteForm.action = tempDeleteUrl;

                deleteModal.style.display = 'flex';
            });
        }

        document.querySelector('.js-close-edit-modal').addEventListener('click', function() {
            editModal.style.display = 'none';
        });

        document.querySelector('.js-close-delete-modal').addEventListener('click', function() {
            deleteModal.style.display = 'none';
        });

        document.querySelector('.js-cancel-delete').addEventListener('click', function() {
            deleteModal.style.display = 'none';
            editModal.style.display = 'flex'; 
        });
    }

    // =================================================================
    // 3. Cellar Detail Page Interactions
    // =================================================================
    
    const editBtns = document.querySelectorAll('.js-edit-btn');
    if (editBtns.length > 0) {
        editBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const card = this.closest('.js-bottle-card');
                card.classList.add('is-editing');
            });
        });
    }

    // Quantity Adjusters
    const minusBtns = document.querySelectorAll('.qty-minus');
    const plusBtns = document.querySelectorAll('.qty-plus');

    if (minusBtns.length > 0) {
        minusBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const input = this.nextElementSibling;
                let val = parseInt(input.value);
                if (val > 1) {
                    input.value = val - 1;
                }
            });
        });

        plusBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const input = this.previousElementSibling;
                let val = parseInt(input.value);
                input.value = val + 1;
            });
        });
    }

    // =================================================================
    // 4. Catalog Page: Add to Cellar Modal
    // =================================================================
    
    const addToCellarModal = document.getElementById('add-to-cellar-modal');
    if (addToCellarModal) {
        const addBtns = document.querySelectorAll('.btn-add, .js-add-to-cellar-btn');
        const closeBtn = document.querySelector('.js-close-modal');
        const form = document.getElementById('catalog-add-form');
        const modalSkuInput = document.getElementById('js-modal-product-sku');
        
        addBtns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const sku = this.dataset.productSku; 
                const productName = this.dataset.productName;

                const targetCellarId = form.dataset.targetCellar;
                const createUrl = form.dataset.createUrl;
                
                const radios = document.querySelectorAll('.cellar-selection-list input[type="radio"]');
                const cellarCount = radios.length;

                if (targetCellarId) {
                    form.action = `/cellars/${targetCellarId}/bottles/add/${sku}/`;
                    form.submit();
                } else if (cellarCount === 0) {
                    window.location.href = createUrl;
                } else if (cellarCount >= 2) {
                    modalSkuInput.value = sku;
                    document.getElementById('js-modal-product-name').textContent = productName;
                    addToCellarModal.style.display = 'flex';
                } else {
                    const cellarId = radios[0].value;
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
            closeBtn.addEventListener('click', function() {
                addToCellarModal.style.display = 'none';
            });
        }
    }

    // =================================================================
    // 5. Shared Formatters & Utilities
    // =================================================================

    // Size Unit Formatter (L vs ml)
    const sizeElements = document.querySelectorAll('.js-format-size');
    sizeElements.forEach(function(el) {
        const val = parseFloat(el.getAttribute('data-value'));
        
        if (!isNaN(val)) {
            if (val >= 1000) {
                el.innerHTML = `${val / 1000} <span class="filter-unit">L</span>`;
            } else {
                el.innerHTML = `${val} <span class="filter-unit">ml</span>`;
            }
        }
    });

    // =================================================================
    // 6. Catalog Filtering & Sorting
    // =================================================================
    
    const catalogContainer = document.querySelector('.cellars-layout');

    if (catalogContainer) {
        
        // Filter Accordion Toggles
        const filterToggles = document.querySelectorAll('.js-filter-toggle');
        filterToggles.forEach(function(toggle) {
            toggle.addEventListener('click', function() {
                const content = this.nextElementSibling;
                const icon = this.querySelector('.toggle-icon');

                content.classList.toggle('is-open');
                
                if (content.classList.contains('is-open')) {
                    icon.textContent = '-';
                } else {
                    icon.textContent = '+';
                }
            });
        });

        // Open Filter Accordion if it has checked items
        const filterContents = document.querySelectorAll('.saq-filter-content');
        filterContents.forEach(function(content) {
            const hasCheckedItem = content.querySelector('input:checked');

            if (hasCheckedItem) {
                content.classList.add('is-open');
                
                const toggleBtn = content.previousElementSibling;
                if (toggleBtn && toggleBtn.classList.contains('js-filter-toggle')) {
                    const icon = toggleBtn.querySelector('.toggle-icon');
                    if (icon) {
                        icon.textContent = '-';
                    }
                }
            }
        });

        // Ensure first category is open by default
        const categoryContent = document.querySelector('.saq-filter-group:first-child .saq-filter-content');
        if (categoryContent) {
            categoryContent.classList.add('is-open');
        }

        // Show More / Show Less Logic
        const showMoreBtns = document.querySelectorAll('.js-toggle-show-more');
        showMoreBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const targetId = this.getAttribute('data-target');
                const list = document.querySelector(`.saq-filter-list[data-filter-group="${targetId}"]`);
                const allItems = list.querySelectorAll('.saq-filter-item');

                if (this.textContent === 'Show more') {
                    allItems.forEach(function(item) {
                        item.classList.remove('hidden-filter-item');
                    });
                    this.textContent = 'Show less';
                } else {
                    allItems.forEach(function(item, index) {
                        if (index >= 5) {
                            item.classList.add('hidden-filter-item');
                        }
                    });
                    this.textContent = 'Show more';
                }
            });
        });
        
        // Category Syncing
        const mainCategoryRadios = document.querySelectorAll('.js-main-category-radio');
        const subCategoryGroups = document.querySelectorAll('.js-sub-category-group');
        const subCategoryRadios = document.querySelectorAll('.js-sub-category-radio');

        mainCategoryRadios.forEach(function(radio) {
            radio.addEventListener('change', function() {
                subCategoryGroups.forEach(function(group) {
                    group.classList.remove('is-active');
                });
                
                const targetGroup = document.querySelector(`.js-sub-category-group[data-parent="${this.value}"]`);
                if (targetGroup) {
                    targetGroup.classList.add('is-active');
                }
                
                subCategoryRadios.forEach(function(r) {
                    r.checked = false;
                });

                if (window.innerWidth > 768) {
                    applyFiltersAndSort();
                }
            });
        });

        // Auto-apply filters on desktop
        const desktopInputs = document.querySelectorAll('#mobile-filter-modal input, .catalog-controls-wrapper select');
        desktopInputs.forEach(function(input) {
            if (!input.classList.contains('js-main-category-radio')) {
                input.addEventListener('change', function() {
                    if (window.innerWidth > 768) {
                        applyFiltersAndSort();
                    }
                });
            }
        });

        // Mobile Apply Button
        const applyBtns = document.querySelectorAll('.js-apply-filters');
        applyBtns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                applyFiltersAndSort();
            });
        });

        // URL Builder for Filters
        function applyFiltersAndSort() {
            const params = new URLSearchParams(window.location.search);
            const keysToClear = ['category_path', 'category', 'taste_tag', 'size', 'country', 'region', 'producer', 'vintage', 'grape_variety', 'degree_of_alcohol', 'sort', 'per_page'];
            
            keysToClear.forEach(function(key) {
                params.delete(key);
            });

            const checkedFilters = document.querySelectorAll('#mobile-filter-modal input:checked');
            checkedFilters.forEach(function(input) {
                if (input.name) {
                    params.append(input.name, input.value);
                }
            });

            if (window.innerWidth <= 768) {
                const mobileSort = document.querySelector('#mobile-sort-modal input[name="sort"]:checked');
                if (mobileSort) {
                    params.set('sort', mobileSort.value);
                }

                const mobilePerPage = document.querySelector('#mobile-sort-modal input[name="per_page"]:checked');
                if (mobilePerPage) {
                    params.set('per_page', mobilePerPage.value);
                }
            } else {
                const desktopSort = document.querySelector('.catalog-controls-wrapper select[name="sort"]');
                if (desktopSort && desktopSort.value) {
                    params.set('sort', desktopSort.value);
                }

                const desktopPerPage = document.querySelector('.catalog-controls-wrapper select[name="per_page"]');
                if (desktopPerPage && desktopPerPage.value) {
                    params.set('per_page', desktopPerPage.value);
                }
            }

            document.querySelectorAll('.cellars-sidebar').forEach(function(modal) {
                modal.classList.remove('is-open');
            });
            document.body.style.overflow = '';

            window.location.search = params.toString();
        }

        // Generic Modal Setup
        function setupModal(openSelector, closeSelector, modalId) {
            const openBtns = document.querySelectorAll(openSelector);
            const closeBtns = document.querySelectorAll(closeSelector);
            const targetModal = document.getElementById(modalId);

            if (openBtns.length > 0 && targetModal) {
                openBtns.forEach(function(btn) {
                    btn.addEventListener('click', function(e) {
                        e.preventDefault();
                        targetModal.classList.add('is-open');
                        document.body.style.overflow = 'hidden';
                    });
                });
            }
            if (closeBtns.length > 0 && targetModal) {
                closeBtns.forEach(function(btn) {
                    btn.addEventListener('click', function(e) {
                        e.preventDefault();
                        targetModal.classList.remove('is-open');
                        document.body.style.overflow = '';
                    });
                });
            }
        }

        setupModal('.js-open-filter', '.js-close-filter', 'mobile-filter-modal');
        setupModal('.js-open-sort', '.js-close-sort', 'mobile-sort-modal');
    }
});
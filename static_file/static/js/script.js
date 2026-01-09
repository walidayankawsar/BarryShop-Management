        // Modal functionality
        const modal = document.getElementById('productModal');
        const addProductBtn = document.getElementById('addProductBtn');
        const closeModal = document.getElementById('closeModal');
        const cancelForm = document.getElementById('cancelForm');
        const productForm = document.getElementById('productForm');
        const scanBtn = document.getElementById('scanBtn');
        const productBarcode = document.getElementById('productBarcode');
        const barcodePreview = document.getElementById('barcodePreview');
        
        // Open modal
        addProductBtn.addEventListener('click', () => {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
        
        // Close modal
        function closeProductModal() {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            productForm.reset();
        }
        
        closeModal.addEventListener('click', closeProductModal);
        cancelForm.addEventListener('click', closeProductModal);
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeProductModal();
            }
        });
        
        // Form submission
        productForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Product saved successfully!');
            closeProductModal();
        });
        
        
        // Barcode preview update
        productBarcode.addEventListener('input', () => {
            barcodePreview.textContent = productBarcode.value || '123456789012';
        });
        
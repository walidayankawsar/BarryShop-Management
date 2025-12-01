        // Modal functionality
        const modal = document.getElementById('productModal');
        const addProductBtn = document.getElementById('addProductBtn');
        const closeModal = document.getElementById('closeModal');
        const cancelForm = document.getElementById('cancelForm');
        const productForm = document.getElementById('productForm');
        const barcodeInput = document.getElementById('barcodeInput');
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
        
        
        // Barcode scanning simulation
        scanBtn.addEventListener('click', () => {
            const barcode = barcodeInput.value;
            if (barcode) {
                alert(`Searching for product with barcode: ${barcode}`);
                // In real implementation, this would search your database
            } else {
                alert('Please enter or scan a barcode');
            }
        });
        
        // Barcode preview update
        productBarcode.addEventListener('input', () => {
            barcodePreview.textContent = productBarcode.value || '123456789012';
        });
        
        // Simulate barcode scanner input
        document.addEventListener('keydown', (e) => {
            if (e.target === barcodeInput && e.key === 'Enter') {
                scanBtn.click();
            }
        });
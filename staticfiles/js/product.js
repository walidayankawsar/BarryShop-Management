        // Simple JavaScript for the template functionality
        document.getElementById('add-product-btn').addEventListener('click', function() {
            document.getElementById('product-form').style.display = 'block';
        });
        
        document.getElementById('cancel-btn').addEventListener('click', function() {
            document.getElementById('product-form').style.display = 'none';
            document.getElementById('new-product-form').reset();
        });
        
        document.getElementById('scan-btn').addEventListener('click', function() {
            const barcode = document.getElementById('barcode-input').value;
            if(barcode) {
                alert(`Searching for product with barcode: ${barcode}`);
                // In a real application, you would search your database for this barcode
            } else {
                alert('Please enter or scan a barcode');
            }
        });
        
        document.getElementById('new-product-form').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Product saved successfully!');
            this.reset();
            document.getElementById('product-form').style.display = 'none';
            // In a real application, you would send this data to your server
        });
        
        // Add event listeners for edit and delete buttons
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const productRow = this.closest('tr');
                const barcode = productRow.cells[0].textContent;
                const name = productRow.cells[1].textContent;
                const category = productRow.cells[2].textContent;
                const price = productRow.cells[3].textContent.replace('$', '');
                const stock = productRow.cells[4].textContent;
                
                // Fill the form with existing data
                document.getElementById('barcode').value = barcode;
                document.getElementById('product-name').value = name;
                document.getElementById('category').value = category.toLowerCase();
                document.getElementById('price').value = price;
                document.getElementById('stock').value = stock;
                
                // Show the form
                document.getElementById('product-form').style.display = 'block';
            });
        });
        
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                if(confirm('Are you sure you want to delete this product?')) {
                    this.closest('tr').remove();
                    alert('Product deleted successfully!');
                }
            });
        });
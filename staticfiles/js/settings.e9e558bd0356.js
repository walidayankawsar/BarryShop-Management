        // Profile Dropdown Toggle
        const userProfile = document.getElementById('userProfile');
        const profileDropdown = document.getElementById('profileDropdown');
        
        userProfile.addEventListener('click', function(e) {
            e.stopPropagation();
            profileDropdown.classList.toggle('show');
        });
        
        // Close dropdown when clicking outside
        document.addEventListener('click', function() {
            profileDropdown.classList.remove('show');
        });
        
        // Settings Navigation
        const settingsLinks = document.querySelectorAll('.settings-link');
        const settingsSections = document.querySelectorAll('.settings-section');
        
        settingsLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Remove active class from all links
                settingsLinks.forEach(l => l.classList.remove('active'));
                // Add active class to clicked link
                this.classList.add('active');
                
                // Hide all sections
                settingsSections.forEach(section => {
                    section.classList.remove('active');
                });
                
                // Show selected section
                const sectionId = this.getAttribute('data-section');
                document.getElementById(`${sectionId}-settings`).classList.add('active');
            });
        });
        
        // Simulate loading for demo purposes
        document.getElementById('general-settings').classList.add('active');
// Toggle mobile menu
document.addEventListener('DOMContentLoaded', function() {
    // Add mobile menu toggle functionality if needed
    
    // Form submission handling
    const postForm = document.getElementById('post-form');
    if (postForm) {
        postForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Post submitted successfully!');
            // In a real application, this would send the form data to the server
            postForm.reset();
        });
    }
    
    // Filter functionality for requests
    const filterInput = document.querySelector('.filter-input');
    const statusFilter = document.querySelector('.status-filter');
    
    if (filterInput) {
        filterInput.addEventListener('input', filterRequests);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterRequests);
    }
    
    function filterRequests() {
        const filterValue = filterInput ? filterInput.value.toLowerCase() : '';
        const statusValue = statusFilter ? statusFilter.value.toLowerCase() : '';
        
        const requestItems = document.querySelectorAll('.request-item');
        
        requestItems.forEach(item => {
            const title = item.querySelector('h2').textContent.toLowerCase();
            const status = item.classList.contains('approved') ? 'approved' : 
                          item.classList.contains('pending') ? 'pending' : 
                          item.classList.contains('rejected') ? 'rejected' : '';
            
            const matchesFilter = filterValue === '' || title.includes(filterValue);
            const matchesStatus = statusValue === '' || status === statusValue;
            
            if (matchesFilter && matchesStatus) {
                item.style.display = 'flex';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    // View Details buttons
    const viewDetailsButtons = document.querySelectorAll('.btn-secondary, .view-details');
    viewDetailsButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Details view would open here.');
            // In a real application, this would navigate to the details page
        });
    });
    
    // Toggle switches
    const toggleSwitches = document.querySelectorAll('.switch input');
    toggleSwitches.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const setting = this.closest('.setting-item').querySelector('span').textContent;
            const status = this.checked ? 'enabled' : 'disabled';
            alert(`${setting} has been ${status}.`);
            // In a real application, this would update the user settings
        });
    });
});
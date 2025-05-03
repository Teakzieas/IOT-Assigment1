document.addEventListener('DOMContentLoaded', function() {
    const automationsContainer = document.querySelector('.automations-container');
    let automationCards = document.querySelectorAll('.automation-card');
    const saveOrderButton = document.querySelector('.save-order');
    const reorderFeedback = document.querySelector('.reorder-feedback');
    let draggedItem = null;
    let orderChanged = false;
    
    // Initialize sortable functionality
    if (automationCards.length > 0) {
        initDragAndDrop();
    }
    
    function initDragAndDrop() {
        automationCards.forEach(card => {
            // Add drag events
            card.setAttribute('draggable', 'true');
            
            card.addEventListener('dragstart', function() {
                draggedItem = this;
                setTimeout(() => this.classList.add('dragging'), 0);
                
                // Show save button
                orderChanged = true;
                saveOrderButton.classList.add('visible');
            });
            
            card.addEventListener('dragend', function() {
                this.classList.remove('dragging');
                showReorderFeedback();
            });
            
            card.addEventListener('dragover', function(e) {
                e.preventDefault();
                
                if (draggedItem === this) return;
                
                const draggingRect = draggedItem.getBoundingClientRect();
                const draggedHeight = draggingRect.height;
                const thisRect = this.getBoundingClientRect();
                const thisMiddleY = thisRect.top + thisRect.height / 2;
                
                if (e.clientY < thisMiddleY) {
                    automationsContainer.insertBefore(draggedItem, this);
                } else {
                    automationsContainer.insertBefore(draggedItem, this.nextSibling);
                }
                
                // Re-index for proper drop
                automationCards = document.querySelectorAll('.automation-card');
            });
        });
    }
    
    // Handle save order button click
    if (saveOrderButton) {
        saveOrderButton.addEventListener('click', updatePriorities);
    }
    
    function showReorderFeedback() {
        reorderFeedback.classList.add('show');
        setTimeout(() => reorderFeedback.classList.remove('show'), 3000);
    }
    
    // Send the new order to the server
    function updatePriorities() {
        // Get all automation IDs in the current order
        automationCards = document.querySelectorAll('.automation-card');
        const automationIds = Array.from(automationCards).map(card => {
            return {
                id: parseInt(card.dataset.id), 
                priority: parseInt(card.dataset.priority)
            };
        });
        
        fetch('/api/automations/reorder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ automations: automationIds })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Show success message
                reorderFeedback.textContent = 'Automation order saved!';
                showReorderFeedback();
                
                // Refresh the page after a short delay
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                alert('Error updating automation order: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the automation order');
        });
    }
    
    // Expose delete function to global scope for the onClick handlers
    window.deleteAutomation = function(id) {
        if (confirm('Are you sure you want to delete this automation?')) {
            fetch(`/api/automation/${id}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Remove the deleted card from DOM
                    const card = document.querySelector(`.automation-card[data-id="${id}"]`);
                    if (card) card.remove();
                    
                    // Show success message
                    reorderFeedback.textContent = 'Automation deleted successfully!';
                    showReorderFeedback();
                    
                    // Update automationCards
                    automationCards = document.querySelectorAll('.automation-card');
                    
                    // If no automations left, reload the page to show empty state
                    if (automationCards.length === 0) {
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        // Otherwise refresh to update priorities
                        setTimeout(() => location.reload(), 1000);
                    }
                } else {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred during deletion');
            });
        }
    };
    
    // Check for unsaved changes before leaving the page
    window.addEventListener('beforeunload', function(e) {
        if (orderChanged) {
            const message = 'You have unsaved changes. Are you sure you want to leave?';
            e.returnValue = message;
            return message;
        }
    });
});

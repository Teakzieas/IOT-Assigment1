document.addEventListener('DOMContentLoaded', function() {
    const triggerTypeSelect = document.getElementById('triggerType');
    const conditionContainer = document.getElementById('conditionContainer');
    const valueContainer = document.getElementById('valueContainer');
    const actionTypeSelect = document.getElementById('actionType');
    const actionContainer = document.getElementById('actionContainer');
    const previewTrigger = document.getElementById('previewTrigger');
    const triggerPreviewContent = document.getElementById('triggerPreviewContent');
    const triggerForm = document.getElementById('triggerForm');

    // Check if we're in edit mode
    const urlParams = new URLSearchParams(window.location.search);
    const editId = urlParams.get('edit');
    const isEditMode = editId !== null;
    
    // Update form UI for edit mode if applicable
    if (isEditMode) {
        document.querySelector('h1').textContent = 'Edit Automation Rule';
        document.getElementById('createTrigger').textContent = 'Update Automation';
        
        // Fetch the automation data
        fetch(`/api/automation/${editId}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    loadAutomationData(data.data);
                } else {
                    alert('Error loading automation: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while loading the automation');
            });
    }

    // Function to load automation data into form for editing
    function loadAutomationData(automation) {
        // Set trigger type
        triggerTypeSelect.value = automation.trigger_type;
        triggerTypeSelect.dispatchEvent(new Event('change'));
        
        // Set trigger details based on type
        setTimeout(() => {
            if (automation.trigger_type === 'time') {
                document.getElementById('timeValue').value = automation.trigger_value;
            } else if (automation.trigger_type === 'humanPresence') {
                document.getElementById('presenceState').value = automation.trigger_value === '1' ? 'detected' : 'notDetected';
            } else {
                document.getElementById('condition').value = automation.trigger_condition === '>' ? 'above' : 'below';
                document.getElementById('thresholdValue').value = automation.trigger_value;
            }
            
            // Set action type
            actionTypeSelect.value = automation.action_type;
            actionTypeSelect.dispatchEvent(new Event('change'));
            
            // Set action details
            setTimeout(() => {
                if (automation.action_type === 'curtain') {
                    const slider = document.getElementById('curtainSlider');
                    const valueSpan = document.getElementById('curtainValue');
                    slider.value = automation.action_value;
                    valueSpan.textContent = automation.action_value;
                }
                
                // Update the preview
                updatePreview();
            }, 100);
        }, 100);
    }

    // Function to update the form based on trigger type selection
    triggerTypeSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        conditionContainer.innerHTML = '';
        valueContainer.innerHTML = '';
        
        if (!selectedValue) {
            conditionContainer.classList.add('hidden');
            valueContainer.classList.add('hidden');
            previewTrigger.classList.add('hidden');
            return;
        }

        conditionContainer.classList.remove('hidden');
        valueContainer.classList.remove('hidden');
        
        // Create different options based on trigger type
        switch (selectedValue) {
            case 'time':
                conditionContainer.innerHTML = `
                    <label for="timeValue">Set Time:</label>
                    <input type="time" id="timeValue" name="timeValue">
                `;
                break;
                
            case 'lightInside':
            case 'lightOutside':
            case 'temperature':
            case 'humidity':
                conditionContainer.innerHTML = `
                    <label for="condition">Condition:</label>
                    <select id="condition" name="condition">
                        <option value="above">Above</option>
                        <option value="below">Below</option>
                    </select>
                `;
                
                valueContainer.innerHTML = `
                    <label for="thresholdValue">Threshold Value:</label>
                    <input type="${selectedValue === 'temperature' || selectedValue === 'humidity' ? 'number' : 'text'}" 
                           id="thresholdValue" 
                           name="thresholdValue" 
                           placeholder="${getPlaceholder(selectedValue)}">
                `;
                
                if (selectedValue === 'temperature') {
                    valueContainer.innerHTML += '<span>°C</span>';
                } else if (selectedValue === 'humidity') {
                    valueContainer.innerHTML += '<span>%</span>';
                } else if (selectedValue.includes('light')) {
                    valueContainer.innerHTML += '<span>lux</span>';
                }
                break;
                
            case 'humanPresence':
                conditionContainer.innerHTML = `
                    <label for="presenceState">Presence State:</label>
                    <select id="presenceState" name="presenceState">
                        <option value="detected">Detected</option>
                        <option value="notDetected">Not Detected</option>
                    </select>
                `;
                break;
        }
        
        // Add event listeners to new elements
        updateEventListeners();
    });

    // Function to update the action form based on action type selection
    actionTypeSelect.addEventListener('change', function() {
        const selectedValue = this.value;
        actionContainer.innerHTML = '';
        
        if (!selectedValue) {
            actionContainer.classList.add('hidden');
            return;
        }

        actionContainer.classList.remove('hidden');
        
        // Create different action options
        switch (selectedValue) {
            case 'curtain':
                actionContainer.innerHTML = `
                    <div class="curtain-control">
                        <div class="curtain-header">
                            <span>Set Curtain Position</span>
                            <i class="fas fa-blinds"></i>
                        </div>
                        <input type="range" min="0" max="100" value="50" class="curtain-slider" id="curtainSlider">
                        <div class="slider-value"><span id="curtainValue">50</span>%</div>
                        <div class="curtain-presets">
                            <button type="button" class="preset-btn" data-value="0">Closed</button>
                            <button type="button" class="preset-btn" data-value="50">Half</button>
                            <button type="button" class="preset-btn" data-value="100">Open</button>
                        </div>
                    </div>
                `;
                
                // Add event listeners for the curtain slider
                const curtainSlider = document.getElementById('curtainSlider');
                const curtainValue = document.getElementById('curtainValue');
                
                curtainSlider.addEventListener('input', function() {
                    curtainValue.textContent = this.value;
                    updatePreview();
                });
                
                // Add event listeners for the preset buttons
                document.querySelectorAll('.preset-btn').forEach(button => {
                    button.addEventListener('click', function() {
                        const value = this.getAttribute('data-value');
                        curtainSlider.value = value;
                        curtainValue.textContent = value;
                        updatePreview();
                    });
                });
                break;
        }
        
        updatePreview();
    });

    // Function to update preview when any input changes
    function updateEventListeners() {
        const allInputs = document.querySelectorAll('select, input');
        allInputs.forEach(input => {
            input.addEventListener('change', updatePreview);
        });
    }

    // Function to generate placeholder based on trigger type
    function getPlaceholder(triggerType) {
        switch(triggerType) {
            case 'temperature': return 'e.g., 25';
            case 'humidity': return 'e.g., 50';
            case 'lightInside':
            case 'lightOutside': return 'e.g., 500';
            default: return '';
        }
    }

    // Function to update the preview based on user selections
    function updatePreview() {
        const triggerType = triggerTypeSelect.value;
        const actionType = actionTypeSelect.value;
        
        if (!triggerType || !actionType) {
            previewTrigger.classList.add('hidden');
            return;
        }
        
        let triggerText = '';
        let actionText = '';
        
        // Generate trigger text
        switch (triggerType) {
            case 'time':
                const timeValue = document.getElementById('timeValue')?.value;
                if (timeValue) {
                    triggerText = `When the time is ${timeValue}`;
                }
                break;
                
            case 'lightInside':
            case 'lightOutside':
            case 'temperature':
            case 'humidity':
                const condition = document.getElementById('condition')?.value;
                const thresholdValue = document.getElementById('thresholdValue')?.value;
                
                if (condition && thresholdValue) {
                    const triggerName = triggerType === 'lightInside' ? 'indoor light level' :
                                       triggerType === 'lightOutside' ? 'outdoor light level' :
                                       triggerType === 'temperature' ? 'temperature' : 'humidity';
                    
                    const unit = triggerType === 'temperature' ? '°C' :
                                triggerType === 'humidity' ? '%' :
                                'lux';
                    
                    triggerText = `When ${triggerName} is ${condition} ${thresholdValue} ${unit}`;
                }
                break;
                
            case 'humanPresence':
                const presenceState = document.getElementById('presenceState')?.value;
                if (presenceState) {
                    triggerText = `When human presence is ${presenceState === 'detected' ? 'detected' : 'not detected'}`;
                }
                break;
        }
        
        // Generate action text
        switch (actionType) {
            case 'curtain':
                const curtainValue = document.getElementById('curtainValue')?.textContent;
                if (curtainValue) {
                    actionText = `Set curtain position to ${curtainValue}%`;
                }
                break;
        }
        
        // Combine trigger and action text
        if (triggerText && actionText) {
            triggerPreviewContent.textContent = `${triggerText}, ${actionText}`;
            previewTrigger.classList.remove('hidden');
        } else {
            previewTrigger.classList.add('hidden');
        }
    }

    // Handle form submission
    triggerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Gather all the automation data
        const triggerType = triggerTypeSelect.value;
        const actionType = actionTypeSelect.value;
        
        if (!triggerType || !actionType) {
            alert('Please complete both trigger and action sections');
            return;
        }
        
        let automationData = {
            trigger: {
                type: triggerType
            },
            action: {
                type: actionType
            }
            // Priority removed - will be assigned automatically on the server
        };
        
        // Add specific trigger data
        switch (triggerType) {
            case 'time':
                automationData.trigger.value = document.getElementById('timeValue').value;
                break;
                
            case 'lightInside':
            case 'lightOutside':
            case 'temperature':
            case 'humidity':
                automationData.trigger.condition = document.getElementById('condition').value;
                automationData.trigger.value = document.getElementById('thresholdValue').value;
                break;
                
            case 'humanPresence':
                automationData.trigger.value = document.getElementById('presenceState').value;
                break;
        }
        
        // Add specific action data
        switch (actionType) {
            case 'curtain':
                automationData.action.value = document.getElementById('curtainSlider').value;
                break;
        }
        
        // Add the edit ID if in edit mode
        if (isEditMode) {
            automationData.id = parseInt(editId);
        }
        
        console.log('Automation data to save:', automationData);
        
        // Send the data to the server
        const endpoint = isEditMode ? `/api/automation/${editId}` : '/api/automation';
        const method = isEditMode ? 'PUT' : 'POST';
        
        fetch(endpoint, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(automationData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert(isEditMode ? 'Automation updated successfully!' : 'Automation saved successfully!');
                // Redirect to automations list page
                window.location.href = '/automations';
            } else {
                alert((isEditMode ? 'Error updating' : 'Error saving') + ' automation: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while ' + (isEditMode ? 'updating' : 'saving') + ' the automation');
        });
    });
    
    // Add back button functionality
    const backButton = document.getElementById('backButton');
    if (backButton) {
        backButton.addEventListener('click', function() {
            window.location.href = '/automations';
        });
    }
});

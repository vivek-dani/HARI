// Custom Streamlit component to handle communication with Google Maps iframe

// Function to initialize the component
function initComponent() {
    // Create a message handler for the iframe
    window.addEventListener('message', function(event) {
        // Check if the message is from our maps component
        if (event.data && event.data.type === 'location_selected') {
            // Send the location data to Streamlit
            Streamlit.setComponentValue(event.data.location);
        }
    });

    // Tell Streamlit we're ready
    Streamlit.setComponentReady();
}

// Initialize the component when Streamlit is connected
Streamlit.onRender(function() {
    initComponent();
});

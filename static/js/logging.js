$(document).ready(function () {
    // Get the CSRF token from the cookies
    const csrftoken = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    const scrollableContainer = document.getElementById('scrollable-lists');
    if (scrollableContainer) {
        scrollableContainer.addEventListener('scroll', logScrollEvent);
    }

    // Generate a unique session ID if not already stored in local storage
    let sessionId = localStorage.getItem('sessionId');
    if (!sessionId) {
        sessionId = generateSessionId();
        localStorage.setItem('sessionId', sessionId);
    }

    // Function to generate a random session ID
    function generateSessionId() {
        return Math.random().toString(36).substring(2, 10); // Adjust length as needed
    }

    // Function to logg scrolling
    function logScrollEvent() {
        const scrollTop = event.target.scrollTop;
        logMessage(`Scrolled to position: ${scrollTop}px`);
    }

    // Function to log a message
    function logMessage(message) {
        // Log the message with the session ID
        const url = '/bookrec/logging/'
        const logMessage = `Session ID: ${sessionId} - ${message}`;
        console.log(logMessage);

        // Send an AJAX request to log the event on the server
        $.ajax({
            type: "POST",
            url: url,  // Replace with your Django URL
            data: { message: logMessage },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
            success: function (response) {
                console.log("Log sent successfully.");
                },
            error: function (error) {
                console.error("Error sending log: " + error);
            }
        });
    }

    // Use event delegation to handle clicks on buttons with the "descriptionButton" class
    $(document).on("click", ".loggingButton", function () {
        // Get the title from the data-title attribute of the clicked button
        const title = $(this).data("title");
        // Log the button click event
        logMessage(`Button clicked: ${title}`);
    })

    // Add a click event listener for cover images
    $(document).on("click", "img[data-title]", function () {
        // Get the book ID from the data-book-id attribute of the clicked image
        const imageTitle = $(this).data("title");
        // Log the image click event
        logMessage(`Image clicked for Title: ${imageTitle}`);
    });

    // Add a click event listener for Links
    $(document).on("click", "a[data-title]", function () {
        // Get the book ID from the data-book-id attribute of the clicked image
        const linkTitle = $(this).data("title");
        // Log the image click event
        logMessage(`Link clicked for Title: ${linkTitle}`);
    });
});
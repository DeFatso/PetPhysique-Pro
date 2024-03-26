document.addEventListener('DOMContentLoaded', function() {
    function showCalendar() {
        var mainContent = document.querySelector('.main');
        mainContent.innerHTML = '<div id="calendar"></div>';

        var calendarEl = document.getElementById('calendar');
        var calendar = new FullCalendar.Calendar(calendarEl, {
            // Configure options here
            initialView: 'dayGridMonth', // Display the calendar in month view by default
            height: '1000px',
            aspect_ratio: 1.1
        });

        calendar.render();
    }

    function showUserInfo() {
        // Make an AJAX request to fetch user information
        fetch('/user-info')
            .then(response => response.json())
            .then(data => {
                var mainContent = document.querySelector('.main');
                mainContent.innerHTML = '<div id="user-info">' +
                                        '<img src="../static/images/person.svg" alt="Default Profile Picture">' +
                                        '<p>Username: ' + data.username + '</p>' +
                                        '<p>Email: ' + data.email + '</p>' +
                                        '<p>User ID: ' + data.user_id + '</p>' +
                                        '</div>';
            });
    }

    function showPetInfo() {
        fetch('/pet-info')
        .then(response => response.json())
        .then(data => {
            var mainContent = document.querySelector('.main');
            var petInfoHTML = '<div id="pet-info">';
            
            data.forEach(pet => {
                petInfoHTML += '<div>' +
                                '<img src="../static/images/dog.svg" alt="Default Pet Picture">' +
                                '<p> Pet name: ' + pet.name + '</p>' +
                                '<p>Weight: ' + pet.weight + '</p>' +
                                '<p>Height: ' + pet.height + '</p>' +
                                '</div>';
            });
    
            petInfoHTML += '</div>';
            mainContent.innerHTML = petInfoHTML;
        });
    }
    
    

    document.getElementById('calendar-icon').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        showCalendar(); // Call the function to display the calendar
    });

    document.getElementById('user-icon').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        showUserInfo(); // Call the function to display user info
    });

    document.getElementById('pet-icon').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent default link behavior
        showPetInfo(); // Call the function to display pet info
    });
});

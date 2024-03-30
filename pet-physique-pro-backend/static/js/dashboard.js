document.addEventListener('DOMContentLoaded', function() {
    function showCalendar() {
        console.log('showCalendar function called');
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
        console.log('showUserInfo function called');
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
        console.log('showPetInfo function called');
        fetch('/pet-info')
        .then(response => response.json())
        .then(data => {
            var mainContent = document.querySelector('.main');
            var petInfoHTML = '<div id="pet-info">';
            
            data.forEach(pet => {
                petInfoHTML += '<div>' +
                                '<img src="../static/images/dog.svg" alt="Default Pet Picture">' +
                                '<p> Name: ' + pet.name + '</p>' +
                                '<p>Weight: ' + pet.weight + '</p>' +
                                '<p>Height: ' + pet.height + '</p>' +
                                '<button type="button" onclick="deletePet(' + pet.id + ')">Delete</button>' +
                                '<button type="button" onclick="updatePet(' + pet.id + ')">Update</button>' +
                                '</div>';
            });
            petInfoHTML += '<button type="button" onclick="window.location.href=\'/create_pet\'">Create Pet</button>';
            petInfoHTML += '</div>';
            mainContent.innerHTML = petInfoHTML;
        });
    }
    
    // Define deletePet function and attach it to the window object
    window.deletePet = function(petId) {
        console.log('deletePet function called for pet ID:', petId);
        // Make an AJAX request to delete the pet with the specified ID
        fetch(`/api/pets/${petId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
                // Pet successfully deleted, you may want to refresh the pet list or take other actions
                console.log('Pet deleted successfully');
                // Optionally, refresh the pet information on the page after deletion
                showPetInfo();
            } else {
                // Handle errors if any
                console.error('Error deleting pet:', response.status);
            }
        })
        .catch(error => console.error('Error deleting pet:', error));
    }

    function updatePet(petId) {
        console.log('Update button clicked for pet ID:', petId);
        // Make an AJAX request to fetch the update_pet template
        fetch('/update_pet/' + petId)
            .then(response => response.text())
            .then(html => {
                // Display the update_pet template in the main content area
                var mainContent = document.querySelector('.main');
                mainContent.innerHTML = html;
            })
            .catch(error => {
                console.error('Error fetching update_pet template:', error);
            });
    }
    
    // Attach updatePet function to the window object
    window.updatePet = updatePet;
    

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

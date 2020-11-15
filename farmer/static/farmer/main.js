document.addEventListener('DOMContentLoaded', function() {

    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }


    document.querySelector('#createplant').onclick = () => {
        alert('start')
        const name = document.querySelector('#id_name').value;
        const seeds = document.querySelector('#id_seeds').value;
        const pressure = document.querySelector('#id_pressure').value;
        const blackout = document.querySelector('#id_blackout').value;
        const harvest = document.querySelector('#id_harvest').value;
        const output = document.querySelector('#id_output').value;
        const csrftoken = getCookie('csrftoken');

        fetch('/plants',{
            method: 'POST',
            credentials: 'same-origin',
            body: JSON.stringify({
                name: name

            }),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then(data =>
            console.log(data))
        return false;    
    }

    function getCookie(name) {
        if (!document.cookie) {
            return null;
        }
        const token = document.cookie.split(';')
            .map(c => c.trim())
            .filter(c => c.startsWith(name + '='));
    
        if (token.length === 0) {
            return null;
        }
        return decodeURIComponent(token[0].split('=')[1]);
    }
    
})

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

    // Create new plant
    document.querySelector('#createplant').onclick = () => {
        var data = 
            {
                name : document.querySelector('#id_name').value,
                seeds : document.querySelector('#id_seeds').value,
                pressure : document.querySelector('#id_pressure').value,
                blackout : document.querySelector('#id_blackout').value,
                harvest : document.querySelector('#id_harvest').value,
                output : document.querySelector('#id_output').value
            }
        
        const csrftoken = getCookie('csrftoken');

        fetch('/plants',{
            method: 'POST',
            body: JSON.stringify({
                data
            }),
            headers: {
                'X-CSRFToken': csrftoken
            },
        })
        .then(response => response.json())
        .then( result => {
            console.log(result);
            if (result.result == "exist") {
                alert("Plant name already exist")
            }
            else {
                modal.style.display = "none";
                document.querySelectorAll('.toset').forEach (element => {
                    element.value = ""
                });

            }
            
            
        })
        return false;
    }
    // CSRF token function  
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

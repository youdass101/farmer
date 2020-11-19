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
                data,
                type : "create"
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
                var table = document.getElementById("planttable");
                var row = table.insertRow(1);
                row.innerHTML = `<td class="name" style="text-transform:capitalize;">${data.name}</td><td class="seeds">${data.seeds}g</td>
                    <td class="blackout">${data.blackout} days</td><td class="pressure">${data.pressure} days</td><td class="harvest">${data.harvest} days</td>
                    <td class="output">${data.output}g</td><td><button class="editplant" value="${data.id}">Edit</button></td>`
            }     
        })
        return false;
    }

    // EDIT PLANT
    document.querySelectorAll(".editplant").forEach (button => {
        button.onclick = () => {
            if (!document.querySelector(".save")) {
                parent = (button.parentElement).parentElement;
                i = button.value
                n = parent.querySelector(".name").innerHTML;
                s = parent.querySelector(".seeds").innerHTML;
                b = parent.querySelector(".blackout").innerHTML;
                p = parent.querySelector(".pressure").innerHTML;
                h = parent.querySelector(".harvest").innerHTML;
                o = parent.querySelector(".output").innerHTML;
                parent.innerHTML=`<td style="text-transform:capitalize;"><input class="namee" value="${n}"></td>
                <td ><input class="seedse" value="${s}"></td>
                <td ><input class="blackoute" value="${b}"></td>
                <td ><input class="pressuree" value="${p}"></td>
                <td ><input class="harveste" value="${h}"></td>
                <td ><input class="outpute" value="${o}"></td>
                <td>
                    <button value="${i}" class="save">Save</button>
                </td>`
                document.querySelector(".save").onclick = () => {
                    var data = {
                        name : document.querySelector(".namee").value,
                        seeds : document.querySelector(".seedse").value,
                        blackout : document.querySelector(".namee").value,
                        pressure : document.querySelector(".pressuree").value,
                        harvest : document.querySelector(".harveste").value,
                        output : document.querySelector(".outpute").value,
                        id : document.querySelector(".save").value
                    }  
                    fetch('/plants', {
                        method: 'POST',
                        body: JSON.stringify({
                            data,
                            type: "put"  
                        }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })

                }
            }
        }
    })

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

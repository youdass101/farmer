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
    if (document.querySelector('#createplant')){
        // Create new plant
        document.querySelector('#createplant').onclick = () => {
            var data = 
                {   // Setting data in json to create new plant 
                    name : document.querySelector('#id_name').value,
                    seeds : document.querySelector('#id_seeds').value,
                    pressure : document.querySelector('#id_pressure').value,
                    blackout : document.querySelector('#id_blackout').value,
                    harvest : document.querySelector('#id_harvest').value,
                    output : document.querySelector('#id_output').value
                }
            // ADDING CSRF FOR FETSH
            const csrftoken = getCookie('csrftoken');
            // REQEST CREATE NEW PLANT VIEW 
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
            // GET NEW DATA 
            .then(response => response.json())
            .then( result => {
                console.log(result);
                // CHECK IF PLANT ALREADY EXIST AND ALERT IF YES
                if (result.result == "exist") {
                    alert("Plant name already exist")
                }
                // RESET NEW PLANT FORM FROM DATA 
                else {
                    modal.style.display = "none";
                    document.querySelectorAll('.toset').forEach (element => {
                        element.value = ""
                    });
                    //ADDIN THE NEW PLANT TO THE TABLE ON PAGE 
                    var table = document.getElementById("planttable");
                    var row = table.insertRow(1);
                    row.innerHTML = `<td class="name" style="text-transform:capitalize;">${data.name}</td><td class="seeds">${data.seeds}g</td>
                        <td class="blackout">${data.blackout} days</td><td class="pressure">${data.pressure} days</td><td class="harvest">${data.harvest} days</td>
                        <td class="output">${data.output}g</td><td><button class="editplant" value="${data.id}">Edit</button></td>`
                }     
            })
            // STOP PAGE FROM RELOAD 
            return false;
        }
    }

    if(document.querySelectorAll(".editplant")){
        // EDIT PLANT
        document.querySelectorAll(".editplant").forEach (button => {
            button.onclick = () => {
                if (!document.querySelector(".save")) {
                    // COLLECT PLANT TO EDIT CURRENT DATA
                    parent = (button.parentElement).parentElement;
                    i = button.value
                    n = parent.querySelector(".name").innerHTML;
                    s = parent.querySelector(".seeds").getAttribute('value');
                    b = parent.querySelector(".blackout").getAttribute('value');
                    p = parent.querySelector(".pressure").getAttribute('value');
                    h = parent.querySelector(".harvest").getAttribute('value');
                    o = parent.querySelector(".output").getAttribute('value');
                    // REPLACE DATA TABLE WITH INPUT TABLE TO EDIT CURRENT DATA 
                    parent.innerHTML=`<td style="text-transform:capitalize;"><input class="namee" value="${n}"></td>
                    <td ><input class="seedse" value="${s}"></td>
                    <td ><input class="blackoute" value="${b}"></td>
                    <td ><input class="pressuree" value="${p}"></td>
                    <td ><input class="harveste" value="${h}"></td>
                    <td ><input class="outpute" value="${o}"></td>
                    <td>
                        <button value="${i}" class="save">Save</button>
                    </td>`
                    // WHEN SAVE BUTTON IS CLICKED 
                    document.querySelector(".save").onclick = () => {
                        // COLLECTING NEW DATA 
                        var data = {
                            name : document.querySelector(".namee").value,
                            seeds : document.querySelector(".seedse").value,
                            blackout : document.querySelector(".blackoute").value,
                            pressure : document.querySelector(".pressuree").value,
                            harvest : document.querySelector(".harveste").value,
                            output : document.querySelector(".outpute").value,
                            id : document.querySelector(".save").value
                        }  
                        // REQUESTING EDIT FROM VIEW 
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
                        // REQUESTING REPLY INFO AND DATA FROM VIEW 
                        .then (response => response.json())
                        .then (result => {
                            console.log(result)
                            // REFORM TABLE TO NORMAL VIEW
                            if (result.error){
                                alert(result.msg)
                            }
                            else {
                                // REDITING ROW TO VIEW DATA 
                                select = (document.querySelector(".save").parentElement).parentElement
                                select.innerHTML = ` <td class="name" style="text-transform:capitalize;">${data.name}</td>
                                    <td class="seeds">${data.seeds}g</td>
                                    <td class="blackout">${data.blackout} days</td>
                                    <td class="pressure">${data.pressure} days</td>
                                    <td class="harvest">${data.harvest} days</td>
                                    <td class="output">${data.output}g</td>
                                    <td>
                                        <button class="editplant" value="${data.id}" >Edit</button>
                                    </td>`
                            }
                        })
                    }
                }
            }
        })
    }
    // CREATE NEW MEDIUM
    if (document.querySelector('#newmedium')){
        document.querySelector('#newmedium').onclick = () => {
            var data = 
                {   // Setting data in json to create new plant 
                    name : document.querySelector('#id_name').value,
                    soil : document.querySelector('#id_soil').value,
                    coco : document.querySelector('#id_coco').value
                }
            // REQEST CREATE NEW PLANT VIEW 
            fetch('/medium',{
                method: 'POST',
                body: JSON.stringify({
                    data,
                    type : "create"
                }),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            // GET NEW DATA 
            .then(response => response.json())
            .then( result => {
                console.log(result);
                // CHECK IF PLANT ALREADY EXIST AND ALERT IF YES
                if (result.result == "exist") {
                    alert("Plant name already exist")
                }
                // RESET NEW PLANT FORM FROM DATA 
                else {
                    modal.style.display = "none";
                    document.querySelectorAll('.toset').forEach (element => {
                        element.value = ""
                    });
                    //ADDIN THE NEW PLANT TO THE TABLE ON PAGE 
                    var table = document.getElementById("mediumtable");
                    var row = table.insertRow(1);
                    row.innerHTML = `<td style = "text-transform:capitalize;">${data.name}</td>
                        <td>${data.soil}%</td>
                        <td>${data.soil}%</td>
                        <td>
                            <form action="" method="POST">
                                <input id="output" name="idmix" type="hidden" value="${data.id}"/>
                                <button type="submit">Edit</button>
                                </form>
                            </td>`
                }
            })
            return false
        }
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

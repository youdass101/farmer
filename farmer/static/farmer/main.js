document.addEventListener('DOMContentLoaded', function() {

    // Get the modal WHICH IS IN LAYOUT A FORM TO CREATE ANY NEW OBJECT
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
    // IF USER AT PLANT PAGE AND CREATE FOR IF EXIST 
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
            // REQEST CREATE NEW PLANT VIEW 
            fetch('/plants',{
                method: 'POST',
                body: JSON.stringify({
                    data,
                    type : "create"
                }),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
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
                        <td>${data.coco}%</td>
                        <td>
                                <button class="editmedium" value="${data.id}">Edit</button>
                            </td>`
                }
            })
            return false
        }
    }

    if(document.querySelectorAll(".editmedium")){
        // EDIT PLANT
        document.querySelectorAll(".editmedium").forEach (button => {
            button.onclick = () => {
                if (!document.querySelector(".save")) {
                    // COLLECT PLANT TO EDIT CURRENT DATA
                    parent = (button.parentElement).parentElement;
                    i = button.value;
                    n = parent.querySelector(".name").innerHTML;
                    s = parent.querySelector(".soil").getAttribute('value');
                    c = parent.querySelector(".coco").getAttribute('value');
                    parent.innerHTML = `<td style = "text-transform:capitalize;"><input class="namee" value="${n}"></input></td>
                        <td><input class="soile" value="${s}"></input></td>
                        <td><input class="cocoe" value="${c}"></input></td>
                        <td>
                            <button class="save" value="${i}">Save</button>
                        </td>`

                    document.querySelector(".save").onclick = () => {
                        // COLLECTING NEW DATA 
                        var data = {
                            name : document.querySelector(".namee").value,
                            soil : document.querySelector(".soile").value,
                            coco : document.querySelector(".cocoe").value,
                            id : document.querySelector(".save").value
                        }  
                    
                        fetch ("/medium", {
                            method : "POST",
                            body : JSON.stringify({
                                data,
                                type : "put"
                            }),
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken')
                            }
                        })
                        .then (response => response.json())
                        .then (result => {
                            console.log(result)
                            if (result.error){
                                alert(result.msg)
                            }
                            else {
                                // REDITING ROW TO VIEW DATA 
                                select = (document.querySelector(".save").parentElement).parentElement
                                select.innerHTML = `<td style = "text-transform:capitalize;">${data.name}</td>
                                    <td>${data.soil}%</td>
                                    <td>${data.coco}%</td>
                                    <td>
                                        <button class="editmedium" value="${data.id}">Edit</button>
                                    </td>`
                            }

                        })


                    }
                    
                }
            }
        })
    }
    //Countdown 
    if (document.querySelector(".countdown")){
        document.querySelectorAll(".countdown").forEach (cell => {
            var parent = (cell.parentElement).querySelector(".end").innerHTML
            
            var countDownDate = new Date(parent).getTime();

            // Update the count down every 1 second
            var x = setInterval(function() {

            // Get today's date and time
            var now = new Date().getTime();

            // Find the distance between now and the count down date
            var distance = countDownDate - now;

            // Time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            // Display the result in the element with id="demo"
            cell.innerHTML = days + "d " + hours + "h "
            + minutes + "m " + seconds + "s ";
            
            
            // If the count down is finished, write some text
            if (distance < 0) {
                clearInterval(x);
                cell.innerHTML = "HARVEST NOW";
            }
            }, 1000);

        })
    }
    // AUTO GET SEED WEIGHT WHEN CREATIING NEW PLANT AND SELECT A PLANT NAME FROM LIST
    if (document.querySelector("#id_plant")){
        select = document.querySelector("#id_plant")
        
        select.addEventListener('change', (event) =>{
            var s = select.value
            fetch('/plants', {
                method: 'POST',
                body: JSON.stringify({
                    data: s,
                    type: "get"  
                }),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            // REQUESTING REPLY INFO AND DATA FROM VIEW 
            .then (response => response.json())
            .then (result => {
                document.querySelector("#id_seed").value = result.result
            })
        })

    }
    // EDIT TRAY 
    if(document.querySelectorAll('.edit_tray')){
        document.querySelectorAll('.edit_tray').forEach (button => {
            var edit = document.getElementById("MyEdit")
            button.onclick = () => {
                parent = (button.parentElement).parentElement
                mw = parent.querySelector(".mw").innerHTML
                sw = parent.querySelector(".sw").innerHTML
                mt = parent.querySelector(".mt").innerHTML
                ts = parent.querySelector(".ts").innerHTML
                tray_name = parent.querySelector(".tn").innerHTML

                op = document.getElementById("id_medium").options
                for (var i = 0; i < op.length; i++){
                    
                    if (document.getElementById("id_medium").options[`${i}`].innerHTML == mt){
                        edit.querySelector("#id_medium").selectedIndex = i+1
                    }
                }
                
                edit.querySelector("#id_seed").value = sw
                edit.querySelector("#id_medium_weight").value = mw
                edit.querySelector("#id_start").value = ts
                document.querySelector(".edit_title").innerHTML = `Edit ${tray_name}`

                document.querySelector("#delete_tray").onclick = () =>{
                    alert(`Are you sure want to delete ${tray_name}`)
                    fetch('/', {
                        method: 'PUT',
                        body: JSON.stringify({
                            delete : true,
                            id : button.value
                        }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.result){
                            parent.remove()
                            edit.style.display = "none";
                        }
                    })
                }

                document.querySelector("#save_tray").onclick = () =>{
                    var medium = edit.querySelector("#id_medium")
                    var seed = edit.querySelector("#id_seed").value
                    var medium_weight = edit.querySelector("#id_medium_weight").value
                    var start = edit.querySelector("#id_start").value

                    fetch('/', {
                        method: 'PUT',
                        body: JSON.stringify({
                            medium : medium.options[medium.selectedIndex].innerHTML,
                            seed : seed,
                            medium_weight : medium_weight,
                            start : start,
                            id : button.value,
                            delete : false
                        }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.result){
                            edit.style.display = "none";
                            parent.querySelector(".mw").innerHTML = medium_weight
                            parent.querySelector(".sw").innerHTML = seed
                            parent.querySelector(".mt").innerHTML = medium.options[medium.selectedIndex].innerHTML
                            parent.querySelector(".ts").innerHTML = start
                        }
                    })
                }

                edit.style.display = "block";
                // Get the <span> element that closes the modal
                var sp = document.getElementsByClassName("cls")[0];
                sp.onclick = function() {
                    edit.style.display = "none";
                }
            
                // When the user clicks anywhere outside of the modal, close it
                window.onclick = function(event) {
                    if (event.target == edit) {
                        edit.style.display = "none";
                    }
                }

            }

        })

        document.querySelectorAll(".harvest").forEach(button => {
            var harvest = document.getElementById("Harvest")
            button.onclick = () =>{
                parent = (button.parentElement).parentElement
                tray_name = parent.querySelector(".tn").innerHTML
                document.querySelector(".harvest_title").innerHTML = tray_name
                harvest.style.display = "block";
                // Get the <span> element that closes the modal
                var sp = document.getElementsByClassName("clsh")[0];
                sp.onclick = function() {
                    harvest.style.display = "none";
                }
            
                // When the user clicks anywhere outside of the modal, close it
                window.onclick = function(event) {
                    if (event.target == harvest) {
                        harvest.style.display = "none";
                    }
                }

                document.querySelector("#harvest_tray").onclick = () =>{
                    h = harvest.querySelector("#harvest_weight").value
                    d = harvest.querySelector("#harvest_date").value

                    fetch('/harvest', {
                        method : 'POST',
                        body: JSON.stringify({
                            h: h,
                            d: d,
                            id: button.value
                        }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    .then(response => response.json())
                    .then(result => {
                        harvest.style.display = "none";
                        parent.remove()
                    })
                }
            }  
        }); 
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

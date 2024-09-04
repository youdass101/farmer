document.addEventListener('DOMContentLoaded', function() {

    // Get the modal WHICH IS IN LAYOUT A FORM TO CREATE ANY NEW OBJECT
    var modal = document.getElementById("myModal");
    var modaledit = document.getElementById("myEditModal");


    // Get the button that opens the modal
    var btn = document.getElementById("myBtn");

    // Get the <span> element that closes the modal
    if (document.getElementsByClassName("close")[1]) {
        var espan = document.getElementsByClassName("close")[1];
        espan.onclick = function() {
                modaledit.style.display = "none";
            }
    }
    
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


    // Harvest button popup and data
    if(document.querySelectorAll('.harvestbt')){    
        // HARVEST A TRAY 
        document.querySelectorAll(".harvestbt").forEach(button => {
            // LOAD HARVEST FORM 
            var trayid = button.value
            var harvestpop = document.querySelector(".modalharvest")
            button.onclick = () =>{
                harvestpop.style.display = "block";
                document.querySelector("#id_tray").value = trayid
                document.querySelector("#harvestplantname").innerHTML = button.parentElement.querySelector(".hplantname").value

                // close icon action
                var harvstbt = document.getElementById("clsh");
                harvstbt.onclick = function() {
                    harvestpop.style.display = "none";
                }
                // press outside the form window to close it
                window.onclick = function(event) {
                    if (event.target == harvestpop) {
                        harvestpop.style.display = "none";
                    }
                }
            }
        })
    }
                
            

    //Harvest bulk
    if (document.querySelector('#harvestbulk')){
        document.querySelectorAll(".harvestbulk").forEach(button => {
            var harvestbulk = document.getElementById("Harvestbulkpop")
            button.onclick = () =>{
                trayqtt = button.parentElement.querySelector(".ana").querySelector(".analytic_box").querySelector(".tray_number").querySelector(".number").innerHTML
                traysids = button.value
                harvestbulk.querySelector(".modal-content").querySelector(".cells").querySelector(".harvest_bulk_trays").value = trayqtt
                harvestbulk.style.display = "block"

                // Get the <span> element that closes the modal
                var sp = document.getElementsByClassName("clsh")[0];
                sp.onclick = function() {
                    harvestbulk.style.display = "none";
                }
                // close when click outside the block container
                window.onclick = function(event) {
                    if (event.target == harvestbulk) {
                        harvestbulk.style.display = "none"
                    }
                }

                document.querySelector("#harvest_bulk").onclick = () =>{
                    traysqtt = harvestbulk.querySelector("#harvest_bulk_trays").value
                    harvestmixweight = harvestbulk.querySelector("#harvest_bulk_mix_weight").value
                    harvestpackqtt = harvestbulk.querySelector("#harvest_bulk_pack_qtt").value
                    harvestdate = harvestbulk.querySelector("#harvest_date").value

                    fetch('/harvest', {
                        method: 'POST',
                        body: JSON.stringify({
                            bulk : true,
                            tqtt : traysqtt,
                            hmw : harvestmixweight,
                            hpw: harvestpackqtt,
                            d : harvestdate,
                            tidl : traysids,
                            h : 0
                        }),
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken')
                        }
                    })
                    // GET ACTION RESPONSE, REMOVE TRAY ELEMENT AND CLOSE FORM 
                    .then(response => response.json())
                    .then(result => {
                        window.location.reload();
                    })
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
    if (document.querySelector("#id_name")){
        select = document.querySelector("#id_name")
        
        select.addEventListener('change', (event) =>{
            var s = select.value
            fetch('/plants', {
                method: 'POST',
                body: JSON.stringify({
                    data: s,
                    type: "fetch"  
                }),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            // REQUESTING REPLY INFO AND DATA FROM VIEW 
            .then (response => response.json())
            .then (result => {
                document.querySelector("#id_seeds_weight").value = result.result[0]
                document.querySelector("#id_medium_weight").value = result.result[1]
            })
        })

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

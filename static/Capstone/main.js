document.addEventListener('DOMContentLoaded', function() {

    // Get the modal WHICH IS IN LAYOUT A GLOBAL FORM TO CREATE ANY NEW OBJECT
    var modal = document.getElementById("myModal");
    var modaledit = document.getElementById("myEditModal");


    // Get the button that opens the Global modal
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
    if (btn){
        btn.onclick = function() {
            modal.style.display = "block";
        }
    }

    // When the user clicks on <span> (x), close the modal
    if (span && modal) {
        span.onclick = function() {
            modal.style.display = "none";
        }
    }


    // When the user clicks anywhere outside of the modal, close it
    window.addEventListener('keydown', function(event) {
        if (event.key == 'Escape') {
            if (modal) {
                modal.style.display = "none";
            }
            if (modaledit) {
                modaledit.style.display = "none";
            }
        }
    })

    //Alert if delete all is presed
    if(document.querySelectorAll(".report_delete_all")){
        document.querySelectorAll(".report_delete_all").forEach(button => {
        button.onclick = () => {
            if (confirm("Are you sure you want to delete")) {
                return true
            }
            else{
                return false
            }
        }})
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

                window.addEventListener('keydown', function(event) {
                    if (event.key == 'Escape') {
                        harvestpop.style.display = "none";
                    }
                })
            }
        })
    }
                
            

    // Harvest bulk
    const harvestbulk = document.getElementById("Harvestbulkpop");
    document.querySelectorAll(".harvestbulk").forEach(button => {
        button.onclick = () => {
            const card = button.closest(".ana-cards");
            if (!harvestbulk || !card) {
                return;
            }

            const trayName = card.querySelector(".tray_name").textContent.trim();
            const trayQuantity = card.querySelector(".tray_number .number").textContent.trim();
            const traysIds = button.value;

            harvestbulk.querySelector("#harvest_title").textContent = trayName;
            harvestbulk.querySelector("#id_Trays").value = trayQuantity;
            harvestbulk.querySelector("#id_Trays").max = trayQuantity;
            harvestbulk.querySelector("#bulkharvest").value = traysIds;
            harvestbulk.style.display = "block";
        }
    });

    const closeHarvest = document.querySelector("#Harvestbulkpop .clsh");
    if (closeHarvest && harvestbulk) {
        closeHarvest.onclick = () => {
            harvestbulk.style.display = "none";
        };
    }

    window.addEventListener("click", event => {
        if (event.target === harvestbulk) {
            harvestbulk.style.display = "none";
        }
    });
  



    // Countdown
    document.querySelectorAll(".countdown").forEach(cell => {
        const endCell = cell.parentElement.querySelector(".end");
        const target = cell.dataset.countdownTarget || (endCell && endCell.textContent.trim());
        const countDownDate = new Date(target).getTime();

        if (Number.isNaN(countDownDate)) {
            cell.textContent = "Countdown unavailable";
            return;
        }

        let interval;
        const updateCountdown = () => {
            const distance = countDownDate - Date.now();

            if (distance < 0) {
                clearInterval(interval);
                cell.textContent = "HARVEST NOW";
                return false;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            cell.textContent = days + "d " + hours + "h " + minutes + "m " + seconds + "s";
            return true;
        };

        if (updateCountdown()) {
            interval = setInterval(updateCountdown, 1000);
        }
    });
    
    // Load plant defaults into the new/edit tray form that changed.
    document.querySelectorAll('select[name="name"]').forEach(select => {
        select.addEventListener("change", () => {
            const form = select.closest("form");
            const seedsWeight = form && form.querySelector('[name="seeds_weight"]');
            const mediumWeight = form && form.querySelector('[name="medium_weight"]');

            if (!select.value || !seedsWeight || !mediumWeight) {
                return;
            }

            fetch("/plants", {
                method: "POST",
                body: JSON.stringify({
                    data: select.value,
                    type: "fetch"
                }),
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Unable to load plant defaults.");
                }
                return response.json();
            })
            .then(result => {
                seedsWeight.value = result.result[0];
                mediumWeight.value = result.result[1];
            })
            .catch(error => console.error(error));
        });
    });
    


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

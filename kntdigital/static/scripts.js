
function editEmployee(){
    document.getElementById("edit_button").style.display = "none";
    document.getElementById("employee_data_edit").style.display="";
    document.getElementById("cancel_button").style.display="";
}

function cacelEditEmployee(){
    document.getElementById("edit_button").style.display = "";
    document.getElementById("employee_data_edit").style.display="none";
    document.getElementById("cancel_button").style.display="none";
}

function searchEmployee(){
    var input = document.getElementById("search-input").value
    var filter = input.toUpperCase();
    var table = document.getElementById("employee-table")
    var rows = table.getElementsByTagName("tr");
    for(i = 1; i < rows.length; i++)
    {
        var cells = rows[i].getElementsByTagName("td")        
        var match = false;
        for(j = 0; j < cells.length; j++)
        {
            console.log("Cell" + cells[j].innerHTML.toUpperCase());
            if(cells[j].innerHTML.toUpperCase().indexOf(filter) > -1)
            {
                match = true;
                break;
            }
        }
        if(match)
        {
            rows[i].style.display="";
        }
        else
        {
            rows[i].style.display="none";   
        }
    }
}

function sendAjaxRequest(event) {
    let row = event.currentTarget;
    let id = $(row).find('td[data-name="email"]').attr("name");;
    console.log(id)
    window.location.href = 'employee/'+ id;    

    // $.ajax({
    //     type: "POST",
    //     url: "employee",
    //     data: { "email": email },
    //     success: function (response) {
    //         $('#main-content').html(response);
    //     }
    // });  
}





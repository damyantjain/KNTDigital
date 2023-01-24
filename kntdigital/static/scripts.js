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
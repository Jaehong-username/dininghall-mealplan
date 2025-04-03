var CSRFToken = ""

function setCSRF(token)
{
    CSRFToken = token;
}

// Get data from db, must be authenticated as an admin.
function loadAdminData(db_table, table_element_id) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if(req.readyState == 4) {
            if(req.status != 200) {
                console.log("Request failed. Error code: " + req.status);
                return null;
            }
            else {
                var response = JSON.parse(req.responseText);
                // request went through, populate the table with recieved data.
                populateTable(response, table_element_id);
            }
        }
    }

    req.open('POST', '/api/get_admin_data');
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.setRequestHeader("X-CSRFToken", CSRFToken);
    var postVars = "table_id=" + db_table;
    req.send(postVars);

    return false;
}

function populateTable(jsonData, table_element_id) {
    var t = document.getElementById(table_element_id);
    if(t == null) {
        return;
    }

    // Create header
    var table_text = "<tr>";
    for(var header in jsonData[0]) {
        table_text += `<th>${header}</th>`;
    }
    table_text += "</tr>"
    // Populate rows
    for(var row in jsonData) {
        table_text += "<tr>";
        var row_data = jsonData[row];
        for(var cell in row_data) {
            table_text += `<td>${ row_data[cell] }</td>`;
        }
        table_text += "</tr>";
    }

    // clear and replace table HTML
    t.innerHTML = table_text;
}


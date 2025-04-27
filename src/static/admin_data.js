var CSRFToken = ""

function setCSRF(token)
{
    CSRFToken = token;
}

function ajax(url, method, vars, callback, ...callbackParams) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function () {
        if(req.readyState == 4) {
            if(req.status != 200) {
                console.log("Request failed. Error code: " + req.status);
                return null;
            }
            else {
                var response = JSON.parse(req.responseText);
                // request went through, populate the table with recieved data.
                callback(response, ...callbackParams);
            }
        }
    }
    req.open(method, url);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.setRequestHeader("X-CSRFToken", CSRFToken);
    req.send(vars);
}


async function writeAdminApi(endpoint, api_table, html_table, form_element) {
    var form = document.getElementById(form_element);
    const response = await fetch(endpoint, {
        method: "POST",
        // Set the FormData instance as the request body
        body: new FormData(form),
      });
    getDataInTable(api_table, html_table); 

}

function deleteRequest(api_table, id, html_table) {
    if(confirm(`Delete ${api_table}?`)) {
        console.log(`Deleting ${api_table} with id ${id}`);
        ajax("/api/delete_object", "POST", `table_id=${String(api_table)}&id=${String(id)}`, () => getDataInTable(api_table, html_table));
    }
     
}

function getDataInTable(api_table, html_table) {
    ajax('/api/get_admin_data', 'POST', 'table_id=' + api_table, populateTable, api_table, html_table);
}

function populateTable(jsonData, api_table, table_element_id) {
    
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
        // Add delete button
        if(row_data["!id"]) {
            table_text += `<td><button onclick="deleteRequest('${api_table}', ${row_data["!id"]}, '${table_element_id}');">Delete</button></td>`;
        }
        table_text += "</tr>";
    }

    // clear and replace table HTML
    t.innerHTML = table_text;
}


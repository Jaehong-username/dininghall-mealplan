var CSRFToken = ""

function setCSRF(token)
{
    CSRFToken = token;
}

function ajax(url, method, vars, callback, reflected_element) {
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
                callback(response, reflected_element);
            }
        }
    }
    req.open(method, url);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.setRequestHeader("X-CSRFToken", CSRFToken);
    req.send(vars);
}

async function addUser() {
    var form = document.getElementById("new_user_form");
    const response = await fetch("/api/add_user", {
        method: "POST",
        // Set the FormData instance as the request body
        body: new FormData(form),
      });
    getAllUsers("user-entries"); 
}

async function updateUser() {
    var form = document.getElementById("update_user_form");
    const response = await fetch("/api/edit_user", {
        method: "POST",
        // Set the FormData instance as the request body
        body: new FormData(form),
      });
    getAllUsers("user-entries"); 
}


async function addStudent() {
    var form = document.getElementById("new_student_form");
    const response = await fetch("/api/add_student", {
        method: "POST",
        // Set the FormData instance as the request body
        body: new FormData(form),
      });
    getAllStudents("student-entries"); 
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

function deleteUserRequest(id, table) {
    if(confirm("Delete user?")) {
        console.log("Deleting user" + id)
        ajax('/api/delete_user', 'POST', 'id=' + String(id), () => {}, null);
        getAllUsers(table);
    }
}

function getAllUsers(table_element) {
    ajax('/api/get_admin_data', 'POST', 'table_id=user', populateUserTable, table_element);
}
function getAllStudents(table_element) {
    ajax('/api/get_admin_data', 'POST', 'table_id=student', populateTable, table_element);
}

function populateUserTable(jsonData, table_element_id) {
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
        console.log(row_data);
        for(var cell in row_data) {
            table_text += `<td>${ row_data[cell] }</td>`;
        }
        // Add user delete button
        table_text += `<td><button onclick="deleteUserRequest(${row_data["!id"]}, '${table_element_id}');">Delete</button></td>`;
        table_text += "</tr>";
    }

    // clear and replace table HTML
    t.innerHTML = table_text;
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


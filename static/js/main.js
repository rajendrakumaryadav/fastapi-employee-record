function initializeTable(employees) {
  const employeeTable = document.querySelector("tbody");

  // Clear the table body
  employeeTable.innerHTML = "";

  if (employees.length > 0) {
    employees.forEach((employee) => {
      const newRow = employeeTable.insertRow();
      newRow.id = `employee-${employee.id}`;

      newRow.insertCell().textContent = employee.id;
      newRow.insertCell().textContent = employee.name;
      newRow.insertCell().textContent = employee.designation.name;
      newRow.insertCell().textContent = employee.joining_date;
      newRow.insertCell().textContent = employee.created_at;
      newRow.insertCell().innerHTML = `
        <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" onclick="deleteEmployee('${employee.id}')">Delete</button>
      `;
    });
  } else {
    // Show "No employees found" message if no records are present
    const newRow = employeeTable.insertRow();
    newRow.classList.add("border-t");
    newRow.insertCell().colSpan = 6;
    newRow.cells[0].textContent = "No employees found.";
    newRow.cells[0].style.textAlign = "center";
  }
}

async function submitEmployeeForm() {
  const name = document.getElementById("name").value;
  const designationId = document.getElementById("designation").value; // Get the ID
  const joiningDate = document.getElementById("joining_date").value;

  if (!name || !designationId || !joiningDate) {
    alert("Please fill all fields.");
    return;
  }

  const data = {
    name: name,
    designation_id: designationId, // Send the ID
    joining_date: joiningDate,
  };

  try {
    const response = await fetch("/employee", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const newEmployee = await response.json();
      alert("Employee added successfully!");

      // Add new employee to the table
      const employeeTable = document.querySelector("tbody");
      const existingRow = document.getElementById(`employee-${newEmployee.id}`);

      if (!existingRow) {
        const newRow = employeeTable.insertRow();
        newRow.id = `employee-${newEmployee.id}`;

        newRow.insertCell().textContent = newEmployee.id;
        newRow.insertCell().textContent = newEmployee.name;
        newRow.insertCell().textContent = newEmployee.designation.name;
        newRow.insertCell().textContent = newEmployee.joining_date;
        newRow.insertCell().textContent = newEmployee.created_at;
        newRow.insertCell().innerHTML = `
          <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" onclick="deleteEmployee('${newEmployee.id}')">Delete</button>
        `;
      }

      // Reset the form fields
      document.querySelector("form").reset();
    } else {
      const error = await response.json();
      alert("Error adding employee: " + error.message);
    }
  } catch (error) {
    console.error("Error submitting form:", error);
    alert("An error occurred while submitting the form.");
  }
}

// Event listener for form submission
const employeeForm = document.querySelector("form");
employeeForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitEmployeeForm();
});

// Function to handle deletion of employees
async function deleteEmployee(employeeId) {
  if (confirm("Are you sure you want to delete this employee?")) {
    try {
      const response = await fetch(`/employee/${employeeId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        alert("Employee deleted successfully!");
        const rowToDelete = document.getElementById(`employee-${employeeId}`);
        if (rowToDelete) {
          rowToDelete.remove();
        }

        const employeeTable = document.querySelector("tbody");
        if (employeeTable.children.length === 0) {
          // Show "No employees found" message if table is empty
          const newRow = employeeTable.insertRow();
          newRow.classList.add("border-t");
          newRow.insertCell().colSpan = 6;
          newRow.cells[0].textContent = "No employees found.";
          newRow.cells[0].style.textAlign = "center";
        }
      } else {
        const error = await response.json();
        alert("Error deleting employee: " + error.message);
      }
    } catch (error) {
      console.error("Error deleting employee:", error);
      alert(
        "An error occurred while deleting the employee. Please try again later.",
      );
    }
  }
}

// Function to initialize table on page load
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/employees"); // Adjust URL based on your API endpoint
    if (response.ok) {
      const employees = await response.json();
      initializeTable(employees);
    } else {
      console.error("Failed to fetch employees");
    }
  } catch (error) {
    console.error("Error loading employees:", error);
  }
});

const designationForm = document.getElementById("designationForm");
designationForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = document.getElementById("name").value;

  try {
    const response = await fetch("/designations/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: name }),
    });
    if (response.ok) {
      const data = await response.json();
      // Update the table with the new designation
      const designationTableBody = document.getElementById(
        "designationTableBody",
      );
      const newRow = designationTableBody.insertRow();
      newRow.innerHTML = `
                <tr class="border-t hover:bg-gray-100" id="designation-${data.id}">
                    <td class="py-2 px-4 font-medium">${data.id}</td>
                    <td class="py-2 px-4">${data.name}</td>
                    <td class="py-2 px-4">${data.created_at}</td>
                    <td class="py-2 px-4">
                        <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" onclick="deleteDesignation('${data.id}')">Delete</button>
                    </td>
                </tr>
            `;
      // Clear the form
      designationForm.reset();
      // Optionally display a success message to the user
      alert("Designation added successfully.");
    } else {
      // Handle the error, e.g., display an error message
      console.error("Error adding designation:", await response.text());
      alert("Error adding designation. Please try again.");
    }
  } catch (error) {
    console.error("Error adding designation:", error);
    alert("Error adding designation. Please try again.");
  }
});

// Delete designation using AJAX
async function deleteDesignation(designationId) {
  if (confirm("Are you sure you want to delete this designation?")) {
    try {
      const response = await fetch(`/designations/${designationId}`, {
        method: "DELETE",
      });
      if (response.ok) {
        // Remove the row from the table
        const row = document.getElementById(`designation-${designationId}`);
        row.remove();
        // Optionally display a success message to the user
        alert("Designation deleted successfully.");
      } else {
        // Handle the error, e.g., display an error message
        console.error("Error deleting designation:", await response.text());
        alert("Error deleting designation. Please try again.");
      }
    } catch (error) {
      console.error("Error deleting designation:", error);
      alert("Error deleting designation. Please try again.");
    }
  }
}

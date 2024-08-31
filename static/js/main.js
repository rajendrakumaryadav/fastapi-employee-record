// Function to initialize the table with existing data
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
      newRow.insertCell().textContent = employee.designation;
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

// Function to handle form submission
async function submitEmployeeForm() {
  const name = document.getElementById("name").value;
  const designation = document.getElementById("designation").value;
  const joiningDate = document.getElementById("joining_date").value;

  if (!name || !designation || !joiningDate) {
    alert("Please fill all fields.");
    return;
  }

  const data = {
    name: name,
    designation: designation,
    joining_date: joiningDate,
  };

  try {
    const response = await fetch("/employee/", {
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
        newRow.insertCell().textContent = newEmployee.designation;
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

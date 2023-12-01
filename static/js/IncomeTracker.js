/* Author: Kim Arenas */

var incomeChart;


function updateChart() {
    var ctx = document.getElementById('incomeChart').getContext('2d');

    if (incomeChart) {
        incomeChart.destroy();
    }

    var data = {
        labels: [],
        datasets: [{
            label: 'Income Amount',
            data: [],
            backgroundColor: 'rgba(0, 191, 0, 0.8)',
            borderColor: 'rgba(0, 191, 0, 1)',
            borderWidth: 1
        }]
    };
    // Populate data from the table
    var table = document.getElementById('incomeTable');
    if (table) {
        for (var i = 1; i < table.rows.length; i++) {
            var row = table.rows[i];
            var date = row.cells[0].innerText;
            var amount = parseFloat(row.cells[3].innerText);
            data.labels.push(date);
            data.datasets[0].data.push(amount);
        }
    }
    // Create the chart
    incomeChart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initIncomeTracker();
});

function initIncomeTracker() {
    createIncomeTableIfNotExists();
    try {
        loadIncomeData();
    } catch (e) {
        console.error("Error loading data from local storage:", e);
        // Provide user feedback
        showAlert('Error loading data. Please try again later.');
    }
}

function createIncomeTableIfNotExists() {
    if (!document.getElementById('incomeTable')) {
        createIncomeTable();
    }
}

function showAlert(message) {
    // Implement user-friendly error display, could be a modal or toast notification
    console.log('ALERT:', message); // Placeholder for actual user alert
}


var incomeData = []; // Initialize an empty array to hold income entries

function saveIncomeData() {
    try {
        localStorage.setItem('incomeData', JSON.stringify(incomeData));
    } catch (e) {
        console.error("Error saving data to local storage:", e);
    }
}

function loadIncomeData() {
    const savedData = localStorage.getItem('incomeData');
    if (savedData) {
        incomeData = JSON.parse(savedData);
        updateIncomeDisplay();
    }
}

function updateIncomeDisplay() {
    var table = document.getElementById('incomeTable');
    while (table.rows.length > 1) {
        table.deleteRow(1);
    }
    // Repopulate the table with income data
    incomeData.forEach(function(item, index) {
        addIncomeRow(item, index); // Pass the index to addIncomeRow
    });
    updateChart(); // Update the chart to reflect the newly loaded data
}

function validateIncomeInput(entry) {
    // Basic validation: check if all fields are filled and if amount is a number
    return entry.date && entry.merchantName && entry.category && !isNaN(parseFloat(entry.amount));
}

function deleteIncomeEntry(index) {
    // Remove the entry from the array
    incomeData.splice(index, 1);

    // Update local storage
    saveIncomeData();

    // Update the display
    updateIncomeDisplay();
}

function addIncomeRow(entry, index) {
    var table = document.getElementById('incomeTable');
    var newRow = table.insertRow(-1);
    newRow.insertCell(0).innerText = entry.date;
    newRow.insertCell(1).innerText = entry.merchantName;
    newRow.insertCell(2).innerText = entry.category;
    newRow.insertCell(3).innerText = entry.amount;

    // Add a delete button cell
    var deleteCell = newRow.insertCell(4);
    var deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.className = 'delete-income-btn';
    deleteButton.onclick = function() { deleteIncomeEntry(index); };
    deleteCell.appendChild(deleteButton);
}

function createIncomeTable() {
    var table = document.createElement('table');
    table.id = 'incomeTable';
    table.className = 'income-table'; // Add your table styling class here

    // Create the header row
    var header = table.createTHead();
    var headerRow = header.insertRow(0);
    var headers = ["Date", "Merchant Name", "Category", "Amount"];
    headers.forEach(function(text, index) {
        var cell = headerRow.insertCell(index);
        cell.innerHTML = text;
    });

    // Append the table to a container element, for example, a div with ID 'tableContainer'
    document.getElementById('tableContainer').appendChild(table);
}

document.getElementById('addIncomeButton').addEventListener('click', function() {
    createIncomeTableIfNotExists();
    addIncomeEntryFromForm();
    //clearIncomeFormFields();
});


function addIncomeEntryFromForm() {
    var newIncomeEntry = collectIncomeFormData();

    if (validateIncomeInput(newIncomeEntry)) {
        addIncomeEntry(newIncomeEntry);
    } else {
        showAlert('Please fill all the fields correctly.');
    }
}


document.getElementById('addIncomeButton').addEventListener('click', function() {

    var table = document.getElementById('incomeTable');
    if (!table) {
        // Create table element
        table = document.createElement('table');
        table.id = 'incomeTable';
        table.className = 'income-table'; // Add your table styling class here

        // Create the header row
        var header = table.createTHead();
        var headerRow = header.insertRow(0);
        var headers = ["Date", "Merchant Name", "Category", "Amount"];
        headers.forEach(function(text, index) {
            var cell = headerRow.insertCell(index);
            cell.innerHTML = text;

        });

        // Append the table to a container element, for example a div with ID 'tableContainer'
        document.getElementById('tableContainer').appendChild(table);

    }

    // Get the date from the date input
    var incomeDate = document.getElementById('incomeDate').value;

    // Insert a new row at the end of the table
    var newRow = table.insertRow(-1);

    // Insert new cells for the new row
    var cellDate = newRow.insertCell(0);
    var cellMerchantName = newRow.insertCell(1);
    var cellCategory = newRow.insertCell(2);
    var cellAmount = newRow.insertCell(3);

    // Assign values to the new cells
    cellDate.innerHTML = incomeDate; // Use the value from the date input
    cellMerchantName.innerHTML = document.getElementById('merchantName').value;
    cellCategory.innerHTML = document.getElementById('category').value;
    cellAmount.innerHTML = document.getElementById('amount').value;

    // Clear the input fields after insertion
    document.getElementById('incomeDate').value = '';
    document.getElementById('merchantName').value = '';
    document.getElementById('category').value = '';
    document.getElementById('amount').value = '';

    saveIncomeData();
    createIncomeTableIfNotExists();

});

function addIncomeEntry(entry) {
    incomeData.push(entry); // Add to the income data array
    addIncomeRow(entry); // Add to the UI table
    saveIncomeData(); // Persist to local storage
    updateChart(); // Update the chart
}

function collectIncomeFormData() {
    return {
        date: document.getElementById('incomeDate').value,
        merchantName: document.getElementById('merchantName').value,
        category: document.getElementById('category').value,
        amount: document.getElementById('amount').value
    };
}

function addIncomeEntry(entry) {
    incomeData.push(entry); // Add to the income data array
    //addIncomeRow(entry); // Add to the UI table
    saveIncomeData(); // Persist to local storage
    updateChart(); // Update the chart
}


// Event listener for the "Generate Chart" button
document.getElementById('generateChartButton').addEventListener('click', updateChart);

document.getElementById('exportChartButton').addEventListener('click', function() {
    // Use html2canvas to take a screenshot of the chart
    html2canvas(document.getElementById('incomeChart')).then(canvas => {
        // Convert the canvas to an image
        const imageData = canvas.toDataURL('image/png');

        // Use jsPDF to create a PDF
        const pdf = new jspdf.jsPDF(); // Notice the case 'jsPDF'
        const imgProps= pdf.getImageProperties(imageData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
        pdf.addImage(imageData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        pdf.save('income-chart.pdf');
    });
});
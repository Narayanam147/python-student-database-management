// API Base URL
const API_BASE = '/api';

// Check database connection on load
window.addEventListener('DOMContentLoaded', () => {
    checkConnection();
});

// Check database connection
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE}/check-connection`);
        const data = await response.json();
        
        const statusEl = document.getElementById('connectionStatus');
        if (data.success) {
            statusEl.classList.add('connected');
            statusEl.innerHTML = '<i class="fas fa-circle"></i><span>Connected</span>';
        } else {
            statusEl.classList.add('disconnected');
            statusEl.innerHTML = '<i class="fas fa-circle"></i><span>Disconnected</span>';
        }
    } catch (error) {
        const statusEl = document.getElementById('connectionStatus');
        statusEl.classList.add('disconnected');
        statusEl.innerHTML = '<i class="fas fa-circle"></i><span>Error</span>';
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Show section
function showSection(section) {
    const contentArea = document.getElementById('contentArea');
    contentArea.style.opacity = '0';
    
    setTimeout(() => {
        switch(section) {
            case 'add':
                showAddStudent();
                break;
            case 'view':
                showViewRecords();
                break;
            case 'search':
                showSearchStudent();
                break;
            case 'update':
                showUpdateStudent();
                break;
            case 'delete':
                showDeleteStudent();
                break;
            case 'export':
                showExportOptions();
                break;
        }
        contentArea.style.opacity = '1';
    }, 200);
}

// Add Student Form
function showAddStudent() {
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = `
        <div class="section-header">
            <h2><i class="fas fa-user-plus"></i> Add New Student</h2>
        </div>
        
        <form id="addStudentForm" onsubmit="addStudent(event)">
            <div class="form-row">
                <div class="form-group">
                    <label>Roll Number *</label>
                    <input type="number" name="rollno" required>
                </div>
                <div class="form-group">
                    <label>Name *</label>
                    <input type="text" name="name" required>
                </div>
            </div>
            
            <div class="form-row">
                <div class="form-group">
                    <label>Father's Name *</label>
                    <input type="text" name="father" required>
                </div>
                <div class="form-group">
                    <label>Password *</label>
                    <input type="password" name="password" required>
                </div>
            </div>
            
            <h3 style="margin: 2rem 0 1rem 0;">Marks (0-100)</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>DSP *</label>
                    <input type="number" name="dsp" min="0" max="100" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>IOT *</label>
                    <input type="number" name="iot" min="0" max="100" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Android *</label>
                    <input type="number" name="android" min="0" max="100" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Compiler *</label>
                    <input type="number" name="compiler" min="0" max="100" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Minor *</label>
                    <input type="number" name="minor" min="0" max="100" step="0.01" required>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-plus"></i> Add Student
            </button>
        </form>
    `;
}

// Add student handler
async function addStudent(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`${API_BASE}/students`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('Student added successfully!', 'success');
            event.target.reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('Error adding student', 'error');
    }
}

// View Records
async function showViewRecords() {
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = `
        <div class="section-header">
            <h2><i class="fas fa-list"></i> Student Records</h2>
            <button class="btn btn-primary" onclick="loadFullDetails()">
                <i class="fas fa-sync"></i> Refresh
            </button>
        </div>
        <div id="tableContainer"></div>
    `;
    
    loadFullDetails();
}

async function loadFullDetails() {
    try {
        const response = await fetch(`${API_BASE}/full-details`);
        const result = await response.json();
        
        const tableContainer = document.getElementById('tableContainer');
        
        if (result.success && result.data.length > 0) {
            let tableHTML = `
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Roll No</th>
                                <th>Name</th>
                                <th>Father's Name</th>
                                <th>DSP</th>
                                <th>IOT</th>
                                <th>Android</th>
                                <th>Compiler</th>
                                <th>Minor</th>
                                <th>Total</th>
                                <th>%</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            result.data.forEach(student => {
                const total = student.dsp + student.iot + student.android + student.compiler + student.minor;
                const percentage = ((total / 500) * 100).toFixed(2);
                
                tableHTML += `
                    <tr>
                        <td>${student.rollno}</td>
                        <td>${student.name}</td>
                        <td>${student.father}</td>
                        <td>${student.dsp}</td>
                        <td>${student.iot}</td>
                        <td>${student.android}</td>
                        <td>${student.compiler}</td>
                        <td>${student.minor}</td>
                        <td><strong>${total.toFixed(1)}</strong></td>
                        <td><strong>${percentage}%</strong></td>
                    </tr>
                `;
            });
            
            tableHTML += `</tbody></table></div>`;
            tableContainer.innerHTML = tableHTML;
        } else {
            tableContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <h3>No Records Found</h3>
                    <p>Add some students to see them here</p>
                </div>
            `;
        }
    } catch (error) {
        showToast('Error loading records', 'error');
    }
}

// Search Student
function showSearchStudent() {
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = `
        <div class="section-header">
            <h2><i class="fas fa-search"></i> Search Student</h2>
        </div>
        
        <form id="searchForm" onsubmit="searchStudent(event)">
            <div class="form-row">
                <div class="form-group">
                    <label>Roll Number *</label>
                    <input type="number" name="rollno" required>
                </div>
                <div class="form-group">
                    <label>Name *</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Password *</label>
                    <input type="password" name="password" required>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-search"></i> Search
            </button>
        </form>
        
        <div id="searchResults"></div>
    `;
}

async function searchStudent(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        // Verify credentials first
        const verifyResponse = await fetch(`${API_BASE}/students/verify`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (!verifyResponse.ok) {
            showToast('Invalid credentials', 'error');
            return;
        }
        
        // Get student details
        const response = await fetch(`${API_BASE}/students/${data.rollno}`);
        const result = await response.json();
        
        if (result.success) {
            const student = result.student;
            const marks = result.marks;
            const total = marks.dsp + marks.iot + marks.android + marks.compiler + marks.minor;
            const percentage = ((total / 500) * 100).toFixed(2);
            
            document.getElementById('searchResults').innerHTML = `
                <div class="student-detail">
                    <h3 style="margin-bottom: 1rem; color: var(--primary-color);">Student Details</h3>
                    <div class="detail-row">
                        <div class="detail-label">Roll Number:</div>
                        <div class="detail-value">${student.rollno}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Name:</div>
                        <div class="detail-value">${student.name}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Father's Name:</div>
                        <div class="detail-value">${student.father}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">DSP:</div>
                        <div class="detail-value">${marks.dsp}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">IOT:</div>
                        <div class="detail-value">${marks.iot}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Android:</div>
                        <div class="detail-value">${marks.android}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Compiler:</div>
                        <div class="detail-value">${marks.compiler}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">Minor:</div>
                        <div class="detail-value">${marks.minor}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label"><strong>Total:</strong></div>
                        <div class="detail-value"><strong>${total.toFixed(1)} / 500</strong></div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label"><strong>Percentage:</strong></div>
                        <div class="detail-value"><strong>${percentage}%</strong></div>
                    </div>
                </div>
            `;
        } else {
            showToast('Student not found', 'error');
        }
    } catch (error) {
        showToast('Error searching student', 'error');
    }
}

// Update Student
function showUpdateStudent() {
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = `
        <div class="section-header">
            <h2><i class="fas fa-edit"></i> Update Student</h2>
        </div>
        
        <p style="margin-bottom: 1rem; color: #7f8c8d;">First, verify student credentials to update records.</p>
        
        <form id="verifyForm" onsubmit="verifyForUpdate(event)">
            <div class="form-row">
                <div class="form-group">
                    <label>Roll Number *</label>
                    <input type="number" name="rollno" required>
                </div>
                <div class="form-group">
                    <label>Name *</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Password *</label>
                    <input type="password" name="password" required>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary">
                <i class="fas fa-check"></i> Verify & Update
            </button>
        </form>
        
        <div id="updateForm"></div>
    `;
}

async function verifyForUpdate(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const verifyResponse = await fetch(`${API_BASE}/students/verify`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (!verifyResponse.ok) {
            showToast('Invalid credentials', 'error');
            return;
        }
        
        const response = await fetch(`${API_BASE}/students/${data.rollno}`);
        const result = await response.json();
        
        if (result.success) {
            const student = result.student;
            const marks = result.marks;
            
            document.getElementById('updateForm').innerHTML = `
                <hr style="margin: 2rem 0;">
                <h3 style="margin-bottom: 1rem;">Update Information</h3>
                <form onsubmit="updateStudent(event, ${student.rollno})">
                    <div class="form-row">
                        <div class="form-group">
                            <label>New Name</label>
                            <input type="text" name="new_name" value="${student.name}">
                        </div>
                        <div class="form-group">
                            <label>New Father's Name</label>
                            <input type="text" name="new_father" value="${student.father}">
                        </div>
                        <div class="form-group">
                            <label>New Password</label>
                            <input type="password" name="new_password" placeholder="Leave blank to keep current">
                        </div>
                    </div>
                    
                    <h4 style="margin: 1.5rem 0 1rem 0;">Update Marks</h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>DSP</label>
                            <input type="number" name="dsp" value="${marks.dsp}" min="0" max="100" step="0.01">
                        </div>
                        <div class="form-group">
                            <label>IOT</label>
                            <input type="number" name="iot" value="${marks.iot}" min="0" max="100" step="0.01">
                        </div>
                        <div class="form-group">
                            <label>Android</label>
                            <input type="number" name="android" value="${marks.android}" min="0" max="100" step="0.01">
                        </div>
                        <div class="form-group">
                            <label>Compiler</label>
                            <input type="number" name="compiler" value="${marks.compiler}" min="0" max="100" step="0.01">
                        </div>
                        <div class="form-group">
                            <label>Minor</label>
                            <input type="number" name="minor" value="${marks.minor}" min="0" max="100" step="0.01">
                        </div>
                    </div>
                    
                    <input type="hidden" name="name" value="${student.name}">
                    <input type="hidden" name="password" value="${data.password}">
                    
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-save"></i> Save Changes
                    </button>
                </form>
            `;
        }
    } catch (error) {
        showToast('Error verifying student', 'error');
    }
}

async function updateStudent(event, rollno) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`${API_BASE}/students/${rollno}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('Student updated successfully!', 'success');
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('Error updating student', 'error');
    }
}

// Delete Student
function showDeleteStudent() {
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = `
        <div class="section-header">
            <h2><i class="fas fa-trash"></i> Delete Student</h2>
        </div>
        
        <div style="background: #ffe6e6; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; color: var(--danger-color);">
            <i class="fas fa-exclamation-triangle"></i> <strong>Warning:</strong> This action cannot be undone!
        </div>
        
        <form id="deleteForm" onsubmit="deleteStudent(event)">
            <div class="form-row">
                <div class="form-group">
                    <label>Roll Number *</label>
                    <input type="number" name="rollno" required>
                </div>
                <div class="form-group">
                    <label>Name *</label>
                    <input type="text" name="name" required>
                </div>
                <div class="form-group">
                    <label>Password *</label>
                    <input type="password" name="password" required>
                </div>
            </div>
            
            <button type="submit" class="btn btn-danger">
                <i class="fas fa-trash"></i> Delete Student
            </button>
        </form>
    `;
}

async function deleteStudent(event) {
    event.preventDefault();
    
    if (!confirm('Are you sure you want to delete this student? This action cannot be undone!')) {
        return;
    }
    
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`${API_BASE}/students/${data.rollno}`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('Student deleted successfully!', 'success');
            event.target.reset();
        } else {
            showToast(result.message, 'error');
        }
    } catch (error) {
        showToast('Error deleting student', 'error');
    }
}

// Export Options
function showExportOptions() {
    const contentArea = document.getElementById('contentArea');
    contentArea.innerHTML = `
        <div class="section-header">
            <h2><i class="fas fa-download"></i> Export Data</h2>
        </div>
        
        <p style="margin-bottom: 2rem; color: #7f8c8d;">Download student records in your preferred format.</p>
        
        <div class="export-buttons">
            <button class="btn btn-success" onclick="exportToExcel()">
                <i class="fas fa-file-excel"></i> Export to Excel
            </button>
            <button class="btn btn-danger" onclick="exportToPDF()">
                <i class="fas fa-file-pdf"></i> Export to PDF
            </button>
        </div>
    `;
}

async function exportToExcel() {
    try {
        showToast('Generating Excel file...', 'info');
        window.location.href = `${API_BASE}/export/excel`;
        setTimeout(() => {
            showToast('Excel file downloaded!', 'success');
        }, 1000);
    } catch (error) {
        showToast('Error exporting to Excel', 'error');
    }
}

async function exportToPDF() {
    try {
        showToast('Generating PDF file...', 'info');
        window.location.href = `${API_BASE}/export/pdf`;
        setTimeout(() => {
            showToast('PDF file downloaded!', 'success');
        }, 1000);
    } catch (error) {
        showToast('Error exporting to PDF', 'error');
    }
}

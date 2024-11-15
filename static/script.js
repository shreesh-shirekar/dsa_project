const signupForm = document.getElementById('signup-form');
const loginForm = document.getElementById('login-form');
const toggleLink = document.getElementById('toggle-link');
const formTitle = document.getElementById('form-title');
const emailSubmitButton = document.getElementById('email-submit');
const auidInput = document.getElementById('login-auid');
const loginSubmitButton = document.getElementById('login-submit');

// Toggle between Login and Signup forms
toggleLink.addEventListener('click', () => {
    if (signupForm.style.display === 'none') {
        signupForm.style.display = 'block';
        loginForm.style.display = 'none';
        formTitle.textContent = 'Sign Up';
        toggleLink.textContent = 'Already have an account? Login';
    } else {
        signupForm.style.display = 'none';
        loginForm.style.display = 'block';
        formTitle.textContent = 'Login';
        toggleLink.textContent = "Don't have an account? Sign Up";
    }
});

// Handle Educator Login - Step 1: Email Check
emailSubmitButton.addEventListener('click', () => {
    const email = document.getElementById('login-email').value;

    fetch('http://127.0.0.1:5000/check-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            // Reveal AU ID input and Login button
            auidInput.style.display = 'block';
            loginSubmitButton.style.display = 'block';
            emailSubmitButton.style.display = 'none';
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Handle Educator Login - Step 2: AU ID Check
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const auid = document.getElementById('login-auid').value;

    fetch('http://127.0.0.1:5000/check-teacher-id', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, teacherId: auid })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            window.location.href = 'teachers_dashboard.html';
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Handle Educator Signup Submission
signupForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('signup-email').value;
    const teacherId = document.getElementById('signup-teacher-id').value;
    const firstName = document.getElementById('signup-first-name').value;
    const lastName = document.getElementById('signup-last-name').value;

    fetch('http://127.0.0.1:5000/signup-teacher', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, teacherId, firstName, lastName })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        signupForm.reset();
        toggleLink.click();  // Switch to login form after signup
    })
    .catch(error => console.error('Error:', error));
});

// Schedule a Class
document.getElementById('schedule-class-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const subject = document.getElementById('subject').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const teacher = document.getElementById('teacher').value;

    fetch('/schedule-class', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject, date, time, teacher })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

// Register a Student
document.getElementById('register-student-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const student_name = document.getElementById('student-name').value;
    const section_number = document.getElementById('section-number').value;
    const student_email = document.getElementById('student-email').value;

    fetch('/register-student', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ student_name, section_number, student_email })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

// View Scheduled Classes
document.getElementById('view-classes-btn').addEventListener('click', function() {
    fetch('/view-classes')
    .then(response => response.json())
    .then(data => {
        const classListDiv = document.getElementById('class-list');
        classListDiv.innerHTML = ''; // Clear previous content

        if (data.classes.length === 0) {
            classListDiv.innerHTML = '<p>No classes scheduled.</p>';
        } else {
            data.classes.forEach(cls => {
                const classItem = document.createElement('p');
                classItem.textContent = `${cls.index}: ${cls.subject} - ${cls.date_time} (Teacher: ${cls.teacher})`;
                classListDiv.appendChild(classItem);
            });
        }
    })
    .catch(error => console.error('Error:', error));
});

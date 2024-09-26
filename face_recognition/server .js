require('dotenv').config();
const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const path = require('path');
const multer = require('multer');
const fs = require('fs');
const { spawn } = require('child_process');

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files from the 'public' and 'uploads' directory
app.use(express.static(path.join(__dirname, 'public')));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// Create a connection to the database
const db = mysql.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});

// Connect to MySQL
db.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
        return;
    }
    console.log('Connected to MySQL database.');
});

// Configure multer for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const dir = './uploads/';
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        cb(null, dir);
    },
    filename: (req, file, cb) => {
        cb(null, `${Date.now()}-${file.originalname}`);
    }
});
const upload = multer({ storage: storage });

// Endpoint for user registration
app.post('/register', (req, res) => {
    const { User_name, PASS_WORD } = req.body;

    const checkUserSql = 'SELECT * FROM users WHERE user_name = ?';
    db.query(checkUserSql, [User_name], (err, results) => {
        if (err) {
            console.error('Error checking user:', err);
            res.status(500).send('Error registering user.');
            return;
        }

        if (results.length > 0) {
            res.send('User already exists.');
        } else {
            const insertUserSql = 'INSERT INTO users (user_name, PASS_WORD) VALUES (?, ?)';
            db.query(insertUserSql, [User_name, PASS_WORD], (err, result) => {
                if (err) {
                    console.error('Error inserting user:', err);
                    res.status(500).send('Error registering user.');
                } else {
                    res.send('User registered successfully!');
                }
            });
        }
    });
});

// Endpoint for user login
app.post('/login', (req, res) => {
    const { User_name, PASS_WORD } = req.body;

    const sql = 'SELECT PASS_WORD FROM users WHERE user_name = ?';
    db.query(sql, [User_name], (err, results) => {
        if (err) {
            console.error('Database error:', err);
            res.status(500).send('Error logging in.');
        } else if (results.length > 0) {
            const storedPassword = results[0].PASS_WORD;
            if (PASS_WORD === storedPassword) {
                res.json({ success: true });
            } else {
                res.json({ success: false, message: 'Invalid credentials.' });
            }
        } else {
            res.json({ success: false, message: 'User not found.' });
        }
    });
});

// Endpoint to fetch student details based on branch and section
app.get('/students', (req, res) => {
    const { branch, section } = req.query;
    const sql = 'SELECT * FROM student WHERE Branch = ? AND Section = ?';
    db.query(sql, [branch, section], (err, results) => {
        if (err) {
            console.error('Database error:', err);
            res.status(500).send('Error fetching student details.');
        } else {
            res.json(results);
        }
    });
});

// Endpoint for registering a student with an image
app.post('/register-student', upload.single('image'), (req, res) => {
    const { name, branch, usn, section } = req.body;
    const imagePath = req.file ? req.file.path : null;

    const insertStudentSql = 'INSERT INTO student (Name, Branch, USN, Section, ImagePath) VALUES (?, ?, ?, ?, ?)';
    db.query(insertStudentSql, [name, branch, usn, section, imagePath], (err, result) => {
        if (err) {
            console.error('Error inserting student:', err);
            res.status(500).send({ success: false, message: 'Error registering student.' });
        } else {
            res.send({ success: true, message: 'Student registered successfully!' });
        }
    });
});

// Endpoint to start the face recognition script
app.get('/take-attendance', (req, res) => {
    const pythonProcess = spawn('base/opt/anaconda3/bin/python', [path.join(__dirname, 'face_recognition', 'real_time.py')]);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });

    res.send('Face recognition script started');
});

app.get('/take-attendance.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'take-attendance.html'));
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
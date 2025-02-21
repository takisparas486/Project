<?php
$user = $_GET['user'] ?? '';
$password = $_GET['password'] ?? '';

if ($user == "admin" && $password == "password") {
    echo "Login successful";
} else {
    echo "Invalid credentials";
}
?>

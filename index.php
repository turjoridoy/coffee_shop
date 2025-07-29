<?php
// PHP wrapper to execute Python Django application
// This works around Hostinger's Python execution limitations

// Set headers for JSON response
header('Content-Type: application/json');

// Check if Python is available
$python_output = shell_exec('python3 --version 2>&1');
$python_available = strpos($python_output, 'Python') !== false;

if (!$python_available) {
    echo json_encode([
        'status' => 'error',
        'message' => 'Python is not available on this server',
        'python_output' => $python_output
    ]);
    exit;
}

// Try to run Django application
$django_output = shell_exec('cd ' . __DIR__ . ' && python3 manage.py runserver 0.0.0.0:8000 2>&1 &');

echo json_encode([
    'status' => 'success',
    'message' => 'Django application started',
    'python_version' => $python_output,
    'django_output' => $django_output
]);
?>
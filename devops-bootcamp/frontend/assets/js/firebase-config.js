// Firebase Configuration and Authentication

// Initialize Firebase with configuration
const firebaseConfig = {
    // These values should be replaced with actual Firebase configuration
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Get Auth instance
const auth = firebase.auth();
const provider = new firebase.auth.GoogleAuthProvider();

// Authentication state observer
auth.onAuthStateChanged((user) => {
    if (user) {
        // User is signed in
        handleSignedInUser(user);
    } else {
        // User is signed out
        handleSignedOutUser();
    }
});

// Handle signed-in user
function handleSignedInUser(user) {
    // Get the user's ID token
    user.getIdToken().then(token => {
        // Store the token
        localStorage.setItem('userToken', token);
        
        // Update UI for signed-in state
        document.getElementById('loginBtn').style.display = 'none';
        
        // Check if user is admin
        checkAdminStatus(user.uid).then(isAdmin => {
            if (isAdmin) {
                window.location.href = '/pages/admin_dashboard.html';
            } else {
                window.location.href = '/pages/dashboard.html';
            }
        });
    });
}

// Handle signed-out user
function handleSignedOutUser() {
    // Clear stored data
    localStorage.removeItem('userToken');
    
    // Update UI for signed-out state
    document.getElementById('loginBtn').style.display = 'block';
    
    // Redirect to home if on protected page
    if (window.location.pathname !== '/' && window.location.pathname !== '/index.html') {
        window.location.href = '/';
    }
}

// Sign in with Google
function signInWithGoogle() {
    auth.signInWithPopup(provider)
        .then((result) => {
            // Handle successful sign-in
            const user = result.user;
            console.log('Successfully signed in:', user.email);
        })
        .catch((error) => {
            // Handle errors
            console.error('Sign-in error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Authentication Error',
                text: error.message,
                background: '#1F2937',
                color: '#fff'
            });
        });
}

// Sign out
function signOut() {
    auth.signOut()
        .then(() => {
            console.log('Successfully signed out');
            window.location.href = '/';
        })
        .catch((error) => {
            console.error('Sign-out error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Failed to sign out. Please try again.',
                background: '#1F2937',
                color: '#fff'
            });
        });
}

// Check if user is admin
async function checkAdminStatus(uid) {
    try {
        const response = await fetch('/api/admin/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('userToken')}`
            },
            body: JSON.stringify({ uid })
        });
        
        if (!response.ok) {
            return false;
        }
        
        const data = await response.json();
        return data.isAdmin;
    } catch (error) {
        console.error('Error checking admin status:', error);
        return false;
    }
}

// API request helper with authentication
async function authenticatedFetch(url, options = {}) {
    const token = localStorage.getItem('userToken');
    if (!token) {
        throw new Error('No authentication token found');
    }

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    };

    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };

    try {
        const response = await fetch(url, mergedOptions);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Login button click handler
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', signInWithGoogle);
    }

    // Logout button click handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', signOut);
    }
});

// Export functions for use in other scripts
window.auth = {
    signInWithGoogle,
    signOut,
    checkAdminStatus,
    authenticatedFetch
};

// Main JavaScript for DevOps Bootcamp

// Course data structure
const courseModules = [
    {
        id: 1,
        title: "Server Virtualization with Proxmox",
        description: "Master server virtualization using Proxmox VE",
        chapters: [
            { title: "VM Creation and Management", duration: "2 hours" },
            { title: "Template Management", duration: "1.5 hours" },
            { title: "High Availability Configuration", duration: "2.5 hours" }
        ]
    },
    {
        id: 2,
        title: "Networking Fundamentals",
        description: "Learn essential networking concepts and implementations",
        chapters: [
            { title: "Basic Network Concepts", duration: "2 hours" },
            { title: "DNS with Cloudflare and BIND9", duration: "2.5 hours" },
            { title: "MikroTik Routing", duration: "2 hours" },
            { title: "Subnetting Practice", duration: "1.5 hours" }
        ]
    },
    // Add more course modules here
];

// DOM Elements
const curriculumSection = document.querySelector('#curriculum .space-y-10');

// Helper Functions
function formatDuration(duration) {
    return duration;
}

function createCourseCard(course) {
    return `
        <div class="course-card p-6 fade-in">
            <div class="flex items-center justify-between">
                <h3 class="text-xl font-bold text-white">${course.title}</h3>
                <span class="badge">${course.chapters.length} Chapters</span>
            </div>
            <p class="mt-2 text-gray-300">${course.description}</p>
            <div class="mt-4">
                <h4 class="text-sm font-semibold text-primary mb-2">Chapters:</h4>
                <ul class="space-y-2">
                    ${course.chapters.map(chapter => `
                        <li class="flex items-center justify-between text-sm">
                            <span class="text-gray-300">${chapter.title}</span>
                            <span class="text-gray-400">${formatDuration(chapter.duration)}</span>
                        </li>
                    `).join('')}
                </ul>
            </div>
            <div class="mt-6 flex justify-end">
                <button onclick="enrollCourse(${course.id})" class="btn-primary">
                    Enroll Now
                </button>
            </div>
        </div>
    `;
}

// UI Functions
function loadCourseContent() {
    if (curriculumSection) {
        curriculumSection.innerHTML = courseModules.map(course => createCourseCard(course)).join('');
    }
}

function showLoading() {
    return Swal.fire({
        title: 'Loading...',
        html: '<div class="spinner"></div>',
        showConfirmButton: false,
        allowOutsideClick: false,
        background: '#1F2937',
        color: '#fff'
    });
}

function showSuccess(message) {
    return Swal.fire({
        icon: 'success',
        title: 'Success',
        text: message,
        background: '#1F2937',
        color: '#fff'
    });
}

function showError(message) {
    return Swal.fire({
        icon: 'error',
        title: 'Error',
        text: message,
        background: '#1F2937',
        color: '#fff'
    });
}

// Course Enrollment
async function enrollCourse(courseId) {
    // Check if user is authenticated
    const token = localStorage.getItem('userToken');
    if (!token) {
        Swal.fire({
            title: 'Authentication Required',
            text: 'Please sign in to enroll in this course',
            icon: 'info',
            showCancelButton: true,
            confirmButtonText: 'Sign In',
            background: '#1F2937',
            color: '#fff'
        }).then((result) => {
            if (result.isConfirmed) {
                window.auth.signInWithGoogle();
            }
        });
        return;
    }

    try {
        const loading = showLoading();

        // Call enrollment API
        const response = await window.auth.authenticatedFetch('/api/user/purchase', {
            method: 'POST',
            body: JSON.stringify({ course_id: courseId })
        });

        loading.close();

        if (response.status === 'pending') {
            // Show payment instructions
            Swal.fire({
                title: 'Complete Payment',
                html: `
                    <div class="text-left">
                        <p class="mb-4">Please complete the payment to access the course:</p>
                        <p class="mb-2">Amount: Rp 200,000</p>
                        <p class="mb-2">Transaction ID: ${response.transaction_id}</p>
                        <p>Payment Method: ${response.payment_method}</p>
                    </div>
                `,
                icon: 'info',
                confirmButtonText: 'OK',
                background: '#1F2937',
                color: '#fff'
            });
        }
    } catch (error) {
        showError('Failed to process enrollment. Please try again.');
    }
}

// Video Submission
async function submitVideo(courseId, chapterId, videoUrl) {
    try {
        const loading = showLoading();

        const response = await window.auth.authenticatedFetch('/api/user/submit', {
            method: 'POST',
            body: JSON.stringify({
                course_id: courseId,
                chapter_id: chapterId,
                video_url: videoUrl
            })
        });

        loading.close();

        if (response.submission) {
            showSuccess('Video submitted successfully! Waiting for review.');
        }
    } catch (error) {
        showError('Failed to submit video. Please try again.');
    }
}

// Progress Tracking
async function updateProgress(courseId, chapterId) {
    try {
        const response = await window.auth.authenticatedFetch('/api/user/progress', {
            method: 'POST',
            body: JSON.stringify({
                course_id: courseId,
                chapter_id: chapterId
            })
        });

        // Update UI with new progress
        if (response.progress) {
            updateProgressUI(response.progress);
        }
    } catch (error) {
        console.error('Failed to update progress:', error);
    }
}

function updateProgressUI(progress) {
    const progressBar = document.querySelector('.progress-bar-fill');
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load course content
    loadCourseContent();

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Initialize tooltips
    document.querySelectorAll('.tooltip').forEach(tooltip => {
        // Add tooltip functionality if needed
    });
});

// Handle form submissions
const videoSubmissionForm = document.getElementById('videoSubmissionForm');
if (videoSubmissionForm) {
    videoSubmissionForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const courseId = e.target.courseId.value;
        const chapterId = e.target.chapterId.value;
        const videoUrl = e.target.videoUrl.value;

        await submitVideo(courseId, chapterId, videoUrl);
    });
}

// Export functions for use in other scripts
window.courseActions = {
    enrollCourse,
    submitVideo,
    updateProgress
};

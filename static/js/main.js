// ============================================================
// Main JavaScript - Nail Disease Diagnosis System
// ============================================================

document.addEventListener('DOMContentLoaded', function () {

    // --- Image Preview Functionality ---
    const imageInput = document.getElementById('imageInput');
    const uploadArea = document.getElementById('uploadArea');
    const previewContainer = document.getElementById('previewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const removeBtn = document.getElementById('removeBtn');
    const predictBtn = document.getElementById('predictBtn');

    if (imageInput) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    imagePreview.src = e.target.result;
                    previewContainer.style.display = 'block';
                    uploadArea.style.display = 'none';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    if (removeBtn) {
        removeBtn.addEventListener('click', function () {
            imageInput.value = '';
            previewContainer.style.display = 'none';
            uploadArea.style.display = 'block';
        });
    }

    // --- Drag and Drop ---
    if (uploadArea) {
        uploadArea.addEventListener('dragover', function (e) {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', function (e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', function (e) {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                imageInput.files = files;
                const event = new Event('change');
                imageInput.dispatchEvent(event);
            }
        });
    }

    // --- Form Submission Loading ---
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function () {
            if (predictBtn) {
                predictBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
                predictBtn.disabled = true;
            }
        });
    }

    // --- Smooth Scroll ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // --- Navbar Scroll Effect ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.4)';
            } else {
                navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
            }
        });
    }

    // --- Animate cards on scroll ---
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card, .scenario-card, .disease-info-card, .about-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});
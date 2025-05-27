document.addEventListener('DOMContentLoaded', () => {
    // --- Navbar Toggle for Mobile ---
    const hamburger = document.querySelector(".hamburger");
    const navMenu = document.querySelector(".nav-menu");

    if (hamburger && navMenu) {
        hamburger.addEventListener("click", () => {
            hamburger.classList.toggle("active");
            navMenu.classList.toggle("active");
        });

        document.querySelectorAll(".nav-link").forEach(n => n.addEventListener("click", () => {
            if (hamburger.classList.contains('active')) { // Only close if menu is open
                hamburger.classList.remove("active");
                navMenu.classList.remove("active");
            }
        }));
    }


    // --- Hero Text Typing Animation ---
    const heroTitleElement = document.getElementById('hero-title');
    if (heroTitleElement) {
        const heroTitleText = "Welcome to PrivyNet."; // Your desired title
        let i = 0;
        let isDeleting = false;
        let typingSpeed = 120; // Milliseconds
        let deletingSpeed = 60;
        let delayAfterTyping = 2000; // Wait 2s after typing before potential deletion/re-type

        function typeHeroTitle() {
            const currentText = heroTitleElement.textContent;
            if (!isDeleting && i < heroTitleText.length) {
                heroTitleElement.textContent += heroTitleText.charAt(i);
                i++;
                setTimeout(typeHeroTitle, typingSpeed);
            } else if (isDeleting && heroTitleElement.textContent.length > 0) {
                heroTitleElement.textContent = heroTitleElement.textContent.slice(0, -1);
                setTimeout(typeHeroTitle, deletingSpeed);
            } else if (!isDeleting && i === heroTitleText.length) {
                // Typing finished
                heroTitleElement.style.borderRight = 'none'; // Remove caret
                document.querySelector('.hero-section').classList.add('loaded'); // Trigger subtitle and button animation
                // Optionally: Start deleting after a pause, or just stay
                // setTimeout(() => { isDeleting = true; typeHeroTitle(); }, delayAfterTyping); 
            } else if (isDeleting && heroTitleElement.textContent.length === 0) {
                isDeleting = false;
                i = 0;
                // Optionally: type a new sentence or loop
                setTimeout(typeHeroTitle, typingSpeed);
            }
        }
        // Clear existing text just in case, then start animation
        heroTitleElement.textContent = ''; 
        setTimeout(typeHeroTitle, 500); // Initial delay
    } else {
        // If no hero title, still load other animations
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            heroSection.classList.add('loaded');
        }
    }

    // --- Scroll Animations ---
    const animatedElements = document.querySelectorAll('.animate-on-scroll');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // Optional: Stop observing after animation
                // observer.unobserve(entry.target);
            }
        });
    }, {
        rootMargin: '0px',
        threshold: 0.1 // Trigger when 10% of the element is visible
    });

    animatedElements.forEach(el => {
        observer.observe(el);
    });

    // --- Footer Current Year ---
    const currentYearSpan = document.getElementById('currentYear');
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

});
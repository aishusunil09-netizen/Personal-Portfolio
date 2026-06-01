document.addEventListener("DOMContentLoaded", () => {
    initMobileNav();
    if (document.getElementById("particlesCanvas")) initParticles();
    if (document.getElementById("carouselTrack")) initCarousel();
    if (document.getElementById("portfolioForm")) initFormValidation();
});

/* ── MOBILE NAV MENU TOGGLE ── */
function initMobileNav() {
    const hamburger = document.getElementById("hamburger");
    const navLinks = document.getElementById("navLinks");
    if (hamburger && navLinks) {
        hamburger.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }
}

/* ── BACKGROUND FLOATING MATH PARTICLES ENGINE ── */
function initParticles() {
    const canvas = document.getElementById("particlesCanvas");
    const ctx = canvas.getContext("2d");
    let particles = [];
    
    function resize() {
        canvas.width = canvas.parentElement.offsetWidth;
        canvas.height = canvas.parentElement.offsetHeight;
    }
    window.addEventListener("resize", resize);
    resize();

    for (let i = 0; i < 24; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            r: Math.random() * 4 + 2,
            dx: (Math.random() - 0.5) * 0.3,
            dy: (Math.random() - 0.5) * 0.3,
            alpha: Math.random() * 0.4 + 0.1
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.x += p.dx;
            p.y += p.dy;
            if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(232, 132, 90, ${p.alpha})`;
            ctx.fill();
        });
        requestAnimationFrame(animate);
    }
    animate();
}

/* ── SEQUENTIAL CONTENT CAROUSEL TRACKER ── */
function initCarousel() {
    const track = document.getElementById("carouselTrack");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const titleText = document.getElementById("carouselTitle");
    const subText = document.getElementById("carouselSub");
    const counter = document.getElementById("carouselCounter");
    const dotsContainer = document.getElementById("carouselDots");

    const slidesData = [
        { title: "Morning Light", sub: "Finding peace on the early mountain trails." },
        { title: "Peak Elevation", sub: "The world looks different when you're above the clouds." },
        { title: "Fueling Curiosity", sub: "Perfecting the Chemex ratio on a Sunday afternoon." },
        { title: "Weekend Experiment", sub: "Homemade wild mushroom tagliatelle from scratch." },
        { title: "The Reading Nook", sub: "Current dive: complex systems and emergent behavior." }
    ];

    let currentIdx = 0;

    // Generate indicator tracking elements
    slidesData.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.classList.add("carousel-dot");
        if (i === 0) dot.classList.add("active");
        dot.addEventListener("click", () => gotoSlide(i));
        dotsContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll(".carousel-dot");

    function gotoSlide(index) {
        currentIdx = index;
        track.style.transform = `translateX(-${index * 100}%)`;
        titleText.textContent = slidesData[index].title;
        subText.textContent = slidesData[index].sub;
        counter.textContent = `${index + 1} / ${slidesData.length}`;
        
        dots.forEach((d, i) => {
            d.classList.toggle("active", i === index);
        });
    }

    prevBtn.addEventListener("click", () => {
        let i = currentIdx - 1;
        if (i < 0) i = slidesData.length - 1;
        gotoSlide(i);
    });

    nextBtn.addEventListener("click", () => {
        let i = currentIdx + 1;
        if (i >= slidesData.length) i = 0;
        gotoSlide(i);
    });
}

/* ── EVENT ROUTING REGEX FORM SUBMISSION ── */
function initFormValidation() {
    const form = document.getElementById("portfolioForm");
    const successBlock = document.getElementById("successBlock");

    form.addEventListener("submit", (e) => {
        e.preventDefault();
        let valid = true;

        const name = document.getElementById("formName");
        const email = document.getElementById("formEmail");
        const msg = document.getElementById("formMessage");

        const errName = document.getElementById("errorName");
        const errEmail = document.getElementById("errorEmail");
        const errMsg = document.getElementById("errorMessage");

        // Validate Input Fields
        if (!name.value.trim()) {
            name.classList.add("error");
            errName.classList.add("show");
            valid = false;
        } else {
            name.classList.remove("error");
            errName.classList.remove("show");
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email.value.trim())) {
            email.classList.add("error");
            errEmail.classList.add("show");
            valid = false;
        } else {
            email.classList.remove("error");
            errEmail.classList.remove("show");
        }

        if (!msg.value.trim()) {
            msg.classList.add("error");
            errMsg.classList.add("show");
            valid = false;
        } else {
            msg.classList.remove("error");
            errMsg.classList.remove("show");
        }

        // Processing Valid Input Signals
        if (valid) {
            form.style.display = "none";
            successBlock.classList.add("show");
            console.log("Contact submission logs processed successfully:", {
                sender: name.value,
                contact: email.value,
                payload: msg.value
            });
        }
    });
}
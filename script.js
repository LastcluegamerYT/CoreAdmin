// Preloader
    window.addEventListener('load', () => {
        document.getElementById('preloader').style.display = 'none';
    });

    // Navigation Highlight
    // Navigation Toggle for Mobile
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('show');
    });

    // Close menu when a link is clicked (optional)
    document.querySelectorAll('#nav-links li a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                navLinks.classList.remove('show');
            }
        });
    });
    document.addEventListener("DOMContentLoaded", () => {
        const unleashButton = document.getElementById("unleashButton");
        const fullscreenBox = document.getElementById("fullscreenBox");
        const closeButton = document.getElementById("closeButton");
        const iframeContent = document.getElementById("iframeContent");
    
        // Function to open the full-screen iframe
        const openFullScreenBox = () => {
            fullscreenBox.style.display = "flex";
            if (iframeContent.src === "about:blank") {
                iframeContent.src = "https://prashantytt34.pythonanywhere.com/"; // Replace with your desired link
            }
        };
    
        // Function to close the full-screen iframe
        const closeFullScreenBox = () => {
            fullscreenBox.style.display = "none";
        };
    
        // Event listener for the "Unleash Your Beat" button
        unleashButton.addEventListener("click", () => {
            openFullScreenBox();
        });
    
        // Event listener for the "X" button
        closeButton.addEventListener("click", () => {
            closeFullScreenBox();
        });
    
        // Automatically load iframe when the page loads
        window.addEventListener("load", () => {
            iframeContent.src = "https://prashantytt34.pythonanywhere.com/"; // Preload iframe content
        });
    
        // Smooth iframe functionality
        iframeContent.onload = () => {
            iframeContent.style.opacity = 1; // Ensure smooth display
        };
    });
    
    
    // Form Submission Alert
        // Form Submission Handling
        document.getElementById("contact-form").addEventListener("submit", async function (event) {
            event.preventDefault(); // Prevent default form submission behavior
    
            const formData = new FormData(this);
            const data = {
                name: formData.get("name"),
                email: formData.get("email"),
                message: formData.get("message")
            };
    
            try {
                const response = await fetch("https://prashantytt34.pythonanywhere.com/save-data", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });
    
                if (response.ok) {
                    alert("Your message has been sent successfully!");
                    this.reset(); // Clear the form
                } else {
                    alert("Failed to send your message. Please try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred while sending your message. Please check your connection.");
            }
        });


    // Smooth Scroll
    document.querySelectorAll('nav ul li a').forEach(anchor => {
        anchor.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            document.getElementById(targetId).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    });

        // Random Background Music with Audio Control and Switch 
        const audioElement = document.getElementById('background-music');
        const volumeControl = document.getElementById('volume-control');
        const switchButton = document.getElementById('audio-switch');
    
        let songs = [];
        let playedSongs = [];
        let isPlaying = false;
    
        // Fetch songs dynamically from the "song" folder
        const fetchSongs = async () => {
            // Simulate fetching song list (replace with server-side API for dynamic fetching in production)
            songs = [
                'song/song1.mp3',
                'song/song2.mp3'
            ];
            // Automatically play a random song after 3 seconds
            setTimeout(() => {
                playRandomSong();
            }, 3000);
        };
    
        // Play a random song
        const playRandomSong = () => {
            if (songs.length === 0) return;
    
            // Reset playedSongs if all songs have been played
            if (playedSongs.length === songs.length) {
                playedSongs = [];
            }
    
            // Filter songs to find unplayed ones
            const unplayedSongs = songs.filter(song => !playedSongs.includes(song));
    
            // Select a random song from the unplayed list
            const randomIndex = Math.floor(Math.random() * unplayedSongs.length);
            const randomSong = unplayedSongs[randomIndex];
    
            // Add the selected song to playedSongs
            playedSongs.push(randomSong);
    
            // Play the selected song
            audioElement.src = randomSong;
            audioElement.play()
                .then(() => {
                    isPlaying = true;
                })
                .catch(err => {
                    console.error("Autoplay error:", err);
                });
        };
    
        // Play next random song when current ends
        audioElement.addEventListener('ended', () => {
            playRandomSong();
        });
    
        // Audio Switch Button: Skip to the next random song
        switchButton.addEventListener('click', () => {
            playRandomSong();
        });
    
        // Volume Control
        volumeControl.addEventListener('input', (event) => {
            audioElement.volume = event.target.value / 100;
        });
    
        // Initialize the system
        window.addEventListener('load', () => {
            fetchSongs();
        });
    
        // Handle autoplay restrictions (optional)
        document.body.addEventListener('click', () => {
            if (!isPlaying) {
                audioElement.play()
                    .then(() => {
                        isPlaying = true;
                    })
                    .catch(err => {
                        console.error("Autoplay error on interaction:", err);
                    });
            }
        });
     // Simulate a click on the screen
     window.addEventListener('load', () => {
        // Wait for 10 seconds after the page is fully loaded
        setTimeout(() => {
            // Create a simulated click event
            const simulatedClick = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window,
            });
    
            // Dispatch the click event on the body
            const targetElement = document.body;
            const clickSuccess = targetElement.dispatchEvent(simulatedClick);
    
            if (clickSuccess) {
                console.log('Simulated click on the screen.');
            } else {
                console.error('Simulated click failed.');
            }
        }, 10000); // 10,000 milliseconds = 10 seconds
    });
    

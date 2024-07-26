document.addEventListener('DOMContentLoaded', () => {
    const videos = document.querySelectorAll('video');
    const options = {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    };

    const handleIntersection = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.play();
            } else {
                entry.target.pause();
            }
        });
    };

    const observer = new IntersectionObserver(handleIntersection, options);

    videos.forEach(video => {
        observer.observe(video);
    });

    const prompt = document.getElementById('scroll-prompt');
    const dismissButton = document.getElementById('dismiss-prompt');

    if (!localStorage.getItem('promptDismissed')) {
        prompt.style.display = 'block';
    }

    dismissButton.addEventListener('click', () => {
        prompt.style.display = 'none';
        localStorage.setItem('promptDismissed', 'true');
    });
});

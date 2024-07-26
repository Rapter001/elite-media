function validateFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'video/mp4'];
    const maxSize = 20 * 1024 * 1024;
    if (file && allowedTypes.includes(file.type)) {
        if (file.type === 'video/mp4' && file.size > maxSize) {
            alert('Please upload a video file smaller than 20MB.');
            return false;
        }
        return true;
    } else {
        alert('Please upload a valid file format (PNG, JPEG, JPG, GIF, MP4).');
        return false;
    }
}
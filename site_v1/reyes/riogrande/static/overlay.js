
// JavaScript to toggle the overlay
document.getElementById("infoBtn").onclick = function() {
    document.getElementById("infoOverlay").style.display = "block";
};
document.getElementById("infoOverlay").onclick = function(event) {
    // Close the overlay if the close button is clicked
    if (event.target.classList.contains('closeBtn') || event.target.parentNode.classList.contains('closeBtn')) {
        document.getElementById("infoOverlay").style.display = "none";
    }
};
document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = "/"; // Adjust if needed for subdirectories

    // Helper function to fetch and populate a list
    async function fetchAndPopulate(endpoint, elementId) {
        const response = await fetch(API_BASE + endpoint);
        const data = await response.json();
        const list = document.getElementById(elementId);

        if (data.frames) {
            data.frames.forEach(item => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `<a href="${item}">${item}</a>`;
                list.appendChild(listItem);
            });
        }
    }

    // Populate timelapse videos
    fetchAndPopulate("timelapse", "timelapse-days");

    // Populate GIFs
    fetchAndPopulate("gif", "gif-days");

    // Populate hourly snapshots
    fetchAndPopulate("frames", "frames");
});

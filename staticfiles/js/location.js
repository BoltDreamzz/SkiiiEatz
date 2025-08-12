document.addEventListener("DOMContentLoaded", function () {
    const locationDiv = document.getElementById("locationDiv");
    const inputAddress = document.getElementById("inputAddress");
    const inputCity = document.getElementById("inputCity");
    const inputState = document.getElementById("inputState");

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;

                try {
                    const response = await fetch(
                        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
                    );
                    const data = await response.json();

                    const address = data.display_name || "";
                    const city = data.address.city || data.address.town || data.address.village || "";
                    const state = data.address.state || "";

                    inputAddress.value = address;
                    inputCity.value = city;
                    inputState.value = state;

                    locationDiv.textContent = `${city}, ${state}`;
                } catch (error) {
                    locationDiv.textContent = "Unable to get location.";
                    console.error("Error:", error);
                }
            },
            (error) => {
                locationDiv.textContent = "Location access denied.";
            }
        );
    } else {
        locationDiv.textContent = "Geolocation not supported.";
    }
});
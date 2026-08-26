const API_URL = "http://localhost:8000/predict";

const fileInput = document.getElementById("file-input");
const chooseButton = document.getElementById("choose-button");

const previewContainer =
    document.getElementById("preview-container");

const previewImage =
    document.getElementById("preview-image");

const fileName =
    document.getElementById("file-name");

const detectButton =
    document.getElementById("detect-button");

const loading =
    document.getElementById("loading");

const resultSection =
    document.getElementById("result-section");

const results =
    document.getElementById("results");

const errorMessage =
    document.getElementById("error-message");


let selectedFile = null;


// Choose image
chooseButton.addEventListener("click", () => {
    fileInput.click();
});


// When image is selected
fileInput.addEventListener("change", () => {

    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    selectedFile = file;

    fileName.textContent = file.name;

    const reader = new FileReader();

    reader.onload = function(event) {

        previewImage.src = event.target.result;

        document
            .getElementById("drop-area")
            .classList.add("hidden");

        previewContainer
            .classList.remove("hidden");

    };

    reader.readAsDataURL(file);

});


// Detect currency
detectButton.addEventListener("click", async () => {

    if (!selectedFile) {
        showError("Please select an image first.");
        return;
    }

    hideError();

    resultSection.classList.add("hidden");

    loading.classList.remove("hidden");

    const formData = new FormData();

    formData.append("file", selectedFile);


    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Prediction failed."
            );

        }


        displayResults(data);


    } catch (error) {

        console.error(error);

        showError(
            "Could not connect to the currency detection API. " +
            error.message
        );

    } finally {

        loading.classList.add("hidden");

    }

});


// Display results
function displayResults(data) {

    results.innerHTML = "";


    if (!data.detections ||
        data.detections.length === 0) {

        results.innerHTML = `
            <div class="detection">
                <div class="denomination">
                    No currency detected
                </div>

                <div class="confidence">
                    Try another image.
                </div>
            </div>
        `;

    } else {

        data.detections.forEach(
            (detection) => {

                const confidence =
                    (detection.confidence * 100)
                    .toFixed(2);


                const detectionElement =
                    document.createElement("div");

                detectionElement.className =
                    "detection";


                detectionElement.innerHTML = `

                    <div class="denomination">
                        💵 ${detection.denomination} Taka
                    </div>

                    <div class="confidence">
                        Confidence: ${confidence}%
                    </div>

                `;


                results.appendChild(
                    detectionElement
                );

            }
        );

    }


    resultSection.classList.remove("hidden");

}


// Error
function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

}


function hideError() {

    errorMessage.classList.add("hidden");

}
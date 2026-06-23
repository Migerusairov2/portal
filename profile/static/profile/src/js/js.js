const btn = document.getElementById('repo-btn');
const spinner = document.getElementById('spinner');
const btnText = document.getElementById('btn-text');
const toast = document.getElementById('toast');

function showToast(message, isError = false) {
    toast.innerText = message;
    toast.className = isError ? "toast error" : "toast";
    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);
}

btn.addEventListener('click', async () => {

    btn.disabled = true;
    btnText.style.display = "none";
    spinner.style.display = "inline-block";

    try {
        const response = await fetch('/api/sync-github/', {
            credentials: 'same-origin'
        });

        const data = await response.json();

        if (data.success) {
            showToast(data.message || "Sync complete!");

            setTimeout(() => {
                window.location.href = "/profile/?tab=repositories";
            }, 1000);

        } else {
            showToast(data.message || "Github Token required", true);
        }

    } catch (err) {
        showToast("Token expired.", true);
    }

    btn.disabled = false;
    btnText.style.display = "inline-block";
    spinner.style.display = "none";
});


document.addEventListener("DOMContentLoaded", function () {

    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get("tab");

    if (tab) {
        const target = document.querySelector(`[data-tab="${tab}"]`);
        if (target) {
            target.click();
        }
    }

});

function previewImages(input) {
    const previewContainer = document.getElementById('imagePreviewContainer');
    const captionInputs = document.getElementById('captionInputs');
    previewContainer.innerHTML = '';
    captionInputs.innerHTML = '';

    Array.from(input.files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            // Thumbnail preview
            const wrapper = document.createElement('div');
            wrapper.className = 'image-preview-wrapper';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = 'image-preview-thumb';

            wrapper.appendChild(img);
            previewContainer.appendChild(wrapper);
        };
        reader.readAsDataURL(file);

        // Caption input per image
        const captionInput = document.createElement('input');
        captionInput.type = 'text';
        captionInput.name = `caption_${index}`;     // caption_0, caption_1 ...
        captionInput.placeholder = `Caption for image ${index + 1} (optional)`;
        captionInputs.appendChild(captionInput);
    });
}

function previewEditImages(input, projectId) {
    const previewContainer = document.getElementById(`editPreviewContainer${projectId}`);
    const captionInputs = document.getElementById(`editCaptionInputs${projectId}`);
    previewContainer.innerHTML = '';
    captionInputs.innerHTML = '';

    Array.from(input.files).forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style = 'width:70px;height:70px;object-fit:cover;border-radius:6px;';
            previewContainer.appendChild(img);
        };
        reader.readAsDataURL(file);

        const caption = document.createElement('input');
        caption.type = 'text';
        caption.name = `caption_${index}`;
        caption.placeholder = `Caption for image ${index + 1} (optional)`;
        captionInputs.appendChild(caption);
    });
}


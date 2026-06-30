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

document.addEventListener("DOMContentLoaded", function () {

    const dialog = document.getElementById("addProjectDialog");
    const search = document.getElementById("langSearch");
    const options = document.querySelectorAll("#langOptions .option");
    const selectedInputs = document.getElementById("selectedInputs");

    let selected = [];

    // SEARCH FILTER
    search.addEventListener("input", function () {
        const val = this.value.toLowerCase();

        options.forEach(opt => {
            opt.style.display = opt.dataset.name.includes(val) ? "block" : "none";
        });
    });

    options.forEach(opt => {
        opt.addEventListener("click", function () {
            const id = this.dataset.id;

            if (selected.includes(id)) {
                selected = selected.filter(x => x !== id);
                this.classList.remove("selected");
            } else {
                selected.push(id);
                this.classList.add("selected");
            }

            renderInputs();
        });
    });

    function renderInputs() {
        selectedInputs.innerHTML = "";

        selected.forEach(id => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "languages";
            input.value = id;
            selectedInputs.appendChild(input);
        });
    }

});

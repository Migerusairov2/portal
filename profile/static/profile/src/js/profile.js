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

document.addEventListener("DOMContentLoaded", () => {
    const toast = document.getElementById("toast");

    function showToast(message, isError = false) {
        toast.innerText = message;
        toast.className = isError ? "toast error" : "toast";
        toast.style.display = "block";

        setTimeout(() => {
            toast.style.display = "none";
        }, 3000);
    }

    const successMessage = sessionStorage.getItem("toast-success");
    if (successMessage) {
        showToast(successMessage);
        sessionStorage.removeItem("toast-success");
    }

    const btn = document.getElementById("repo-btn");
    if (!btn) return;

    const spinner = document.getElementById("spinner");
    const btnText = document.getElementById("btn-text");

    btn.addEventListener("click", async () => {
        btn.disabled = true;
        btnText.style.display = "none";
        spinner.style.display = "inline-block";

        try {
            const response = await fetch("/api/sync-github/", {
                credentials: "same-origin"
            });

            const data = await response.json();

            if (data.success) {
                sessionStorage.setItem(
                    "toast-success",
                    data.message || "Sync complete!"
                );

                window.location.href = "/profile/?tab=repositories";
            } else {
                showToast(data.message || "GitHub Token required", true);
            }
        } catch (err) {
            showToast("Token expired.", true);
        }

        btn.disabled = false;
        btnText.style.display = "inline-block";
        spinner.style.display = "none";
    });
});



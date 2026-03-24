// 🌟 1. Form Validation (All pages)
document.addEventListener("DOMContentLoaded", function () {

    let forms = document.querySelectorAll("form");

    forms.forEach(form => {
        form.addEventListener("submit", function (e) {
            let inputs = form.querySelectorAll("input");

            for (let input of inputs) {
                if (input.value.trim() === "") {
                    alert("⚠️ Please fill all fields!");
                    e.preventDefault();
                    return;
                }
            }
        });
    });

});


// 🌟 2. Button Loading Effect
document.addEventListener("DOMContentLoaded", function () {

    let buttons = document.querySelectorAll("button");

    buttons.forEach(btn => {
        btn.addEventListener("click", function () {
            btn.innerText = "Processing...";
        });
    });

});


// 🌟 3. Input Highlight Effect
document.addEventListener("DOMContentLoaded", function () {

    let inputs = document.querySelectorAll("input");

    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            input.style.border = "2px solid green";
        });

        input.addEventListener("blur", () => {
            input.style.border = "1px solid gray";
        });
    });

});


// 🌟 4. Dark Mode Toggle
function toggleMode() {
    document.body.classList.toggle("dark-mode");
}


// 🌟 5. Show Page Loaded Message
window.onload = function () {
    console.log("✅ Page Loaded Successfully");
};


// 🌟 6. Live Time Display
setInterval(() => {
    let timeElement = document.getElementById("time");
    if (timeElement) {
        timeElement.innerText = "⏰ " + new Date().toLocaleTimeString();
    }
}, 1000);
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    
    // Завантажуємо відповіді з localStorage
    function loadAnswers() {
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            const field = document.querySelector(`[name="${key}"]`);
            console.log('---------------');
            console.log(localStorage.length);
            if (field) {
                const value = localStorage.getItem(key);
                if (field.type === "radio" || field.type === "checkbox") {
                    if (value === "true") {
                        field.checked = true;
                    }
                } else {
                    field.value = value;
                }
            }
        }
    }

    // Зберігаємо відповіді в localStorage
    form.addEventListener('change', function(event) {
        const target = event.target;
        if (target.name) {
            if (target.type === "radio" || target.type === "checkbox") {
                localStorage.setItem(target.name, target.checked);
            } else {
                localStorage.setItem(target.name, target.value);
            }
        }
    });

    // Очищаємо localStorage при сабміті форми
    form.addEventListener('submit', function() {
        localStorage.clear();
    });

    // Викликаємо завантаження відповідей при старті
    loadAnswers();
});

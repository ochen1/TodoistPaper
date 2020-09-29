window.addEventListener('load', function () {
    window.nonContentHeight = 0.0;
    var elementStyles;
    for (element of document.body.children) {
        if (element.id === "content-main") {
            continue;
        }
        elementStyles = getComputedStyle(element);
        for (height of [parseFloat(elementStyles.marginTop), parseFloat(elementStyles.marginBottom), parseFloat(elementStyles.height)]) {
            if (!isNaN(height)) {
                window.nonContentHeight += height;
            }
        }
    }
});

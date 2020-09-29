window.addEventListener('load', function () {
    let todoListStyles = getComputedStyle(window.todoList);
    let footerStyles = getComputedStyle(window.footer);
    while (
        parseFloat(
            todoListStyles.height
        )
        >
        parseFloat(
            getComputedStyle(
                window.todoList.parentElement
            ).height
        ) - (
            parseFloat(todoListStyles.marginTop) +
            parseFloat(todoListStyles.marginBottom) +
            parseFloat(todoListStyles.paddingTop) +
            parseFloat(todoListStyles.paddingBottom) +
            window.nonContentHeight
        )
        ) {
        window.todoList.removeChild(window.todoList.children[window.todoList.children.length - 1]);
    }
});

window.addEventListener('load', function () {
    let url = new URL(window.location.href);
    console.log(url);
    document.getElementById("pager-most-previous").href = "/?after=0";
    document.getElementById("pager-previous").href = "/?after=" + encodeURIComponent(Math.max(0, parseInt(url.searchParams.get('after')) - window.todoList.children.length));
    document.getElementById("pager-next").href = "/?after=" + encodeURIComponent(parseInt(url.searchParams.get('after')) + window.todoList.children.length);
    // document.getElementById("pager-most-next").href = "/?before=-1";
});

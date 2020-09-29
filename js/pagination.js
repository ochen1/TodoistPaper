window.addEventListener('load', function () {
    let url = new URL(window.location.href);
    let perpage = parseInt(window.todoList.getAttribute('data-perpage'));
    let perpageQuery = "&perpage=" + perpage;
    let total_pages = parseInt(window.todoList.getAttribute('data-total-pages'));
    let current = parseInt(window.todoList.getAttribute('data-current-page'));
    if (isNaN(current)) {
        current = 0;
    }
    document.getElementById("pager-most-previous").onclick = () => {
        window.location.href = "/?after=0" + perpageQuery;
    }
    document.getElementById("pager-previous").onclick = () => {
        window.location.href = "/?after=" + Math.max(0, (current - 2) * perpage) + perpageQuery;
    }
    document.getElementById("pager-next").onclick = () => {
        window.location.href = "/?after=" + (current * perpage) + perpageQuery;
    }
    document.getElementById("pager-most-next").onclick = () => {
        window.location.href = "/?after=" + (total_pages - 1) * perpage + perpageQuery;
    }
});

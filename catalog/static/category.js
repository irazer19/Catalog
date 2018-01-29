$(function() {
    category = $("#catName").text()
    if (category == 'Gift items') {
        category = 'Gift'
    } 
    $('#'+category).addClass("active")
})
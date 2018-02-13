/* This module helps in making the selected category name active 
    after being clicked. */

$(function() {
    category = $("#catName").text()
    if (category == 'Gift items') {
        category = 'Gift'
    } 
    $('#'+category).addClass("active")
})

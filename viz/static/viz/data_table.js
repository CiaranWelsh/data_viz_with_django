function setDataTableWidthUrl() {
    // get width of viz box
    var inner_width = $('#viz-box').innerWidth();

    // shave off 10% because viz box is slightly too big
    // inner_width = inner_width;
    // $('.bk-data-table').width(inner_width);

    // console.log('inner width1');
    // console.log(inner_width);

    inner_width = Math.ceil(inner_width);
    // console.log('inner width2');
    // console.log(inner_width);
    var html_with_width = 'data_table?width=' + inner_width;
    // console.log('html with width');
    // console.log(html_with_width);

    $('#navitem-data-table').attr('href',html_with_width);
}

function downloadData(){
    var data_table = $('.bk-data-table');
    console.log(data_table);
};

$(document).ready(function () {
    setDataTableWidthUrl();
});


$(window).on('resize', function () {
    setDataTableWidthUrl();
});


// var html_with_width = 'data_table/' + inner_width + '/';
// console.log(document.getElementById('#navitem-data-table').href());



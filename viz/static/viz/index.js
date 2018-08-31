
defaultTab();

//set size of genes box
var option_height = $('#genes-box option:first').height();
var table_height = $('#ctrl-panel-tbl').height();
size = Math.floor(table_height / option_height);
$('#genes-box>select').attr('size', size);

$(window).resize(function () {

    $('#genes-box>select').attr('size', size);
    // console.log(table_height);
});

$('#ctrl-panel-tbl').height = $('#genes-box').height;



// $(document).ready(function () {
//     var submit_button = $('#button-box>input:first');
//     submit_button.click();
// });
// setInterval(function (){
//     var submit_button = $('#button-box>input:first');
//     submit_button.click();
// }, 1000);
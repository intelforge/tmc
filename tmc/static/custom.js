$(function(){
  // Change first column background color.
  $("#firstColumn").click(function(){
    $("table tr td:first-child").css("background-color","#ff0000");
  });
  // Change second column background color.
  $("#secondColumn").click(function(){
    $("table tr td:nth-child(2)").css("background-color","#ff0000");
  });
});

$(document).ready(function() {
   
    var table = $('#explore_results').DataTable();
    var anchor = document.querySelectorAll('.disabled');

    var loc = location.href;
    
    $('#explore_results tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            for (var i = 0; i < anchor.length; i++) {
              anchor[i].classList.add('disabled');
            }
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            for (var i = 0; i < anchor.length; i++) {
              anchor[i].classList.remove('disabled');
              
            }
        }
    } );

} );

function clickRowListener(anchor) {
    var table = $('#explore_results').DataTable();
    var headers = document.querySelectorAll("th");
    var element_value = table.$('tr.selected').find('td').eq(0).text();
    var element_name = headers[2].innerText;
    var atb = anchor.getAttribute('title');
    var link = atb + "/" + element_name.toLowerCase() + "/" + element_value.toLowerCase();
    window.location.replace(link);
}


function open_tram()
{
  var win=window.open('http://localhost:9999', '_blank');
  win.focus();
}
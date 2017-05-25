 $(function () {
     $('#error').hide();
 });

 function FireCall() {
     $('.ajaxProgress').show();
     $('#output').html('');
     var url = $('form').attr('action');
     $.ajax({
         type: 'POST',
         url: url,
         data: $("form").serialize(),
         cache: false,
         success: function (data, status) {
             $('.ajaxProgress').hide();
             if (data.stat == 'ok') {
                 var message = '';
                 data.message.forEach(function(element){
                    message += element + '<br>';
                 });
                 message += "En este <a href='" + data.test_link + "'>enlace</a> puede comprobar el estado del " +
                     "proceso. Tenga en cuenta que puede tardar varias horas dependiendo de otras peticiones y del " +
                     "propio experimento en si";
                 $('#output').html(message);
             }
             else {
                 $('#error').show();
             }
         }
     });
 }

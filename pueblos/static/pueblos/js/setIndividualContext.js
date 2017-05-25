 $(function () {
     $('.error').hide();
     if($('#myform').length > 0){
         $('#myform').submit(function(e){
             $form = $(this);
             var url = $form.attr('action');
             execForm(url);
             e.preventDefault();
        });
     }
 });
 
 function check_valid(url) {
     $('.error').hide();
     var value_error1000 = 'El valor tiene que estar entre 1 y 1000';
     var value_error100 = 'El valor tiene que estar entre 1 y 100';
     switch(url){
         case 'pueblos/cleanDB/setIndividualContext/':
             var value = $('#id_numberOfNotices').val();

             if($('#id_delete').prop("checked") && (value == '' || value < 1 || value > 1000)){
                return value_error1000;
             }
             break;
         case 'pueblos/generateContext/setIndividualContext/':
             var percentage = $('#id_percentage').val();
             if(percentage < 1 || percentage > 1000){
                 return 'El porcentaje tiene que estar entre 1 y 1000';
             }
             var limit = $('#id_limit').val();
             if(limit < 1 || limit > 100){
                 return 'El límite tiene que estar entre 1 y 100';
             }
             break;
         case 'pueblos/getRandomNotices/setIndividualContext/':
             var value = $('#id_testNotices').val();
             if(value == '' || value < 1 || value > 1000){
                return value_error1000;
             }
             break;
     }
     return '';
 }

 function execForm(url) {
     var error = check_valid(url);

     if(error === ''){
         $('.ajaxProgress').show();
         $.ajax({
             type: 'POST',
             url: '/' + url,
             data: $("form").serialize(),
             cache: false,
             success: function (data, status) {
                 $('.ajaxProgress').hide();
                 if (data.stat == 'ok') {
                     //$('#output').html(JSON.stringify(data));
                     $('#output').html(data.message);
                 }
                 else {
                     $('.error').html(data.message);
                     $('.error').show();
                 }
             }
         });
     }else{
         $('.error').html(error);
         $('.error').show();
     }
 }

 function execCall(url) {
     $('.error').hide();
     $('.ajaxProgress').show();
     $.ajax({
         type: 'GET',
         url: '/' + url,
         cache: false,
         success: function (data, status) {
             $('.ajaxProgress').hide();
             if (data.stat == 'ok') {
                 $('#output').html(data.message);
             }
             else {
                 $('.error').html(data.message);
                 $('.error').show();
             }
         }
     });
 }

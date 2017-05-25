var utils = null;

$("document").ready(function(){

	if (utils == null) {
		utils = new Utils();
	}

    var anchor = '#message';
    $(anchor).hide();
     // First add class for pre-checked entries
    $(".table input[type=checkbox]:checked").each(function() {
        //console.log('Row preselected');
        $(this).closest("tr").addClass("danger");
    });

    $('table').delegate(':checkbox','change',function(){
        //console.log('Row changed');
        var $elem = $(this),
        $tr = $elem.closest('tr');

        if($elem.is(':checked')){
            $tr.addClass('danger');
        }else{
            $tr.removeClass('danger');
        }
        return false;
     });

    var searchWord = '#search_word_form';
    var saveWord = '#save_word_form';
    $(searchWord).submit(function (e) {
        e.preventDefault();
        $(anchor).hide();
        var $form = $(this);
        var search_word =  $form.find('input[name="search_word"]').val();
        if(search_word.length >= 3){
            var csrfmiddlewaretoken = $form.find('input[name="csrfmiddlewaretoken"]').val();
            var url = $form.attr('action');
            var method = 'POST';
            var data = {
                search_word: search_word,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            };
            utils.manageCall(url, method, data, function(error, data){
                if(error){
                    //console.log(error);
                    utils.manageMessage(anchor, error, true);
                    $(saveWord).hide();
                }else{
                    var wordFound = data.word_found;
                    $(saveWord).find('input[name="found_word"]').val(wordFound.word);
                    $(saveWord).find('.control-label:first').text(wordFound.word);
                    $(saveWord).find('input[name="replace_word"]').val(wordFound.replace_word);
                    $(saveWord).find('input[type="checkbox"]').prop('checked', false);
                    $(saveWord).show();
                }
            });
        }else{
            utils.manageMessage(anchor, 'La palabra debe tener al menos 3 caracteres', true);
            //console.log("Palabra muy corta");
        }
        return false;
    });

    $(saveWord).submit(function (e) {
        e.preventDefault();
        $(anchor).hide();
        var $form = $(this);
        var replace_word =  $form.find('input[name="replace_word"]').val();
        var delete_word = $form.find('input[type="checkbox"]').is(":checked");
        if(replace_word.length >= 3 || delete_word){
            var found_word = $form.find('input[name="found_word"]').val();
            var csrfmiddlewaretoken = $form.find('input[name="csrfmiddlewaretoken"]').val();
            var url = $form.attr('action');
            var method = 'POST';
            var data = {
                word: found_word,
                replace_word: replace_word,
                delete_word: delete_word,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            };
            utils.manageCall(url, method, data, function(error, response){
                if(error){
                    //console.log(error);
                    utils.manageMessage(anchor, error, true);
                }else{
                    utils.manageMessage(anchor, response.message, false);
                    if(delete_word){
                        $(saveWord).hide();
                    }
                }
            });
        }else{
            utils.manageMessage(anchor, 'La palabra debe tener al menos 3 caracteres', true);
            //console.log("Palabra muy corta");
        }
        return false;
    });
    /*
    function _manageCall(url, method, data, callback){
        $.ajax({
            url : url,
            method : method,
            data : data,
            dataType : "json",
            async : true,
            cache : false
        })
        .done(function(data, textStatus, jqXHR) {
            //console.log(data);
            if (typeof data !== 'undefined' && data.stat.localeCompare('ok') == 0) {
                return callback(null, data);
            }else{
                return callback(data.message);
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            return callback(new Error("Error calling " + errorThrown));
        })
        .always(function() {});
    }

    function _manageMessage(anchorId, message, error){
        var $anchor = $(anchorId);
        if(error){
            $anchor.removeClass('label-success');
            $anchor.addClass('label-danger');
        }else{
            $anchor.removeClass('label-danger');
            $anchor.addClass('label-success');
        }
        $anchor.text(message);
        $anchor.show();
    }
    */
 });

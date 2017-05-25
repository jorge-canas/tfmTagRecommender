var Utils = function () {
};

Utils.prototype.manageCall = function(url, method, data, callback){
        /*
        console.log('_manageCall');
        console.log(url);
        console.log(method);
        console.log(data);
        */
        $.ajax({
            url : url,
            method : method,
            data : data,
            dataType : "json",
            async : true,
            cache : false
        })
        .done(function(response, textStatus, jqXHR) {
            //console.log(response);
            if (typeof response !== 'undefined' && response.stat.localeCompare('ok') == 0) {
                return callback(null, response);
            }else{
                var error = 'Hubo un problema con la petición';
                if (response.length > 0){
                    error = response.message;
                }
                return callback(error);
            }
        })
        .fail(function(jqXHR, textStatus, errorThrown) {
            return callback(new Error("Error calling " + errorThrown));
        })
        .always(function() {});
};

Utils.prototype.manageMessage = function(anchorId, message, error){
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
};

var utils = null;

$("document").ready(function(){

	if (utils == null) {
		utils = new Utils();
	}

	var anchor = '#message';
    $(anchor).hide();

    var anchorOk = '.btn-add';
    var anchorNotOk = '.btn-remove';
    $(anchorOk).on('click', function (e) {
        e.preventDefault();
        var sThis = $(this);
        var type = 'add';
        getData(sThis, type, function (error, data) {
            //console.log(data);
            if(error){
                utils.manageMessage(anchor, error, true);
            }else{
                var url = $('form').attr('action');
                var method = 'POST';
                utils.manageCall(url, method, data, function(error, data){
                    if(error){
                        //console.log(error);
                        utils.manageMessage(anchor, error, true);
                    }else{
                        utils.manageMessage(anchor, data.message, false);
                        var spanSelector = sThis.parent().parent().find('.category');
                        setStatus(spanSelector, type);
                    }
                });
            }
        });
    });

    $(anchorNotOk).on('click', function (e) {
        e.preventDefault();
        var sThis = $(this);
        var type = 'remove';
        getData(sThis, type, function (error, data) {
            //console.log(data);
            if(error){
                //console.log(error);
                utils.manageMessage(anchor, error, true);
            }else{
                var url = $('form').attr('action');
                var method = 'POST';
                utils.manageCall(url, method, data, function(error, data){
                    if(error){
                        //console.log(error);
                        utils.manageMessage(anchor, error, true);
                    }else{
                        utils.manageMessage(anchor, data.message, false);
                        var spanSelector = sThis.parent().parent().find('.category');
                        setStatus(spanSelector, type);
                    }
                });
            }
        });
    });

    function getData($selector, type, callback){
        var category_id = $selector.parent().find('input[name="category_id"]').val();
        var news_id = $('form').find('input[name="id"]').val();
        var csrfmiddlewaretoken = $('form').find('input[name="csrfmiddlewaretoken"]').val();
        if (typeof category_id !== 'undefined' && category_id >= 1){
            var data = {
                'news_id': news_id,
                'category_id': category_id,
                'option': type,
                'csrfmiddlewaretoken': csrfmiddlewaretoken
            };
            return callback(null, data);
        }
        return callback('Hubo un problema al generar los datos');
    }

    function setStatus($spanSelector, type){
        console.log($spanSelector);
        $spanSelector.find('span').remove();
        var span = '';
        switch (type){
            case 'add':
                span = "<span class='glyphicon glyphicon-ok'></span>";
                break;
            case 'remove':
                span = "<span class='glyphicon glyphicon-remove'></span>";
                break;
        }
        $spanSelector.prepend(span);
    }
 });

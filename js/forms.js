$('.cryptoform').submit(function () {
    //alert($(this).parent().attr('id'));
    outputid="#output"+$(this).attr('id');
    $.ajax({
      url: './py/'+$(this).parent().attr('id')+"/"+$(this).attr('id')+'.py',
      type: "POST",
      data: new FormData(this),
      contentType: false,
      cache: false,
      processData:false,
      success: function(data) {
          $(outputid).html(data);
      }
    });
//    $.post('./py/'+$(this).parent().attr('id')+"/"+$(this).attr('id')+'.py', $(this).serialize(), function (data, textStatus) {
//         $(outputid).html(data);
//    });
    return false;
});

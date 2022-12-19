
$(document).ready(function(){
    $(":input").inputmask();
    
    
    
    $("#phone").inputmask({
  mask: '999 999 9999',
  placeholder: ' ',
  showMaskOnHover: false,
  showMaskOnFocus: false,
  onBeforePaste: function (pastedValue, opts) {
    var processedValue = pastedValue;

    //do something with it

    return processedValue;
  }
});
});


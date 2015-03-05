function submitModalForm(formSelector, modalSelector, responseSelector) {
  return function() {
    $(formSelector).ajaxForm(function(responseText) {
      if (responseText === '1') {
        $(modalSelector).modal('hide');
      } else {
        $(responseSelector).replaceWith(responseText);
      }
    });
    $(formSelector).submit();
  };
}

function setupModalFormSubmit(modalId, formSelector) {
  var baseSelector = '#' + modalId;
  if (formSelector === undefined) {
    formSelector = baseSelector + '-form';
  }
  $(baseSelector + '-ok-button').click(
      submitModalForm(
        formSelector,
        baseSelector,
        baseSelector + '-container'
        )
      );
}

function setupBaseModalForm(modalId, formSelector) { // jshint ignore:line
  var baseSelector = '#' + modalId;
  if (formSelector === undefined) {
    formSelector = baseSelector + '-form';
  }
  $(formSelector).bind('keyup keypress', function(e) {
    var code = e.keyCode || e.which;
    if (code === 13) {
      $(baseSelector + '-ok-button').click();
      e.preventDefault();
      return false;
    }
  });

  setupModalFormSubmit(modalId, formSelector);
}

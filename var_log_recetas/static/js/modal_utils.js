function submitModalForm(form_selector, modal_selector, response_selector) {
  return function() {
    $(form_selector).ajaxForm(function(responseText, statusText, xhr, $form) {
      if (responseText === '1') {
        $(modal_selector).modal('hide');
      } else {
        $(response_selector).replaceWith(responseText);
      }
    });
    $(form_selector).submit();
  }
}

function setupModalFormSubmit(modal_id, form_selector) {
  var base_selector = "#" + modal_id;
  if (form_selector === undefined) {
    form_selector = base_selector + "-form";
  }
  $(base_selector + '-ok-button').click(
      submitModalForm(
        form_selector,
        base_selector,
        base_selector + '-container'
        )
      );
}

function setupBaseModalForm(modal_id, form_selector) {
  var base_selector = "#" + modal_id;
  if (form_selector === undefined) {
    form_selector = base_selector + "-form";
  }
  $(form_selector).bind("keyup keypress", function(e) {
    var code = e.keyCode || e.which;
    if (code  == 13) {
      $(base_selector + '-ok-button').click();
      e.preventDefault();
      return false;
    }
  });

  setupModalFormSubmit(modal_id, form_selector);
}

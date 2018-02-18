// Listen for form submits
document.body.addEventListener('submit', function (event) {
  // Abort the form's POST
  event.preventDefault()

  // POST manually with the Fetch API
  var form = event.originalTarget

  fetch(form.action, {
    body: new FormData(form),
    credentials: 'include',
    headers: {
      'accept': 'application/json'
    },
    method: 'POST'
  }).then(function () {
    // Update the UI
    var parentBox = form.closest('div.verifymatchbox')

    // Remove the match box
    parentBox.parentNode.removeChild(parentBox)
  })
})

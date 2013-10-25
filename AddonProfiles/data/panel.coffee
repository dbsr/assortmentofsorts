self.port.on('panel', (profiles, curProfile) ->
  console.log curProfile
  $('li[class="nav-header sub"]').nextAll().remove()
  $('#config').click(->
    self.port.emit('panel', {
      name: 'openConfig'
    })
  )
  for p in profiles
    if p == curProfile then kls = 'active' else kls = ''
    $('ul').append(
      $("<li/>", {class:"#{kls} profile"}).append(
        $('<a/>', {id: p, href:'#', text:p}).click(->
          pName = $(this).attr('id')
          self.port.emit('panel', {
            name: 'activateProfile',
            pName: pName
          })
        )
      )
    )
)

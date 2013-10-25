clickEvents = []

_profilePage = (data) ->
  addons = data.addons
  profiles = data.profiles
  pName = data.pName

  # Teardown
  $('.li-profiles').remove()
  $('tbody').empty()


  # Dropdown menu

  # Profiles
  for cur_pName, v of profiles
    $('.dropdown-menu').prepend(
      $("<li/>", {class: 'li-profiles'}).append(
        $("<a/>", {href: '#', id: "#{cur_pName}", text: "#{cur_pName}"}).click(->
            _pName = $(this).attr('id')
            unless clickEvents.indexOf(_pName) > -1
              idx = clickEvents.push(_pName)
              buildPage('profile-page', _pName)
        )
      )
    )
  # Create Profile
  $('#create-profile').click(->
    unless clickEvents.indexOf('create-profile') > -1
      clickEvents.push('create-profile')
      self.port.emit('get', {
        name: 'createProfile'
      })
      self.port.on('createProfile', (pName) ->
        buildPage('profile-page', pName)
      )
  )
  # Help/About
  $('#help').click(->
    buildPage('help-page')
  )
  $('#about').click(->
    buildPage('about-page')
  )

  # Addons
  regkls = 'success'
  if pName == 'default'
    defkls = regkls
  else
    defkls = 'defkls'

  for addon in addons

    if addon.id in profiles.default
      kls = defkls
    else if addon.id in profiles[pName]
      kls = regkls
    else
      kls = ''

    $('tbody').append(
      $("<tr/>", {class: kls, id: addon.id}).append(
          $("<td/>", {text: addon.name}),
          $("<td/>", {text: addon.id})
      ).click(->
        unless $(this).attr('class') == 'defkls' and pName != 'default'
          _addonID = $(this).attr('id')
          unless clickEvents.indexOf(_addonID) > -1
            idx = clickEvents.push(_addonID)
            if $(this).attr('class')
              kls = ''
            else
              kls = 'success'
            $(this).attr('class', kls)
            self.port.emit('get', {
              name: 'editProfile',
              eventData:
                pName: $('h4#profile-name').html(),
                addonID: _addonID
            })
            self.port.on('editProfile', (status) ->
              clickEvents.pop(idx)
            )
      )
    )

  # Current profile header
  $('h4#profile-name').text(pName)
  if pName == 'default'
    $('#default-profile').show()
    $('.edit-profile-controls').hide()
  else
    $('#default-profile').hide()
    $('.edit-profile-controls').show()

    # Rename Button
    $('.title-edit').hide()
    $('#rename').click(->
      $('.title-edit').show()
    )
    $('#submit-rename').click(->
      pName = $('h4#profile-name').html()
      new_pName = $('#input-profile-name').val()
      unless clickEvents.indexOf('submit-rename') > - 1 or new_pName == ''
        _idx = clickEvents.push('submit-rename')
        self.port.emit('get', {
          name: 'renameProfile',
          eventData:
            new_pName: new_pName,
            cur_pName: pName
        })
        self.port.on('renameProfile', (new_pName) ->
          buildPage(pageID='profile-page', pName=new_pName)
          $('.title-edit').hide()
        )
    )
    # Delete Button
    $('#delete').click(->
      unless clickEvents.indexOf('delete') > - 1
        _idx = clickEvents.push('delete')
        pName = $('h4#profile-name').html()
        self.port.emit('get', {
          name: 'deleteProfile',
          eventData:
            pName: pName
        })
        self.port.on('deleteProfile', (resp) ->
          buildPage()
        )
    )

buildPage = (pageID='profile-page', pName=null) ->
  clickEvents = []
  for id in ['profile-page', 'help-page', 'about-page']
    unless id == pageID
      $("div[id='#{id}']").hide()
      continue
    $("div[id='#{id}']").show()

    if id == 'profile-page'
      self.port.emit('get', {
        name: 'buildPage',
        pName: pName
      })
      self.port.on('buildPage', (data) ->
        _profilePage(data)
      )

# init
$(->
  buildPage()
)

initTable = ->
  # sorting
  for th in $('td', 'thead')
    $th = $(th)
    direction = $th.attr('data-sort-direction')
    unless direction == '-1'
      dir = if direction == '1' then 'up' else 'down'
      icon = "icon-circle-arrow-#{dir}"
      $th.addClass("td-active")
      $th.append("<i style='margin-left: 1em; position: relative; top: .09em;' class='#{icon}' />")
    $th
      .click(->
        param = $(this).html().split('<')[0].split(' ').join('_')
        reverse = if $(this).attr('data-sort-direction') == '1' then "0" else '1'
        window.location.href = "/index?sort=#{param}&reverse=#{reverse}"
      )

  # form
  $('#create_cmd').click((event) ->
    event.preventDefault()
    $.get('/pacman-cmd',  $('form').serialize())
  )

initFilters = ->
  for filter in $('a', '#filters')
    $(filter)
      .click((event) ->
        event.preventDefault()
        url = window.location.href
        $f = $(this)
        if $f.hasClass('active')
          $f.removeClass('active')
          $f.addClass('inactive')
          # update url
          if url.split('=').length > 2

            if url.match("[&?]#{$f.attr('id')}")[0][0] == "?"
              url = url.replace("#{$f.attr('id')}=1&", '')
            else
              url = url.replace("&#{$f.attr('id')}=1", '')
          else
            url = url.replace("\?#{$f.attr('id')}=1", '')
        else
          $f.removeClass('inactive')
          $f.addClass('active')
          sep = if url.match(/\?/) then '&' else '?'
          url += "#{sep}#{$f.attr('id')}=1"
        window.location.href = url
      )


initModal = (link, contentElement) ->
  $(contentElement).hide()
  $(link).click((event) ->
    event.preventDefault()
    for cb in $(':checked')
      pkg = $(cb).attr('name')
      $('.packages')
        .append("<p id='#{pkg}' class='package-list'>#{pkg}</p>")
    doModal(contentElement)
  )

  getText = (separator=' ') ->
    ($(p).attr('id') for p in $('p', '.packages')).join(separator)

  $('#copy').click((event) ->
    text = getText()
    console.log text
    window.prompt("Copy to clipboard: Ctrl + C, Enter", text)
  )
  $('#save').click((event) ->
    event.preventDefault()
    text = getText(',')
    url = "/download-textfile?packages=#{text}"
    window.open(url, 'Download')
  )



doModal = (contentElement) ->
  $(contentElement)
    .show()
    .addClass('modal')

killModal = (modal) ->
  $(modal).hide()


$(->
  initTable()
  initFilters()
  initModal('#selected-packages', '#packages-modal')
)

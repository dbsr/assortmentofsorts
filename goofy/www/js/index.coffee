#<< cycle_provider

index = {}

index.init = ->
    pselector = new ProviderSelector(['spotify', 'deezer'],
        'input[name="direction"]', '#arrow', '#arrow-helper' )

    $('button').click((event) =>

        event.preventDefault()

        for val in [$(input).val() for input in $('input')]

            if val in ['', 0]

                return


        formData = $('form').serialize()

        clearErrorsForm()

        pselector.cycleProviders()


        $.get('/', formData, (data) ->

            if data.status == 'INPUT_ERROR'

                setErrorsForm(data.message)

                pselector.reset()

            else

                loadPlaylistModal(data.provider, data.plugin_data)



        )

    )


loadPlaylistModal = (provider, plugin_data) ->

    $iframe = $('iframe#playlist')

    $button = $('button[class="btn to-provider"]')

    if provider == 'spotify'
        url = "https://embed.spotify.com/?uri=spotify:trackset:goofy:#{plugin_data}"
        $button.html('Open in Spotify')
        $button.wrap("<a href='spotify:trackset:goofy:#{plugin_data}'/>")
    else
        url = ("http://www.deezer.com/nl/plugins/player?playlist=true&width" +
               "=#{$iframe.attr('width')}&height=#{$iframe.attr('height')}&" +
               "cover=false&type=tracks&id=#{plugin_data}&format=vertical")
        $button.html('Add to Deezer library')
        $button.click((event) ->

            window.open("/create-deezer-playlist")

        )

    $iframe.attr('src', url)
    $('div#playlist-modal').modal('show')


clearErrorsForm = ->

    $('label.invalid-input').html('&nbsp;')

    $('div[class="control-group error"]').attr('class', 'control-group')

    $('input#inputError').attr('id', 'input')


setErrorsForm = (message) ->

    $('div.control-group').attr('class', 'control-group error')

    $('input#input').attr('id', 'inputError')

    $('label.invalid-input').html(message)

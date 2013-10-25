class ProviderSelector

    @me = null

    constructor: (providers, @formElementId, arrowElement, arrowHelperElement) ->

        @providers = {}

        for p in providers

            @providers[p] = new ProviderImage(p)

        @arrow = new DirectionArrow(arrowElement, arrowHelperElement)

        ProviderSelector.me = @

    activateProvider: (@angle) ->

        if @angle == 360

            @providers['deezer'].on()

        else
            for k, v of @providers
                v.toggle()

        @setForm()

    curProvider: ->

        for name, provider of @providers

            if provider.cur_slide != 1

                return name

    setForm: ->

        $(@formElementId).val(@curProvider())

    cycleProviders: =>

        @cur_prov = @curProvider()

        @intervalId = setInterval(=>

            for k, v of @providers

                v.toggle()

        1000)

    reset: =>

        clearInterval(@intervalId)

        for n, p of @providers

            if n == @cur_prov

                p.off()

            else

                p.on()


class ProviderImage

    constructor: (name) ->

        @$_ = $("div[class='provider #{name}']")

        @$_.cycle({
            timeout: 0,
            speed: 300,
            startingSlide: 0
        })

        @cur_slide = 0

    on: ->

        @cur_slide = 1

        @$_.cycle(1)

    off: ->

        @cur_slide = 0

        @$_.cycle(0)

    toggle: =>

        if @cur_slide == 1 then @off() else @on()

class DirectionArrow

    constructor: (element, helperElement) ->

        @$_ = $(element)

        @$_h = $(helperElement)

        @$_.rotate(90)

        angle = 180

        @setClick()

        @doHelper()

    setClick: (angle=180) ->

        @$_.stop(true, true)

        @$_.rotate({
            bind: {
                click: =>

                    @killHelper()

                    angle += 180

                    @$_.rotate({ animateTo: angle })

                    ProviderSelector.me.activateProvider(angle)
            }
        })


    doHelper: (oldAngle=15) ->

        newAngle = oldAngle * -1

        @$_h.rotate({
            angle: oldAngle,
            animateTo: newAngle,
            duration: 500,
            callback: =>
                @doHelper(newAngle)
        })


    killHelper: ->

        @$_h.remove()

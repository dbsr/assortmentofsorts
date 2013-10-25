self = require('sdk/self')
data = self.data
require("chrome").components.utils.import(
  "resource://gre/modules/PopupNotifications.jsm")


profiles = new require('profiles')

pm = new profiles.ProfileManager(self.id)
require('page-mod').PageMod({
  include: data.url('config.html'),
  contentScriptFile: [
      data.url('ext/jquery-2.0.0.min.js'),
      data.url('ext/bootstrap-2.3.1.min.js'),
      data.url('config.js'),
  ],
  contentStyleFile: [
      data.url('ext/bootstrap-2.3.1.min.css')
      data.url('config.css')
  ],
  onAttach: (worker) ->
    worker.port.on('get', (event) =>

      if event.name == "buildPage"

        _profiles = pm.profiles
        addons = pm.addons
        unless event.pName?
          event.pName = Object.keys(_profiles)[0]
        worker.port.emit(event.name, {
          profiles: _profiles,
          addons: addons,
          pName: event.pName
        })
      else
        if not event.eventData?
          data = null
        else
          data = event.eventData

        pm[event.name](data, (response=true) ->
          worker.port.emit(event.name, response)
        )
    )
})


panel = require('sdk/panel').Panel({
  width: 200,
  height: 120 + Object.keys(pm.profiles).length * 40,
  contentURL: data.url('panel.html'),
  contentScriptFile: [
      data.url('ext/jquery-2.0.0.min.js'),
      data.url('panel.js'),
  ],
  onShow: ->
    this.port.emit('panel', Object.keys(pm.profiles), pm.curProfile())

})

widget = require('sdk/widget').Widget({
  id: 'addon-profiles',
  label: 'AddonProfiles',
  contentURL: data.url('icons/addon-profiles.ico'),
  panel: panel
})

panel.port.on('panel', (event) ->
  switch event.name
    when 'openConfig' then require('sdk/tabs').open(data.url('config.html'))
    when 'activateProfile'
      pm.activateProfile(event.pName, (needRestart) ->
        if needRestart
          require('ext/notification-box').NotificationBox({
            value: 'AddonProfiles Notification',
            label: 'Firefox needs to be restarted for all changes to take effect.',
            image: data.url('icons/addon-profiles.ico'),
            priority: this.WARNING_LOW,
          })
      )
  panel.hide()
)




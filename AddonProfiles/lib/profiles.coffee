ss = require('sdk/simple-storage')
require("chrome").components.utils.import(
    "resource://gre/modules/AddonManager.jsm")

class ProfileManager
  constructor: (@id) ->
    unless ss.storage.profiles?
      ss.storage.profiles = {}
    unless ss.storage.profiles.default?
      ss.storage.profiles['default'] = []
      ss.storage.curProfile = 'default'
    @profiles = {}
    @_loadProfiles()
    @addons = []
    @_getAddons()

  _loadProfiles: ->
    @profiles = {}
    for name, addonIDs of ss.storage.profiles
      @profiles[name] = addonIDs

  _getAddons: ->
    AddonManager.getAllAddons((aAddons) =>
      for addon in (a for a in aAddons when a.id != @id and a.type == 'extension')
        AddonManager.getAddonByID(addon.id, (_addon) =>
          @addons.push(_addon)
        )
    )

  curProfile: ->
    console.log "curProfile: #{ss.storage.curProfile}"
    return ss.storage.curProfile

  activateProfile: (profile, callback) =>
    ss.storage.curProfile = profile
    pAddons = @profiles[profile]
    unless pAddons?
      pAddons = []
    unless profile == 'default'
      pAddons = pAddons.concat(@profiles.default)

    needRestart = false
    for addon in @addons
      if addon.id in pAddons
        unless addon.isActive
          addon.isActive = true
          addon.userDisabled = false
      else
        unless addon.userDisabled
          addon.isActive = false
          addon.userDisabled = true

      if addon.pendingOperations > 0
        needRestart = true

    callback(needRestart)

  renameProfile: (data, cb) ->
    unless @profiles[data.new_pName]?
      ss.storage.profiles[data.new_pName] = ss.storage.profiles[data.cur_pName]
      delete ss.storage.profiles[data.cur_pName]
      @_loadProfiles()
      cb(data.new_pName)

  editProfile: (data, cb) ->
    if ss.storage.profiles[data.pName].indexOf(data.addonID) > -1
      ss.storage.profiles[data.pName].pop(data.addonID)
    else
      ss.storage.profiles[data.pName].push(data.addonID)

    cb()

  createProfile: (data, cb) ->
    n = 0
    while true
      n += 1
      tmpName = "AddonProfile#{n}"
      unless ss.storage.profiles[tmpName]?
        ss.storage.profiles[tmpName] = []
        break

    @_loadProfiles()
    cb(tmpName)

  deleteProfile: (data, cb) ->
    try
      delete ss.storage.profiles[data.pName]
    catch error
      console.log error

    @_loadProfiles()
    cb()


module?.exports =
  ProfileManager: ProfileManager

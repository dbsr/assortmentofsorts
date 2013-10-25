###
  noQuery v0.2

  author:       Daan Mathot
  email:        daanmathot@gmail.com
  description:  dom traversal and manipulation utilities
  license:      UNLICENSE
###
namespace = ( target, name, block ) ->
  [target, name, block] = [(if typeof exports isnt 'undefined' then exports else window), arguments...] if arguments.length < 3
  top    = target
  target = target[item] or= {} for item in name.split '.'
  block target, top

namespace "nQ", ( exports ) ->

  exports.nq_wrap = ( selector ) ->
    n = new nQ.NoQuery( selector )
    if n.node
      n
    else if n.nodes
      n.nodes

  class exports.NoQuery
    constructor: ( @selector ) ->
      switch typeof @selector
        when 'object' and @selector instanceof Node
          @node = @selector
          @selector = null
        when 'string'
          sElements = @select( @selector )
          if sElements instanceof HTMLCollection and sElements.length > 0
            if sElements.length == 1
              @node = sElements[0]
            else
              @nodes = Array.prototype.slice.call( sElements )
          else if sElements instanceof Node
            @node = sElements

    select: ( selector ) ->
      parent = if @node? then @node else document
      sType = selector[0]
      sSplit = selector[1...]
      switch sType
        when "#" then document.getElementById( sSplit )
        when "." then parent.getElementsByClassName( sSplit )
        else parent.getElementsByTagName( selector )

    append: ( html ) ->
      @node.appendChild( nQ.dom.createFrag( html ) )

    appendTo: ( selector ) ->
      nQ.nq_wrap( selector ).append( @node )

    prepend: ( html ) ->
      @node.insertBefore( nQ.dom.createFrag( html ), @node.firstChild )

    prependTo: ( selector ) ->
      nQ.nq_wrap( selector ).prepend( @node )

    remove: ->
      @node.parentNode.removeChild( @node )

    replaceChild: ( html ) ->
      @node.replaceChild(html, @node.firstChild)

    attr: ( attr, value=null ) ->
      # Set value to false to completely remove the attribute
      if value? then nQ.attribute.set( @node, attr, value ) else nQ.attribute.get( @node, attr )

    hasClass: ( className ) ->
      nQ.klass.has( @node, className )

    addClass: ( className ) ->
      nQ.klass.add( @node, className )

    removeClass: ( className ) ->
      nQ.klass.remove( @node, className )

    toggleClass: ( className ) ->
      nQ.klass.toggle( @node, className )

    toggleHide: ->
      nQ.style.toggleHide( @node )

    css: ( cssStyles ) ->
      nQ.style.css( @node, cssStyles )

    value: ->
      @node.value



  ###
  noQuery functions
  ###

  exports.dom =
    createFrag: ( html ) ->
      ###
      Used by append and prepend functions. Text is detected by looking 1 token
      ahead. If this is not an opening < tag, assumes textNode.
      @TODO style tag implementation switch to YAML syntax?

      args
        html: <string> html formatted text string

      returns: <fragmentNode> with childNodes parsed from html string
      ###
      unless typeof html is 'string'
        return html

      frag = document.createDocumentFragment()
      for e in html.match( /<[^>]+>/g )
        text = null
        textIdx = html.indexOf( e ) + e.length
        unless html[textIdx] == "<"
          text = document.createTextNode( html[textIdx..textIdx + html[textIdx...].search( /</ ) - 1] )
        if e.match( /\// ) then continue
        e_obj = {}
        for attr in ( x.replace( /[\<\>\s]/g, '' ) for x in e.split " " )
          if attr.match /\=/
            e_obj[attr.split("=")[0]] = attr.split("=")[1].replace( /["']/g, '' )
          else
            e_obj.tag = attr
        element = document.createElement( e_obj.tag )
        if text? then element.appendChild( text )
        for k, v of e_obj
          unless k == 'tag'
            element.setAttribute( k, v )
        frag.appendChild( element )
      frag

  exports.attribute =
    has: ( elem, attr ) ->
      elem.hasAttribute( attr )

    get: ( elem, attr ) ->
      if this.has( elem, attr )
        elem.getAttribute( attr )

    set: ( elem, attr, value ) ->
      if value != false then elem.setAttribute( attr, value ) else this.remove( elem, attr )

    remove: ( elem, attr ) ->
      elem.removeAttribute( attr )

  exports.klass =
    ###
    Except for OperaMini all modern browsers support classList. Suck it oldtimers.
    @TODO regex based alternative for classListless browsers.
    ###
    has: (elem, c) ->
      elem.classList.contains( c )

    add: (elem, c) ->
      elem.classList.add( c )

    remove: (elem, c) ->
      elem.classList.remove( c )

    toggle: (elem, c) ->
      if this.hasClass( elem, c ) then removeClass( elem, c ) else addClass( elem, c )

  exports.style =
    css: ( elem, cssStyle ) ->
      for k, v of cssStyle
        elem.style[k] = v
    toggleHide: ( elem ) ->
      elem.style.display = if elem.style.display == "none" then "" else "none"


window._$ = nQ.nq_wrap

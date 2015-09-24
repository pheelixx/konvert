(($) ->
  $.fn.upload = (options) ->
    this.each ->
      $.data this, 'upload', {}
      $.data this, 'upload', Upload this, options

  Upload = (element, options) ->
    new Upload.prototype.init element, options

  $.Upload = Upload
  $.Upload.options =
    async: true
    url: false
    prefix: 'uploaded_file'

  Upload.fn = $.Upload.prototype =
    uniqueId: (prefix) ->
      _.uniqueId prefix
    init: (element, options) ->
      this.$id = 0
      this.$element = if element then $(element) else false
      this.loadOptions options
      this.load()
    loadOptions: (options) ->
      this.options = $.extend(
        {}
        $.extend true, {}, $.Upload.options
        this.$element.data()
        options
      )
    setCallback: (type, event, data) ->
      events = $._data this.$element[0], 'events'
      if events and events[type]
        value = []
        for key, current of events[type]
          namespace = current.namespace
          if namespace is 'upload'
            callback = current.handler
            value.push if data
            then callback.call this, event, data
            else callback.call this, event
        return if value.length is 1
        then value[0]
        else value
      if data
      then data
      else event
    proxyChange: (event) ->
      this.traverseFile this.$element[0].files[0], event.originalEvent ? event
    proxyDrop: (event) ->
      event.preventDefault()
      this.$droparea.removeClass('drag-hover').addClass('drag-drop')
      this.onDrop event
    load: ->
      this.$droparea = this.$element.closest('.upload-container') ? this.$element.parent()
      this.$droparea
        .addClass 'drop-area'
        .off '.upload'
        .on 'dragover.upload', $.proxy(this.onDrag, this)
        .on 'dragleave.upload', $.proxy(this.onDragLeave, this)
      this.$element
        .off '.upload'
        .on 'change.upload', $.proxy(this.proxyChange, this)
      this.$droparea.on 'drop.upload', $.proxy(this.proxyDrop, this)
    onDrop: (event) ->
      event = event.originalEvent ? event
      file = event.dataTransfer.files[0]
      this.traverseFile file, event
    traverseFile: (file, event) ->
      formData = if !!window.FormData then new FormData() else null
      if window.FormData
        name = this.$element.attr 'name'
        this.$id = this.uniqueId this.options.prefix
        formData.append name, file
        if this.options.key? then formData.append 'key', this.options.key
      this.setCallback 'start', file, this.$id
      this.sendData formData, event
    sendData: (formData) ->
      xhr = new XMLHttpRequest()
      xhr.open 'POST', this.options.url, this.options.async
      xhr.upload.onprogress = $.proxy ((event) -> this.setCallback 'progress', event, this.$id), this
      xhr.onreadystatechange = $.proxy ( ->
        complete = 4
        success = 200
        if xhr.readyState is complete
          data = xhr.responseText
          this.$droparea.removeClass 'drag-drop'
          if xhr.status is success
          then this.setCallback 'success', data, this.$id
          else this.setCallback 'error', data, this.$id
          this.$element.val ''
      ), this
      xhr.send(formData)
    onDrag: (event) ->
      event.preventDefault()
      this.$droparea.addClass 'drag-hover'
    onDragLeave: (event) ->
      event.preventDefault()
      this.$droparea.removeClass 'drag-hover'

  Upload.prototype.init.prototype = Upload.prototype
) jQuery